"""Pytest suite for Pass 95 -- genus and Minkowski-Siegel mass of the W(3,3) code-lattice."""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass95_genus_mass as mod

    mod.main()
    return json.loads(Path("w33_pass95_genus_mass.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_mass_routine_validated() -> None:
    import w33_pass95_genus_mass as mod

    assert mod.std_mass(8) == Fraction(1, 696729600)  # E8
    assert mod.std_mass(24) == Fraction(
        1027637932586061520960267, 129477933340026851560636148613120000000
    )  # Conway-Sloane dim-24


def test_aut_lower_bound() -> None:
    a = _data()["aut_lower_bound"]
    assert a["value"] == 2**40 * 51840
    assert a["value"] == 56998682783907840


def test_genus_symbol() -> None:
    d = _data()
    assert d["lattice"]["determinant"] == "2^8"
    assert d["lattice"]["discriminant_form"].startswith("O+_8(2)")
    assert "2^{+8}" in d["genus_symbol"]


def test_dim40_mass_astronomical() -> None:
    approx = float(_data()["mass"]["dim40_reference"])
    assert approx > 1e40
