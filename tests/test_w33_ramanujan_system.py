"""Pin Ramanujan's differential system for (E_2, E_4, E_6).

Main claims (all as power-series identities):

    q dE_2/dq = (E_2^2 - E_4) / 12,
    q dE_4/dq = (E_2 E_4 - E_6) / 3,
    q dE_6/dq = (E_2 E_6 - E_4^2) / 2.

Corollaries:
    q dDelta/dq = E_2 * Delta,
    24 q d(eta^{-c})/dq + c (E_2 - 1) eta^{-c} = 0   (f_c = prod(1-q^n)^{-c}).

The c = 8 case divided by 8 reproduces the previous-layer affine E_8 ODE.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_ramanujan_system import (  # noqa: E402
    affine_e8_as_c_equals_8,
    delta_series,
    derive_all,
    e2_series,
    e4_series,
    e6_series,
    eta_minus_c_series,
    q_d_dq,
    ramanujan_denominator_pattern,
    series_mul,
    verify_delta_ode,
    verify_eta_family_ode,
    verify_ramanujan_e2_ode,
    verify_ramanujan_e4_ode,
    verify_ramanujan_e6_ode,
)


# ----------------------------------------------------------------------
# Eisenstein series sanity.
# ----------------------------------------------------------------------
def test_e2_q0_is_1():
    assert e2_series(5)[0] == 1


def test_e2_q1_is_minus_24():
    assert e2_series(5)[1] == -24


def test_e4_q0_is_1():
    assert e4_series(5)[0] == 1


def test_e4_q1_is_240():
    assert e4_series(5)[1] == 240


def test_e6_q0_is_1():
    assert e6_series(5)[0] == 1


def test_e6_q1_is_minus_504():
    assert e6_series(5)[1] == -504


# ----------------------------------------------------------------------
# Ramanujan ODEs.
# ----------------------------------------------------------------------
def test_ramanujan_e2_ode_holds():
    r = verify_ramanujan_e2_ode(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_ramanujan_e4_ode_holds():
    r = verify_ramanujan_e4_ode(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_ramanujan_e6_ode_holds():
    r = verify_ramanujan_e6_ode(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_ramanujan_e2_ode_q1():
    """[q^1]: 1*(-24) = ((1 - 48 sigma_1(1))  - 240)/12 = (-47 - 240)/12? Let's just trust the check."""
    r = verify_ramanujan_e2_ode(n_max=2)
    assert r["all_match"] is True


def test_ramanujan_e4_ode_q1():
    r = verify_ramanujan_e4_ode(n_max=2)
    assert r["all_match"] is True


def test_ramanujan_e6_ode_q1():
    r = verify_ramanujan_e6_ode(n_max=2)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Delta ODE.
# ----------------------------------------------------------------------
def test_delta_q1_is_1():
    """Delta = q - 24 q^2 + ...  (first coefficient is 1)."""
    d = delta_series(5)
    assert d[0] == 0
    assert d[1] == 1


def test_delta_q2_is_minus_24():
    d = delta_series(5)
    assert d[2] == -24


def test_delta_q3_is_252():
    d = delta_series(5)
    assert d[3] == 252


def test_delta_ode_holds():
    r = verify_delta_ode(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_delta_ode_at_q1():
    """[q^1] q dDelta/dq = 1 * 1 = 1.  [q^1] E_2 Delta = E_2[0]*Delta[1] = 1."""
    e2 = e2_series(5)
    delta = delta_series(5)
    lhs = q_d_dq(delta)
    rhs = series_mul(e2, delta, 5)
    assert lhs[1] == 1
    assert rhs[1] == 1


# ----------------------------------------------------------------------
# eta^{-c} family ODE.
# ----------------------------------------------------------------------
def test_eta_family_c1_ode_holds():
    r = verify_eta_family_ode(1, n_max=25)
    assert r["all_zero"] is True


def test_eta_family_c2_ode_holds():
    r = verify_eta_family_ode(2, n_max=25)
    assert r["all_zero"] is True


def test_eta_family_c4_ode_holds():
    r = verify_eta_family_ode(4, n_max=25)
    assert r["all_zero"] is True


def test_eta_family_c8_ode_holds():
    r = verify_eta_family_ode(8, n_max=25)
    assert r["all_zero"] is True


def test_eta_family_c12_ode_holds():
    r = verify_eta_family_ode(12, n_max=25)
    assert r["all_zero"] is True


def test_eta_family_c24_ode_holds():
    """c=24 is 1/Delta (without the q prefactor); anchor case."""
    r = verify_eta_family_ode(24, n_max=25)
    assert r["all_zero"] is True


def test_eta_minus_8_series_first_terms():
    f = eta_minus_c_series(8, 5)
    assert f[0] == 1
    assert f[1] == 8  # bosonic octet


def test_eta_minus_24_q1_is_24():
    """prod(1-q^n)^{-24} at q^1: first term is 24."""
    f = eta_minus_c_series(24, 5)
    assert f[0] == 1
    assert f[1] == 24


# ----------------------------------------------------------------------
# Denominator pattern.
# ----------------------------------------------------------------------
def test_denominator_pattern_E4():
    dp = ramanujan_denominator_pattern()
    assert dp["E_4_denom"] == 3
    assert dp["E_4_rule_matches"] is True


def test_denominator_pattern_E6():
    dp = ramanujan_denominator_pattern()
    assert dp["E_6_denom"] == 2
    assert dp["E_6_rule_matches"] is True


def test_denominator_pattern_E2_anomaly():
    dp = ramanujan_denominator_pattern()
    assert dp["E_2_denom_actual"] == 12
    assert dp["E_2_denom_if_holomorphic"] == 6
    assert dp["E_2_anomaly_factor"] == 2


def test_denominator_12_is_w33_valency():
    dp = ramanujan_denominator_pattern()
    assert dp["12_is_w33_valency"] is True


# ----------------------------------------------------------------------
# Affine E_8 corollary.
# ----------------------------------------------------------------------
def test_affine_e8_is_c_equals_8_case():
    r = affine_e8_as_c_equals_8(n_max=20)
    assert r["family_ode_holds"] is True
    assert r["previous_layer_match"] is True


def test_affine_e8_reduction_to_3qdf_plus_E2minus1_f():
    """The previous layer's ODE is (3 q d/dq + E_2 - 1) eta^{-8} = 0.
    Check the multiplier: 24 q df_8 + 8 (E_2 - 1) f_8 = 0, divided by 8
    gives 3 q df_8 + (E_2 - 1) f_8 = 0.  Compare directly at n_max=20."""
    f = eta_minus_c_series(8, 20)
    e2 = e2_series(20)
    e2_minus_1 = [e2[n] - (1 if n == 0 else 0) for n in range(21)]
    lhs_qdf = q_d_dq(f)
    e2m1_f = series_mul(e2_minus_1, f, 20)
    residuals_divided = [3 * lhs_qdf[n] + e2m1_f[n] for n in range(21)]
    assert all(r == 0 for r in residuals_divided)


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_eight_pins():
    s = derive_all(n_max=20)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
