"""Pin the Jacobi triple product and its three classical specialisations.

    prod (1 - q^{2n})(1 + q^{2n-1} z)(1 + q^{2n-1} z^{-1}) = sum_{k in Z} q^{k^2} z^k

specialises to:
 (a) Euler pentagonal theorem: prod (1 - q^n) = sum (-1)^k q^{k(3k-1)/2}
 (b) Triangular theta at z = q
 (c) Jacobi four-squares theorem: theta_3^4 = 1 + 8 sum sigma_1^{(4)}(n) q^n
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_jacobi_triple import (  # noqa: E402
    derive_all_jacobi,
    jacobi_lhs,
    jacobi_rhs,
    pentagonal_from_jacobi_check,
    r4_jacobi,
    theta3,
    theta3_to_the_4,
    triangular_theta,
    verify_jacobi_triple,
    verify_r4,
    verify_triangular_identity,
)


# ----------------------------------------------------------------------
# Jacobi triple product itself.
# ----------------------------------------------------------------------
def test_jacobi_triple_matches_small_order():
    r = verify_jacobi_triple(q_order=15, z_range=4)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_jacobi_triple_matches_larger_order():
    r = verify_jacobi_triple(q_order=25, z_range=5)
    assert r["all_match"] is True


def test_jacobi_z0_row_is_theta3():
    """[z^0] LHS should equal the q-series of theta_3 with only even powers hit,
    but actually z^0 row of Jacobi RHS is sum_{k=0} q^0 = 1 (only k=0)."""
    r = verify_jacobi_triple(q_order=10, z_range=3)
    # z^0 row picks up k=0 only -> [1, 0, 0, ...]
    lhs_k0 = jacobi_lhs(10, 3).get(0, [])
    assert lhs_k0[0] == 1
    assert lhs_k0[1:] == [0] * (len(lhs_k0) - 1)


def test_jacobi_z1_row_has_q_at_exponent_1():
    """[z^1] RHS = q^{1^2} = q.  LHS must agree."""
    lhs_k1 = jacobi_lhs(10, 3).get(1, [])
    assert lhs_k1[0] == 0
    assert lhs_k1[1] == 1
    # All other entries zero
    assert lhs_k1[2:] == [0] * (len(lhs_k1) - 2)


def test_jacobi_z_minus_1_row_has_q_at_exponent_1():
    """[z^{-1}] RHS = q^{(-1)^2} = q."""
    lhs_km1 = jacobi_lhs(10, 3).get(-1, [])
    assert lhs_km1[0] == 0
    assert lhs_km1[1] == 1


def test_jacobi_z2_row_has_q4():
    """[z^2] RHS = q^{4}."""
    lhs_k2 = jacobi_lhs(10, 3).get(2, [])
    assert lhs_k2[4] == 1
    for i, c in enumerate(lhs_k2):
        if i != 4:
            assert c == 0


def test_jacobi_rhs_direct():
    r = jacobi_rhs(q_order=16, z_range=4)
    assert r[0][0] == 1
    assert r[1][1] == 1
    assert r[2][4] == 1
    assert r[-2][4] == 1
    assert r[3][9] == 1
    assert r[-4][16] == 1


# ----------------------------------------------------------------------
# (a) Pentagonal specialisation.
# ----------------------------------------------------------------------
def test_pentagonal_from_jacobi():
    r = pentagonal_from_jacobi_check(q_order=25)
    assert r["all_match"] is True


def test_pentagonal_coefficients_explicit():
    r = pentagonal_from_jacobi_check(q_order=20)
    # prod (1-q^n) known: 1, -1, -1, 0, 0, 1, 0, 1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1
    expected = [1, -1, -1, 0, 0, 1, 0, 1, 0, 0, 0, 0, -1, 0, 0, -1]
    assert r["prod"][:16] == expected
    assert r["pentagon"][:16] == expected


# ----------------------------------------------------------------------
# (b) Triangular theta specialisation at z = q.
# ----------------------------------------------------------------------
def test_triangular_identity_passes():
    r = verify_triangular_identity(q_order=30)
    assert r["all_match"] is True


def test_triangular_theta_small():
    t = triangular_theta(10)
    # T_0=0, T_1=1, T_2=3, T_3=6, T_4=10
    expected = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1]
    assert t == expected


# ----------------------------------------------------------------------
# (c) Four-squares theorem.
# ----------------------------------------------------------------------
def test_theta3_first_coefs():
    t = theta3(16)
    # 1 + 2q + 2q^4 + 2q^9 + 2q^16
    expected = [1, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2]
    assert t == expected


def test_r4_of_0_is_1():
    assert r4_jacobi(0) == 1


def test_r4_of_1_is_8():
    """r_4(1) = 8: (+/-1, 0, 0, 0) in 4 positions, each with 2 signs = 8."""
    assert r4_jacobi(1) == 8


def test_r4_of_2_is_24():
    assert r4_jacobi(2) == 24


def test_r4_of_3_is_32():
    assert r4_jacobi(3) == 32


def test_r4_of_4_is_24():
    """Note r_4(4) = 24, not 32 (the divisor 4 is excluded)."""
    assert r4_jacobi(4) == 24


def test_r4_matches_theta3_fourth_power():
    r = verify_r4(q_order=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


@pytest.mark.parametrize("n,expected", [
    (0, 1), (1, 8), (2, 24), (3, 32), (4, 24),
    (5, 48), (6, 96), (7, 64), (8, 24), (9, 104), (10, 144),
])
def test_r4_explicit(n, expected):
    assert r4_jacobi(n) == expected


def test_theta3_4_explicit_values():
    t4 = theta3_to_the_4(10)
    assert t4[0] == 1
    assert t4[1] == 8
    assert t4[2] == 24
    assert t4[3] == 32
    assert t4[4] == 24


def test_r4_for_odd_n_equals_8_sigma():
    """For odd n, the 4-does-not-divide-d restriction is vacuous, so r_4(n) = 8 sigma_1(n)."""
    for n in [1, 3, 5, 7, 9, 11, 13, 15]:
        sigma = sum(d for d in range(1, n + 1) if n % d == 0)
        assert r4_jacobi(n) == 8 * sigma


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_chain_all_true():
    chain = derive_all_jacobi(q_order=25)
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"
