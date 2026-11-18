import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import University


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestingSessionLocal() as db:
        db.add(University(
            name="Test University",
            slug="test-university",
            state="Lagos",
            institution_type="university",
        ))
        db.commit()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def register_and_get_token(client, email, role):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "CampusNest Test User",
            "email": email,
            "password": "strong-password-123",
            "role": role,
        },
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def listing_payload():
    return {
        "title": "Clean student room near campus",
        "description": "A clean and secure student room close to the university gate.",
        "accommodation_type": "single room",
        "price": "250000.00",
        "price_period": "yearly",
        "area": "Akoka",
        "address": "12 Campus Road, Akoka",
        "university_id": 1,
    }


def test_landlord_can_create_listing_and_owns_it(client):
    token = register_and_get_token(client, "landlord@example.com", "landlord")
    response = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json()["owner_id"] == 1
    assert response.json()["title"] == listing_payload()["title"]


def test_student_cannot_create_listing(client):
    token = register_and_get_token(client, "student@example.com", "student")
    response = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_listing_creation_requires_login(client):
    response = client.post("/accommodations/", json=listing_payload())
    assert response.status_code == 401


def test_listing_requires_existing_university(client):
    token = register_and_get_token(client, "agent@example.com", "agent")
    payload = listing_payload()
    payload["university_id"] = 999
    response = client.post(
        "/accommodations/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_owner_can_update_listing_but_other_user_cannot(client):
    owner_token = register_and_get_token(client, "owner@example.com", "landlord")
    other_token = register_and_get_token(client, "other@example.com", "agent")
    created = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    listing_id = created.json()["id"]

    forbidden = client.patch(
        f"/accommodations/{listing_id}",
        json={"price": "300000"},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert forbidden.status_code == 403

    updated = client.patch(
        f"/accommodations/{listing_id}",
        json={"price": "300000"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert updated.status_code == 200
    assert updated.json()["price"] == "300000.00"


def test_owner_can_delete_listing(client):
    token = register_and_get_token(client, "delete@example.com", "landlord")
    created = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )
    listing_id = created.json()["id"]

    deleted = client.delete(
        f"/accommodations/{listing_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert deleted.status_code == 204
    assert client.get(f"/accommodations/{listing_id}").status_code == 404


def test_invalid_listing_values_are_rejected(client):
    token = register_and_get_token(client, "invalid@example.com", "landlord")
    payload = listing_payload()
    payload["price"] = "0"
    response = client.post(
        "/accommodations/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
