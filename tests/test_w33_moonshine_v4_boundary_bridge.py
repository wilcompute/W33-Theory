"""Pin the exact moonshine V4 boundary."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_moonshine_v4_boundary_bridge import (  # noqa: E402
    build_summary,
    exact_chi4_from_series,
    exact_v4_package_from_series,
    naive_chi5_from_series,
)


def test_exact_quartic_formula_for_3c_is_minus_247():
    assert exact_chi4_from_series("3C") == -247


def test_exact_quartic_package_for_41a_is_2_2_3_4():
    assert exact_v4_package_from_series("41A") == {
        "V1": 2,
        "V2": 2,
        "V3": 3,
        "V4": 4,
    }


def test_exact_quartic_formula_matches_all_anchored_classes():
    summary = build_summary()
    rows = summary["moonshine_v4_boundary_dictionary"]["anchored_v4_rows"]
    assert all(row["chi4_match"] for row in rows) is True


def test_supported_seed_has_32_distinct_quartic_packages():
    summary = build_summary()
    assert summary["moonshine_v4_boundary_dictionary"]["distinct_package_count"] == 32


def test_3c_has_sparse_quartic_package():
    summary = build_summary()
    rows = {
        row["class_name"]: row for row in summary["moonshine_v4_boundary_dictionary"]["supported_rows"]
    }
    assert rows["3C"]["package"] == {"V1": 0, "V2": 248, "V3": 0, "V4": 0}


def test_8a_and_8aprime_have_opposite_even_quartic_package_entries():
    summary = build_summary()
    rows = {
        row["class_name"]: row for row in summary["moonshine_v4_boundary_dictionary"]["supported_rows"]
    }
    assert rows["8A"]["package"] == {"V1": 36, "V2": 128, "V3": 386, "V4": 1024}
    assert rows["8A'"]["package"] == {"V1": 36, "V2": -128, "V3": 386, "V4": -1024}


def test_naive_quintic_boundary_fails_at_2a_and_2b():
    summary = build_summary()
    rows = summary["moonshine_v4_boundary_dictionary"]["anchored_v5_boundary_rows"]
    bad = {row["class_name"] for row in rows if not row["chi5_match"]}
    assert bad == {"2A", "2B"}


def test_naive_quintic_formula_for_2a_is_not_actual_character():
    summary = build_summary()
    rows = {
        row["class_name"]: row for row in summary["moonshine_v4_boundary_dictionary"]["anchored_v5_boundary_rows"]
    }
    assert naive_chi5_from_series("2A") == rows["2A"]["naive_chi_293553734298"]
    assert rows["2A"]["naive_chi_293553734298"] != rows["2A"]["actual_chi_293553734298"]


def test_prime_power_edge_count_is_35():
    summary = build_summary()
    rows = summary["moonshine_v4_boundary_dictionary"]["atlas_edge_rows"]
    assert len(rows) == 35
    assert all(row["matches_atlas"] for row in rows) is True


def test_v4_boundary_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["moonshine_v4_boundary_theorem"]
    assert all(theorem.values()) is True
