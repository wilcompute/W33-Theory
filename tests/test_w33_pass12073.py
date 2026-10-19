import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12073_three_families_of_one_plus_a_q8_torsor.json"


def test_three_families_of_one_plus_a_q8_torsor():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12073_three_families_of_one_plus_a_q8_torsor.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
