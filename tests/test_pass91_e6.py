"""Pytest suite for Pass 91 -- Aut(W(3,3)) is the Weyl group of E6."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass91_e6 as mod

    mod.main()
    return json.loads(Path("w33_pass91_e6.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_aut_is_weyl_group_of_E6() -> None:
    d = _data()
    assert d["aut_order"] == 51840  # = |W(E6)| = |Sp(4,3)|
    assert d["WE6"]["order"] == 51840
    assert d["Aut_W_isomorphic_to_WE6"] is True  # GAP IsomorphismGroups succeeds


def test_derived_is_simple_PSp43() -> None:
    der = _data()["derived"]
    assert der["order"] == 25920  # simple PSp(4,3) = PSU(4,2) = P.Omega_6^-(2)
    assert der["simple"] is True
    assert der["index_in_aut"] == 2  # Aut(W) = PSp(4,3):2
    assert "S(4,3)" in der["name"] and "U(4,2)" in der["name"]


def test_e6_configuration_threads_the_tower() -> None:
    cfg = _data()["e6_configuration"]
    assert "tritangent planes" in cfg["45"]  # = 45 min-weight codewords (Pass 85)
    assert "E8" in cfg["240"]  # dual code min-weight words (Pass 86)
    assert cfg["78"].startswith("dim E6")  # Ihara amplitude (Pass 74)
