from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, crud
from .database import engine, get_db, SessionLocal
from .seed import seed_database, add_default_cards

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
