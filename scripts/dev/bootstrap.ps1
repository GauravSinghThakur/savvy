<#
  Bootstrap Script (PowerShell)
  Purpose:
    - Sets up a local Python virtual environment and installs backend deps.
    - Installs web dependencies for the React placeholder app.
    - Prints quick-start instructions and environment variable guidance.

  Usage:
    - Right-click > Run with PowerShell, or run: powershell -ExecutionPolicy Bypass -File scripts/dev/bootstrap.ps1

  Notes:
    - This script is idempotent; re-running updates dependencies as needed.
    - Does not create or modify production secrets. See .env.example.
#>

Param()

$ErrorActionPreference = 'Stop'

Write-Host "[1/4] Creating Python virtual environment (.venv) if missing..."
if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

Write-Host "[2/4] Installing backend dependencies..."
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt ruff black mypy

Write-Host "[3/4] Installing web dependencies (if web/ exists)..."
if (Test-Path "web\package.json") {
  Push-Location web
  if (Test-Path "package-lock.json") {
    npm ci
  } else {
    npm install
  }
  Pop-Location
} else {
  Write-Host "web/ not initialized; see web/README.md for Vite setup." -ForegroundColor Yellow
}

Write-Host "[4/4] Done. Next steps:" -ForegroundColor Green
Write-Host "- Start API:   uvicorn backend.app.main:app --reload" -ForegroundColor Cyan
Write-Host "- Run tests:   pytest -q" -ForegroundColor Cyan
Write-Host "- Start web:   cd web && npm run dev (set VITE_API_BASE_URL=http://localhost:8000)" -ForegroundColor Cyan

Write-Host "\nEnvironment variables (see .env.example):" -ForegroundColor Green
Write-Host "- API_KEY, DATABASE_URL (backend)" -ForegroundColor Gray
Write-Host "- VITE_API_BASE_URL (web)" -ForegroundColor Gray

