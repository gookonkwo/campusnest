import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_register_student_and_read_profile(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Ada Student",
            "email": "ADA@example.com",
            "password": "strong-password-123",
            "role": "student",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "ada@example.com"
    assert data["user"]["role"] == "student"
    assert "hashed_password" not in data["user"]

    profile = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {data['access_token']}"},
    )
    assert profile.status_code == 200
    assert profile.json()["full_name"] == "Ada Student"


@pytest.mark.parametrize("role", ["landlord", "agent"])
def test_register_landlord_and_agent(client, role):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Property Owner",
            "email": f"{role}@example.com",
            "password": "strong-password-123",
            "role": role,
        },
    )

    assert response.status_code == 201
    assert response.json()["user"]["role"] == role


def test_public_registration_cannot_create_admin(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Not an Admin",
            "email": "admin@example.com",
            "password": "strong-password-123",
            "role": "admin",
        },
    )

    assert response.status_code == 422


def test_duplicate_email_is_rejected_case_insensitively(client):
    payload = {
        "full_name": "First User",
        "email": "person@example.com",
        "password": "strong-password-123",
    }
    assert client.post("/auth/register", json=payload).status_code == 201

    payload["email"] = "PERSON@example.com"
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409


def test_login_returns_token_and_rejects_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "full_name": "Login User",
            "email": "login@example.com",
            "password": "strong-password-123",
        },
    )

    success = client.post(
        "/auth/login",
        json={
            "email": "LOGIN@example.com",
            "password": "strong-password-123",
        },
    )
    assert success.status_code == 200
    assert success.json()["token_type"] == "bearer"

    failure = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "wrong-password",
        },
    )
    assert failure.status_code == 401


def test_profile_requires_valid_token(client):
    assert client.get("/auth/me").status_code == 401
    assert client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    ).status_code == 401


def test_password_must_be_at_least_eight_characters(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Short Password",
            "email": "short@example.com",
            "password": "short",
        },
    )
    assert response.status_code == 422
