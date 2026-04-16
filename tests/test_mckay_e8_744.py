"""Pin the McKay E_8 observation and the 744 decomposition.

744 = j[0] = 720 + 24 = 3*240 + 2k = 3*|E_8 roots| + 2k
    = 3 * 248 = 3 * dim(E_8).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_mckay_e8_744 import (  # noqa: E402
    E8_AFFINE_MARKS,
    decompose_744_arithmetically,
    derive_mckay_744,
    leech_connection,
    mckay_e8_observation,
    verify_e8_affine_marks,
    verify_j_constant_is_744,
    verify_720_from_e4,
)


# ----------------------------------------------------------------------
# j[0] = 744.
# ----------------------------------------------------------------------
def test_j_constant_is_744():
    r = verify_j_constant_is_744()
    assert r["j[0]"] == 744
    assert r["j[-1]"] == 1
    assert r["is_744"] is True


# ----------------------------------------------------------------------
# 744 = 720 + 24 from E_4^3 / Delta arithmetic.
# ----------------------------------------------------------------------
def test_744_equals_720_plus_24():
    r = decompose_744_arithmetically()
    assert r["j_constant"] == 744
    assert r["E4_cubed_q1"] == 720
    assert r["inv_Delta_q0"] == 24


def test_720_is_3_times_240():
    r = decompose_744_arithmetically()
    assert r["720_is_3_times_240"] is True
    assert 3 * 240 == 720


def test_24_is_2k():
    r = decompose_744_arithmetically()
    assert r["24_is_2k"] is True
    assert 2 * 12 == 24


def test_E4_cubed_q0_is_1():
    r = decompose_744_arithmetically()
    assert r["E4_cubed_q0"] == 1


# ----------------------------------------------------------------------
# 720 from the E_4 Eisenstein constant 240.
# ----------------------------------------------------------------------
def test_E4_eisenstein_constant_is_240():
    r = verify_720_from_e4()
    assert r["E4_eisenstein_constant"] == 240
    assert r["240_is_E8_root_count"] is True


def test_3_times_240_is_720():
    r = verify_720_from_e4()
    assert r["3_times_constant"] == 720
    assert r["is_720"] is True


# ----------------------------------------------------------------------
# McKay: 744 = 3 * 248 = 3 * dim(E_8).
# ----------------------------------------------------------------------
def test_mckay_744_is_3_times_248():
    m = mckay_e8_observation()
    assert m["is_744"] is True
    assert m["3_times_E8_dim"] == 744


def test_e8_dim_is_248():
    m = mckay_e8_observation()
    assert m["E8_dim"] == 248
    assert m["E8_roots"] == 240
    assert m["E8_rank"] == 8
    assert 240 + 8 == 248


def test_744_equals_3_times_248():
    assert 3 * 248 == 744


def test_744_equals_3_times_240_plus_24():
    assert 3 * 240 + 24 == 744


# ----------------------------------------------------------------------
# Leech connection: j - 720 has constant term 24.
# ----------------------------------------------------------------------
def test_leech_constant_is_24():
    r = leech_connection()
    assert r["chi_constant"] == 24
    assert r["is_24"] is True


def test_leech_beta_is_minus_720():
    r = leech_connection()
    assert r["leech_beta"] == -720


def test_744_minus_720_is_24():
    assert 744 - 720 == 24


# ----------------------------------------------------------------------
# Extended E_8 Dynkin diagram.
# ----------------------------------------------------------------------
def test_e8_affine_marks():
    r = verify_e8_affine_marks()
    assert r["marks"] == [1, 2, 3, 4, 5, 6, 3, 4, 2]
    assert r["sum"] == 30
    assert r["num_nodes"] == 9


def test_e8_affine_marks_sum_30():
    assert sum(E8_AFFINE_MARKS) == 30


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_derive_mckay_744_all_true():
    chain = derive_mckay_744(12)
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"
