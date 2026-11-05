import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12624_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12624_why_three_heavy_axion.py")], check=True, cwd=ROOT)
    res = json.loads((ROOT / "data" / "w33_pass12624_why_three_heavy_axion.json").read_text())
    assert res["all_checks_pass"], res["checks"]
