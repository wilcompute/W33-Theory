import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11909_up_sector_coleman_weinberg.json"


def test_up_sector_coleman_weinberg():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11909_up_sector_coleman_weinberg.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=1800)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
