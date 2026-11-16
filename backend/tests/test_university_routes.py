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
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def add_universities():
    # The fixture database is isolated for each test.
    from app.database import SessionLocal

    return SessionLocal


def test_list_universities_returns_empty_list(client):
    response = client.get("/universities")

    assert response.status_code == 200
    assert response.json() == []


def test_list_universities_supports_filters_and_pagination(client):
    # Add records through the same database dependency used by the API.
    from app.database import get_db

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    db.add_all(
        [
            University(
                name="University of Lagos",
                slug="unilag",
                state="Lagos",
                institution_type="federal",
            ),
            University(
                name="Lagos State University",
                slug="lasu",
                state="Lagos",
                institution_type="state",
            ),
            University(
                name="University of Nigeria, Nsukka",
                slug="unn",
                state="Enugu",
                institution_type="federal",
            ),
        ]
    )
    db.commit()
    db_generator.close()

    response = client.get(
        "/universities",
        params={"state": "lagos", "institution_type": "federal", "limit": 1},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "University of Lagos"


def test_get_university_returns_record(client):
    from app.database import get_db

    db_generator = app.dependency_overrides[get_db]()
    db = next(db_generator)
    university = University(
        name="University of Nigeria, Nsukka",
        slug="unn",
        state="Enugu",
        institution_type="federal",
    )
    db.add(university)
    db.commit()
    db.refresh(university)
    university_id = university.id
    db_generator.close()

    response = client.get(f"/universities/{university_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "University of Nigeria, Nsukka"


def test_get_university_returns_404_when_missing(client):
    response = client.get("/universities/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "University not found"}
