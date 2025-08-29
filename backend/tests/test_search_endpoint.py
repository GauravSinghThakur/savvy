"""
Search endpoint tests

Validates minimal functionality of GET /v1/verify/search using the default
seed file, including substring matching and optional country filter.
"""

from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_search_returns_candidates_by_partial_name() -> None:
    """Searching for 'acme' should return Acme Corp in the results."""

    client = TestClient(create_app())
    resp = client.get("/v1/verify/search", params={"q": "acme"})
    assert resp.status_code == 200
    data = resp.json()
    assert any(item["legal_name"] == "Acme Corp" for item in data)


def test_search_can_filter_by_country() -> None:
    """Filtering by GB should exclude US-only entities when name overlaps."""

    client = TestClient(create_app())
    resp = client.get("/v1/verify/search", params={"q": "globex", "country": "gb"})
    assert resp.status_code == 200
    data = resp.json()
    assert all(item["address"]["country"] == "GB" for item in data)


def test_search_enforces_min_query_length() -> None:
    """q shorter than 2 should fail validation (422)."""

    client = TestClient(create_app())
    resp = client.get("/v1/verify/search", params={"q": "a"})
    assert resp.status_code == 422

