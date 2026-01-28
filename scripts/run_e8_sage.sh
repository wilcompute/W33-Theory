#!/usr/bin/env bash
set -euo pipefail

IMAGE=${1:-sagemath/sagemath:10.7}
ROOT=$(pwd)
mkdir -p "$ROOT/logs"

echo "Running E8 Sage test in Docker image: $IMAGE"

docker run --rm -v "$(pwd):/work" -w /work "$IMAGE" bash -lc "sage -preparse THEORY_PART_CVII_SAGE_E8_TEST.sage && python3 THEORY_PART_CVII_SAGE_E8_TEST.sage.py 2>&1 | tee /work/logs/E8_test.log"

echo "Logs written to $ROOT/logs/E8_test.log"
