import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11912_entangling_modulus_is_the_wilson_line.json"


def test_entangling_modulus_is_the_wilson_line():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11912_entangling_modulus_is_the_wilson_line.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
