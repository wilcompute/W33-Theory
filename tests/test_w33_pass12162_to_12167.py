import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12162_to_12167_survivors_thresholds_proton_closure.json"


def test_survivors_thresholds_proton_closure():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12162_to_12167_survivors_thresholds_proton_closure.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
