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
    st = res["12489_stabilisers"]
    assert st["7"]["stabiliser"] == 24 and st["11"]["stabiliser"] == 60   # cube (S4), icosahedron (A5)
    assert res["12486_symmetric_upper_bounds"]["11"] == 84 and res["12486_symmetric_upper_bounds"]["13"] == 168
