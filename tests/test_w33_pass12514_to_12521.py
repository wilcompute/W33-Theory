import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12514_to_12521_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12514_to_12521_explicit_braid_iso.py")], check=True, cwd=ROOT,
                   capture_output=True)
    res = json.loads((ROOT / "data" / "w33_pass12514_to_12521_explicit_braid_iso.json").read_text())
    assert res["all_checks_pass"], res["checks"]
