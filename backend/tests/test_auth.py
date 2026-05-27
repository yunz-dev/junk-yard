import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import hash_password, verify_password
from app.main import app
from app.database import Base, get_db

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


# ── Password hashing ──────────────────────────────────────────────────────────

def test_hash_password_does_not_return_plain_password():
    hashed = hash_password("secret123")
    assert hashed != "secret123"


def test_verify_password_accepts_correct_password():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("secret123")
    assert verify_password("wrong-password", hashed) is False


# ── Register ──────────────────────────────────────────────────────────────────

def test_register_returns_token_and_role(client):
    response = client.post("/api/register", json={"username": "amy", "password": "meow"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "amy"
    assert data["role"] == "user"


def test_register_duplicate_username_returns_400(client):
    payload = {"username": "amy", "password": "meow"}
    client.post("/api/register", json=payload)
    response = client.post("/api/register", json=payload)
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


# ── Login ─────────────────────────────────────────────────────────────────────

def test_login_returns_token_and_role(client):
    client.post("/api/register", json={"username": "amy", "password": "meow"})
    response = client.post("/api/login", json={"username": "amy", "password": "meow"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["username"] == "amy"
    assert data["role"] == "user"


def test_login_wrong_password_returns_401(client):
    client.post("/api/register", json={"username": "amy", "password": "meow"})
    response = client.post("/api/login", json={"username": "amy", "password": "wrong"})
    assert response.status_code == 401


def test_login_unknown_user_returns_401(client):
    response = client.post("/api/login", json={"username": "nobody", "password": "x"})
    assert response.status_code == 401


# ── /api/me ───────────────────────────────────────────────────────────────────

def test_me_returns_user_detail_with_card_views(client):
    client.post("/api/register", json={"username": "amy", "password": "meow"})
    token = client.post("/api/login", json={"username": "amy", "password": "meow"}).json()["access_token"]
    response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "amy"
    assert "card_views" in data
    assert isinstance(data["card_views"], list)


def test_me_without_token_returns_401(client):
    response = client.get("/api/me")
    assert response.status_code == 401


def test_me_invalid_token_returns_401(client):
    response = client.get("/api/me", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401


# ── Change own password ───────────────────────────────────────────────────────

def test_change_password_success(client):
    client.post("/api/register", json={"username": "amy", "password": "meow"})
    token = client.post("/api/login", json={"username": "amy", "password": "meow"}).json()["access_token"]
    response = client.put(
        "/api/me",
        json={"current_password": "meow", "new_password": "woof"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    login = client.post("/api/login", json={"username": "amy", "password": "woof"})
    assert login.status_code == 200


def test_change_password_wrong_current_returns_400(client):
    client.post("/api/register", json={"username": "amy", "password": "meow"})
    token = client.post("/api/login", json={"username": "amy", "password": "meow"}).json()["access_token"]
    response = client.put(
        "/api/me",
        json={"current_password": "wrong", "new_password": "woof"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_change_password_requires_auth(client):
    response = client.put("/api/me", json={"current_password": "a", "new_password": "b"})
    assert response.status_code == 401
