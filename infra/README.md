# Infra Placeholder

This folder documents planned infrastructure components and holds IaC stubs.

Planned components:
- API Gateway (single entry point, auth, rate limiting)
- FastAPI services (containerized) behind the gateway
- PostgreSQL (managed)

Notes:
- Use environment variables for secrets (e.g., DATABASE_URL, API_KEY).
- Keep cloud credentials out of the repo; rely on CI/OIDC or local profiles.

