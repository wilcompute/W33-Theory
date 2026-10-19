import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12065_landau_phases_have_no_rest_frame.json"


def test_landau_phases_have_no_rest_frame():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12065_landau_phases_have_no_rest_frame.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
