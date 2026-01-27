#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

if [ ! -f "$REPO_ROOT/artifacts_archive/e8_root_to_w33_edge.json" ]; then
  echo "Mapping artifact missing; generating via Sage..."
  "$REPO_ROOT/run_sage.sh" "$REPO_ROOT/tools/sage_e8_root_edge_bijection.py"
fi

python3 "$REPO_ROOT/tools/verify_e8_root_edge_bijection.py"
