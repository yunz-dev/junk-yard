from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal


class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str


class FlashcardCreate(BaseModel):
    chinese: str
    pinyin: str
    english: str
    category: str

class FlashcardUpdate(BaseModel):
    chinese: Optional[str] = None
    pinyin: Optional[str] = None
    english: Optional[str] = None
    category: Optional[str] = None

class FlashcardOut(BaseModel):
    id: int
    chinese: str
    pinyin: str
    english: str
    category: str
    studied: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class CardViewOut(BaseModel):
    id: int
    card_id: int
    card_chinese: str
    card_english: str
    viewed_at: datetime

    class Config:
        from_attributes = True

class UserDetailOut(UserOut):
    card_views: list[CardViewOut]

class AdminUpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Literal["user", "admin"]] = None

class SelfChangePassword(BaseModel):
    current_password: str
    new_password: str

class MarkStudiedRequest(BaseModel):
    studied: bool = True
