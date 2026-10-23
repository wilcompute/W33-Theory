import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12211_to_12216_no_order3_interpolation_no_twisted_ten.json"


def test_no_order3_interpolation_no_twisted_ten():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12211_to_12216_no_order3_interpolation_no_twisted_ten.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
