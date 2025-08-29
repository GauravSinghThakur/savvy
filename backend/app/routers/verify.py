"""
Verification endpoints

Provides the `/v1/verify` API used by developers to submit a business name and
country and receive a structured response with basic verification fields and a
simple risk status, as outlined in the PRD.
"""

from typing import Literal, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, ConfigDict

# Import the data provider abstraction to retrieve basic business facts.
from ..services.datasource import (
    BusinessRecord,
    DataProvider,
    InMemoryDataProvider,
    FileDataProvider,
)
from pathlib import Path
import os


router = APIRouter(prefix="", tags=["verify"])  # Empty prefix; mounted at /v1


_PROVIDER: DataProvider | None = None
_PROV_KEY: str | None = None


def get_provider() -> DataProvider:
    """Dependency that supplies a data provider instance.

    Using a function allows dependency overrides in tests if needed, while the
    default returns a simple in-memory dataset for local development.
    """

    # Decide provider based on presence of a JSON seed file. This supports
    # local iteration on data without code changes.
    path_env = os.getenv("DATA_SEED_PATH", "backend/data/seed_entities.json")
    key = "MEMORY"
    seed_path = Path(path_env)
    if seed_path.exists():
        key = str(seed_path.resolve())

    global _PROVIDER, _PROV_KEY
    if _PROVIDER is None or _PROV_KEY != key:
        _PROV_KEY = key
        _PROVIDER = (
            FileDataProvider(seed_path) if key != "MEMORY" else InMemoryDataProvider()
        )

    return _PROVIDER


class VerifyRequest(BaseModel):
    """Request payload for a verification lookup.

    Fields:
    - name: Business name to verify.
    - country: ISO 3166-1 alpha-2 country code (e.g., "US").
    """

    name: str = Field(..., min_length=1, description="Business legal or trade name")
    country: str = Field(..., min_length=2, max_length=2, description="ISO2 code")

    # OpenAPI example to guide integrators in docs (/docs)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Acme Corp", "country": "US"}
        }
    )


class Address(BaseModel):
    """Basic business address fields.

    This is a placeholder for the MVP; real integrations may provide more
    granular fields (e.g., region codes, geocodes).
    """

    line1: str
    city: str
    country: str


class VerifyResponse(BaseModel):
    """Standardized verification result.

    Fields:
    - legal_name: Verified/normalized name when available.
    - address: Minimal address object.
    - registration_status: Simplified status from registries (e.g., Active).
    - risk_flags: Optional list of screening hits (e.g., ["sanctions_hit"]).
    - status: Top-level decision helper: "clear" or "review_required".
    """

    legal_name: str
    address: Address
    registration_status: Literal["Active", "Inactive", "Unknown"]
    risk_flags: Optional[list[str]] = None
    status: Literal["clear", "review_required"]

    # OpenAPI example for a clear response
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "legal_name": "Acme Corp",
                "address": {"line1": "123 Main St", "city": "Springfield", "country": "US"},
                "registration_status": "Active",
                "status": "clear",
            }
        }
    )


@router.post(
    "/verify",
    response_model=VerifyResponse,
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "clear": {
                            "summary": "No screening hits",
                            "value": {
                                "legal_name": "Acme Corp",
                                "address": {"line1": "123 Main St", "city": "Springfield", "country": "US"},
                                "registration_status": "Active",
                                "status": "clear",
                            },
                        },
                        "review": {
                            "summary": "Possible match triggers review",
                            "value": {
                                "legal_name": "Test Holdings",
                                "address": {"line1": "Unknown", "city": "Unknown", "country": "GB"},
                                "registration_status": "Unknown",
                                "risk_flags": ["possible_match"],
                                "status": "review_required",
                            },
                        },
                    }
                }
            }
        }
    },
)
def verify(
    req: VerifyRequest,
    provider: DataProvider = Depends(get_provider),
) -> VerifyResponse:
    """Stub verification endpoint for the MVP.

    This implementation returns a deterministic example payload suitable for
    front-end and integration scaffolding. Replace with real data sources and
    screening logic in later iterations.
    """

    # For the stub, infer a trivial "hit" when the name contains the word "test".
    has_hit = "test" in req.name.lower()

    # Try to resolve a known business from the data provider. If not found,
    # return a minimal structure with unknown fields.
    rec: Optional[BusinessRecord] = provider.lookup_business(req.name, req.country)

    if rec is None:
        # Unknown business: supply normalized inputs and default values.
        legal_name = req.name.strip().title()
        address = Address(
            line1="Unknown",
            city="Unknown",
            country=req.country.upper(),
        )
        registration_status: Literal["Active", "Inactive", "Unknown"] = "Unknown"
    else:
        # Map provider record to response schema.
        legal_name = rec.legal_name
        address = Address(line1=rec.address_line1, city=rec.city, country=rec.country)
        # Constrain to allowed literals for the API response.
        registration_status = (
            rec.registration_status
            if rec.registration_status in {"Active", "Inactive"}
            else "Unknown"
        )

    risk_flags = ["possible_match"] if has_hit else None
    status: Literal["clear", "review_required"] = (
        "review_required" if has_hit else "clear"
    )

    return VerifyResponse(
        legal_name=legal_name,
        address=address,
        registration_status=registration_status,
        risk_flags=risk_flags,
        status=status,
    )


class Candidate(BaseModel):
    """Slimmed candidate record for search results.

    Used by the search endpoint to list possible matches before running full
    verification/screening.
    """

    legal_name: str
    address: Address
    registration_status: Literal["Active", "Inactive", "Unknown"]

    # Example used in OpenAPI docs
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "legal_name": "Acme Corp",
                "address": {"line1": "123 Main St", "city": "Springfield", "country": "US"},
                "registration_status": "Active",
            }
        }
    )


@router.get(
    "/verify/search",
    response_model=list[Candidate],
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "acme": {
                            "summary": "Search for 'acme'",
                            "value": [
                                {
                                    "legal_name": "Acme Corp",
                                    "address": {"line1": "123 Main St", "city": "Springfield", "country": "US"},
                                    "registration_status": "Active",
                                }
                            ],
                        }
                    }
                }
            }
        }
    },
)
def search(
    q: str, country: Optional[str] = None, limit: int = 10, provider: DataProvider = Depends(get_provider)
) -> list[Candidate]:
    """Search for businesses by partial legal name.

    Query params:
      q: partial name to match (min length 2)
      country: optional ISO2 country filter
      limit: maximum results (default 10)
    """

    q_norm = q.strip()
    if len(q_norm) < 2:
        # FastAPI will convert this ValueError to 422 Unprocessable Entity.
        raise ValueError("q must be at least 2 characters")

    results = provider.search_businesses(q_norm, country=country, limit=limit)
    out: list[Candidate] = []
    for rec in results:
        reg_status: Literal["Active", "Inactive", "Unknown"] = (
            rec.registration_status if rec.registration_status in {"Active", "Inactive"} else "Unknown"
        )
        out.append(
            Candidate(
                legal_name=rec.legal_name,
                address=Address(line1=rec.address_line1, city=rec.city, country=rec.country),
                registration_status=reg_status,
            )
        )
    return out
