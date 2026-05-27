from sqlalchemy.orm import Session
from . import models
from .schemas import FlashcardCreate, FlashcardUpdate, AdminUpdateUser
from .auth import hash_password


def get_flashcards(db: Session, category: str | None = None):
    query = db.query(models.Flashcard)
    if category:
        query = query.filter(models.Flashcard.category == category)
    return query.all()


def get_flashcards_for_user(
    db: Session,
    user_id: int,
    category: str | None = None,
    studied: bool | None = None,
):
    query = db.query(models.Flashcard, models.UserCardProgress).outerjoin(
        models.UserCardProgress,
        (models.UserCardProgress.card_id == models.Flashcard.id)
        & (models.UserCardProgress.user_id == user_id),
    )
    if category:
        query = query.filter(models.Flashcard.category == category)

    results = []
    for card, progress in query.all():
        user_studied = progress.studied if progress else False
        if studied is not None and user_studied != studied:
            continue
        card.studied = user_studied
        results.append(card)
    return results


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


def delete_all_flashcards(db: Session):
    db.query(models.Flashcard).delete()
    db.commit()
    return True


def record_card_view(db: Session, user_id: int, card_id: int):
    view = models.CardView(user_id=user_id, card_id=card_id)
    db.add(view)
    db.commit()


def upsert_card_progress(db: Session, user_id: int, card_id: int, studied: bool):
    progress = (
        db.query(models.UserCardProgress)
        .filter_by(user_id=user_id, card_id=card_id)
        .first()
    )
    if progress:
        progress.studied = studied
    else:
        progress = models.UserCardProgress(user_id=user_id, card_id=card_id, studied=studied)
        db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def reset_user_progress(db: Session, user_id: int):
    db.query(models.UserCardProgress).filter_by(user_id=user_id).update({"studied": False})
    db.commit()


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: int, data: AdminUpdateUser):
    user = get_user(db, user_id)
    if not user:
        return None
    if data.username is not None:
        user.username = data.username
    if data.password is not None:
        user.hashed_password = hash_password(data.password)
    if data.role is not None:
        user.role = data.role
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
