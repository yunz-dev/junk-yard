import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import hash_password, verify_password
from app.main import app
from app.database import Base, get_db

# ── in-memory SQLite DB so tests never touch the real nihowl.db ──────────────
# StaticPool forces all connections to reuse the same in-memory database,

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test, drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(setup_db):  # pytest will automatically use the setup_db fixture first
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# unit tests

def test_hash_password_does_not_return_plain_password():
    password = "secret123"
    hashed = hash_password(password)
    assert hashed != password


def test_verify_password_accepts_correct_password():
    password = "secret123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_rejects_wrong_password():
    password = "secret123"
    hashed = hash_password(password)
    assert verify_password("wrong-password", hashed) is False


# integration tests

def test_register_duplicate_username_returns_400(client):
    """Registering the same username twice should be rejected with 400."""
    payload = {"username": "amy", "password": "meow"}
    client.post("/api/register", json=payload)  # first registration succeeds
    response = client.post("/api/register", json=payload)  # duplicate
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_login_with_correct_password_returns_token(client):
    """Registering then logging in with the right password should return a JWT."""
    payload = {"username": "amy", "password": "meow"}
    client.post("/api/register", json=payload)

    response = client.post("/api/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "amy"


def test_login_with_wrong_password_returns_401(client):
    """Registering then logging in with the wrong password should return 401."""
    client.post("/api/register", json={"username": "amy", "password": "meow"})

    response = client.post("/api/login", json={"username": "amy", "password": "wrong-password"})
    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]
