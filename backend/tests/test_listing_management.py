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
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def register(client: TestClient, email: str, role: str) -> str:
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


def add_university(client: TestClient) -> None:
    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    db.add(
        University(
            name="University of Lagos",
            slug="unilag",
            state="Lagos",
            institution_type="federal",
        )
    )
    db.commit()
    db_generator.close()


def listing_payload() -> dict:
    return {
        "title": "Comfortable student hostel",
        "description": "A clean and secure student hostel close to campus.",
        "accommodation_type": "private_hostel",
        "price": "250000.00",
        "price_period": "yearly",
        "area": "Akoka",
        "address": "Akoka, Lagos",
        "university_id": 1,
    }


def test_landlord_can_create_and_view_own_listing(client):
    add_university(client)
    token = register(client, "landlord@example.com", "landlord")
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post("/accommodations/", json=listing_payload(), headers=headers)

    assert created.status_code == 201
    data = created.json()
    assert data["title"] == "Comfortable student hostel"
    assert isinstance(data["owner_id"], int)

    mine = client.get("/accommodations/mine", headers=headers)
    assert mine.status_code == 200
    assert len(mine.json()) == 1
    assert mine.json()[0]["id"] == data["id"]


def test_agent_can_create_listing(client):
    add_university(client)
    token = register(client, "agent@example.com", "agent")
    response = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_student_cannot_create_or_manage_listings(client):
    add_university(client)
    token = register(client, "student@example.com", "student")
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post("/accommodations/", json=listing_payload(), headers=headers)
    mine_response = client.get("/accommodations/mine", headers=headers)

    assert create_response.status_code == 403
    assert mine_response.status_code == 403


def test_landlord_can_update_own_listing(client):
    add_university(client)
    token = register(client, "owner@example.com", "landlord")
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/accommodations/", json=listing_payload(), headers=headers)
    listing_id = created.json()["id"]

    updated_payload = listing_payload()
    updated_payload["title"] = "Updated student accommodation"
    updated_payload["is_available"] = False
    updated = client.put(
        f"/accommodations/{listing_id}",
        json=updated_payload,
        headers=headers,
    )

    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated student accommodation"
    assert updated.json()["is_available"] is False


def test_landlord_cannot_change_another_users_listing(client):
    add_university(client)
    first_token = register(client, "first@example.com", "landlord")
    second_token = register(client, "second@example.com", "landlord")
    created = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {first_token}"},
    )

    response = client.put(
        f"/accommodations/{created.json()['id']}",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {second_token}"},
    )
    assert response.status_code == 404


def test_landlord_can_delete_own_listing(client):
    add_university(client)
    token = register(client, "delete@example.com", "landlord")
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/accommodations/", json=listing_payload(), headers=headers)
    listing_id = created.json()["id"]

    deleted = client.delete(f"/accommodations/{listing_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/accommodations/{listing_id}").status_code == 404


def test_listing_creation_rejects_unknown_university(client):
    token = register(client, "unknown-university@example.com", "landlord")
    response = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_listing_creation_requires_authentication(client):
    add_university(client)
    response = client.post("/accommodations/", json=listing_payload())
    assert response.status_code == 401
