import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12418_to_12425_one_identity_two_codes.json"


def test_one_identity_two_codes():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12418_to_12425_one_identity_two_codes.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
