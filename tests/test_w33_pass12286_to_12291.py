import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12286_to_12291_left_right_candidate_and_vetting.json"


def test_left_right_candidate_and_vetting():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12286_to_12291_left_right_candidate_and_vetting.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
