import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12363_to_12368_all_radius_closure_z6ii.json"


def test_all_radius_closure_z6ii():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12363_to_12368_all_radius_closure_z6ii.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["12365"]["liftable_all_orders_upper"] == 40
