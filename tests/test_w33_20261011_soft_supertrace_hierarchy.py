import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_20261011_soft_supertrace_hierarchy.py"
CERT=ROOT/"data"/"w33_20261011_soft_supertrace_hierarchy.json"

def test_soft_supertrace_hierarchy_certificate():
    subprocess.run([sys.executable,str(SCRIPT),"--check"],cwd=ROOT,check=True,
                   capture_output=True,timeout=300)
    d=json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert all(d["checks"].values())
    assert d["asymptotic"]["A_zero_mode_sum"] > 7.999
    assert d["angular_witnesses"]["intermediate_witness"]["residual_Delta54_projective_order"] == 1
