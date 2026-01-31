#!/usr/bin/env bash
set -euo pipefail

# Minimal developer environment setup script
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

echo "Dev env ready. Activate with: source .venv/bin/activate"
