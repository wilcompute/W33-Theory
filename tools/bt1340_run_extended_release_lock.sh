#!/usr/bin/env bash
set -euo pipefail

bash tools/bt1307_run_v1_release_lock.sh
python tools/bt1334_gk_threshold_capacity_gate.py
python tools/bt1335_foundry_layout_feasibility_gate.py
python tools/bt1336_erasure_distance_benchmark.py
python tools/bt1338_extract_q4_chain_checks.py
python tools/bt1339_optical_loss_crosstalk_budget.py
python -m pytest -q tests/test_bt1333_bt1335_paper_threshold_layout.py tests/test_bt1336_bt1337_decoder_release_lock.py tests/test_bt1338_bt1340_stabilizer_optical_release.py

echo "BT1340 extended release lock passed"
