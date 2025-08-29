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
from fastapi.middleware.cors import CORSMiddleware
import os

# Routers encapsulate feature areas; the verify router handles KYB checks.
from .routers import verify


def create_app() -> FastAPI:
    """Factory to create the FastAPI app.

    Using a factory helps testing (fresh app per test) and future configuration
    (e.g., dependency injection, settings, middleware) without side effects.
    """

    # Title and version can be surfaced in OpenAPI docs.
    app = FastAPI(title="Business Entity Resolution API", version="0.1.0")

    # CORS: allow the local web dev server to call the API from the browser.
    # Origins are configured via CORS_ORIGINS (comma-separated), defaulting to
    # common Vite dev hosts. In production, set a strict allowlist.
    origins_env = os.getenv("CORS_ORIGINS")
    if origins_env:
        allow_origins = [o.strip() for o in origins_env.split(",") if o.strip()]
    else:
        allow_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"]
    )

    # Health check: simple and dependency-free to maximize reliability.
    @app.get("/health", tags=["system"])  # GET /health -> {"status": "ok"}
    def health() -> dict[str, str]:
        return {"status": "ok"}

    # Register domain routers under a versioned API prefix.
    app.include_router(verify.router, prefix="/v1")

    return app


# ASGI entrypoint used by uvicorn
app = create_app()
