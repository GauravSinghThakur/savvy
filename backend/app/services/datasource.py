"""
Data source abstraction and in-memory dataset

This module defines a minimal interface for looking up a business by name and
country and provides an in-memory implementation suitable for development and
testing. Replace or extend with real registry integrations in future work.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json

from pydantic import BaseModel, Field, ValidationError


@dataclass(frozen=True)
class BusinessRecord:
    """Normalized business record returned by a data provider.

    Attributes:
      legal_name: Canonical or normalized legal name.
      address_line1: Simple street line placeholder.
      city: City or locality.
      country: ISO2 country code (uppercased).
      registration_status: Simplified status string (e.g., "Active").
    """

    legal_name: str
    address_line1: str
    city: str
    country: str
    registration_status: str


class DataProvider:
    """Simple interface for business lookups by name and country.

    Implementations should perform a case-insensitive match and return a
    `BusinessRecord` on success or `None` when not found.
    """

    def lookup_business(self, name: str, country: str) -> Optional[BusinessRecord]:  # noqa: D401
        """Look up a business by name and country."""

        raise NotImplementedError

    def search_businesses(
        self, query: str, country: Optional[str] = None, limit: int = 10
    ) -> list[BusinessRecord]:
        """Case-insensitive substring search by legal name.

        Parameters:
          query: The partial name to match (e.g., "acme").
          country: Optional ISO2 filter; when set, restrict results to that country.
          limit: Maximum number of results to return.
        """

        raise NotImplementedError


class InMemoryDataProvider(DataProvider):
    """Static, in-memory provider with a tiny sample dataset.

    This allows realistic responses during scaffolding without external
    dependencies.
    """

    def __init__(self) -> None:
        # Internal index: (name_lower, country_upper) -> BusinessRecord
        self._data: dict[tuple[str, str], BusinessRecord] = {}

        # Seed a few sample records. Extend as needed for demos/tests.
        self._add(
            BusinessRecord(
                legal_name="Acme Corp",
                address_line1="123 Main St",
                city="Springfield",
                country="US",
                registration_status="Active",
            )
        )
        self._add(
            BusinessRecord(
                legal_name="Globex LLC",
                address_line1="1 Long Acre",
                city="London",
                country="GB",
                registration_status="Inactive",
            )
        )

    def _add(self, rec: BusinessRecord) -> None:
        """Add a record to the internal index."""

        key = (rec.legal_name.lower(), rec.country.upper())
        self._data[key] = rec

    def lookup_business(self, name: str, country: str) -> Optional[BusinessRecord]:
        """Case-insensitive exact-name match within a country.

        For MVP simplicity, we normalize by trimming and title-casing names when
        comparing; production systems may use fuzzy matching.
        """

        normalized_name = name.strip().title()
        code = country.strip().upper()
        return self._data.get((normalized_name.lower(), code))

    def search_businesses(
        self, query: str, country: Optional[str] = None, limit: int = 10
    ) -> list[BusinessRecord]:
        """Linear scan over the small in-memory index for substring matches."""

        q = query.strip().lower()
        code = country.strip().upper() if country else None
        results: list[BusinessRecord] = []
        for (name_key, ctry), rec in self._data.items():
            if q in name_key and (code is None or code == ctry):
                results.append(rec)
                if len(results) >= limit:
                    break
        return results


class _RecordModel(BaseModel):
    """Pydantic schema used to validate JSON seed records.

    Using a separate validation model keeps parsing concerns isolated and allows
    clearer error messages when loading from files.
    """

    legal_name: str = Field(min_length=1)
    address_line1: str = Field(min_length=1)
    city: str = Field(min_length=1)
    country: str = Field(min_length=2, max_length=2)
    registration_status: str = Field(min_length=1)


class FileDataProvider(DataProvider):
    """File-backed provider that loads business records from a JSON file.

    File format:
      A JSON array of objects with the fields defined in `_RecordModel`.

    Loading strategy:
      The file is read once during initialization, validated, and stored in an
      internal index for fast lookups.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._data: dict[tuple[str, str], BusinessRecord] = {}

        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Seed file not found: {self._path}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in seed file: {self._path}") from e

        if not isinstance(raw, list):
            raise ValueError("Seed JSON must be a list of records")

        for idx, item in enumerate(raw):
            try:
                rec = _RecordModel.model_validate(item)
            except ValidationError as e:
                # Include index to ease troubleshooting of malformed entries.
                raise ValueError(f"Invalid record at index {idx}: {e}") from e

            # Normalize country and name for predictable lookups
            b = BusinessRecord(
                legal_name=rec.legal_name.strip().title(),
                address_line1=rec.address_line1.strip(),
                city=rec.city.strip(),
                country=rec.country.strip().upper(),
                registration_status=rec.registration_status.strip().title(),
            )
            key = (b.legal_name.lower(), b.country)
            self._data[key] = b

    def lookup_business(self, name: str, country: str) -> Optional[BusinessRecord]:
        """Retrieve a record by normalized name and country."""

        normalized_name = name.strip().title()
        code = country.strip().upper()
        return self._data.get((normalized_name.lower(), code))

    def search_businesses(
        self, query: str, country: Optional[str] = None, limit: int = 10
    ) -> list[BusinessRecord]:
        """Substring search over the loaded dataset.

        For simplicity this performs an O(n) scan; for larger files consider
        indexing by trigram or using a search library.
        """

        q = query.strip().lower()
        code = country.strip().upper() if country else None
        results: list[BusinessRecord] = []
        for (name_key, ctry), rec in self._data.items():
            if q in name_key and (code is None or code == ctry):
                results.append(rec)
                if len(results) >= limit:
                    break
        return results
