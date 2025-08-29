# Repository Guidelines

## Project Structure & Module Organization
- Current docs at root: `Project Brief.md`, `prd.md`, `system_architecture.md`, `test_plan.md`, `Epics and Stories.md`.
- Planned layout (when code is added):
  - `backend/` FastAPI microservices (`verification`, `screening`), `backend/tests/`.
  - `backend/data/` JSON seeds for local development (e.g., `seed_entities.json`).
  - `web/` React dashboard (`web/src/`, `web/public/`, `web/src/__tests__/`).
  - `infra/` IaC and API Gateway config; `docs/` for extended documentation.

## Build, Test, and Development Commands
- Backend: `uvicorn backend.app.main:app --reload` (run API), `pytest -q` (tests), `ruff . && black .` (lint/format).
 - Makefile: `make help` lists common tasks; try `make setup-backend`, `make run-backend`, `make test-backend`, `make web-dev`.
 - Bootstrap: `scripts/dev/bootstrap.ps1` (PowerShell) sets up venv and installs web deps.
 - Quickstart: See `README.md` for front-end and back-end run instructions.
- Web (expected): `npm install && npm start` (dev server), `npm test -- --watch=false` (unit tests).
- Infra (if used): `terraform init && terraform apply` or `make deploy`.

## Coding Style & Naming Conventions
- Python: format with Black (88 cols) and Ruff; type hints required; snake_case for functions/vars, PascalCase for classes; FastAPI routers in `app/routers/verify.py` style.
- JavaScript/React: Prettier + ESLint; camelCase for functions/vars, PascalCase for components; one component per file.
- Files: use kebab-case for non-components; tests mirror source paths.

## Commenting Standards
- Add a brief module/file header comment describing purpose and context.
- For every function, class, and significant block, include concise comments explaining inputs, outputs, side effects, and any non-obvious logic.
- For config files that support comments (e.g., `.gitignore`, `requirements.txt`, YAML), annotate sections with what and why. For formats that don’t (e.g., JSON), add a sibling `README` note or inline comments in the code that loads the config.
- Keep comments current with code; update or remove stale comments during changes.

## Testing Guidelines
- Refer to `test_plan.md` for scenarios. Aim ≥80% coverage on services handling verification and screening.
- Python: `pytest`, place tests in `backend/tests/` with `test_*.py`; use HTTPX client for API tests.
- Web: React Testing Library in `web/src/__tests__/` with `*.test.jsx`.

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`.
  - Example: `feat(api): add /verify endpoint with risk status`.
- PRs: include what/why, linked issues, API changes (OpenAPI diff or curl example), and screenshots for UI.
- Checks: tests pass, lint/format clean, docs updated.

## Security & Configuration
- Do not commit secrets. Use environment variables (e.g., `API_KEY`, `DATABASE_URL`) and a local `.env` excluded by `.gitignore`.
- Encrypt data in transit; follow authentication at the gateway (API keys/OAuth per PRD).
 - Data seeds: set `DATA_SEED_PATH` to point to an alternate JSON file; defaults to `backend/data/seed_entities.json`.

## Architecture Overview
- Microservices via FastAPI behind an API Gateway; React dashboard; PostgreSQL for auth and search history (see `system_architecture.md`).
