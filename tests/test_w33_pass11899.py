import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11899_kahler_special_points_cp.json"


def test_kahler_special_points_cp():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11899_kahler_special_points_cp.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["special_points"] == 13805
    assert [o["stabiliser"] for o in d["orbits"]] == [648, 576, 162, 120, 108, 48, 36, 16, 12, 9, 5]
