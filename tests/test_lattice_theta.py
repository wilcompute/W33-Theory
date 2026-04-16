"""Tests for the lattice theta exploration (E8 and Leech)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_lattice_theta import (
    derive_all_lattice_theta,
    verify_e8_theta_equals_e4,
    verify_leech_theta,
)


def test_e8_theta_equals_e4_small():
    r = verify_e8_theta_equals_e4(n_max=3)
    assert r["all_match"] is True
    assert r["q1_is_240_roots"] is True


def test_leech_theta_pins_kissing():
    r = verify_leech_theta(n_max=4)
    assert r["kissing_number_196560"] is True
    assert r["constant_term_is_1"] is True


def test_driver_chain_all_true():
    chain = derive_all_lattice_theta(n_max=3)
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"
