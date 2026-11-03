import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12546_to_12549_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12546_to_12549_dark_sector.py")], check=True, cwd=ROOT, capture_output=True)
    res = json.loads((ROOT / "data" / "w33_pass12546_to_12549_dark_sector.json").read_text())
    assert res["all_checks_pass"], res["checks"]
