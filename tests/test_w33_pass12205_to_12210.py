import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12205_to_12210_twisted_sectors_carry_no_ten.json"


def test_twisted_sectors_carry_no_ten():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12205_to_12210_twisted_sectors_carry_no_ten.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
