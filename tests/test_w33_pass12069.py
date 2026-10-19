import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12069_flavour_cp_is_a_bosonic_time_reversal.json"


def test_flavour_cp_is_a_bosonic_time_reversal():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12069_flavour_cp_is_a_bosonic_time_reversal.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
