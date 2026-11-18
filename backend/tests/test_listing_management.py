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
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        db = testing_session()
        db.add(
            University(
                name="University of Lagos",
                slug="unilag",
                state="Lagos",
                institution_type="federal",
            )
        )
        db.commit()
        db.close()
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def register(client, email, role):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "CampusNest User",
            "email": email,
            "password": "strong-password-123",
            "role": role,
        },
    )
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def listing_payload(title="Student room near campus"):
    return {
        "title": title,
        "description": "A clean and secure room close to the university.",
        "accommodation_type": "single_room",
        "price": "250000.00",
        "price_period": "yearly",
        "area": "Akoka",
        "address": "Akoka, Lagos",
        "university_id": 1,
        "is_available": True,
    }


def test_landlord_can_create_listing(client):
    headers = register(client, "landlord@example.com", "landlord")
    response = client.post("/accommodations/", json=listing_payload(), headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Student room near campus"
    assert "owner_id" not in response.json()


def test_agent_can_create_listing(client):
    headers = register(client, "agent@example.com", "agent")
    response = client.post("/accommodations/", json=listing_payload(), headers=headers)
    assert response.status_code == 201


def test_student_cannot_create_listing(client):
    headers = register(client, "student@example.com", "student")
    response = client.post("/accommodations/", json=listing_payload(), headers=headers)
    assert response.status_code == 403


def test_listing_creation_requires_login(client):
    response = client.post("/accommodations/", json=listing_payload())
    assert response.status_code == 401


def test_landlord_can_update_own_listing(client):
    headers = register(client, "owner@example.com", "landlord")
    created = client.post("/accommodations/", json=listing_payload(), headers=headers)
    response = client.patch(
        f"/accommodations/{created.json()['id']}",
        json={"price": "300000.00", "area": "Yaba"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["price"] == "300000.00"
    assert response.json()["area"] == "Yaba"


def test_landlord_cannot_update_another_users_listing(client):
    owner_headers = register(client, "owner@example.com", "landlord")
    other_headers = register(client, "other@example.com", "landlord")
    created = client.post("/accommodations/", json=listing_payload(), headers=owner_headers)
    response = client.patch(
        f"/accommodations/{created.json()['id']}",
        json={"price": "300000.00"},
        headers=other_headers,
    )
    assert response.status_code == 403


def test_landlord_can_delete_own_listing(client):
    headers = register(client, "delete@example.com", "landlord")
    created = client.post("/accommodations/", json=listing_payload(), headers=headers)
    listing_id = created.json()["id"]
    response = client.delete(f"/accommodations/{listing_id}", headers=headers)
    assert response.status_code == 204
    assert client.get(f"/accommodations/{listing_id}").status_code == 404


def test_landlord_cannot_delete_another_users_listing(client):
    owner_headers = register(client, "owner@example.com", "landlord")
    other_headers = register(client, "other@example.com", "agent")
    created = client.post("/accommodations/", json=listing_payload(), headers=owner_headers)
    response = client.delete(
        f"/accommodations/{created.json()['id']}",
        headers=other_headers,
    )
    assert response.status_code == 403


def test_listing_creation_rejects_unknown_university(client):
    headers = register(client, "university@example.com", "landlord")
    payload = listing_payload()
    payload["university_id"] = 999
    response = client.post("/accommodations/", json=payload, headers=headers)
    assert response.status_code == 404


def test_listing_creation_rejects_non_positive_price(client):
    headers = register(client, "price@example.com", "landlord")
    payload = listing_payload()
    payload["price"] = "0"
    response = client.post("/accommodations/", json=payload, headers=headers)
    assert response.status_code == 422


def test_listing_update_rejects_empty_changes(client):
    headers = register(client, "empty@example.com", "landlord")
    created = client.post("/accommodations/", json=listing_payload(), headers=headers)
    response = client.patch(
        f"/accommodations/{created.json()['id']}",
        json={},
        headers=headers,
    )
    assert response.status_code == 422
