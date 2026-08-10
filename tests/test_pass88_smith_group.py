"""Pytest suite for Pass 88 -- Smith group, critical group, and the p-rank separator."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass88_smith_group as mod

    mod.main()
    return json.loads(Path("w33_pass88_smith_group.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_smith_groups_differ_same_order() -> None:
    d = _data()
    assert d["smith_group_W"]["order"] == d["smith_group_Q"]["order"] == 3 * 2**56
    assert d["smith_groups_differ"] is True
    assert d["smith_group_W"]["invariant_factors"] == {"2": 8, "8": 15, "24": 1}
    assert d["smith_group_Q"]["invariant_factors"] == {"2": 14, "4": 6, "8": 9, "24": 1}


def test_p_rank_separator() -> None:
    p = _data()["p_ranks"]
    assert (p["2rank_W"], p["2rank_Q"]) == (16, 10)  # the separator
    assert p["3rank_W"] == p["3rank_Q"] == 39  # 3-rank does not separate


def test_binary_codes_differ() -> None:
    b = _data()["binary_codes"]
    assert b["C2_W"] == [40, 16, 8]
    assert b["C2_Q"] == [40, 10, 12]  # different code entirely


def test_critical_groups_differ() -> None:
    assert _data()["critical_groups"]["differ"] is True


def test_two_adic_transfer_switches_sides() -> None:
    """The factor of 2 switches sides across the central 2-band: 6 low-side 1->2, 6 high-side 8->4,
    net valuation transfer 0 (so |S(W)|=|S(Q)|), symmetric about the eight agreeing 2's.
    """
    t = _data()["two_adic_transfer"]
    assert t["positions_Q_gains_a_2_low_side"] == 6
    assert t["positions_W_gains_a_2_high_side"] == 6
    assert t["net_valuation_transfer"] == 0
    assert t["v2_total_W"] == t["v2_total_Q"] == 56
    assert t["middle_agreeing_two_band"] == 8
    assert t["conserved"] is True
