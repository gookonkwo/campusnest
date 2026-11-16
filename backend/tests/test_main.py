from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_returns_welcome_message() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to CampusNest API",
        "status": "running",
    }


def test_health_check_returns_healthy_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
