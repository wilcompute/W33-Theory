import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12621_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12621_outside_links.py")], check=True, cwd=ROOT)
    res = json.loads((ROOT / "data" / "w33_pass12621_outside_links.json").read_text())
    assert res["all_checks_pass"], res["checks"]
