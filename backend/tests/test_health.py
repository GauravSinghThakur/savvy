"""
Health check tests

Validates that the `/health` endpoint responds with a minimal OK payload. Uses
FastAPI's TestClient for simple, synchronous testing.
"""

from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_health_ok() -> None:
    """GET /health returns 200 with {"status": "ok"}."""

    app = create_app()  # fresh app instance for test isolation
    client = TestClient(app)

    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

