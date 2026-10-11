import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11902_a8_census_kahler_independent_degeneracy.json"


def test_a8_census_kahler_independent_degeneracy():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11902_a8_census_kahler_independent_degeneracy.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["kinds"] == {"untwisted": 73, "twisted_one_torus": 31}
