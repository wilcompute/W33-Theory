from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from w33_selector_decimal_toroidal_jacobi_bridge import (  # noqa: E402
    build_selector_decimal_toroidal_jacobi_summary,
)


def test_local_selector_packet_has_exact_one_sixth_average() -> None:
    summary = build_selector_decimal_toroidal_jacobi_summary()
    packet = summary["local_selector_packet"]
    theorem = packet["theorem"]

    assert packet["selector_order"] == 6
    assert packet["local_bulk"] == 27
    assert packet["ordered_adjacent_pairs"] == 60
    assert packet["global_selector_carrier"] == 1620
    assert packet["average_weight"] == "1/6"
    assert packet["trivial_projector"]["rational_matrix"] == [
        ["1/3", "1/3", "1/3"],
        ["1/3", "1/3", "1/3"],
        ["1/3", "1/3", "1/3"],
    ]
    assert packet["sign_projector"]["rational_matrix"] == [
        ["0", "0", "0"],
        ["0", "0", "0"],
        ["0", "0", "0"],
    ]
    assert theorem["selector_order_is_exactly_six"] is True
    assert theorem["global_scaling_is_exactly_60_times_27_equals_1620"] is True
    assert theorem["plus_one_sixth_is_exact_local_selector_average"] is True
    assert theorem["sign_projector_vanishes_on_the_three_branch_permutation_rep"] is True
    assert theorem["standard_projector_has_rank_two"] is True


def test_decimal_toroidal_shell_packet_closes_exactly() -> None:
    summary = build_selector_decimal_toroidal_jacobi_summary()
    packet = summary["decimal_toroidal_shell_packet"]
    theorem = packet["theorem"]

    assert packet["decimal_period"] == 6
    assert packet["heawood_shell"] == 7
    assert packet["genus_denominator"] == 12
    assert packet["heawood_vertices"] == 14
    assert packet["heawood_edges"] == 21
    assert packet["tetra_fixed_point"] == 4
    assert packet["single_surface_flags"] == 84
    assert packet["fraction_dictionary"] == {
        "1_over_6": "1/6",
        "1_over_7": "1/7",
        "1_over_12": "1/12",
    }
    assert theorem["decimal_period_equals_local_selector_order"] is True
    assert theorem["shell_84_factorization_holds"] is True
    assert theorem["one_over_six_is_heawood_vertices_over_shell_84"] is True
    assert theorem["one_over_seven_is_genus_denominator_over_shell_84"] is True
    assert theorem["one_over_twelve_is_heawood_shell_over_shell_84"] is True


def test_common_packet_splices_hold_exactly() -> None:
    summary = build_selector_decimal_toroidal_jacobi_summary()
    packet = summary["common_packet_packet"]
    theorem = packet["theorem"]

    assert packet["q_cubic_identity"]["q_cubic"] == 27
    assert packet["q_cubic_identity"]["phi3_plus_two_phi6"] == 27
    assert packet["q_cubic_identity"]["splice_defect"] == 0
    assert packet["q_cubic_identity"]["splice_rhs"] == 0
    assert packet["exact_splices"]["27_equals_13_plus_14"] == [27, 13, 14]
    assert packet["exact_splices"]["81_equals_39_plus_42"] == [81, 39, 42]
    assert packet["exact_splices"]["162_equals_78_plus_84"] == [162, 78, 84]
    assert theorem["common_packet_is_exactly_6_times_27"] is True
    assert theorem["common_packet_is_exactly_2_times_81"] is True
    assert theorem["common_packet_is_exactly_81_plus_81"] is True
    assert theorem["q_cubic_splits_exactly_as_phi3_plus_two_phi6_at_q3"] is True
    assert theorem["protected_81_sector_splits_as_39_plus_42"] is True
    assert theorem["common_162_packet_splits_as_78_plus_84"] is True


def test_jacobi_packet_and_frontier_boundary_are_honest() -> None:
    summary = build_selector_decimal_toroidal_jacobi_summary()
    packet = summary["jacobi_packet"]
    theorem = packet["theorem"]
    bridge = summary["bridge_theorem"]

    assert packet["status"] == "ok"
    assert packet["scales"]["scale_sl3"] == 1 / 6
    assert packet["scales"]["scale_g2g2"] == -1 / 6
    assert theorem["artifact_status_is_ok"] is True
    assert theorem["scale_sl3_is_exact_plus_one_sixth"] is True
    assert theorem["scale_g2g2_is_exact_minus_one_sixth"] is True
    assert theorem["jacobi_closes_at_exact_plus_minus_one_sixth"] is True
    assert bridge["local_selector_average_explains_plus_one_sixth"] is True
    assert bridge["decimal_period_matches_selector_order"] is True
    assert bridge["shell_84_is_exactly_12_times_7_equals_14_times_6"] is True
    assert bridge["q_cubic_identity_specializes_exactly_at_q3"] is True
    assert bridge["protected_81_packet_splits_as_39_plus_42"] is True
    assert bridge["common_162_packet_splits_as_78_plus_84"] is True
    assert bridge["jacobi_closes_at_exact_plus_minus_one_sixth"] is True
    assert bridge["minus_one_sixth_remains_dual_orientation_frontier"] is True
