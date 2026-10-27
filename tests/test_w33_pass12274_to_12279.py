import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12274_to_12279_torsion_bicharacter_and_brothers.json"


def test_torsion_bicharacter_and_brothers():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12274_to_12279_torsion_bicharacter_and_brothers.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
