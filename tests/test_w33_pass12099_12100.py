import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12099_12100_selection_and_proton_bound.json"


def test_selection_and_proton_bound():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12099_12100_selection_and_proton_bound.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
