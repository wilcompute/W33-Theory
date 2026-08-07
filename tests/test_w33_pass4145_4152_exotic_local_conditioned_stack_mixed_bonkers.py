from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_pass4145_4152_exotic_local_conditioned_stack_mixed_bonkers.py"

def test_pass4145_4152_exact_packet():
    out=subprocess.check_output([sys.executable,str(SCRIPT)],text=True)
    data=json.loads(out)
    assert data["status"].startswith("PASS_EXACT_")
    assert data["exotic_total_dimension"]==252
    assert data["moment_max"]==11992
    assert data["mixed_classes"]==[18,5]
    assert data["perfect_matchings"]==56260624960
    assert data["susy_zero_modes"]==82
    assert data["echo_residual"]<1e-12
