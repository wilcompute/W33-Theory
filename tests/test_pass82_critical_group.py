"""Pytest suite for Pass 82 -- critical group separates the cospectral W(3,3)/Q(4,3) pair.

Reads the committed GAP certificate w33_pass82_critical_group_out.txt (Smith normal forms of the
two Laplacians); no live GAP install required.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass82_critical_group as mod

    mod.main()
    return json.loads(Path("w33_pass82_critical_group.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_orders_equal_and_are_spanning_tree_count() -> None:
    d = _data()
    kw = d["critical_group_W33"]
    kq = d["critical_group_Q43"]
    assert kw["order"] == kq["order"] == (2**81) * (5**23)
    assert kw["order_factored"] == "2^81 * 5^23"


def test_W33_critical_group_structure() -> None:
    kw = _data()["critical_group_W33"]
    # (Z/10)^8 (+) Z/40 (+) (Z/160)^14
    assert kw["invariant_factors"] == {"10": 8, "40": 1, "160": 14}
    assert kw["sylow_5"] == {"5": 23}


def test_Q43_critical_group_structure() -> None:
    kq = _data()["critical_group_Q43"]
    # (Z/2)^6 (+) (Z/10)^8 (+) Z/40 (+) (Z/80)^6 (+) (Z/160)^8
    assert kq["invariant_factors"] == {"2": 6, "10": 8, "40": 1, "80": 6, "160": 8}
    assert kq["sylow_5"] == {"5": 23}


def test_separation_in_2_sylow() -> None:
    d = _data()
    sep = d["separation"]
    assert sep["same_order"] is True
    assert sep["same_5_sylow"] is True
    assert sep["different_2_sylow"] is True
    assert sep["separates_cospectral_pair"] is True
    # groups are genuinely non-isomorphic
    assert (
        d["critical_group_W33"]["invariant_factors"]
        != d["critical_group_Q43"]["invariant_factors"]
    )
