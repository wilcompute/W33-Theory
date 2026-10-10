import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11887_11889_e6_family_at_w33_point.json"


def test_e6_family_at_w33_point():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11887_11889_e6_family_at_w33_point.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["11889_w33_point"]["distinct_points"] == 40
