import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11931_theta_zero_needs_eisenstein_flux.json"


def test_theta_zero_needs_eisenstein_flux():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11931_theta_zero_needs_eisenstein_flux.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
