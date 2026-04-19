"""Pin Jacobi theta functional equation and Poisson summation.

Tests cover:
    (1) Period-2 invariance theta_3(tau + 2) = theta_3(tau);
    (2) Imaginary-axis inversion theta_3(i t) = (1/sqrt t) theta_3(i/t);
    (3) Full Jacobi inversion theta_3(-1/tau) = sqrt(-i tau) theta_3(tau);
    (4) Self-dual value theta_3(i) = pi^{1/4} / Gamma(3/4);
    (5) Poisson summation on Gaussians: sum exp(-sigma n^2)
        = sqrt(pi/sigma) sum exp(-pi^2 k^2/sigma);
    (6) Gamma(3/4) Gamma(1/4) = pi sqrt 2 (Euler reflection at 1/4).
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_theta_functional_equation import (  # noqa: E402
    derive_all,
    poisson_gaussian_lhs,
    poisson_gaussian_rhs,
    theta3_imag,
    theta3_tau,
    verify_general_inversion,
    verify_imaginary_inversion,
    verify_periodicity,
    verify_poisson_summation,
    verify_reflection_gamma_identity,
    verify_theta3_i_equals_closed_form,
)


# ----------------------------------------------------------------------
# theta_3 sanity.
# ----------------------------------------------------------------------
def test_theta3_at_i_positive():
    mp.mp.dps = 40
    val = theta3_imag(mp.mpf(1), N=60)
    assert val > 1.0
    assert val < 1.2


def test_theta3_large_t_limits_to_1():
    """theta_3(i t) -> 1 as t -> infinity."""
    mp.mp.dps = 40
    val = theta3_imag(mp.mpf(100), N=20)
    assert abs(val - 1) < mp.mpf("1e-100")


# ----------------------------------------------------------------------
# Period-2 invariance.
# ----------------------------------------------------------------------
def test_periodicity_at_i():
    mp.mp.dps = 40
    tau = mp.mpc(0, 1)
    assert abs(theta3_tau(tau) - theta3_tau(tau + 2)) < mp.mpf("1e-30")


def test_periodicity_verifier():
    r = verify_periodicity(dps=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Imaginary inversion.
# ----------------------------------------------------------------------
def test_inversion_at_t_1_fixed_point():
    """theta_3(i) is the fixed point of Jacobi inversion."""
    mp.mp.dps = 40
    t = mp.mpf(1)
    a = theta3_imag(t)
    b = theta3_imag(1 / t) / mp.sqrt(t)
    assert abs(a - b) < mp.mpf("1e-30")


def test_inversion_at_t_3():
    mp.mp.dps = 40
    t = mp.mpf(3)
    lhs = theta3_imag(t, N=80)
    rhs = theta3_imag(1 / t, N=80) / mp.sqrt(t)
    assert abs(lhs - rhs) < mp.mpf("1e-15")


def test_imaginary_inversion_verifier():
    r = verify_imaginary_inversion(dps=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Full Jacobi inversion.
# ----------------------------------------------------------------------
def test_general_inversion_at_2i():
    mp.mp.dps = 40
    tau = mp.mpc(0, 2)
    lhs = theta3_tau(-1 / tau)
    rhs = mp.sqrt(mp.mpc(0, -1) * tau) * theta3_tau(tau)
    assert abs(lhs - rhs) < mp.mpf("1e-15")


def test_general_inversion_verifier():
    r = verify_general_inversion(dps=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Self-dual point theta_3(i) = pi^{1/4} / Gamma(3/4).
# ----------------------------------------------------------------------
def test_theta3_i_closed_form():
    r = verify_theta3_i_equals_closed_form(dps=50)
    assert r["match"] is True


def test_theta3_i_numerical_value():
    """theta_3(i) ~ 1.086434811213308014575316121510223..."""
    mp.mp.dps = 40
    val = theta3_imag(mp.mpf(1), N=80)
    assert abs(val - mp.mpf("1.086434811213308014575316121510")) < mp.mpf("1e-25")


# ----------------------------------------------------------------------
# Poisson summation.
# ----------------------------------------------------------------------
def test_poisson_at_sigma_1():
    """sigma = 1 is the fixed point sigma = pi^2/sigma => sigma = pi."""
    mp.mp.dps = 40
    lhs = poisson_gaussian_lhs(1.0, N=80)
    rhs = poisson_gaussian_rhs(1.0, N=80)
    assert abs(lhs - rhs) < mp.mpf("1e-25")


def test_poisson_verifier():
    r = verify_poisson_summation(dps=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Gamma reflection.
# ----------------------------------------------------------------------
def test_gamma_reflection_at_one_quarter():
    """Gamma(s) Gamma(1-s) = pi / sin(pi s) at s = 1/4 gives
    Gamma(1/4) Gamma(3/4) = pi / sin(pi/4) = pi sqrt 2."""
    mp.mp.dps = 40
    lhs = mp.gamma(mp.mpf("0.25")) * mp.gamma(mp.mpf("0.75"))
    rhs = mp.pi * mp.sqrt(2)
    assert abs(lhs - rhs) < mp.mpf("1e-25")


def test_reflection_verifier():
    r = verify_reflection_gamma_identity(dps=50)
    assert r["match"] is True


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
        "periodicity",
        "imaginary_inversion",
        "general_inversion",
        "self_dual_point",
        "poisson",
        "reflection",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_six_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 6
