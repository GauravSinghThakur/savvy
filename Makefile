# Makefile
# Purpose: Provide common developer tasks with readable targets.
# Note: On Windows, run via Git Bash or WSL; otherwise use the PowerShell
# bootstrap script in scripts/dev/bootstrap.ps1.

.PHONY: help setup-backend run-backend test-backend lint format format-check typecheck web-install web-dev web-test ci clean

## help: List available targets with short descriptions
help:
	@echo "Available targets:" && \
	awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

## setup-backend: Create venv and install backend deps + dev tools
setup-backend:
	python -m venv .venv && . .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r backend/requirements.txt ruff black mypy

## run-backend: Start FastAPI locally on :8000 (reload on changes)
run-backend:
	. .venv/bin/activate && uvicorn backend.app.main:app --reload --port 8000

## test-backend: Run Python tests quietly
test-backend:
	. .venv/bin/activate && pytest -q

## lint: Run Ruff linter across the repo
lint:
	. .venv/bin/activate && ruff check .

## format: Auto-format code with Black
format:
	. .venv/bin/activate && black .

## format-check: Check formatting without changing files
format-check:
	. .venv/bin/activate && black --check .

## typecheck: Run mypy static type checker
typecheck:
	. .venv/bin/activate && mypy .

## web-install: Install web dependencies in web/
web-install:
	cd web && npm install

## web-dev: Start the React dev server
web-dev:
	cd web && npm run dev

## web-test: Run web unit tests
web-test:
	cd web && npm test -- --run

## ci: Run local approximation of CI checks
ci: lint format-check typecheck test-backend web-test

## clean: Remove caches and build artifacts (keeps .venv)
clean:
	rm -rf **/__pycache__ .pytest_cache web/node_modules web/dist

