import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12474_to_12481_xwide_hypercharge_even_sets.json"


def test_xwide_hypercharge_even_sets():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12474_to_12481_xwide_hypercharge_even_sets.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
