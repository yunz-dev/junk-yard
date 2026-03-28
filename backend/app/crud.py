from sqlalchemy.orm import Session
from . import models
from pydantic import BaseModel

class FlashcardCreate(BaseModel):
    chinese: str
    pinyin: str
    english: str
    category: str

class FlashcardUpdate(BaseModel):
    chinese: str | None = None
    pinyin: str | None = None
    english: str | None = None
    category: str | None = None
    studied: bool | None = None

def get_flashcards(db: Session, category: str | None = None, studied: bool | None = None):
    query = db.query(models.Flashcard)
    if category:
        query = query.filter(models.Flashcard.category == category)
    if studied is not None:
        query = query.filter(models.Flashcard.studied == studied)
    return query.all()

def get_flashcard(db: Session, flashcard_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()

def create_flashcard(db: Session, flashcard: FlashcardCreate):
    db_flashcard = models.Flashcard(**flashcard.model_dump())
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def update_flashcard(db: Session, flashcard_id: int, flashcard: FlashcardUpdate):
    db_flashcard = get_flashcard(db, flashcard_id)
    if db_flashcard:
        update_data = flashcard.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_flashcard, key, value)
        db.commit()
        db.refresh(db_flashcard)
    return db_flashcard

def delete_flashcard(db: Session, flashcard_id: int):
    db_flashcard = get_flashcard(db, flashcard_id)
    if db_flashcard:
        db.delete(db_flashcard)
        db.commit()
        return True
    return False

def get_categories(db: Session):
    return db.query(models.Flashcard.category).distinct().all()

def reset_studied(db: Session):
    db.query(models.Flashcard).update({models.Flashcard.studied: False})
    db.commit()
    return True

def delete_all_flashcards(db: Session):
    db.query(models.Flashcard).delete()
    db.commit()
    return True
