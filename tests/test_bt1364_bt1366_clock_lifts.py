#!/usr/bin/env python3
"""Regression tests for BT1364-BT1366 clock lifts."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def test_bt1364_q6_flag_bus_lift() -> None:
    run_script("analysis/bt1364_q6_tomotope_flag_bus_lift.py")
    data = load_json("data/bt1364_q6_tomotope_flag_bus_lift.json")
    assert data["verified"] is True
    assert data["q6"]["edges"] == 192
    assert data["q6"]["direction_pair_profile"] == {"0": 64, "1": 64, "2": 64}
    assert data["tomotope_flag_bus"]["flags"] == 192
    assert (
        data["tomotope_flag_bus"]["identity"]
        == "192 = 48 * 4 = 3 * 16 * 4 = 12 * 4 * 4"
    )
    assert data["checks"]["assignment_is_bijective_to_flags"] is True
    assert data["checks"]["binary_to_ternary_bus_identity"] is True


def test_bt1365_qutrit_phase_alignment() -> None:
    run_script("analysis/bt1365_qutrit_phase_sheet_alignment.py")
    data = load_json("data/bt1365_qutrit_phase_sheet_alignment.json")
    assert data["verified"] is True
    assert data["local_bt1363_phase_bus"]["phase_count"] == 3
    assert data["local_bt1363_phase_bus"]["blocks_per_phase"] == [16, 16, 16]
    assert data["selector_bt361_phase_bundle"]["selector_sheets"] == 120
    assert (
        data["alignment"]["identity"]
        == "3 local tomotope sheets * 40 W33 lines = 120 selector phase sheets"
    )


def test_bt1366_global_2160_clock_grading() -> None:
    run_script("analysis/bt1366_global_2160_d12_clock_grading.py")
    data = load_json("data/bt1366_global_2160_d12_clock_grading.json")
    assert data["verified"] is True
    assert data["grading"]["identity"] == "2160 = 45 * 48 = 45 * 12 * 4 = 45 * 3 * 16"
    assert data["grading"]["chart_count_from_clock"] == 540
    assert data["grading"]["slots_per_chart_from_c4"] == 4
    assert data["grading"]["descended_global_orbits"] == 135
    assert data["grading"]["descended_global_orbit_size"] == 16
    assert data["d12_boundary"]["bt815_stabilizer"]["structure"] == "D12"


def test_bt1364_bt1366_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "BT1364&ndash;BT1366: Q6, qutrit phase, and 2160 clock lifts" in text
    assert "BT1364_BT1366_q6_phase_2160_clock_lifts.md" in text
    assert "2160 = 45&times;48 = 45&times;12&times;4 = 45&times;3&times;16" in text


if __name__ == "__main__":
    test_bt1364_q6_flag_bus_lift()
    test_bt1365_qutrit_phase_alignment()
    test_bt1366_global_2160_clock_grading()
    test_bt1364_bt1366_docs_index_card_present()
    print("BT1364-BT1366 focused tests passed")
