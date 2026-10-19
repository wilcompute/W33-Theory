import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12089_fermion_parity_makes_the_16_fermionic.json"


def test_fermion_parity_makes_the_16_fermionic():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12089_fermion_parity_makes_the_16_fermionic.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
