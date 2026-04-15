"""Pin the E_8 root lattice and its theta series.

E_8 is even unimodular of rank 8 with 240 minimum vectors (roots).
Its theta series equals the unique weight-4 holomorphic Eisenstein form:

    theta_{E_8}(tau)  =  E_4(tau)  =  1 + 240 q + 2160 q^2 + 6720 q^3 + ...

This test pins both the brute-force lattice enumeration AND the Jacobi-theta
formula  theta_{E_8} = (theta_2^8 + theta_3^8 + theta_4^8) / 2,  and verifies
they agree with E_4 from w33_eisenstein.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_e8_lattice import (  # noqa: E402
    E8_decomposition_chain,
    E8_roots,
    E8_W33_bridge,
    derive_all_E8,
    enumerate_E8_by_norm_squared,
    jacobi_theta2_in_s,
    jacobi_theta3_in_s,
    jacobi_theta4_in_s,
    theta_E8_qseries,
    verify_240_roots_brute,
    verify_2160_norm_4,
    verify_theta_E8_equals_E4,
)


# ----------------------------------------------------------------------
# Brute-force lattice counts.
# ----------------------------------------------------------------------
def test_240_roots_in_E8():
    counts = enumerate_E8_by_norm_squared(2)
    assert counts[2] == 240


def test_only_origin_at_norm_zero():
    counts = enumerate_E8_by_norm_squared(2)
    assert counts[0] == 1


def test_no_E8_vector_of_squared_norm_one():
    """E_8 is even, so |v|^2 is always even. No vectors at norm^2=1."""
    counts = enumerate_E8_by_norm_squared(2)
    assert counts[1] == 0


def test_2160_at_norm_squared_4():
    nb = verify_2160_norm_4()
    assert nb["count"] == 2160
    assert nb["match"] is True


def test_explicit_root_split_112_plus_128():
    rb = verify_240_roots_brute()
    assert rb["D_8_roots"] == 112
    assert rb["coset_roots"] == 128
    assert rb["explicit_root_total"] == 240
    assert rb["match"] is True


def test_E8_roots_all_have_squared_norm_2():
    roots = E8_roots()
    for v in roots:
        sq = sum(Fraction(x) ** 2 for x in v)
        assert sq == Fraction(2), f"root {v} has wrong norm {sq}"


def test_E8_roots_no_duplicates():
    roots = E8_roots()
    assert len(set(roots)) == 240


# ----------------------------------------------------------------------
# Jacobi theta building blocks.
# ----------------------------------------------------------------------
def test_jacobi_theta3_starts_1_2():
    """theta_3(tau) = 1 + 2 q^{1/2} + 2 q^2 + ...   In s = q^{1/8}: 1 + 2 s^4 + 2 s^16 + ..."""
    t3 = jacobi_theta3_in_s(20)
    assert t3[0] == 1
    assert t3[4] == 2     # n=1
    assert t3[16] == 2    # n=2


def test_jacobi_theta4_alternates_sign():
    t4 = jacobi_theta4_in_s(20)
    assert t4[0] == 1
    assert t4[4] == -2    # n=1, sign -1
    assert t4[16] == 2    # n=2, sign +1


def test_jacobi_theta2_starts_at_s1():
    """theta_2 in s = q^{1/8}:  2 s^1 + 2 s^9 + 2 s^25 + ..."""
    t2 = jacobi_theta2_in_s(30)
    assert t2[1] == 2
    assert t2[9] == 2
    assert t2[25] == 2
    assert t2[0] == 0


# ----------------------------------------------------------------------
# theta_{E_8} via Jacobi.
# ----------------------------------------------------------------------
EXPECTED_THETA_E8 = [1, 240, 2160, 6720, 17520, 30240, 60480]


@pytest.mark.parametrize("n,expected", list(enumerate(EXPECTED_THETA_E8)))
def test_theta_E8_coefficient(n, expected):
    theta = theta_E8_qseries(6)
    assert theta[n] == expected


def test_theta_E8_equals_E4_qseries():
    v = verify_theta_E8_equals_E4(order=6)
    assert v["match"] is True
    assert v["theta_E8"] == v["E_4"]


def test_theta_E8_equals_E4_higher_order():
    v = verify_theta_E8_equals_E4(order=10)
    assert v["match"] is True


# ----------------------------------------------------------------------
# Brute force matches the formula at low orders.
# ----------------------------------------------------------------------
def test_brute_force_matches_jacobi_at_order_2():
    counts = enumerate_E8_by_norm_squared(4)
    theta = theta_E8_qseries(2)
    # theta[k] is # of vectors with |v|^2 = 2k.
    assert counts[0] == theta[0]
    assert counts[2] == theta[1]
    assert counts[4] == theta[2]


# ----------------------------------------------------------------------
# E_8 -> SM and W(3,3) bridge structure.
# ----------------------------------------------------------------------
def test_E8_adjoint_is_248():
    chain = E8_decomposition_chain()
    assert chain["E_8"]["adjoint_dim"] == 248
    assert chain["E_8"]["rank"] == 8


def test_W33_bridge_240_equals_6_times_40():
    bridge = E8_W33_bridge()
    assert bridge["E_8_roots"] == 240
    assert bridge["W(3,3)_v_x_6"]["v"] == 40
    assert bridge["W(3,3)_v_x_6"]["6 v"] == 240
    assert bridge["E_6_27_dim"] == 27


# ----------------------------------------------------------------------
# Driver consistency.
# ----------------------------------------------------------------------
def test_derive_all_E8_consistent():
    chain = derive_all_E8(order=5)
    assert chain["rank"] == 8
    assert chain["number_of_roots"] == 240
    assert chain["matches_E_4"]["match"] is True
    assert chain["norm_2_brute"]["match"] is True
    assert chain["norm_4_brute"]["match"] is True
    assert chain["theta_E8_qseries"][:6] == [1, 240, 2160, 6720, 17520, 30240]
