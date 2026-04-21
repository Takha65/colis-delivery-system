"""Tests d'integration du endpoint health."""
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_returns_ok() -> None:
    """Le endpoint /health doit retourner un statut OK."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app" in data
    assert "version" in data
