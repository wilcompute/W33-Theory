"""Pin the moonshine head character transport bridge."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_moonshine_head_character_transport_bridge import build_summary  # noqa: E402


def test_integer_character_subset_has_17_classes():
    summary = build_summary()
    classes = summary["moonshine_head_character_transport_dictionary"]["integer_character_classes"]
    assert len(classes) == 17


def test_all_rows_match_on_all_three_head_irreps():
    summary = build_summary()
    rows = summary["moonshine_head_character_transport_dictionary"]["rows"]
    assert all(row["all_match"] for row in rows) is True


def test_3c_exceptional_signature_is_minus1_248_minus248():
    summary = build_summary()
    rows = {row["class_name"]: row for row in summary["moonshine_head_character_transport_dictionary"]["rows"]}
    sig = rows["3C"]["inferred_head_characters"]
    assert sig["196883"] == -1
    assert sig["21296876"] == 248
    assert sig["842609326"] == -248


def test_41a_endpoint_signature_is_1_0_minus1():
    summary = build_summary()
    rows = {row["class_name"]: row for row in summary["moonshine_head_character_transport_dictionary"]["rows"]}
    sig = rows["41A"]["inferred_head_characters"]
    assert sig["196883"] == 1
    assert sig["21296876"] == 0
    assert sig["842609326"] == -1


def test_head_character_transport_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["moonshine_head_character_transport_theorem"]
    assert all(theorem.values()) is True
