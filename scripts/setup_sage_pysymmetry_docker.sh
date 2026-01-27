#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
IMAGE="${SAGE_DOCKER_IMAGE:-sagemath/sagemath:10.7}"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker not found on PATH" >&2
  exit 1
fi

echo "Pulling Sage image: ${IMAGE}"
docker pull "${IMAGE}"

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
  echo "Running Sage + PySymmetry smoke test in Docker..."
  local pysym_path="/work/external/pysymmetry"
  local py_path="$pysym_path:/work"
  USER_ARGS=()
  if command -v id >/dev/null 2>&1; then
    USER_ARGS=(--user "$(id -u):$(id -g)")
  fi
  docker run --rm \
    -v "${REPO_ROOT}:/work" \
    -w /work \
    "${USER_ARGS[@]}" \
    -e "PYTHONPATH=${py_path}" \
    "${IMAGE}" \
    sage -python - <<'PY'
from pysymmetry import FiniteGroup, representation
print("PySymmetry import OK", FiniteGroup, representation)
PY
}

ensure_pysymmetry
smoke_test

echo ""
echo "Docker Sage + PySymmetry ready. Example run:"
echo "  ./run_sage.sh w33_sage_incidence_and_h1.py"
