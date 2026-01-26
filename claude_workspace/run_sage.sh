#!/usr/bin/env bash
set -euo pipefail

# Wrapper for CI: route claude_workspace/run_sage.sh to repo scripts.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)

if [ $# -eq 0 ]; then
    exec bash "${REPO_ROOT}/scripts/run_all_sage.sh"
fi

args=()
for a in "$@"; do
    if [[ "$a" == claude_workspace/scripts/* ]]; then
        a="scripts/${a#claude_workspace/scripts/}"
    fi
    args+=("$a")
done

exec bash "${REPO_ROOT}/run_sage.sh" "${args[@]}"
