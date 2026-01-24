#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)

MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX:-$HOME/micromamba}"
export MAMBA_ROOT_PREFIX
export PATH="$HOME/bin:$PATH"

ensure_micromamba() {
  if ! command -v micromamba >/dev/null 2>&1; then
    echo "Installing micromamba..."
    mkdir -p "$HOME"
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest -o /tmp/micromamba.tar.bz2
    tar -xvjf /tmp/micromamba.tar.bz2 -C "$HOME" bin/micromamba
  fi
}

ensure_sage_env() {
  if micromamba env list | awk '{print $1}' | grep -qx sage; then
    echo "Sage env already exists."
  else
    echo "Creating sage env via conda-forge..."
    micromamba create -n sage -c conda-forge sage -y
  fi
}

ensure_pysymmetry() {
  local target="$REPO_ROOT/external/pysymmetry"
  if [ -d "$target/.git" ]; then
    echo "PySymmetry already present at $target"
  else
    echo "Cloning PySymmetry into $target"
    mkdir -p "$REPO_ROOT/external"
    git clone https://github.com/ldsufrpe/pysymmetry "$target"
  fi
}

smoke_test() {
  echo "Running Sage + PySymmetry smoke test..."
  local pysym_path="$REPO_ROOT/external/pysymmetry"
  PYTHONPATH="$pysym_path:$REPO_ROOT:${PYTHONPATH:-}" \
    micromamba run -n sage sage -python - <<'PY'
import sys
from pysymmetry import FiniteGroup, representation
print("PySymmetry import OK", FiniteGroup, representation)
PY
}

ensure_micromamba
ensure_sage_env
ensure_pysymmetry
smoke_test

echo ""
echo "Setup complete. To run Sage scripts:"
echo "  ./run_sage.sh w33_sage_incidence_and_h1.py"
