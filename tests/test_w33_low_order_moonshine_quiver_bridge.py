"""Pin the finite low-order moonshine quiver."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_low_order_moonshine_quiver_bridge import build_summary  # noqa: E402


def test_node_counts_match_expected_split():
    summary = build_summary()
    counts = summary["low_order_moonshine_quiver_dictionary"]["node_counts"]
    assert counts == {
        "quotient": 1,
        "quadratic_fricke": 5,
        "linear_eta": 6,
        "affine_exceptional": 1,
        "composite_power": 4,
    }


def test_all_expected_nodes_are_present():
    summary = build_summary()
    names = {row["name"] for row in summary["low_order_moonshine_quiver_dictionary"]["nodes"]}
    assert names == {
        "1A",
        "2A", "3A", "5A", "7A", "13A",
        "2B", "3B", "5B", "7B", "13B", "4C",
        "3C",
        "4A", "6A", "8A", "10A",
    }


def test_key_power_edges_are_present():
    summary = build_summary()
    edges = {(e["src"], e["dst"], e["kind"]) for e in summary["low_order_moonshine_quiver_dictionary"]["edges"]}
    assert ("4A", "2B", "square_map") in edges
    assert ("8A", "4C", "square_map") in edges
    assert ("10A", "5A", "square_map") in edges
    assert ("6A", "2A", "cube_map") in edges
    assert ("1A", "3C", "prime_faber_source") in edges


def test_quiver_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["low_order_moonshine_quiver_theorem"]
    assert all(theorem.values()) is True
