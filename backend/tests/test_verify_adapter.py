"""
Verification with in-memory data provider

Ensures the `/v1/verify` endpoint maps records from the in-memory data source
and handles unknown businesses gracefully.
"""

from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_verify_known_business_uses_dataset() -> None:
    """Known record should return Active status and concrete address fields."""

    client = TestClient(create_app())
    payload = {"name": "acme corp", "country": "us"}  # lowercased to test normalization

    resp = client.post("/v1/verify", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert data["legal_name"] == "Acme Corp"
    assert data["registration_status"] == "Active"
    assert data["address"]["country"] == "US"
    assert data["address"]["line1"] != "Unknown"


def test_verify_unknown_business_defaults() -> None:
    """Unknown record should yield registration_status=Unknown and placeholder address."""

    client = TestClient(create_app())
    payload = {"name": "Unknown Trading", "country": "CA"}

    resp = client.post("/v1/verify", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert data["registration_status"] == "Unknown"
    assert data["address"]["line1"] == "Unknown"
    assert data["address"]["country"] == "CA"

