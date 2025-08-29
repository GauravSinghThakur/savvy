"""
File-backed provider test

Uses a temporary JSON file to exercise the FileDataProvider path controlled by
the DATA_SEED_PATH environment variable.
"""

import json
import os
import tempfile
from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_verify_uses_file_seed_when_configured() -> None:
    """Setting DATA_SEED_PATH should cause the app to load from that file."""

    seed = [
        {
            "legal_name": "File Seed Co",
            "address_line1": "9 Temp Way",
            "city": "Testville",
            "country": "US",
            "registration_status": "Active",
        }
    ]

    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "seed.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(seed, f)

        prev = os.environ.get("DATA_SEED_PATH")
        os.environ["DATA_SEED_PATH"] = path
        try:
            client = TestClient(create_app())
            resp = client.post("/v1/verify", json={"name": "File Seed Co", "country": "US"})
            assert resp.status_code == 200
            data = resp.json()
            assert data["legal_name"] == "File Seed Co"
            assert data["registration_status"] == "Active"
            assert data["address"]["city"] == "Testville"
        finally:
            # Restore to avoid impacting other tests
            if prev is None:
                os.environ.pop("DATA_SEED_PATH", None)
            else:
                os.environ["DATA_SEED_PATH"] = prev

