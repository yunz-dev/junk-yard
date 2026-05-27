from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    card_views = relationship("CardView", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserCardProgress", back_populates="user", cascade="all, delete-orphan")


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    chinese = Column(String, nullable=False)
    pinyin = Column(String, nullable=False)
    english = Column(String, nullable=False)
    category = Column(String, nullable=False)
    studied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    views = relationship("CardView", back_populates="card", cascade="all, delete-orphan")
    progress = relationship("UserCardProgress", back_populates="card", cascade="all, delete-orphan")


class CardView(Base):
    __tablename__ = "card_views"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("flashcards.id"), nullable=False)
    viewed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="card_views")
    card = relationship("Flashcard", back_populates="views")


class UserCardProgress(Base):
    __tablename__ = "user_card_progress"
    __table_args__ = (UniqueConstraint("user_id", "card_id", name="uq_user_card"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("flashcards.id"), nullable=False)
    studied = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="progress")
    card = relationship("Flashcard", back_populates="progress")
