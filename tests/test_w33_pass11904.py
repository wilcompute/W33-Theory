import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11904_magnetized_unlock_and_theta_zero_law.json"


def test_magnetized_unlock_and_theta_zero_law():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11904_magnetized_unlock_and_theta_zero_law.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
