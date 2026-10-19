import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12053_gate_sets_and_real_forms.json"


def test_gate_sets_and_real_forms():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12053_gate_sets_and_real_forms.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
