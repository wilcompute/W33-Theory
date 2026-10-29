import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12369_to_12372_information_duality.json"


def test_information_duality():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12369_to_12372_information_duality.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["12369"]["nonmetric"] == 0
