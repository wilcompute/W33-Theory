"""Pin the full offline-supported moonshine transport graph."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_supported_seed_moonshine_transport_bridge import build_summary  # noqa: E402


def test_supported_seed_has_32_classes():
    summary = build_summary()
    supported = summary["supported_seed_moonshine_transport_dictionary"]["supported_classes"]
    assert len(supported) == 32


def test_supported_orders_match_expected_list():
    summary = build_summary()
    by_order = summary["supported_seed_moonshine_transport_dictionary"]["supported_classes_by_order"]
    assert list(by_order.keys()) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]


def test_all_atlas_available_edges_match():
    summary = build_summary()
    avail = summary["supported_seed_moonshine_transport_dictionary"]["atlas_available_counts"]
    good = summary["supported_seed_moonshine_transport_dictionary"]["atlas_match_counts"]
    assert good["square"] == avail["square"]
    assert good["cube"] == avail["cube"]
    assert good["fifth"] == avail["fifth"]


def test_all_18_composite_checks_are_verified():
    summary = build_summary()
    rows = summary["supported_seed_moonshine_transport_dictionary"]["composite_rows"]
    assert len(rows) == 18
    assert all(row["verified"] for row in rows) is True
    assert all(row["power_map_source"] == "atlas" for row in rows) is True


def test_transport_graph_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["supported_seed_moonshine_transport_theorem"]
    assert all(theorem.values()) is True
