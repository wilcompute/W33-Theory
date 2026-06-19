#!/usr/bin/env bash
set -euo pipefail

python tools/bt1281_verify_recovery_certificate.py
python tools/bt1274_batch_score_candidates.py
python tools/bt1291_verify_release_packet.py
python tools/bt1296_verify_release_readiness_badge.py
python tools/bt1300_verify_paper_build_handshake.py
python -m pytest -q \
  tests/test_bt1269_bt1272_external_candidates.py \
  tests/test_bt1274_bt1276_recovery_packet.py \
  tests/test_bt1280_bt1282_recovery_docs.py \
  tests/test_bt1288_readme_recovery_pointer.py \
  tests/test_bt1290_bt1292_release_packet.py \
  tests/test_bt1295_bt1296_readiness_badge.py

echo "BT1299 v1 release gates passed"
