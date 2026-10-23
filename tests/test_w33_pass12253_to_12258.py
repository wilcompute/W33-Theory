import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12253_to_12258_note_and_cross_engine.json"


def test_note_and_cross_engine():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12253_to_12258_note_and_cross_engine.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
