"""Pin the exact qutrit foundation bridge of W(3,3)."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_qutrit_foundation_bridge import build_summary  # noqa: E402


def test_qutrit_foundation_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["qutrit_foundation_theorem"]
    assert all(theorem.values()) is True


def test_w33_has_40_vertices_240_edges():
    summary = build_summary()
    d = summary["qutrit_foundation_dictionary"]
    assert d["n_vertices"] == 40
    assert d["n_edges"] == 240


def test_every_local_shell_has_12_27_split():
    summary = build_summary()
    rows = summary["qutrit_foundation_dictionary"]["local_shell_rows"]
    assert all(row["N12_size"] == 12 and row["H27_size"] == 27 for row in rows)


def test_every_local_shell_has_four_triangles_and_nine_size3_fibers():
    summary = build_summary()
    rows = summary["qutrit_foundation_dictionary"]["local_shell_rows"]
    assert all(row["triangle_sizes"] == [3, 3, 3, 3] for row in rows)
    assert all(row["fiber_sizes"] == [3] * 9 for row in rows)


def test_every_pair_of_distinct_fibers_has_three_edges_between_them():
    summary = build_summary()
    rows = summary["qutrit_foundation_dictionary"]["local_shell_rows"]
    assert all(row["inter_fiber_counts"] == [3] for row in rows)


def test_every_h27_shell_has_36_internal_triangles():
    summary = build_summary()
    rows = summary["qutrit_foundation_dictionary"]["local_shell_rows"]
    assert all(row["h27_triangle_count"] == 36 for row in rows)


def test_point_line_incidence_has_40_lines_of_size_4():
    summary = build_summary()
    inc = summary["qutrit_foundation_dictionary"]["incidence"]
    assert inc["line_count"] == 40
    assert inc["line_sizes"] == [4]


def test_point_line_incidence_operator_identity_holds():
    summary = build_summary()
    inc = summary["qutrit_foundation_dictionary"]["incidence"]
    assert inc["bbt_equals_a_plus_4i"] is True
    assert inc["h_can_equals_16i_minus_bbt"] is True


def test_canonical_quadratic_operator_has_expected_spectrum():
    summary = build_summary()
    inc = summary["qutrit_foundation_dictionary"]["incidence"]
    assert inc["h_can_spectrum"] == {"0": 1, "10": 24, "16": 15}
