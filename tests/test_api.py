"""Tests for the FastAPI application."""

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_metadata() -> None:
    response = client.get("/api")
    assert response.status_code == 200
    assert "message" in response.json()
