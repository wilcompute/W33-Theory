import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass12482_to_12489_producer():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12482_to_12489_even_line_sets_pair_structure.py")],
                   check=True, cwd=ROOT, capture_output=True)
    res = json.loads((ROOT / "data" / "w33_pass12482_to_12489_even_line_sets_pair_structure.json").read_text())
    assert res["all_checks_pass"], res["checks"]
    assert res["12483"]["count"] == 216
    assert res["12484"]["pair_graph_is_petersen"]
