"""Pin the supported-seed moonshine head-signature bridge."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_supported_seed_head_signature_bridge import build_summary  # noqa: E402


def test_supported_seed_has_32_head_signature_rows():
    summary = build_summary()
    rows = summary["supported_seed_head_signature_dictionary"]["rows"]
    assert len(rows) == 32


def test_distinct_signature_count_is_32():
    summary = build_summary()
    assert summary["supported_seed_head_signature_dictionary"]["distinct_signature_count"] == 32


def test_atlas_available_prime_power_edge_count_is_35():
    summary = build_summary()
    rows = summary["supported_seed_head_signature_dictionary"]["atlas_edge_rows"]
    assert len(rows) == 35
    assert all(row["matches_atlas"] for row in rows) is True


def test_composite_transport_row_count_is_18():
    summary = build_summary()
    rows = summary["supported_seed_head_signature_dictionary"]["composite_rows"]
    assert len(rows) == 18


def test_10e_extended_signature_is_0_1_minus1():
    summary = build_summary()
    rows = {
        row["class_name"]: row
        for row in summary["supported_seed_head_signature_dictionary"]["rows"]
    }
    sig = rows["10E"]["signature"]
    assert sig["196883"] == 0
    assert sig["21296876"] == 1
    assert sig["842609326"] == -1


def test_8a_and_8aprime_are_separated_by_head_signature():
    summary = build_summary()
    rows = {
        row["class_name"]: row
        for row in summary["supported_seed_head_signature_dictionary"]["rows"]
    }
    assert rows["8A"]["signature"] != rows["8A'"]["signature"]


def test_supported_seed_head_signature_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["supported_seed_head_signature_theorem"]
    assert all(theorem.values()) is True
