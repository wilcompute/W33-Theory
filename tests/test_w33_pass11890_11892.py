import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11890_11892_vacuum_phase_diagram.json"


def test_vacuum_phase_diagram():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11890_11892_vacuum_phase_diagram.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["11890_hosotani"]["regimes"]["periodic_nF2"]["root_components"] == [24, 24]
