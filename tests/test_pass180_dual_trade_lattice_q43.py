import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass180_dual_trade_lattice_q43.py"
DATA = ROOT / "data" / "w33_pass180_dual_trade_lattice_q43.json"
NOTE = ROOT / "PASS180_Q43_DUAL_TRADE_REGULARITY_BOUNDARY.md"


def test_pass180_corrected_witness_runs():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=180,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_pass180_exact_new_content_and_boundaries():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    assert payload["schema"] == "w33.pass180.dual_trade_lattice_q43.v2"
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    identity = payload["identification"]
    assert identity["w33_span_sizes"] == [4]
    assert identity["q43_span_sizes"] == [2]
    assert "nonisomorphic" in identity["statement"]
    assert "does not by itself derive" in identity["boundary"]

    mod8 = payload["mod8_row"]
    assert mod8["selected_smith_z8_generator_q_value"] == "11/8"
    assert mod8["fixed_generator_values_from_pass174"] == ["11/8", "3/8"]
    assert "not canonical" in mod8["reading"]
    assert "eleven_eighths_law_holds_on_route_side" not in mod8

    note = NOTE.read_text(encoding="utf-8")
    assert "nonisomorphic dual pair" in note
    assert "not invariant" in note
