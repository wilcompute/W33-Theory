import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12055_microscopic_tick_model.json"


def test_microscopic_tick_model():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12055_microscopic_tick_model.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
