import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11913_flux_vacua_near_hierarchy_point.json"


def test_pass11913():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11913_flux_vacua_near_hierarchy_point.py")], check=True, cwd=ROOT, capture_output=True,
                   timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
