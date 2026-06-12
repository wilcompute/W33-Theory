#!/usr/bin/env python3
"""Focused direct tests for BT840-BT842 GC/tomotope carrier packets."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    with (ROOT / relpath).open() as f:
        return json.load(f)


def test_bt840_clifford_rook_sentinel_sheet() -> None:
    run_script("analysis/bt840_clifford_rook_sentinel_sheet.py")
    data = load_json("data/bt840_clifford_rook_sentinel_sheet.json")
    assert all(data["checks"].values())
    assert data["sentinel_sheet"]["edge_count"] == 180
    assert data["sentinel_sheet"]["duads_per_fiber"] == {"15": 12}
    assert data["gc_completion"]["w33_petersen_home_flags"] == 3240
    assert data["gc_completion"]["completed_flags"] == 3420
    assert data["gc_completion"]["core_count_reading"] == {
        "w33_cores": 216,
        "sentinel_fibers": 12,
        "completed_cores": 228,
        "edge_or_duad_count_per_core": 15,
    }


def test_bt841_eleven_cell_a5_boundary_carrier() -> None:
    run_script("analysis/bt841_eleven_cell_a5_boundary_carrier.py")
    data = load_json("data/bt841_eleven_cell_a5_boundary_carrier.json")
    assert all(data["checks"].values())
    assert data["a5_selector"]["element_count"] == 60
    assert data["a5_selector"]["order_profile"] == {"1": 1, "2": 15, "3": 20, "5": 24}
    assert data["eleven_label_carriers"]["carrier_count"] == 36
    assert data["eleven_label_carriers"]["flag_count_per_carrier"] == 660
    assert data["eleven_label_carriers"]["factorizations"] == {
        "11_times_A5": 660,
        "k_times_Neff": 660,
        "Neff": 55,
    }


def test_bt842_tomotope_24cell_half_flag_edge_lift() -> None:
    run_script("analysis/bt842_tomotope_24cell_half_flag_edge_lift.py")
    data = load_json("data/bt842_tomotope_24cell_half_flag_edge_lift.json")
    assert all(data["checks"].values())
    assert data["edge_lift"]["twenty_four_cell_edges"] == 96
    assert data["edge_lift"]["reye_incidences"] == 48
    assert data["edge_lift"]["preimage_profile"] == {"2": 48}
    assert data["hexagon_k6_completion"]["duad_slots_total"] == 240
    assert data["hexagon_k6_completion"]["duad_dot_profile_with_multiplicity"] == {
        "-2": 48,
        "-1": 96,
        "1": 96,
    }
    assert data["hexagon_k6_completion"]["distinct_duad_multiplicity_profile"] == {"1": 192, "4": 12}


if __name__ == "__main__":
    test_bt840_clifford_rook_sentinel_sheet()
    test_bt841_eleven_cell_a5_boundary_carrier()
    test_bt842_tomotope_24cell_half_flag_edge_lift()
    print("BT840-BT842 GC carrier tests passed")
