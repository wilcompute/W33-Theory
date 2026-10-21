import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12146_to_12150_crossed_models_vetted.json"


def test_crossed_models_vetted():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12146_to_12150_crossed_models_vetted.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
