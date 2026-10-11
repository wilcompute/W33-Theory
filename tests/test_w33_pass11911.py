import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11911_susy_z3_scan.json"


def test_susy_z3_scan():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11911_susy_z3_scan.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert all(f["SM"] == 0 for f in d["final"].values())
