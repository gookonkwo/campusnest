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


def test_frontend_origin_is_allowed_by_cors() -> None:
    response = client.options(
        "/accommodations/",
        headers={
            "Origin": "http://localhost:5500",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5500"
