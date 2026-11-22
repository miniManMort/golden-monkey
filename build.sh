#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

cd "$ROOT_DIR"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Error: Python interpreter '$PYTHON' was not found." >&2
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "Error: npm was not found." >&2
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    "$PYTHON" -m venv .venv
fi

echo "Installing backend dependencies..."
".venv/bin/python" -m pip install -r app-react/requirements.txt

echo "Installing frontend dependencies..."
cd app-react
npm ci

echo "Building frontend..."
npm run build

echo ""
echo "Build complete. Start the application with:"
echo "  ./run.sh"
