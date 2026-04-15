"""Pin Eisenstein series, Ramanujan tau, j-invariant, and Moonshine.

Eisenstein series of weight 2k:

    E_{2 k}(tau)  =  1  -  (4 k / B_{2 k})  sum_{n >= 1}  sigma_{2 k - 1}(n)  q^n.

Discriminant cusp form:  Delta = (E_4^3 - E_6^2) / 1728  =  sum tau(n) q^n.

Klein j-invariant:  j(tau) = E_4^3 / Delta = 1/q + 744 + 196884 q + ...

Monstrous Moonshine:  196884 = 196883 + 1,  with 196883 the smallest
non-trivial Monster simple-group irrep dimension.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_eisenstein import (  # noqa: E402
    delta_qseries,
    derive_all_modular,
    eisenstein_constant,
    eisenstein_qseries,
    j_invariant_qseries,
    moonshine_check,
    ramanujan_tau,
    sigma_k,
    verify_E4_cubed_minus_E6_squared_equals_1728_delta,
    verify_E8_equals_E4_squared,
    verify_E10_equals_E4_times_E6,
)


# ----------------------------------------------------------------------
# Divisor sums.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n,k,expected", [
    (1, 1, 1),
    (6, 1, 12),         # 1+2+3+6
    (12, 1, 28),
    (1, 3, 1),
    (2, 3, 9),          # 1 + 8
    (3, 3, 28),         # 1 + 27
    (6, 3, 252),        # 1 + 8 + 27 + 216
    (1, 5, 1),
    (2, 5, 33),         # 1 + 32
])
def test_sigma_k(n, k, expected):
    assert sigma_k(n, k) == expected


# ----------------------------------------------------------------------
# Eisenstein constants  -4k/B_{2k}.
# ----------------------------------------------------------------------
EXPECTED_EISENSTEIN_CONSTANTS = {
    2: Fraction(240),               # E_4
    3: Fraction(-504),              # E_6
    4: Fraction(480),               # E_8
    5: Fraction(-264),              # E_10
    6: Fraction(65520, 691),        # E_12
}


@pytest.mark.parametrize("k,expected", sorted(EXPECTED_EISENSTEIN_CONSTANTS.items()))
def test_eisenstein_constant(k, expected):
    assert eisenstein_constant(k) == expected


# ----------------------------------------------------------------------
# E_4 and E_6 Fourier coefficients (classical sequences).
# ----------------------------------------------------------------------
EXPECTED_E4 = [1, 240, 2160, 6720, 17520, 30240, 60480, 82560, 140400, 181680, 272160]
EXPECTED_E6 = [1, -504, -16632, -122976, -532728, -1575504, -4058208,
               -8471232, -17047800, -29883672, -51991632]


def test_E4_qseries_matches_OEIS_A004009():
    E4 = eisenstein_qseries(2, 10)
    assert [int(c) for c in E4] == EXPECTED_E4


def test_E6_qseries_matches_OEIS_A013973():
    E6 = eisenstein_qseries(3, 10)
    assert [int(c) for c in E6] == EXPECTED_E6


# ----------------------------------------------------------------------
# Ramanujan tau (OEIS A000594).
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
def test_ramanujan_tau_via_delta(n, expected):
    assert ramanujan_tau(n) == expected


def test_delta_qseries_starts_with_zero():
    D = delta_qseries(5)
    assert D[0] == 0
    assert D[1] == 1


def test_ramanujan_tau_multiplicative_at_coprime():
    # tau is multiplicative: tau(2)*tau(3) = tau(6).
    assert ramanujan_tau(2) * ramanujan_tau(3) == ramanujan_tau(6)


def test_ramanujan_tau_5_squared_minus_tau_25_relation():
    # tau is Hecke-eigen: tau(p^2) = tau(p)^2 - p^11 for prime p.
    # Cross-check at p = 2:  tau(4) = tau(2)^2 - 2^11 = 576 - 2048 = -1472.
    assert ramanujan_tau(2) ** 2 - 2 ** 11 == ramanujan_tau(4)


# ----------------------------------------------------------------------
# Modular identities (q-series level).
# ----------------------------------------------------------------------
def test_E4_cubed_minus_E6_squared_equals_1728_delta():
    assert verify_E4_cubed_minus_E6_squared_equals_1728_delta(15) is True


def test_E8_equals_E4_squared():
    assert verify_E8_equals_E4_squared(15) is True


def test_E10_equals_E4_times_E6():
    assert verify_E10_equals_E4_times_E6(15) is True


# ----------------------------------------------------------------------
# Klein j-invariant Laurent coefficients (OEIS A000521).
# ----------------------------------------------------------------------
EXPECTED_J = {
    -1: 1,
     0: 744,
     1: 196884,
     2: 21493760,
     3: 864299970,
     4: 20245856256,
     5: 333202640600,
     6: 4252023300096,
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_J.items()))
def test_j_invariant_coefficients(n, expected):
    j = j_invariant_qseries(6)
    assert j[n] == expected


# ----------------------------------------------------------------------
# Monstrous Moonshine.
# ----------------------------------------------------------------------
def test_moonshine_196884_equals_196883_plus_1():
    m = moonshine_check(order_min=2)
    assert m["j_coef_q"] == 196884
    assert m["monster_irrep_196883"] == 196883
    assert m["plus_trivial"] == 1
    assert m["match"] is True


def test_moonshine_q_squared_decomposition():
    # 21493760 = 1 + 196883 + 21296876  (sum of three smallest Monster irreps).
    j = j_invariant_qseries(2)
    assert j[2] == 1 + 196883 + 21296876


# ----------------------------------------------------------------------
# Driver dictionary structure.
# ----------------------------------------------------------------------
@pytest.fixture(scope="module")
def chain():
    return derive_all_modular(order=10)


def test_driver_has_all_constants(chain):
    consts = chain["eisenstein_constants"]
    assert consts["240 (E_4)"] == "240"
    assert consts["-504 (E_6)"] == "-504"
    assert consts["480 (E_8)"] == "480"
    assert consts["-264 (E_10)"] == "-264"
    assert consts["65520/691 (E_12)"] == "65520/691"


def test_driver_has_all_identities(chain):
    ids = chain["identities"]
    assert ids["E_4^3 - E_6^2 = 1728 Delta"] is True
    assert ids["E_8 = E_4^2"] is True
    assert ids["E_10 = E_4 E_6"] is True


def test_driver_moonshine_match(chain):
    assert chain["moonshine"]["match"] is True
    assert chain["moonshine"]["j_coef_q"] == 196884


def test_driver_ramanujan_tau_first_10(chain):
    tau = chain["ramanujan_tau"]
    for n, expected in EXPECTED_TAU.items():
        assert tau[n] == expected
