import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11922_neutrino_qutrit_complementarity.json"


def test_neutrino_qutrit_complementarity():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11922_neutrino_qutrit_complementarity.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
