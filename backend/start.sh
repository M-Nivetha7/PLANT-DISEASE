#!/usr/bin/env bash
# Start the backend using the project's virtual environment
# Usage: ./start.sh
set -e
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT_DIR/venv"
if [ ! -x "$VENV/bin/activate" ]; then
  echo "Virtualenv not found at $VENV. Create one with: python3 -m venv $VENV && source $VENV/bin/activate && pip install -r requirements.txt"
  exit 1
fi
# Activate venv
# shellcheck disable=SC1091
source "$VENV/bin/activate"
python3 "$ROOT_DIR/app.py"
