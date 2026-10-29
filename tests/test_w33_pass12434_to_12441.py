import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12434_to_12441_distance_stabilizer_geometry.json"


def test_distance_stabilizer_geometry():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12434_to_12441_distance_stabilizer_geometry.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
