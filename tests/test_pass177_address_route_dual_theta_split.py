import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass177_address_route_dual_theta_split.py"
DATA = ROOT / "data" / "w33_pass177_address_route_dual_theta_split.json"
NOTE = ROOT / "PASS177_ADDRESS_ROUTE_DUAL_THETA_SPLIT.md"


def test_pass177_witness_runs_cleanly():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_pass177_exact_shell_split_and_objects():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    assert payload["codes"]["address_dual_A4_A6_A8"] == [40, 240, 5085]
    assert payload["codes"]["route_dual_A4_A6_A8"] == [40, 240, 3645]

    theta = payload["theta"]
    assert theta["address_scaled_0_to_6"] == [
        1,
        0,
        720,
        15360,
        1350960,
        50016256,
        1534663360,
    ]
    assert theta["route_scaled_0_to_6"] == [
        1,
        0,
        720,
        15360,
        982320,
        57094144,
        1452088000,
    ]
    assert theta["q4_split"] == {
        "common_coordinate_sector": 3120,
        "common_weight4_plus_coordinate_sector": 46080,
        "address_weight8_sector": 1301760,
        "route_weight8_sector": 933120,
        "address_total": 1350960,
        "route_total": 982320,
        "difference": 368640,
    }

    note = NOTE.read_text(encoding="utf-8")
    assert "line/point-star openings" in note
    assert "\\boxed{368{,}640}" in note
    assert "does not assert" in note
