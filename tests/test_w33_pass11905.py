import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11905_symmetric_wilson_lines_degenerate.json"


def test_symmetric_wilson_lines_degenerate():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11905_symmetric_wilson_lines_degenerate.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
