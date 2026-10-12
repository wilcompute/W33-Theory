import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11936_radial_weld.json"


def test_radial_weld():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11936_radial_weld.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
