import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12490_to_12497_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12490_to_12497_moore_family_hs_exclusion.py")],
                   check=True, cwd=ROOT, capture_output=True)
    res = json.loads((ROOT / "data" / "w33_pass12490_to_12497_moore_family_hs_exclusion.json").read_text())
    assert res["all_checks_pass"], res["checks"]
    assert res["12490_geometric"]["5"]["size"] == 20
    assert res["12493_moore_search"]["found"] == [5]
