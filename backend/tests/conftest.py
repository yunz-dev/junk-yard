import os
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app import models
from app.auth import hash_password

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(setup_db):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def db(setup_db):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def admin_token(client):
    db = TestingSessionLocal()
    user = models.User(username="admin", hashed_password=hash_password("admin123"), role="admin")
    db.add(user)
    db.commit()
    db.close()
    resp = client.post("/api/login", json={"username": "admin", "password": "admin123"})
    return resp.json()["access_token"]


@pytest.fixture()
def user_token(client):
    resp = client.post("/api/register", json={"username": "amy", "password": "meow"})
    return resp.json()["access_token"]


@pytest.fixture()
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture()
def user_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture()
def sample_card(client, admin_headers):
    resp = client.post(
        "/api/flashcards",
        json={"chinese": "你好", "pinyin": "nǐ hǎo", "english": "hello", "category": "Greetings"},
        headers=admin_headers,
    )
    return resp.json()
