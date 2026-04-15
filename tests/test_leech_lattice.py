"""Pin Dedekind eta, the Niemeier family, and the Leech lattice.

Three layers verified:

  (1) Euler's pentagonal product  P(q) = prod (1 - q^n)  has the signs predicted
      by the pentagonal number theorem  P(q) = sum_{k in Z} (-1)^k q^{k(3k-1)/2}.

  (2) Delta computed via  eta^{24} = q * P(q)^{24}  matches Delta computed via
      (E_4^3 - E_6^2) / 1728.  The two constructions agree, giving Ramanujan
      tau two independent ways.

  (3) Solving  [q^1] (E_4^3 + beta Delta) = 0  forces beta = -720, isolating
      the Leech lattice as the unique rootless Niemeier; its minimum vector
      count is then 196560 = [q^2] (E_4^3 - 720 Delta).
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_leech_lattice import (  # noqa: E402
    derive_all_leech,
    eta_power_24_qseries,
    euler_product,
    leech_minimum_count,
    leech_no_roots,
    leech_vs_moonshine_bridge,
    niemeier_theta,
    ramanujan_tau_via_eta,
    solve_beta_for_rootless,
    theta_leech,
    verify_delta_eta_equals_delta_eisenstein,
)


# ----------------------------------------------------------------------
# Euler pentagonal product.
# ----------------------------------------------------------------------
EXPECTED_EULER = [1, -1, -1, 0, 0, 1, 0, 1, 0, 0, 0, 0, -1, 0, 0, -1]


def test_euler_product_pentagonal_signs():
    P = euler_product(15)
    assert [int(c) for c in P] == EXPECTED_EULER


def test_euler_product_q1_is_minus_1():
    """k=1 -> exponent 1 -> (-1)^1 = -1."""
    P = euler_product(5)
    assert P[1] == -1


def test_euler_product_q5_is_plus_1():
    """k=2 -> exponent 5 -> (-1)^2 = +1."""
    P = euler_product(5)
    assert P[5] == 1


# ----------------------------------------------------------------------
# Ramanujan tau via eta^24 (independent route).
# ----------------------------------------------------------------------
EXPECTED_TAU = {
    1: 1,
    2: -24,
    3: 252,
    4: -1472,
    5: 4830,
    6: -6048,
    7: -16744,
    8: 84480,
    9: -113643,
    10: -115920,
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_TAU.items()))
def test_ramanujan_tau_via_eta(n, expected):
    assert ramanujan_tau_via_eta(n) == expected


def test_eta_24_starts_with_zero_then_one():
    eta24 = eta_power_24_qseries(3)
    assert eta24[0] == 0
    assert eta24[1] == 1


# ----------------------------------------------------------------------
# The two Delta constructions agree.
# ----------------------------------------------------------------------
def test_delta_eta_matches_delta_eisenstein():
    v = verify_delta_eta_equals_delta_eisenstein(15)
    assert v["match"] is True


def test_delta_eta_matches_delta_eisenstein_higher():
    v = verify_delta_eta_equals_delta_eisenstein(25)
    assert v["match"] is True


# ----------------------------------------------------------------------
# Niemeier family beta solver.
# ----------------------------------------------------------------------
def test_solve_beta_for_rootless_is_minus_720():
    assert solve_beta_for_rootless() == Fraction(-720)


def test_E_4_cubed_q1_is_720():
    """[q^1] E_4^3 = 3 * [q^1] E_4 = 3 * 240 = 720."""
    from w33_eisenstein import eisenstein_qseries
    from w33_eisenstein import qpow
    E4 = eisenstein_qseries(2, 3)
    E4_cubed = qpow(E4, 3, 3)
    assert E4_cubed[1] == 720


# ----------------------------------------------------------------------
# Leech lattice properties.
# ----------------------------------------------------------------------
def test_leech_has_no_roots():
    assert leech_no_roots() is True


def test_leech_minimum_count_is_196560():
    assert leech_minimum_count() == 196560


def test_leech_theta_full_qseries():
    """First several coefficients of E_4^3 - 720 Delta."""
    th = theta_leech(6)
    expected = [1, 0, 196560, 16773120, 398034000, 4629381120, 34417656000]
    assert [int(c) for c in th] == expected


def test_196560_arithmetic_breakdown():
    """N_4(Leech) = [q^2] E_4^3 - 720 * tau(2) = 179280 + 17280 = 196560."""
    from w33_eisenstein import eisenstein_qseries, qpow
    E4 = eisenstein_qseries(2, 3)
    E4_cubed = qpow(E4, 3, 3)
    # [q^2] E_4^3 = 3 * [q^2] E_4 + 3 * ([q^1] E_4)^2 = 3*2160 + 3*240^2.
    assert E4_cubed[2] == 3 * 2160 + 3 * 240 ** 2
    assert E4_cubed[2] == 179280
    # tau(2) = -24, so -720 * tau(2) = +17280.
    assert E4_cubed[2] - Fraction(720) * Fraction(-24) == Fraction(196560)


# ----------------------------------------------------------------------
# Niemeier sample structure.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("beta,expected_N2", [
    (-720, 0),     # Leech
    (   0, 720),   # E_8^3
    ( 384, 1104),  # D_24
    (-672, 48),    # A_1^{24}
    (-648, 72),    # A_2^{12}
])
def test_niemeier_N2_is_720_plus_beta(beta, expected_N2):
    th = niemeier_theta(beta, 2)
    assert int(th[1]) == expected_N2
    assert int(th[1]) == 720 + beta


def test_niemeier_constant_term_always_one():
    """All Niemeier theta series have constant term 1 (only zero vector)."""
    for beta in (-720, -672, -648, 0, 384, 1000):
        th = niemeier_theta(beta, 2)
        assert th[0] == 1


# ----------------------------------------------------------------------
# Moonshine bridge structure.
# ----------------------------------------------------------------------
def test_moonshine_bridge_difference_is_324():
    bridge = leech_vs_moonshine_bridge()
    assert bridge["Leech_min_count"] == 196560
    assert bridge["j_q1_coefficient"] == 196884
    assert bridge["difference"] == 324


# ----------------------------------------------------------------------
# Driver consistency.
# ----------------------------------------------------------------------
def test_driver_chain_consistent():
    chain = derive_all_leech(order=6)
    assert chain["delta_constructions_agree"] is True
    assert chain["leech_no_roots"] is True
    assert chain["leech_minimum_count"] == 196560
    assert chain["rootless_beta_solution"] == "-720"
    for n, ok in chain["ramanujan_tau_match"].items():
        assert ok is True
