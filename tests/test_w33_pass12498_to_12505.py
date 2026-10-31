import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12498_to_12505_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12498_to_12505_information_physics_audits.py")],
                   check=True, cwd=ROOT, capture_output=True)
    res = json.loads((ROOT / "data" / "w33_pass12498_to_12505_information_physics_audits.json").read_text())
    assert res["all_checks_pass"], res["checks"]
    assert res["12499"]["2"]["parity_proof"] and not res["12499"]["4"]["parity_proof"]
    assert not res["12500"]["self_dual"]
