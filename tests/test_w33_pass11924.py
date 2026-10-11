import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11924_residual_s3_and_misaligned_flavon.json"


def test_residual_s3_and_misaligned_flavon():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11924_residual_s3_and_misaligned_flavon.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
