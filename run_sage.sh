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
REPO_ROOT="${SCRIPT_DIR}"

PYSYM_PATHS=(
    "${REPO_ROOT}/external/pysymmetry"
    "${REPO_ROOT}/lib/pysymmetry_deck_z2_integration_patch"
)

# Prefer micromamba sage env, then system sage, then bundled Sage, then Docker
if [ -x "$HOME/bin/micromamba" ]; then
    # Use micromamba run to execute in sage environment
    SAGE_CMD="$HOME/bin/micromamba run -n sage sage"
elif command -v sage >/dev/null 2>&1; then
    SAGE_CMD="sage"
elif [ -x "${REPO_ROOT}/external/sage/bin/sage" ]; then
    # Fallback: bundled Sage tree (bash-based). Works only if it is a functional Sage install.
    SAGE_CMD="${REPO_ROOT}/external/sage/bin/sage"
elif command -v docker >/dev/null 2>&1; then
    SAGE_MODE="docker"
    SAGE_IMAGE="${SAGE_DOCKER_IMAGE:-sagemath/sagemath:10.7}"
else
    echo "ERROR: Could not find Sage. Install Sage inside WSL (recommended) or ensure external/sage/bin/sage is usable." >&2
    exit 1
fi

EXTRA_PYTHONPATH=""
for path in "${PYSYM_PATHS[@]}"; do
    if [ -d "${path}" ]; then
        if [ -z "${EXTRA_PYTHONPATH}" ]; then
            EXTRA_PYTHONPATH="${path}"
        else
            EXTRA_PYTHONPATH="${EXTRA_PYTHONPATH}:${path}"
        fi
    fi
done

if [ -n "${EXTRA_PYTHONPATH}" ]; then
    export PYTHONPATH="${EXTRA_PYTHONPATH}:${REPO_ROOT}:${PYTHONPATH:-}"
else
    export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"
fi
cd "${REPO_ROOT}"

if [ "${SAGE_MODE:-}" = "docker" ]; then
    DOCKER_USER_ARGS=()
    if command -v id >/dev/null 2>&1; then
        DOCKER_USER_ARGS=(--user "$(id -u):$(id -g)")
    fi

    DOCKER_RUN=(
        docker run --rm
        -v "${REPO_ROOT}:/work"
        -w /work
        "${DOCKER_USER_ARGS[@]}"
        -e "PYTHONPATH=${PYTHONPATH}"
        "${SAGE_IMAGE}"
    )

    if [ $# -eq 0 ]; then
        exec "${DOCKER_RUN[@]}" sage -python
    else
        case "$1" in
            *.sage)
                exec "${DOCKER_RUN[@]}" sage "$@"
                ;;
            *)
                exec "${DOCKER_RUN[@]}" sage -python "$@"
                ;;
        esac
    fi
else
    if [ $# -eq 0 ]; then
        exec ${SAGE_CMD} -python
    else
        case "$1" in
            *.sage)
                exec ${SAGE_CMD} "$@"
                ;;
            *)
                exec ${SAGE_CMD} -python "$@"
                ;;
        esac
    fi
fi
