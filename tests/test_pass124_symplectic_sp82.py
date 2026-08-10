"""Pytest suite for Pass 124 -- Sp(8,2) = SRG(255,126,61,63), the E8/2E8 orthogonality graph."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass124_symplectic_sp82 as mod

    mod.main()
    return json.loads(Path("w33_pass124_symplectic_sp82.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_full_graph_is_sp82() -> None:
    fg = _data()["full_graph"]
    assert fg["vertices"] == 255
    assert fg["params"] == "SRG(255,126,61,63)"
    assert {int(k): v for k, v in fg["spectrum"].items()} == {126: 1, 7: 135, -9: 119}


def test_subconstituents_are_the_two_glue_graphs() -> None:
    sc = _data()["subconstituents"]
    assert sc["isotropic_135"].startswith("SRG(135,70,37,35)")
    assert sc["anisotropic_120"].startswith("SRG(120,63,30,36)")


def test_symmetry_tower_indices() -> None:
    t = _data()["symmetry_tower"]
    assert t["Sp(8,2)"] == 47377612800
    assert t["GO+_8(2)"] == 348364800
    assert t["W(E6)"] == 51840
    assert t["index_Sp_over_GO"] == 136  # 135 + 1 isotropic incl 0
    assert t["index_GO_over_WE6"] == 6720  # 120 * 56 (Pass 117)
