import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12357_to_12362_sub_orbifolds_thresholds_vacuum_proton.json"


def test_sub_orbifolds_thresholds_vacuum_proton():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12357_to_12362_sub_orbifolds_thresholds_vacuum_proton.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["12361_N_eff_exact"] == "-752/9"
    assert d["12359_validation"]["census_summary"]["e5e6_tachyonic"] == 52
