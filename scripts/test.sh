#!/usr/bin/env bash
set -euo pipefail

# Backend tests
python -m pip install -r backend/requirements.txt
pytest -q backend/tests

# Frontend tests
if command -v npm >/dev/null 2>&1; then
  (cd frontend && npm i && npm test)
else
  echo "npm not found; skipping frontend tests"
fi
