from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text())


def test_nonabelian_golden_certificate() -> None:
    data = load("PART_BT2974_BT2981_NONABELIAN_GOLDEN_INFORMATION_results.json")
    assert data["schema"] == "w33.pass2974_2981.nonabelian_golden_information.v1"
    assert data["check_count"] == 6
    assert data["pass2974"]["fundamental_chords"] == 36
    assert data["pass2974"]["gauge_orbit_count"] == 81129638418148456557941239054336
    assert data["pass2975"]["design"] == "2-(10,3,4)"
    assert data["pass2975"]["explicit_s6_actions"] == 720
    assert abs(data["pass2976"]["unrestricted_single_copy_helstrom"] - 0.9082482904638599) < 1e-14
    assert data["pass2979"]["canonical_golden_word"] == "rru = R4^2 U6"
    assert data["pass2980"]["no_consecutive_expensive_slots"] is True
    assert data["pass2981"]["faithful_order3_lift_to_D4"] is False
    assert data["pass2981"]["a4_element_order_histogram"] == {"1": 1, "2": 3, "3": 8}


def test_general_isotropic_pilot_boundary() -> None:
    data = load("PART_BT2977_GENERAL_ISOTROPIC_M36_PILOT_results.json")
    assert data["total_rank4_isotropic_subspaces"] == 213648435
    assert data["rref_pivot_shards"] == 495
    assert data["partition_is_duplicate_free"] is True
    assert data["distinct_general_subspaces_examined"] == 649940
    assert data["single_error_collinear_projectors"] == 6
    assert data["non_css_collinear_projectors"] == 6
    assert data["nonstabilizer_collinear_candidates"] == 0
    assert all(row["clean_success"] == "1/27" for row in data["candidate_rows"])
    assert all(row["accepted_clean_is_stabilizer"] for row in data["candidate_rows"])


def test_manuscript_and_frontdoor_sources() -> None:
    shared = ROOT / "analysis" / "BT2974_BT2983_nonabelian_golden_information_insert.tex"
    blueprint = ROOT / "analysis" / "BT2974_BT2983_nonabelian_golden_information_blueprint_insert.tex"
    integrator = ROOT / "tools" / "integrate_bt2974_bt2983.py"
    assert shared.exists() and "General-isotropic M36 frontier" in shared.read_text()
    assert blueprint.exists() and "route memory has two layers" in blueprint.read_text()
    assert integrator.exists()
