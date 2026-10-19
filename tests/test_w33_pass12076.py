import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12076_time_rotates_so10.json"


def test_time_rotates_so10():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12076_time_rotates_so10.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
