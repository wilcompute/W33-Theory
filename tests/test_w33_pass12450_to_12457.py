import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12450_to_12457_majorana_rescue_deficit_cutrank_index.json"


def test_majorana_rescue_deficit_cutrank_index():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12450_to_12457_majorana_rescue_deficit_cutrank_index.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
