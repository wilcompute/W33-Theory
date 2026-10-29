import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12402_to_12409_closure_all_q_joint_symmetry_constants.json"


def test_closure_all_q_joint_symmetry_constants():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12402_to_12409_closure_all_q_joint_symmetry_constants.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["12405_counts"]["3"]["metric_count"] == 16848
