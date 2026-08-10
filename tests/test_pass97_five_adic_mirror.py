"""Pytest suite for Pass 97 -- the 5-adic mirror (why E8 lives at p=2)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass97_five_adic_mirror as mod

    mod.main()
    return json.loads(Path("w33_pass97_five_adic_mirror.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_critical_order_two_primes() -> None:
    o = _data()["critical_group_order"]
    assert o["two_part"] == 81
    assert o["five_part"] == 23
    assert o["only_2_and_5"] is True


def test_bad_primes() -> None:
    assert _data()["ducey_bad_primes_p_div_rs"] == [2, 3]


def test_five_part_elementary() -> None:
    d = _data()
    p = d["parameters"]
    assert (p["r_minus_s"]) % 5 != 0  # 5 is a good prime
    assert (p["k_minus_r"]) % 5 == 0 and (p["k_minus_r"]) % 25 != 0  # 5 || k-r
    assert d["critical_group_order"]["five_part"] == 24 - 1  # (Z/5)^{f-1}


def test_mod5_jordan_block() -> None:
    j = _data()["mod5_jordan"]
    assert j["nullity_A_2I"] == 24
    assert j["nullity_A_2I_squared"] == 25
    assert j["one_size2_jordan_block"] is True
