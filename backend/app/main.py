import os
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, crud
from .database import engine, get_db, SessionLocal
from .seed import seed_database, add_default_cards
from .auth import hash_password, verify_password, create_access_token, decode_access_token
from .schemas import AuthRequest

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

@app.get("/api/flashcards")
def read_flashcards(category: str | None = None, studied: bool | None = None, db: Session = Depends(get_db)):
    return crud.get_flashcards(db, category=category, studied=studied)

@app.get("/api/flashcards/{flashcard_id}")
def read_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    flashcard = crud.get_flashcard(db, flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return flashcard

@app.post("/api/flashcards")
def create_flashcard(flashcard: crud.FlashcardCreate, db: Session = Depends(get_db)):
    return crud.create_flashcard(db, flashcard)

@app.put("/api/flashcards/{flashcard_id}")
def update_flashcard(flashcard_id: int, flashcard: crud.FlashcardUpdate, db: Session = Depends(get_db)):
    updated = crud.update_flashcard(db, flashcard_id, flashcard)
    if not updated:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return updated

@app.delete("/api/flashcards/{flashcard_id}")
def delete_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_flashcard(db, flashcard_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return {"message": "Flashcard deleted"}

@app.get("/api/categories")
def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return [cat[0] for cat in categories]

@app.post("/api/reset")
def reset_database(db: Session = Depends(get_db)):
    crud.delete_all_flashcards(db)
    add_default_cards(db)
    return {"message": "Database reset to defaults"}


@app.post(
    "/api/register",
    summary="Create an account",
    description="Creates a new user and signs them in.",
)
def register(body: AuthRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == body.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = models.User(username=body.username, hashed_password=hash_password(body.password))
    db.add(user)
    db.commit()
    token = create_access_token(body.username)
    return {"access_token": token, "token_type": "bearer", "username": body.username}


@app.post(
    "/api/login",
    summary="Log in",
    description="Checks the username and password, then signs the user in.",
)
def login(body: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == body.username).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(body.username)
    return {"access_token": token, "token_type": "bearer", "username": body.username}


@app.get(
    "/api/me",
    summary="Get current user",
    description="Returns the user for the current login token.",
)
def get_me(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    username = decode_access_token(authorization.split(" ", 1)[1])
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {"username": user.username}

