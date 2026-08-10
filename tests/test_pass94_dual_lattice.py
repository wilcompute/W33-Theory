"""Pytest suite for Pass 94 -- W(3,3) vs Q(4,3) code-lattice discriminant forms."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass94_dual_lattice as mod

    mod.main()
    return json.loads(Path("w33_pass94_dual_lattice.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_W_is_E8_form() -> None:
    W = _data()["W"]
    assert W["code"] == "[40,16,8]"
    assert W["glue_dim"] == 8
    assert W["disc_form"] == "O+_8(2)"
    assert W["nonzero_isotropic"] == 135


def test_Q_is_rank20() -> None:
    Q = _data()["Q"]
    assert Q["code"] == "[40,10,12]"
    assert Q["glue_dim"] == 20
    assert Q["disc_form"] == "O+_20(2)"


def test_both_doubly_even_and_separate() -> None:
    d = _data()
    assert d["W"]["doubly_even"] and d["Q"]["doubly_even"]
    assert d["W"]["glue_dim"] != d["Q"]["glue_dim"]
    assert d["W"]["glue_dim"] + d["Q"]["glue_dim"] == 28


def test_glue_rank_formula() -> None:
    d = _data()
    assert d["W"]["glue_dim"] == d["W"]["glue_dim_formula_n_minus_2k"]  # 40 - 2*16
    assert d["Q"]["glue_dim"] == d["Q"]["glue_dim_formula_n_minus_2k"]  # 40 - 2*10
