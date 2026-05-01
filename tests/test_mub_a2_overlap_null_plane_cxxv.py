from __future__ import annotations

from scripts.w33_mub_a2_overlap_null_plane_audit import (
    mub_a2_overlap_null_plane_summary,
)


def test_cxxv_sector_packet_is_the_three_by_twelve_mub_frame_split() -> None:
    summary = mub_a2_overlap_null_plane_summary()

    assert summary["sector_packet"] == {
        "sector_labels": ("E+", "E-", "O"),
        "sector_size": 12,
        "frame_count": 36,
        "coarse_quotient_shape": "36 = 12 x 3",
        "a2_basis": ((1, -1, 0), (1, 1, -2)),
    }


def test_cxxv_four_overlap_graph_has_remote_quotient_and_edge_counts() -> None:
    summary = mub_a2_overlap_null_plane_summary()

    assert summary["four_overlap_graph"] == {
        "quotient": ((3, 6, 6), (6, 3, 6), (6, 6, 3)),
        "row_sums": (15, 15, 15),
        "regular_degree": 15,
        "within_sector_edges": 54,
        "cross_sector_edges": 216,
        "total_edges": 270,
        "constant_eigenvalue": (15, 15, 15),
        "a2_eigenvalue": -3,
        "a2_images": ((-3, 3, 0), (-3, -3, 6)),
    }


def test_cxxv_total_overlap_quotient_balances_same_and_cross_sectors() -> None:
    summary = mub_a2_overlap_null_plane_summary()

    assert summary["total_overlap_form"] == {
        "quotient": ((30, 30, 30), (30, 30, 30), (30, 30, 30)),
        "same_sector_total": 30,
        "cross_sector_total": 30,
        "row_sums": (90, 90, 90),
        "constant_eigenvalue": (90, 90, 90),
        "a2_images": ((0, 0, 0), (0, 0, 0)),
        "determinant": 0,
        "rank": 1,
    }


def test_cxxv_theorem_flags_are_all_true() -> None:
    summary = mub_a2_overlap_null_plane_summary()

    assert summary["theorem"] == {
        "four_overlap_graph_is_15_regular": True,
        "same_and_cross_sector_total_overlap_balances_to_30": True,
        "four_overlap_quotient_has_a2_eigenvalue_minus_3": True,
        "total_overlap_quotient_kills_a2_plane": True,
        "total_overlap_quotient_is_rank_one": True,
    }
