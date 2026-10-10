import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11896_flagship_tension.json"


def test_flagship_tension():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11896_flagship_tension.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["family_plane_states"] == 16
