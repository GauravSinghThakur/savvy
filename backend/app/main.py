"""
Application entry point for the FastAPI backend.

Responsibilities:
- Create and configure the FastAPI app instance.
- Register API routers (e.g., verification endpoints).
- Expose lightweight health checks used by CI and infrastructure.

Run locally (example):
    uvicorn backend.app.main:app --reload
"""

from fastapi import FastAPI

# Routers encapsulate feature areas; the verify router handles KYB checks.
from .routers import verify


def create_app() -> FastAPI:
    """Factory to create the FastAPI app.

    Using a factory helps testing (fresh app per test) and future configuration
    (e.g., dependency injection, settings, middleware) without side effects.
    """

    # Title and version can be surfaced in OpenAPI docs.
    app = FastAPI(title="Business Entity Resolution API", version="0.1.0")

    # Health check: simple and dependency-free to maximize reliability.
    @app.get("/health", tags=["system"])  # GET /health -> {"status": "ok"}
    def health() -> dict[str, str]:
        return {"status": "ok"}

    # Register domain routers under a versioned API prefix.
    app.include_router(verify.router, prefix="/v1")

    return app


# ASGI entrypoint used by uvicorn
app = create_app()

