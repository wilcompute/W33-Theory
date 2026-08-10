"""Pytest suite for Pass 76 -- cospectral non-isomorphic mate of W(3,3)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass76_cospectral_mates as mod

    mod.main()
    return json.loads(Path("w33_pass76_cospectral_mates.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    pytest.importorskip("networkx")
    assert _data()["status"] == "PASS"


def test_Q43_is_cospectral_srg() -> None:
    t1 = _data()["track1_Q43_mate"]
    assert t1["is_SRG_40_12_2_4"] is True
    assert t1["srg_params"] == [40, 12, 2, 4]
    assert t1["cospectral_with_W33"] is True


def test_Q43_non_isomorphic_but_locally_identical() -> None:
    pytest.importorskip("networkx")
    t1 = _data()["track1_Q43_mate"]
    # non-isomorphic (exact test)
    assert t1["isomorphic_to_W33"] is False
    assert t1["non_isomorphic"] is True
    # yet locally identical: both 4K3 neighbourhoods and 4K1 mu-graphs
    assert t1["neighbourhood_W33"] == t1["neighbourhood_Q43"]
    assert t1["mu_graph_W33"] == t1["mu_graph_Q43"]
    assert t1["locally_identical"] is True


def test_gm_switching_rigid() -> None:
    t2 = _data()["track2_godsil_mckay_negative"]
    assert t2["gm_size4_switching_sets"] == 0
    assert t2["switching_rigid_at_size_4"] is True


def test_integral_invariants() -> None:
    t3 = _data()["track3_integral_invariants"]
    assert t3["det_A"] == -(3 * 2**56)
    assert t3["det_check"] is True
    assert t3["rank_mod_2"] == 16
    assert t3["rank_mod_3"] == 39
    assert t3["rank_mod_5"] == 40
