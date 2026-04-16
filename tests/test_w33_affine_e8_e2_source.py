"""Pin the E_2-source derivation of the affine E8 cumulative regime.

Main claim: (3 q d/dq + E_2 - 1) * eta^{-8} = 0 as a power series, and
its [q^n] coefficient is exactly the recurrence  n a_n = 8 sum sigma_1(m) a_{n-m}.

Structural closure at q^11:
    [q^11] eta^-8 = 2 dim(E_8) * sigma_3(k) + D_bosonic * tau(3) + |V(W33)|
                  = 496 * 2044 + 26 * 252 + 40.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_affine_e8_e2_source import (  # noqa: E402
    bridge_q11_closure,
    derive_all,
    e2_coefficients,
    eta_minus_8_coefficients,
    packet_weights,
    quasi_modular_anomaly,
    sigma1,
    verify_e2_ode,
    verify_recurrence_from_ode,
)


# ----------------------------------------------------------------------
# E_2 coefficients.
# ----------------------------------------------------------------------
def test_e2_constant_is_1():
    e2 = e2_coefficients(5)
    assert e2[0] == 1


def test_e2_q1_is_minus_24():
    e2 = e2_coefficients(5)
    assert e2[1] == -24


def test_e2_q2_is_minus_72():
    e2 = e2_coefficients(5)
    assert e2[2] == -72


def test_e2_qm_equals_minus_24_sigma1_m():
    e2 = e2_coefficients(10)
    for m in range(1, 11):
        assert e2[m] == -24 * sigma1(m)


# ----------------------------------------------------------------------
# The source ODE:  3 q f' + (E_2 - 1) f = 0  for  f = eta^{-8}.
# ----------------------------------------------------------------------
def test_ode_all_residuals_zero():
    r = verify_e2_ode(n_max=25)
    assert r["all_zero"] is True
    assert all(x == 0 for x in r["residuals"])


def test_ode_zero_at_q0():
    r = verify_e2_ode(n_max=5)
    # 3 * 0 * f[0] + (E_2[0] - 1) * f[0] = 0 trivially.
    assert r["residuals"][0] == 0


def test_ode_zero_at_q1():
    r = verify_e2_ode(n_max=5)
    assert r["residuals"][1] == 0


# ----------------------------------------------------------------------
# The recurrence is EXACTLY the ODE read in q-coefficients.
# ----------------------------------------------------------------------
def test_recurrence_matches_ode():
    r = verify_recurrence_from_ode(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_eta_minus_8_q0_is_1():
    f = eta_minus_8_coefficients(5)
    assert f[0] == 1


def test_eta_minus_8_q1_is_8():
    """n a_n at n=1: 1*a_1 = 8 sigma_1(1) a_0 = 8.  So a_1 = 8."""
    f = eta_minus_8_coefficients(5)
    assert f[1] == 8


# ----------------------------------------------------------------------
# Packet weights = -[q^m] E_2 / 3 = 8 sigma_1(m).
# ----------------------------------------------------------------------
def test_packet_weights_first_four():
    pw = packet_weights(m_max=4)
    assert pw["first_15"] == [8, 24, 32, 56]


def test_packet_weights_match_e2_divided_by_3():
    pw = packet_weights(m_max=15)
    for w in pw["weights"]:
        assert w["matches"] is True


def test_packet_weight_m1_is_8_bosonic_octet():
    pw = packet_weights(m_max=1)
    assert pw["first_15"][0] == 8


def test_packet_weight_m2_is_24():
    pw = packet_weights(m_max=2)
    assert pw["first_15"][1] == 24


def test_packet_weight_m3_is_32_Spin10():
    pw = packet_weights(m_max=3)
    assert pw["first_15"][2] == 32


def test_packet_weight_m4_is_56_E7_fundamental():
    pw = packet_weights(m_max=4)
    assert pw["first_15"][3] == 56


# ----------------------------------------------------------------------
# Structural q^11 closure.
# ----------------------------------------------------------------------
def test_q11_structural_closure_matches():
    br = bridge_q11_closure()
    assert br["match"] is True


def test_q11_coefficients_are_named():
    br = bridge_q11_closure()
    assert br["2_dim_E8"] == 496
    assert br["D_bosonic_2k+2"] == 26
    assert br["|V(W33)|"] == 40
    assert br["sigma_3(12)"] == 2044
    assert br["tau(3)"] == 252


def test_q11_computed_explicit():
    br = bridge_q11_closure()
    assert br["computed"] == 496 * 2044 + 26 * 252 + 40


def test_q11_matches_eta_minus_8_at_q11():
    br = bridge_q11_closure()
    assert br["computed"] == br["eta_minus_8_11"]


# ----------------------------------------------------------------------
# Quasi-modular role of E_2.
# ----------------------------------------------------------------------
def test_e2_shift_coefficient_is_k_equals_12():
    qm = quasi_modular_anomaly()
    assert qm["shift_coefficient"] == 12
    assert qm["shift_coefficient_is_k"] is True


def test_e2_rank_in_holomorphic_ring_is_0():
    qm = quasi_modular_anomaly()
    assert qm["rank_in_M_star"] == 0


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_four_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
