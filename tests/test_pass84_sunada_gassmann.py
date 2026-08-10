"""Pytest suite for Pass 84 -- W(3,3)/Q(4,3) as a Sunada-Gassmann pair."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass84_sunada_gassmann as mod

    mod.main()
    return json.loads(Path("w33_pass84_sunada_gassmann.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_identical_ihara_zeta() -> None:
    t1 = _data()["T1_ihara"]
    assert t1["identical"] is True
    assert t1["N_m_W"] == t1["N_m_Q"]
    assert t1["N_m_W"]["3"] == 960  # both graphs, cross-checks Pass 73


def test_identical_spectral_zeta_special_values() -> None:
    t2 = _data()["T2_spectral_zeta"]
    assert t2["identical"] is True
    sv = t2["special_values"]
    assert sv["zeta_L(0)"] == 39  # n - 1
    assert sv["zeta_L(-1)"] == 480  # 2m
    assert sv["det_prime_L"] == sv["n_times_kappa"]


def test_same_class_number_different_class_group() -> None:
    t3 = _data()["T3_class_group"]
    assert t3["class_number_kappa"] == (2**81) * (5**23)
    assert t3["same_class_number"] is True
    assert t3["different_class_group"] is True
    assert t3["K_W"] != t3["K_Q"]


def test_all_checks_pass() -> None:
    assert all(_data()["checks"].values())
