"""Pytest suite for Pass 77 -- seven frontier ideas (GAP rep theory + geometry + equidistribution).

The GAP-dependent tracks (1, 5, 6) read the committed certificate w33_pass77_group_out.txt
(produced by w33_pass77_group.g); the test does not require a live GAP install.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass77_frontier as mod

    mod.main()
    return json.loads(Path("w33_pass77_frontier.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    pytest.importorskip("networkx")
    assert _data()["status"] == "PASS"


def test_T1_eigenspaces_irreducible() -> None:
    t1 = _data()["track1_gap_rank3_irreducible"]
    assert t1["rank_action"] == 3
    assert t1["perm_group_order"] == 25920
    assert t1["constituent_degrees"] == {"1": 1, "15": 1, "24": 1}
    assert t1["eigenspaces_irreducible"] is True


def test_T2_ovoid_separator() -> None:
    pytest.importorskip("networkx")
    t2 = _data()["track2_3_ovoid_separator"]
    assert t2["alpha_W33"] == 7
    assert t2["alpha_Q43"] == 10
    assert t2["W33_has_ovoid"] is False
    assert t2["Q43_has_ovoid"] is True
    assert t2["separated_by_ovoids"] is True


def test_T4_terwilliger_dim() -> None:
    t4 = _data()["track4_terwilliger"]
    assert t4["dim_terwilliger_algebra"] == 16


def test_T5_smith_normal_form() -> None:
    t5 = _data()["track5_gap_smith_normal_form"]
    assert t5["product"] == 3 * 2**56
    assert t5["product_is_3x2^56"] is True
    # elementary divisors 1^16 2^8 8^15 24
    from collections import Counter

    c = Counter(t5["elementary_divisors"])
    assert c[1] == 16 and c[2] == 8 and c[8] == 15 and c[24] == 1


def test_T6_weil_representation() -> None:
    t6 = _data()["track6_gap_weil_representation"]
    assert t6["Sp43_has_deg4"] is True
    assert t6["Sp43_has_deg5"] is True
    assert t6["weil_dim_9_splits_5_plus_4"] is True


def test_T7_joint_equidistribution() -> None:
    t7 = _data()["track7_joint_equidistribution"]
    assert t7["both_irrational_multiples_of_pi"] is True
    assert t7["small_integer_relation"] is None
    assert t7["rationally_independent"] is True
    assert t7["equidistributes_on_2_torus"] is True
