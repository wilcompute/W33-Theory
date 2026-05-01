"""Tests for the holonomy parity classification theorem (Chapter 6 frontier)."""
from __future__ import annotations

from scripts.w33_cct_holonomy_parity_classification_audit import (
    cct_holonomy_parity_classification_summary,
    classify_cycle_transports,
    parity_theorem_holds,
)


def test_parity_law_holds_for_lengths_3_to_6() -> None:
    for n in (3, 4, 5, 6):
        assert parity_theorem_holds(n), f"parity theorem failed for cycle length {n}"


def test_trivial_holonomy_patterns_count_correctly() -> None:
    # Length n: 2^(n-1) even-complement and 2^(n-1) odd-complement patterns
    for n in (3, 4, 5, 6):
        records = classify_cycle_transports(n)
        trivial = [r for r in records if r["holonomy_parity"] == 0]
        nontrivial = [r for r in records if r["holonomy_parity"] == 1]
        assert len(trivial) == 2 ** (n - 1)
        assert len(nontrivial) == 2 ** (n - 1)
        # trivial → selector, nontrivial → no selector
        assert all(r["has_global_selector"] for r in trivial)
        assert all(not r["has_global_selector"] for r in nontrivial)


def test_chapter6_canonical_cycle_is_nontrivial_obstruction_instance() -> None:
    summary = cct_holonomy_parity_classification_summary()
    instance = summary["chapter6_canonical_instance"]

    assert instance["cycle"] == ("A", "B", "C", "A")
    assert instance["complement_edges"] == 1
    assert instance["holonomy_class"] == 1
    assert instance["matches_obstruction_instance"] is True


def test_parity_law_packet_statement_and_theorem_bundle() -> None:
    summary = cct_holonomy_parity_classification_summary()

    law = summary["parity_law_packet"]
    assert "if and only if" in law["statement"]
    assert law["holonomy_group"] == "Z2"
    assert law["min_consistent_period_when_obstructed"] == 2

    assert all(summary["theorem"].values())
    assert "complete finite classification" in summary["w33_alignment_packet"]["boundary"]
