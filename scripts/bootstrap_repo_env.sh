#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/.venv}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "error: ${PYTHON_BIN} is not available in PATH" >&2
  exit 1
fi

cd "${ROOT_DIR}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[bootstrap] creating virtualenv at ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
else
  echo "[bootstrap] reusing existing virtualenv at ${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "[bootstrap] upgrading pip tooling"
python -m pip install --upgrade pip setuptools wheel

echo "[bootstrap] installing requirements-dev.txt"
python -m pip install -r requirements-dev.txt

cat <<'EOF'

[bootstrap] environment ready

Next steps:
EOF
printf '  1. source %s/bin/activate\n' "${VENV_DIR}"
cat <<'EOF'
  2. make doctor
  3. python3 tools/repo_cleanup_audit.py

If you only want the quick health check without installing anything:
  python3 tools/repo_doctor.py
EOF
