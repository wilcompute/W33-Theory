"""Pytest suite for Pass 83 -- graph analytic class number formula for W(3,3)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass83_class_number_formula as mod

    mod.main()
    return json.loads(Path("w33_pass83_class_number_formula.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_order_of_vanishing_is_first_betti() -> None:
    d = _data()
    assert d["graph"]["first_betti"] == 201  # m - n + 1 = 240 - 40 + 1
    assert d["order_of_vanishing_at_u1"] == 201


def test_class_number_is_spanning_trees_and_critical_group_order() -> None:
    d = _data()
    assert d["class_number_kappa"] == (2**81) * (5**23)
    assert d["kappa_factored"] == "2^81*5^23"
    assert d["kappa_equals_critical_group_order"] is True


def test_class_number_formula_special_values() -> None:
    d = _data()
    kappa = d["class_number_kappa"]
    # reduced (topology-free) special value = -(q-1)*n*kappa = -400*kappa
    assert d["reduced_special_value"] == -400 * kappa
    # full leading coefficient = 2^(m-n)*(1-q)*n*kappa = -2^200 * 400 * kappa
    assert d["full_special_value"] == (2**200) * (1 - 11) * 40 * kappa
    assert d["full_special_value_factored"] == "-2^285*5^25"


def test_all_checks_pass() -> None:
    assert all(_data()["checks"].values())
