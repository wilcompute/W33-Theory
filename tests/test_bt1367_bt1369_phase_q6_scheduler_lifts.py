#!/usr/bin/env python3
"""Regression tests for BT1367-BT1369."""
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


def test_bt1367_global_phase_holonomy() -> None:
    run_script("analysis/bt1367_global_qutrit_phase_gauge_holonomy.py")
    data = load_json("data/bt1367_global_qutrit_phase_gauge_holonomy.json")
    assert data["verified"] is True
    assert data["transport"]["skew_line_matchings"] == 540
    assert data["quadrangle_holonomy"]["quadrangles"] == 59670
    assert data["quadrangle_holonomy"]["holonomy_order_profile"] == {
        "1": 11070,
        "2": 29160,
        "3": 19440,
    }
    assert data["checks"]["quadrangle_holonomy_is_not_flat"] is True


def test_bt1368_q6_tomotope_equivariant_lift() -> None:
    run_script("analysis/bt1368_q6_tomotope_equivariant_flag_lift.py")
    data = load_json("data/bt1368_q6_tomotope_equivariant_flag_lift.json")
    assert data["verified"] is True
    assert data["tomotope_aut"]["aut_order"] == 96
    assert data["tomotope_aut"]["orbit_sizes"] == [96, 96]
    assert data["q6_edge_subgroup"]["group_order"] == 96
    assert data["q6_edge_subgroup"]["orbit_sizes"] == [96, 96]
    assert data["q6_edge_subgroup"]["order_profile"] == {
        "1": 1,
        "2": 27,
        "3": 32,
        "4": 36,
    }
    assert data["gap_witness"]["isomorphic"] == "true"


def test_bt1369_generation_time_scheduler() -> None:
    run_script("analysis/bt1369_steinberg_generation_time_scheduler.py")
    data = load_json("data/bt1369_steinberg_generation_time_scheduler.json")
    assert data["verified"] is True
    assert data["scheduler"]["phase_orbits"] == 135
    assert data["scheduler"]["orbit_size"] == 16
    assert data["scheduler"]["total_slots"] == 2160
    assert data["scheduler"]["lanes_per_generation_state"] == 5
    assert data["scheduler"]["slots_per_generation_state"] == 80
    assert data["checks"]["geography_is_time_lift_of_bt868_positive_chirality"] is True


def test_bt1367_bt1369_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert (
        "BT1367&ndash;BT1369: phase holonomy, Q6 equivariance, and generation-time scheduling"
        in text
    )
    assert "BT1367_BT1369_phase_q6_scheduler_lifts.md" in text
    assert "59670" in text
    assert "135 = 5&times;27" in text


if __name__ == "__main__":
    test_bt1367_global_phase_holonomy()
    test_bt1368_q6_tomotope_equivariant_lift()
    test_bt1369_generation_time_scheduler()
    test_bt1367_bt1369_docs_index_card_present()
    print("BT1367-BT1369 focused tests passed")
