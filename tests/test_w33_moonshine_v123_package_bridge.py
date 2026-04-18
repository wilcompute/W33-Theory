"""Pin the exact graded moonshine package V1⊕V2⊕V3."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_moonshine_v123_package_bridge import (  # noqa: E402
    build_summary,
    head_to_v123_package,
    v123_package_to_head,
)


def test_head_to_package_and_back_is_exact():
    head = {196883: 35, 21296876: 92, 842609326: 222}
    pkg = head_to_v123_package(head)
    assert pkg == {"V1": 36, "V2": 128, "V3": 386}
    assert v123_package_to_head(pkg) == {
        "196883": 35,
        "21296876": 92,
        "842609326": 222,
    }


def test_anchored_rows_match_actual_monster_traces():
    summary = build_summary()
    rows = summary["moonshine_v123_package_dictionary"]["anchored_rows"]
    assert all(row["all_match"] for row in rows) is True


def test_supported_seed_has_32_distinct_packages():
    summary = build_summary()
    assert summary["moonshine_v123_package_dictionary"]["distinct_package_count"] == 32


def test_3c_has_sparse_package_0_248_0():
    summary = build_summary()
    rows = {row["class_name"]: row for row in summary["moonshine_v123_package_dictionary"]["rows"]}
    assert rows["3C"]["package"] == {"V1": 0, "V2": 248, "V3": 0}


def test_41a_has_endpoint_package_2_2_3():
    summary = build_summary()
    rows = {row["class_name"]: row for row in summary["moonshine_v123_package_dictionary"]["rows"]}
    assert rows["41A"]["package"] == {"V1": 2, "V2": 2, "V3": 3}


def test_8a_and_8aprime_are_separated_only_by_v2_sign():
    summary = build_summary()
    rows = {row["class_name"]: row for row in summary["moonshine_v123_package_dictionary"]["rows"]}
    assert rows["8A"]["package"]["V1"] == rows["8A'"]["package"]["V1"] == 36
    assert rows["8A"]["package"]["V3"] == rows["8A'"]["package"]["V3"] == 386
    assert rows["8A"]["package"]["V2"] == 128
    assert rows["8A'"]["package"]["V2"] == -128


def test_prime_power_edge_count_is_35():
    summary = build_summary()
    rows = summary["moonshine_v123_package_dictionary"]["atlas_edge_rows"]
    assert len(rows) == 35
    assert all(row["matches_atlas"] for row in rows) is True


def test_composite_transport_row_count_is_18():
    summary = build_summary()
    rows = summary["moonshine_v123_package_dictionary"]["composite_rows"]
    assert len(rows) == 18


def test_v123_package_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["moonshine_v123_package_theorem"]
    assert all(theorem.values()) is True
