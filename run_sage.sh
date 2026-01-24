#!/usr/bin/env bash
set -euo pipefail

# Run a Python script inside Sage (recommended: Sage installed in WSL).
#
# Usage (from repo root):
#   ./run_sage.sh w33_sage_incidence_and_h1.py [args...]
#
# Or from Windows PowerShell:
#   wsl.exe -e bash -lc "cd \"$(wslpath 'C:\\path\\to\\repo')\"; ./run_sage.sh ..."

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)

PYSYM_ROOT="${REPO_ROOT}/lib/pysymmetry_deck_z2_integration_patch"

# Prefer micromamba sage env, then system sage
if [ -x "$HOME/bin/micromamba" ]; then
    # Use micromamba run to execute in sage environment
    SAGE_CMD="$HOME/bin/micromamba run -n sage sage"
elif command -v sage >/dev/null 2>&1; then
    SAGE_CMD="sage"
elif [ -x "${REPO_ROOT}/external/sage/bin/sage" ]; then
    # Fallback: bundled Sage tree (bash-based). Works only if it is a functional Sage install.
    SAGE_CMD="${REPO_ROOT}/external/sage/bin/sage"
else
    echo "ERROR: Could not find Sage. Install Sage inside WSL (recommended) or ensure external/sage/bin/sage is usable." >&2
    exit 1
fi

export PYTHONPATH="${PYSYM_ROOT}:${REPO_ROOT}:${PYTHONPATH:-}"
cd "${REPO_ROOT}"

if [ $# -eq 0 ]; then
    exec ${SAGE_CMD} -python
else
    exec ${SAGE_CMD} -python "$@"
fi
