from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_pass4205_4212_carrier_native_hodge_delay_interval_bonkers.py"

def test_pass4205_4212_quick_packet():
    out=subprocess.check_output([sys.executable,str(SCRIPT)],text=True)
    data=json.loads(out)
    assert data["status"]=="PASS_EXACT_CARRIER_SURGERY_NATIVE_DUALRAIL_COMPRESSED_HODGE_COMPONENT_DELAY_INTERVAL_STRATA_ABSORBER_UNCERTAINTY_HARMONIC_STORAGE"
    assert data["packet_sha256"]=="3ac264ad9e91406b0016b01fa987f6e2d5770d5ee3874fb729707b38c475cf37"
    assert data["carrier_generations"]==5
    assert data["native_transmons"]==87
    assert data["delay_units"]==919
    assert data["full"] is False
