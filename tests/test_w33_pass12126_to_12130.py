import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12126_to_12130_charges_masses_vacuum.json"


def test_charges_masses_vacuum():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12126_to_12130_charges_masses_vacuum.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
