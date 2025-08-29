"""
Verification endpoint tests (stub)

Covers the MVP `/v1/verify` behavior defined by the placeholder implementation
in `backend.app.routers.verify`. Ensures deterministic responses for clear and
review_required scenarios.
"""

from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_verify_clear_minimal_payload() -> None:
    """A neutral name should yield status=clear and no risk flags."""

    client = TestClient(create_app())
    payload = {"name": "Acme Corp", "country": "us"}

    resp = client.post("/v1/verify", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["legal_name"] == "Acme Corp"
    assert data["address"]["country"] == "US"
    assert data["status"] == "clear"
    assert data.get("risk_flags") is None


def test_verify_review_required_on_hit() -> None:
    """Names containing 'test' should simulate a possible match and require review."""

    client = TestClient(create_app())
    payload = {"name": "Test Holdings", "country": "GB"}

    resp = client.post("/v1/verify", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["status"] == "review_required"
    assert data["risk_flags"] == ["possible_match"]

