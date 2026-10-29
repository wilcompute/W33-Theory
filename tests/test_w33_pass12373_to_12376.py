import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12373_to_12376_targeted_witten_shift_search.json"


def test_targeted_witten_shift_search():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12373_to_12376_targeted_witten_shift_search.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
