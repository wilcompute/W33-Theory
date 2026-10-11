import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11910_cross_sector_invariant_and_ckm.json"


def test_cross_sector_invariant_and_ckm():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11910_cross_sector_invariant_and_ckm.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
