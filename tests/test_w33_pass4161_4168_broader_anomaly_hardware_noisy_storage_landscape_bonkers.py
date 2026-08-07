from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_pass4161_4168_broader_anomaly_hardware_noisy_storage_landscape_bonkers.py"

def test_pass4161_4168_exact_packet():
    out=subprocess.check_output([sys.executable,str(SCRIPT)],text=True)
    data=json.loads(out)
    assert data["status"]=="PASS_EXACT_BROADER_ANOMALY_HARDWARE_GRAPH_QUANTIZED_T7_STORAGE_BOUND_LANDSCAPE_PUSH_SEARCH_RESISTANCE_DIAMONDS"
    assert data["semantic_sha256"]=="db91cd6c70138d44917ba4274a7d087927caec691be5d49efd83528e7f8d4bd5"
    assert data["anomaly_total"]==213
    assert data["hardware_max_degree"]==7
    assert data["quantized_noise_margin"]=="Delta/2"
    assert data["storage_five_use_delay_dB"]==0.15
    assert data["selector24_new_macro_mixed"]==20
    assert abs(data["grover_k4"]-0.98003433025)<1e-15
    assert data["Kirchhoff_index"]==133.5
    assert data["diameter4_diamonds"]==1080
