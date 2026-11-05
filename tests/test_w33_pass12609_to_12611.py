import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12609_to_12611_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12609_to_12611_pq_tests.py")], check=True, cwd=ROOT)
    res = json.loads((ROOT / "data" / "w33_pass12609_to_12611_pq_tests.json").read_text())
    assert res["all_checks_pass"], res["checks"]
