#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_heawood_spread_pair_psp_equivariance import build_result as build_heawood_psp  # noqa: E402
from w33_marcelis_trace_flag_law import build_result as build_marcelis_flag  # noqa: E402


def test_heawood_spread_pair_bijection_is_psp_equivariant() -> None:
    result = build_heawood_psp()
    assert result["status"] == "PASS"
    assert all(result["checks"].values())
    assert result["counts"]["transvection_generators"] == 8
    assert result["counts"]["C6_components"] == 270
    assert result["counts"]["four_intersection_spread_pairs"] == 270
    assert result["counts"]["PSp_orbit_of_one_C6"] == 270
    assert result["counts"]["PSp_C6_stabilizer_order"] == 96
    assert result["checks"]["all_generators_preserve_intrinsic_slot_graph"] is True
    assert result["checks"]["all_generators_commute_with_cycle_spread_bijection"] is True


def test_marcelis_trace_complete_flag_controls_line_lifts() -> None:
    result = build_marcelis_flag()
    assert result["status"] == "PASS"
    assert all(result["checks"].values())
    assert result["flag"]["p_inf"] == "0001"
    assert result["flag"]["L_inf_equations"] == "x0=x1=0"
    assert result["flag"]["H0_equation"] == "x0=0"

    strata = result["line_lift_flag_strata"]
    assert strata["L_inf"] == {
        "binary_lines": 1,
        "lifts_per_line": [1],
        "GF4_line_mass": 1,
    }
    assert strata["H0_minus_L_inf"] == {
        "binary_lines": 6,
        "lifts_per_line": [2],
        "GF4_line_mass": 12,
    }
    assert strata["outside_H0"] == {
        "binary_lines": 28,
        "lifts_per_line": [4],
        "GF4_line_mass": 112,
    }
    assert strata["mass_identity"] == "1*1 + 6*2 + 28*4 = 125"


def test_marcelis_punctured_images_obey_plane_line_point_flag_law() -> None:
    result = build_marcelis_flag()
    law = result["punctured_plane_flag_law"]
    assert len(law["puncture_lines"]) == 7
    assert law["puncture_line_plane_multiplicity_histogram"] == {"2": 6, "3": 1}
    assert law["puncture_point_plane_counts"] == {
        "0001": 7,
        "0010": 4,
        "0011": 4,
    }
    assert result["checks"]["puncture_lines_are_exactly_the_7_Fano_lines_of_H0"] is True
    assert result["checks"]["plane_puncture_line_is_P_intersect_H0_except_H0_to_Linf"] is True
    assert result["checks"]["puncture_point_is_line_intersect_Linf_except_Linf_to_pinf"] is True
    assert result["checks"]["two_images_are_exactly_delete_r_a_and_r_b"] is True
    assert result["checks"]["punctured_GF4_line_mass_is_232"] is True


if __name__ == "__main__":
    test_heawood_spread_pair_bijection_is_psp_equivariant()
    test_marcelis_trace_complete_flag_controls_line_lifts()
    test_marcelis_punctured_images_obey_plane_line_point_flag_law()
    print("W33 Heawood PSp + Marcelis flag tests passed")
