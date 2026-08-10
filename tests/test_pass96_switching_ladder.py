"""Pytest suite for Pass 96 -- the 2-rank ladder is finer than the two-graph switching structure."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass96_switching_ladder as mod

    mod.main()
    return json.loads(Path("w33_pass96_switching_ladder.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_ladder() -> None:
    d = _data()
    assert d["num_graphs"] == 28
    assert d["ladder_multiplicities"] == [17, 8, 2, 1]


def test_W_generic_Q_unique_min() -> None:
    d = _data()
    assert d["W_index_28_rank"] == 16
    assert d["Q_index_27_rank"] == 10
    assert d["Q_is_unique_min_2rank"] is True


def test_seidel_smith_constant_switching_invariant() -> None:
    ss = _data()["seidel_smith_group"]
    assert ss["constant_across_all_28"] is True
    assert ss["as_prime_power_multiplicities"] == {"3": 1, "5": 23, "7": 15, "25": 1}


def test_ducey_type_law() -> None:
    ss = _data()["seidel_smith_group"]
    assert ss["p_part_ranks"]["5"] == 24  # mult of Seidel eigenvalue -5
    assert ss["p_part_ranks"]["7"] == 15  # mult of Seidel eigenvalue 7
