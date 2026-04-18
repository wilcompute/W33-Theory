"""Pin the classical modular polynomial Phi_2(X, Y).

Tests cover:
    (1) Integer vanishing Phi_2(1728, 287496) = 0 and Phi_2(0, 54000) = 0;
    (2) Symmetry Phi_2(X, Y) = Phi_2(Y, X) at integer test points;
    (3) Numerical Phi_2(j(tau), j(2 tau)) = 0 at tau = i;
    (4) Same identity at Heegner taus for d in {3, 7, 11, 19};
    (5) Coefficient prime factorizations:
            1488            = 2^4 . 3 . 31
            162000          = 2^4 . 3^4 . 5^3
            40773375        = 3^4 . 5^3 . 4027
            8748000000      = 2^8 . 3^7 . 5^6
            157464000000000 = 2^12 . 3^9 . 5^9.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_modular_polynomial_phi2 import (  # noqa: E402
    derive_all,
    phi_2,
    phi_2_symmetric,
    verify_coefficient_factorizations,
    verify_phi2_at_heegner_pairs,
    verify_phi2_at_tau_i,
    verify_phi2_integer_vanishing_at_0_54000,
    verify_phi2_integer_vanishing_at_j_i_j_2i,
    verify_phi2_symmetric_at_integer_pairs,
)


# ----------------------------------------------------------------------
# Integer vanishing.
# ----------------------------------------------------------------------
def test_phi2_integer_vanishing_at_1728_287496():
    """j(i) = 1728, j(2i) = 287496, Phi_2 vanishes exactly in Z."""
    assert phi_2(1728, 287496) == 0


def test_phi2_integer_vanishing_at_0_54000():
    """j(rho) = 0, j(2 rho) = 54000 = 30^3 * 2, Phi_2(0, 54000) = 0."""
    assert phi_2(0, 54000) == 0


def test_phi2_vanishing_by_duality_swapped_args():
    """Phi_2(287496, 1728) = 0 = Phi_2(1728, 287496) by symmetry."""
    assert phi_2(287496, 1728) == 0
    assert phi_2(54000, 0) == 0


def test_integer_vanishing_1728_verifier():
    r = verify_phi2_integer_vanishing_at_j_i_j_2i()
    assert r["equals_zero"] is True


def test_integer_vanishing_0_54000_verifier():
    r = verify_phi2_integer_vanishing_at_0_54000()
    assert r["equals_zero"] is True


# ----------------------------------------------------------------------
# Symmetry.
# ----------------------------------------------------------------------
def test_phi2_symmetric_at_1_2():
    assert phi_2_symmetric(1, 2) is True


def test_phi2_symmetric_at_100_3():
    assert phi_2_symmetric(100, 3) is True


def test_phi2_symmetric_at_minus_5280_1728():
    """-5280 = -j(-12)/... (negative example) paired with j(i)."""
    assert phi_2_symmetric(-5280, 1728) is True


def test_phi2_symmetric_verifier_all_pairs():
    r = verify_phi2_symmetric_at_integer_pairs()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Direct polynomial form — degree checks.
# ----------------------------------------------------------------------
def test_phi2_degree_3_in_each_variable():
    """Phi_2(X, 0) = X^3 - 162000 X^2 + 8748000000 X - 157464000000000,
    a cubic in X."""
    # Evaluate at Y=0 and verify matches expected cubic.
    val_at_X = lambda X: (X ** 3 - 162000 * X ** 2
                           + 8748000000 * X
                           - 157464000000000)
    for X in [0, 1, 1728, -100, 54000]:
        assert phi_2(X, 0) == val_at_X(X)


def test_phi2_constant_term():
    """Phi_2(0, 0) = -157464000000000 = -2^12 * 3^9 * 5^9."""
    assert phi_2(0, 0) == -157464000000000
    assert phi_2(0, 0) == -(2 ** 12 * 3 ** 9 * 5 ** 9)


def test_phi2_is_antidiagonal_cross_term():
    """The -X^2 Y^2 term dominates at large simultaneous X=Y=N."""
    N = 10 ** 5
    v = phi_2(N, N)
    # Leading behaviour: 2 N^3 - N^4 + 2 * 1488 N^3 + ... dominated by - N^4
    assert v < 0


# ----------------------------------------------------------------------
# Coefficient factorizations.
# ----------------------------------------------------------------------
def test_factorization_1488():
    assert 2 ** 4 * 3 * 31 == 1488


def test_factorization_162000():
    assert 2 ** 4 * 3 ** 4 * 5 ** 3 == 162000


def test_factorization_40773375():
    assert 3 ** 4 * 5 ** 3 * 4027 == 40773375


def test_factorization_8748000000():
    assert 2 ** 8 * 3 ** 7 * 5 ** 6 == 8748000000


def test_factorization_157464000000000():
    assert 2 ** 12 * 3 ** 9 * 5 ** 9 == 157464000000000


def test_factorization_verifier():
    r = verify_coefficient_factorizations()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Numerical vanishing.
# ----------------------------------------------------------------------
def test_phi2_at_tau_i_numerical():
    r = verify_phi2_at_tau_i(dps=50)
    assert r["match"] is True


def test_phi2_at_heegner_d_3_7_11_19():
    r = verify_phi2_at_heegner_pairs(dps=60)
    assert r["all_match"] is True


def test_phi2_heegner_has_at_least_4_rows():
    r = verify_phi2_at_heegner_pairs(dps=60)
    assert len(r["rows"]) >= 4


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_subresults():
    s = derive_all()
    for key in [
        "at_tau_i",
        "at_heegner_pairs",
        "symmetry",
        "zero_1728_287496",
        "zero_0_54000",
        "factorizations",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_six_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 6
