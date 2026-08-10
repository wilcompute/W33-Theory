"""Pytest suite for Pass 90 -- automorphism census of the 28 SRG(40,12,2,4) graphs."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass90_aut as mod

    mod.main()
    return json.loads(Path("w33_pass90_aut.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_two_GQ_maximal_symmetry() -> None:
    d = _data()
    assert d["GQ_graphs_max_aut"]["order"] == 51840  # = |Sp(4,3)| = |W(E6)|
    assert d["GQ_graphs_max_aut"]["indices"] == [27, 28]  # Q(4,3), W(3,3)
    assert d["next_largest_aut"] == 648  # every other graph is far smaller


def test_W_and_Q_bookend_the_ladder() -> None:
    d = _data()
    assert (
        d["W"]["two_rank"] == 16 and d["W"]["aut"] == 51840
    )  # generic rung, max symmetry
    assert (
        d["Q"]["two_rank"] == 10 and d["Q"]["aut"] == 51840
    )  # extreme rung, max symmetry


def test_median_symmetry_anticorrelates_off_the_bookends() -> None:
    # excluding the two 51840 GQs, the median |Aut| rises as 2-rank falls: 9 (r16), 48 (r14), 384 (r12)
    rs = _data()["rung_summary"]
    assert rs["16"]["median_aut"] == 9
    assert rs["14"]["median_aut"] == 48
    assert rs["12"]["median_aut"] == 384


def test_family_mass_invariant() -> None:
    d = _data()
    assert d["mass_sum_1_over_aut"] == "189457/51840"
    assert d["labelled_graph_count"] > 0
