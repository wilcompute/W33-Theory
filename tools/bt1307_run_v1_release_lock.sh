#!/usr/bin/env bash
set -euo pipefail

bash tools/bt1299_run_v1_release_gates.sh
python tools/bt1306_verify_release_lock.py
python -m pytest -q tests/test_bt1302_bt1304_release_closure.py

echo "BT1307 v1 release lock passed"
