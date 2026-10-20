import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12106_to_12110_orbifold_realisations.json"


def test_orbifold_realisations():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12106_to_12110_orbifold_realisations.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
