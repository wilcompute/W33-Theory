"""Pin the j-invariant layer.

Main integer-series claims:

    J_tilde := q * j = E_4^3 / prod(1-q^n)^24,
    J_tilde * prod(1-q^n)^24 = E_4^3                 (definition),
    (E_4 * prod(1-q^n)^{-8})^3 = J_tilde              (affine E_8 cube),
    E_4 * q * dJ_tilde/dq = J_tilde * (E_4 - E_6)     (j-ODE),
    E_4 * q * dJ_inv/dq = E_6 * J_inv                 (inverse j-ODE).

Moonshine seed: J_tilde = 1 + 744 q + 196884 q^2 + 21493760 q^3 + ...
Klein: j(i) = 1728 = 12^3 = k^3.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_j_invariant import (  # noqa: E402
    derive_all,
    eta_negative_power_series,
    eta_positive_power_series,
    j_inv_series,
    j_tilde_series,
    klein_discriminant_constants,
    monster_moonshine_seed,
    verify_affine_e8_cube,
    verify_j_definition,
    verify_j_inv_ode,
    verify_j_ode,
    verify_j_times_j_inv_equals_q,
)
from w33_ramanujan_system import (  # noqa: E402
    delta_series,
    e4_series,
    series_mul,
)


# ----------------------------------------------------------------------
# J_tilde = q*j coefficients.
# ----------------------------------------------------------------------
def test_j_tilde_q0_is_1():
    jt = j_tilde_series(5)
    assert jt[0] == 1


def test_j_tilde_q1_is_744():
    jt = j_tilde_series(5)
    assert jt[1] == 744


def test_j_tilde_q2_is_196884():
    jt = j_tilde_series(5)
    assert jt[2] == 196884


def test_j_tilde_q3_is_21493760():
    jt = j_tilde_series(5)
    assert jt[3] == 21493760


# ----------------------------------------------------------------------
# (I) J_tilde * g_24 = E_4^3.
# ----------------------------------------------------------------------
def test_j_definition_holds():
    r = verify_j_definition(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_j_definition_q0():
    jt = j_tilde_series(3)
    g24 = eta_positive_power_series(24, 3)
    e4 = e4_series(3)
    e4_cubed = series_mul(series_mul(e4, e4, 3), e4, 3)
    lhs = series_mul(jt, g24, 3)
    assert lhs[0] == e4_cubed[0] == 1


def test_j_definition_q1_is_720():
    """E_4^3[1] = 3 * E_4[1] = 720."""
    jt = j_tilde_series(3)
    g24 = eta_positive_power_series(24, 3)
    lhs = series_mul(jt, g24, 3)
    assert lhs[1] == 720


# ----------------------------------------------------------------------
# (II) (E_4 * f_8)^3 = J_tilde.
# ----------------------------------------------------------------------
def test_affine_e8_cube_holds():
    r = verify_affine_e8_cube(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_affine_e8_cube_q0_is_1():
    f8 = eta_negative_power_series(8, 3)
    e4 = e4_series(3)
    base = series_mul(e4, f8, 3)
    cube = series_mul(series_mul(base, base, 3), base, 3)
    assert cube[0] == 1


def test_affine_e8_cube_q1_is_744():
    f8 = eta_negative_power_series(8, 3)
    e4 = e4_series(3)
    base = series_mul(e4, f8, 3)
    cube = series_mul(series_mul(base, base, 3), base, 3)
    assert cube[1] == 744


def test_affine_e8_cube_q2_is_196884_moonshine():
    """The Monster moonshine coefficient lives inside the affine E_8 cube."""
    f8 = eta_negative_power_series(8, 3)
    e4 = e4_series(3)
    base = series_mul(e4, f8, 3)
    cube = series_mul(series_mul(base, base, 3), base, 3)
    assert cube[2] == 196884


# ----------------------------------------------------------------------
# (III) j and j-inverse ODEs.
# ----------------------------------------------------------------------
def test_j_ode_holds():
    r = verify_j_ode(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_j_inv_ode_holds():
    r = verify_j_inv_ode(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_j_inv_q1_is_1():
    """J_inv = Delta/E_4^3 = q - 744 q^2 + ..., so [q^1] = 1."""
    ji = j_inv_series(3)
    assert ji[1] == 1


def test_j_inv_q2_is_minus_744():
    ji = j_inv_series(3)
    assert ji[2] == -744


def test_j_times_j_inv_equals_q():
    r = verify_j_times_j_inv_equals_q(n_max=12)
    assert r["matches_q"] is True
    assert r["product"][0] == 0
    assert r["product"][1] == 1


# ----------------------------------------------------------------------
# Monster moonshine seed.
# ----------------------------------------------------------------------
def test_moonshine_q2_is_Griess_plus_1():
    m = monster_moonshine_seed()
    assert m["q2_coefficient"] == 196884
    assert m["q2_equals_Griess_plus_1"] is True
    assert m["monster_Griess_dim_plus_1"] == 196884


def test_moonshine_q1_is_744():
    m = monster_moonshine_seed()
    assert m["q1_coefficient"] == 744


# ----------------------------------------------------------------------
# Klein / Ramanujan discriminant.
# ----------------------------------------------------------------------
def test_klein_point_j_of_i_is_k_cubed():
    k = klein_discriminant_constants()
    assert k["k"] == 12
    assert k["k_cubed"] == 1728
    assert k["1728_equals_k_cubed"] is True
    assert k["j_at_tau_i"] == 1728


def test_ramanujan_discriminant_identity():
    k = klein_discriminant_constants()
    assert k["discriminant_holds_up_to_q3"] is True
    assert k["discriminant_lhs_q1"] == 1728
    assert k["discriminant_rhs_q1"] == 1728


# ----------------------------------------------------------------------
# Cross-check: q*j agrees with E_4^3 / prod(1-q^n)^24 coefficient-wise.
# ----------------------------------------------------------------------
def test_j_tilde_matches_E4cubed_over_g24_direct():
    """Consistency: J_tilde computed two ways should agree."""
    jt1 = j_tilde_series(10)
    e4 = e4_series(10)
    from w33_affine_e8 import _series_inv as inv
    g24 = eta_positive_power_series(24, 10)
    g24_inv = inv(g24, 10)
    jt2 = series_mul(series_mul(series_mul(e4, e4, 10), e4, 10), g24_inv, 10)
    assert jt1 == jt2


def test_delta_equals_q_times_g24():
    """Delta = q * prod(1-q^n)^24.  Verify coefficient-wise."""
    delta = delta_series(10)
    g24 = eta_positive_power_series(24, 10)
    # Delta[n+1] == g24[n]
    for n in range(10):
        assert delta[n + 1] == g24[n]


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_eight_pins():
    s = derive_all(n_max=20)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
