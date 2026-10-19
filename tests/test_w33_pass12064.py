import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12064_a_second_clock_is_a_yukawa_monomial.json"


def test_a_second_clock_is_a_yukawa_monomial():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12064_a_second_clock_is_a_yukawa_monomial.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
