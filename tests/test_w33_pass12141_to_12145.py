import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12141_to_12145_cp_witten_parity_cross_routes.json"


def test_cp_witten_parity_cross_routes():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12141_to_12145_cp_witten_parity_cross_routes.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
