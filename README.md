# Savvy – Business Entity Resolution (MVP)

This repository contains a FastAPI backend and a React front‑end (Vite) for a KYB/AML MVP. See AGENTS.md for contributor guidelines and commenting standards.

## Front‑End: Run Locally
- Prereqs: Node.js 20+
- Configure API base URL (shell examples):
  - PowerShell: `$env:VITE_API_BASE_URL="http://localhost:8000"`
  - Bash: `export VITE_API_BASE_URL=http://localhost:8000`
- Install and run:
  - `cd web && npm install`
  - `npm run dev`
- Open: `http://localhost:5173`

## Back‑End: Run Locally
- Prereqs: Python 3.11+
- Optional CORS for web dev (allow Vite origin):
  - PowerShell: `$env:CORS_ORIGINS="http://localhost:5173"`
  - Bash: `export CORS_ORIGINS=http://localhost:5173`
- Start API: `uvicorn backend.app.main:app --reload`
- Health check: `GET http://localhost:8000/health`

## Tests
- Backend: `pytest -q`
- Web: `cd web && npm test -- --run`

## Quick Bootstrap (Windows)
- One command to set up venv and install web deps:
  - `powershell -ExecutionPolicy Bypass -File scripts/dev/bootstrap.ps1`

## Troubleshooting
- CORS error in browser: ensure `CORS_ORIGINS` includes your dev URL (e.g., http://localhost:5173).
- 404/Network error: confirm backend is on `http://localhost:8000` and `VITE_API_BASE_URL` matches.
- Different dev port: `npm run dev -- --port 3001` and add that origin to `CORS_ORIGINS`.

