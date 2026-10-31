import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12506_to_12513_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12506_to_12513_quantum_bridges.py")], check=True, cwd=ROOT,
                   capture_output=True)
    res = json.loads((ROOT / "data" / "w33_pass12506_to_12513_quantum_bridges.json").read_text())
    assert res["all_checks_pass"], res["checks"]
    assert res["braid"]["by_k"]["4"]["orbits_on_216"] == [108, 108]
