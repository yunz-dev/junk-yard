from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .database import get_db
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    from . import models
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    username = decode_access_token(authorization.split(" ", 1)[1])
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


def get_optional_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    from . import models
    if not authorization or not authorization.startswith("Bearer "):
        return None
    username = decode_access_token(authorization.split(" ", 1)[1])
    if not username:
        return None
    return db.query(models.User).filter(models.User.username == username).first()
