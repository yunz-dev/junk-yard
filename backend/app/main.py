import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, crud
from .database import engine, get_db, SessionLocal
from .seed import seed_database, add_default_cards
from .auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_admin, get_optional_user,
)
from .schemas import (
    AuthRequest, AuthResponse, UserOut, UserDetailOut, CardViewOut,
    FlashcardCreate, FlashcardUpdate, FlashcardOut,
    AdminUpdateUser, SelfChangePassword, MarkStudiedRequest,
)

os.makedirs("data", exist_ok=True)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
seed_database(db)
db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/register", response_model=AuthResponse)
def register(body: AuthRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == body.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = models.User(
        username=body.username,
        hashed_password=hash_password(body.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(body.username)
    return AuthResponse(access_token=token, token_type="bearer", username=body.username, role=user.role)


@app.post("/api/login", response_model=AuthResponse)
def login(body: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == body.username).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(body.username)
    return AuthResponse(access_token=token, token_type="bearer", username=body.username, role=user.role)


@app.get("/api/me", response_model=UserDetailOut)
def get_me(current_user=Depends(get_current_user)):
    views = [
        CardViewOut(
            id=v.id,
            card_id=v.card_id,
            card_chinese=v.card.chinese,
            card_english=v.card.english,
            viewed_at=v.viewed_at,
        )
        for v in sorted(current_user.card_views, key=lambda v: v.viewed_at, reverse=True)[:50]
    ]
    return UserDetailOut(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role,
        created_at=current_user.created_at,
        card_views=views,
    )


@app.put("/api/me")
def change_own_password(body: SelfChangePassword, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.hashed_password = hash_password(body.new_password)
    db.commit()
    return {"message": "Password updated"}


@app.get("/api/flashcards")
def read_flashcards(
    category: str | None = None,
    studied: bool | None = None,
    current_user=Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    if current_user:
        cards = crud.get_flashcards_for_user(db, current_user.id, category=category, studied=studied)
    else:
        cards = crud.get_flashcards(db, category=category)
        for card in cards:
            card.studied = False
    return cards


@app.get("/api/flashcards/{flashcard_id}")
def read_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    flashcard = crud.get_flashcard(db, flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return flashcard


@app.post("/api/flashcards")
def create_flashcard(
    flashcard: FlashcardCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    return crud.create_flashcard(db, flashcard)


@app.put("/api/flashcards/{flashcard_id}")
def update_flashcard(
    flashcard_id: int,
    flashcard: FlashcardUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    updated = crud.update_flashcard(db, flashcard_id, flashcard)
    if not updated:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return updated


@app.delete("/api/flashcards/{flashcard_id}")
def delete_flashcard(
    flashcard_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    deleted = crud.delete_flashcard(db, flashcard_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return {"message": "Flashcard deleted"}


@app.post("/api/flashcards/{flashcard_id}/view")
def record_view(
    flashcard_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = crud.get_flashcard(db, flashcard_id)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    crud.record_card_view(db, current_user.id, flashcard_id)
    return {"message": "Recorded"}


@app.put("/api/flashcards/{flashcard_id}/studied")
def mark_studied(
    flashcard_id: int,
    body: MarkStudiedRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = crud.get_flashcard(db, flashcard_id)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    crud.upsert_card_progress(db, current_user.id, flashcard_id, body.studied)
    card.studied = body.studied
    return card


@app.get("/api/categories")
def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return [cat[0] for cat in categories]


@app.post("/api/reset")
def reset_database(
    current_user=Depends(require_admin),
    db: Session = Depends(get_db),
):
    crud.delete_all_flashcards(db)
    add_default_cards(db)
    return {"message": "Database reset to defaults"}


@app.get("/api/users", response_model=list[UserOut])
def list_users(
    _: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return crud.get_users(db)


@app.get("/api/users/{user_id}", response_model=UserDetailOut)
def get_user(
    user_id: int,
    _: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    views = [
        CardViewOut(
            id=v.id,
            card_id=v.card_id,
            card_chinese=v.card.chinese,
            card_english=v.card.english,
            viewed_at=v.viewed_at,
        )
        for v in sorted(user.card_views, key=lambda v: v.viewed_at, reverse=True)[:50]
    ]
    return UserDetailOut(
        id=user.id,
        username=user.username,
        role=user.role,
        created_at=user.created_at,
        card_views=views,
    )


@app.put("/api/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    body: AdminUpdateUser,
    _: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = crud.update_user(db, user_id, body)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/api/users/{user_id}")
def delete_user(
    user_id: int,
    current_user=Depends(require_admin),
    db: Session = Depends(get_db),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=403, detail="Cannot delete yourself")
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


@app.post("/api/users/{user_id}/reset-progress")
def reset_user_progress(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.reset_user_progress(db, user_id)
    return {"message": "Progress reset"}
