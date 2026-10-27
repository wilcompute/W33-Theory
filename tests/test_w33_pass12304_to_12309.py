import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12304_to_12309_tachyons_confirmed_and_radius_window.json"


def test_tachyons_confirmed_and_radius_window():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12304_to_12309_tachyons_confirmed_and_radius_window.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
