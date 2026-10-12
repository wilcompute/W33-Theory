import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11930_fixed_point_avoiding_higgs.json"


def test_fixed_point_avoiding_higgs():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11930_fixed_point_avoiding_higgs.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
