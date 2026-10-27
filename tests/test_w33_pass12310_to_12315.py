import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12310_to_12315_vacuum_potential_unification.json"


def test_vacuum_potential_unification():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12310_to_12315_vacuum_potential_unification.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
