#!/usr/bin/env bash
set -euo pipefail
# Usage: ./run_in_container.sh [shots] [bootstrap]
SHOTS=${1:-5000}
BOOT=${2:-500}
export TDA_FOLLOWUP_SHOTS=$SHOTS
export TDA_FOLLOWUP_BOOTSTRAP=$BOOT
python scripts/quantum_photonics/run_gbs_tda_followup.py || true
python scripts/quantum_photonics/run_gbs_tda_followup_stub.py || true
python scripts/finite_geometry/check_lemma1.py || true
python scripts/finite_geometry/check_lemma1_expanded.py || true
python scripts/finite_geometry/check_lemma2.py || true
