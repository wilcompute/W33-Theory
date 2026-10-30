import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12466_to_12473_dual_lines_even_sets_ky_floor.json"


def test_dual_lines_even_sets_ky_floor():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12466_to_12473_dual_lines_even_sets_ky_floor.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
