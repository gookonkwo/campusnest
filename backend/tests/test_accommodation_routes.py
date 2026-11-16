from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Accommodation, University


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


def add_sample_accommodations():
    from app.database import get_db

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    university = University(
        name="University of Lagos",
        slug="unilag",
        state="Lagos",
        institution_type="federal",
    )
    db.add(university)
    db.flush()

    db.add_all(
        [
            Accommodation(
                title="Affordable private hostel",
                description="A room close to campus.",
                accommodation_type="private_hostel",
                price=Decimal("250000.00"),
                price_period="yearly",
                area="Akoka",
                address="Akoka, Lagos",
                university_id=university.id,
                is_available=True,
            ),
            Accommodation(
                title="Shared student apartment",
                description="A shared apartment for students.",
                accommodation_type="shared_apartment",
                price=Decimal("150000.00"),
                price_period="yearly",
                area="Yaba",
                address="Yaba, Lagos",
                university_id=university.id,
                is_available=False,
            ),
        ]
    )
    db.commit()
    db_generator.close()


def test_list_accommodations_returns_empty_list(client):
    response = client.get("/accommodations")

    assert response.status_code == 200
    assert response.json() == []


def test_list_accommodations_filters_available_listings(client):
    add_sample_accommodations()

    response = client.get(
        "/accommodations",
        params={"area": "Akoka", "min_price": "200000"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Affordable private hostel"
    assert data[0]["is_available"] is True


def test_list_accommodations_rejects_invalid_price_range(client):
    response = client.get(
        "/accommodations",
        params={"min_price": "300000", "max_price": "100000"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "min_price cannot be greater than max_price"


def test_get_accommodation_returns_404_when_missing(client):
    response = client.get("/accommodations/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Accommodation not found"}
