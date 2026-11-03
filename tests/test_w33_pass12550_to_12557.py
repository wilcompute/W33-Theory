import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12550_to_12557_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12550_to_12557_dark_drag.py")], check=True, cwd=ROOT)
    res = json.loads((ROOT / "data" / "w33_pass12550_to_12557_dark_drag.json").read_text())
    assert res["all_checks_pass"], res["checks"]
