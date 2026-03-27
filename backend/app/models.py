from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .database import Base

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    chinese = Column(String, nullable=False)
    pinyin = Column(String, nullable=False)
    english = Column(String, nullable=False)
    category = Column(String, nullable=False)
    studied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
