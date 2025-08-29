---
name: Project Scaffolding Checklist
about: Set up backend, web, and infra skeletons with tooling
title: "chore(scaffold): project structure and tooling"
labels: ["chore", "scaffolding"]
assignees: []
---

## Goal
Create the initial project structure for the KYB/AML MVP per PRD and architecture docs.

## Scope
- Backend (FastAPI services), Web (React dashboard), Infra (API Gateway/IaC), base CI, and developer tooling.

## Checklist
- [ ] Create directories: `backend/`, `backend/app/`, `backend/tests/`, `web/`, `web/src/`, `web/public/`, `infra/`, `docs/`.
- [ ] Backend init: `python -m venv .venv && . .venv/Scripts/Activate.ps1 && pip install fastapi uvicorn[standard] pydantic httpx pytest pytest-asyncio ruff black mypy`
- [ ] Add `backend/app/main.py` with `/health` and stub `/verify` (returns example payload with `status: clear`).
- [ ] Add `backend/tests/test_health.py` using `pytest` + `httpx.AsyncClient`.
- [ ] Lint/format: add `ruff.toml` and `pyproject.toml` with Black config; wire `pre-commit` (optional).
- [ ] Web init: `npm create vite@latest web -- --template react` then `cd web && npm i`.
- [ ] Web test setup: add React Testing Library; sample `src/__tests__/App.test.jsx`.
- [ ] Web `/health` ping to backend env var (e.g., `VITE_API_BASE_URL`).
- [ ] Infra stub: create `infra/README.md` and placeholders for API Gateway config and PostgreSQL connection; note secrets via env vars.
- [ ] CI (GitHub Actions): backend `pytest` + `ruff/black --check`; web `npm ci && npm test -- --watch=false`.
- [ ] Update `AGENTS.md` if paths or commands differ from defaults.

## Acceptance Criteria
- Repository contains the directories above with minimal runnable backend (`uvicorn backend.app.main:app --reload`) and web (`npm run dev`).
- Tests for backend health pass locally (`pytest -q`).
- Lint and format checks pass or are configured to run.
- Docs cross-reference: `AGENTS.md`, `system_architecture.md`, and `test_plan.md` remain accurate.

## References
- AGENTS.md (Repository Guidelines)
- system_architecture.md
- prd.md / test_plan.md

