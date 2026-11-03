import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12560_to_12562_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12560_to_12562_casimir_tower.py")], check=True, cwd=ROOT)
    res = json.loads((ROOT / "data" / "w33_pass12560_to_12562_casimir_tower.json").read_text())
    assert res["all_checks_pass"], res["checks"]
