import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11945_lepton_mu_tau_classes.json"


def test_lepton_mu_tau_classes():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11945_lepton_mu_tau_classes.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
