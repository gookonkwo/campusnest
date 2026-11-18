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

    db = testing_session()
    db.add(
        University(
            name="Example University",
            slug="example-university",
            state="Lagos",
            institution_type="university",
        )
    )
    db.commit()
    db.close()

    def override_get_db():
        session = testing_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def register(client, role, email):
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
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def listing_payload():
    return {
        "title": "Clean private student room",
        "description": "A clean and secure room close to the university campus.",
        "accommodation_type": "single_room",
        "price": "250000",
        "price_period": "yearly",
        "area": "Akoka",
        "address": "12 Example Street, Akoka",
        "university_id": 1,
    }


def test_landlord_can_create_view_update_and_delete_own_listing(client):
    headers = register(client, "landlord", "landlord@example.com")

    created = client.post("/accommodations/", json=listing_payload(), headers=headers)
    assert created.status_code == 201
    listing_id = created.json()["id"]
    assert created.json()["owner_id"] is not None

    mine = client.get("/accommodations/mine", headers=headers)
    assert mine.status_code == 200
    assert len(mine.json()) == 1
    assert mine.json()[0]["id"] == listing_id

    update_data = listing_payload()
    update_data["title"] = "Updated private student room"
    update_data["is_available"] = False
    updated = client.put(
        f"/accommodations/{listing_id}",
        json=update_data,
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated private student room"
    assert updated.json()["is_available"] is False

    deleted = client.delete(f"/accommodations/{listing_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/accommodations/{listing_id}").status_code == 404


def test_agent_can_create_listing(client):
    headers = register(client, "agent", "agent@example.com")
    response = client.post("/accommodations/", json=listing_payload(), headers=headers)
    assert response.status_code == 201


def test_student_cannot_create_or_manage_listings(client):
    headers = register(client, "student", "student@example.com")
    payload = listing_payload()

    assert client.post("/accommodations/", json=payload, headers=headers).status_code == 403
    assert client.get("/accommodations/mine", headers=headers).status_code == 403


def test_listing_management_requires_login(client):
    assert client.post("/accommodations/", json=listing_payload()).status_code == 401
    assert client.get("/accommodations/mine").status_code == 401


def test_owner_cannot_edit_or_delete_another_owners_listing(client):
    first_owner = register(client, "landlord", "first@example.com")
    second_owner = register(client, "landlord", "second@example.com")

    created = client.post(
        "/accommodations/",
        json=listing_payload(),
        headers=first_owner,
    )
    listing_id = created.json()["id"]

    assert client.put(
        f"/accommodations/{listing_id}",
        json=listing_payload(),
        headers=second_owner,
    ).status_code == 403
    assert client.delete(
        f"/accommodations/{listing_id}",
        headers=second_owner,
    ).status_code == 403


def test_listing_requires_existing_university(client):
    headers = register(client, "landlord", "owner@example.com")
    payload = listing_payload()
    payload["university_id"] = 999

    response = client.post("/accommodations/", json=payload, headers=headers)
    assert response.status_code == 404


def test_listing_validation_rejects_invalid_price_and_type(client):
    headers = register(client, "landlord", "owner@example.com")

    invalid_price = listing_payload()
    invalid_price["price"] = "0"
    assert client.post(
        "/accommodations/",
        json=invalid_price,
        headers=headers,
    ).status_code == 422

    invalid_type = listing_payload()
    invalid_type["accommodation_type"] = "palace"
    assert client.post(
        "/accommodations/",
        json=invalid_type,
        headers=headers,
    ).status_code == 422
