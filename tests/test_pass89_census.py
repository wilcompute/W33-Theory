"""Pytest suite for Pass 89 -- arithmetic census of the 28 SRG(40,12,2,4) graphs.

Reads the committed GAP census certificate w33_pass89_census_out.txt; no live GAP needed.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass89_census as mod

    mod.main()
    return json.loads(Path("w33_pass89_census.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_four_smith_and_critical_groups() -> None:
    d = _data()
    assert d["num_graphs"] == 28
    assert len(d["smith_groups"]) == 4
    assert len(d["critical_groups"]) == 4
    assert d["class_sizes"] == [17, 8, 2, 1]


def test_partitions_coincide() -> None:
    assert _data()["partitions_coincide_smith_critical_2rank"] is True


def test_five_sylow_constant() -> None:
    # Ducey: 5 does not divide r-s=6, so the 5-part is parameter-determined
    assert _data()["five_sylow_constant_Z5_23"] is True


def test_two_GQ_at_opposite_extremes() -> None:
    d = _data()
    assert d["W_class_size"] == 17  # symplectic W(3,3): generic
    assert d["Q_class_size"] == 1  # parabolic quadric Q(4,3): unique extreme


def test_W_smith_group_is_generic_class() -> None:
    # the size-17 Smith group is (Z/2)^8 (+) (Z/8)^15 (+) Z/24, W(3,3)'s
    d = _data()
    generic = max(d["smith_groups"], key=lambda s: s["count"])
    assert generic["count"] == 17
    assert generic["structure"] == {"2": 8, "8": 15, "24": 1}
    assert generic["two_rank"] == 16


def test_graded_transfer_ladder() -> None:
    """Both the Smith and critical group census form the same arithmetic 2-adic transfer ladder."""
    lad = _data()["graded_transfer_ladder"]
    assert lad["ordered_by_two_rank"] == [16, 14, 12, 10]
    assert lad["transfer_count_from_W"] == [
        0,
        2,
        4,
        6,
    ]  # Q=6 matches the Pass 88 transfer
    # Smith ladder: Z/2 +2, Z/4 +2, Z/8 -2
    assert lad["smith"]["Z2"] == [8, 10, 12, 14]
    assert lad["smith"]["Z4"] == [0, 2, 4, 6]
    assert lad["smith"]["Z8"] == [15, 13, 11, 9]
    assert lad["smith"]["arithmetic_ok"] is True
    # critical ladder: Z/2 +2, Z/80 +2, Z/160 -2; Z/10, Z/40 constant
    assert lad["critical"]["Z2"] == [0, 2, 4, 6]
    assert lad["critical"]["Z80"] == [0, 2, 4, 6]
    assert lad["critical"]["Z160"] == [14, 12, 10, 8]
    assert lad["critical"]["Z10_const"] == [8, 8, 8, 8]
    assert lad["critical"]["arithmetic_ok"] is True
