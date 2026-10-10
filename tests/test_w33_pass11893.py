import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11893_trinification_chiral_spectrum.json"


def test_trinification_chiral_spectrum():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11893_trinification_chiral_spectrum.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["massless"] == {"X1": 28, "X2": 28, "X3": 28}
