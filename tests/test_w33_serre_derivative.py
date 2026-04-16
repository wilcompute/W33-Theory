"""Pin the Serre derivative layer.

Main claims (all as integer power-series identities):

    D_4(E_4) = -E_6 / 3                   in M_6,
    D_6(E_6) = -E_4^2 / 2                 in M_8,
    D_12(Delta) = 0                       (Delta extremal),
    [E_4, E_6]_1 = -3456 * Delta = -2 * 12^3 * Delta.

All six eta positive powers  c in {1, 2, 4, 8, 12, 24} satisfy
    24 q d g_c/dq = c (E_2 - 1) g_c       (Serre flatness of eta).
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_serre_derivative import (  # noqa: E402
    derive_all,
    eta_positive_power_series,
    rankin_cohen_bracket_1,
    serre_derivative_12x,
    verify_eta_positive_power_serre,
    verify_rankin_cohen_E4_E6_is_minus_3456_delta,
    verify_rankin_cohen_via_E4_cubed_minus_E6_sq,
    verify_serre_delta_is_zero,
    verify_serre_E4_gives_minus_E6_over_3,
    verify_serre_E6_gives_minus_E4_sq_over_2,
    w33_valency_signatures,
)
from w33_ramanujan_system import (  # noqa: E402
    delta_series,
    e4_series,
    e6_series,
)


# ----------------------------------------------------------------------
# Serre derivative identities on the holomorphic generators.
# ----------------------------------------------------------------------
def test_D4_E4_holds():
    r = verify_serre_E4_gives_minus_E6_over_3(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_D6_E6_holds():
    r = verify_serre_E6_gives_minus_E4_sq_over_2(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_D4_E4_q1_matches_minus_4_E6_at_q1():
    """[q^1] 12*D_4(E_4) = 12*(1*240) - 4*(1*240 - 504) ... use -4*E_6[1]."""
    e4 = e4_series(5)
    e6 = e6_series(5)
    lhs = serre_derivative_12x(e4, k=4, n_max=5)
    assert lhs[1] == -4 * e6[1]
    assert lhs[1] == -4 * (-504)


def test_D6_E6_q1_matches_minus_6_E4_sq_at_q1():
    e4 = e4_series(5)
    e6 = e6_series(5)
    lhs = serre_derivative_12x(e6, k=6, n_max=5)
    # [q^1] E_4^2 = 2*E_4[0]*E_4[1] = 2*240 = 480
    assert lhs[1] == -6 * 480


# ----------------------------------------------------------------------
# Extremality of Delta: D_12(Delta) = 0.
# ----------------------------------------------------------------------
def test_D12_delta_is_zero():
    r = verify_serre_delta_is_zero(n_max=25)
    assert r["all_zero"] is True
    assert all(v == 0 for v in r["residuals"])


def test_D12_delta_zero_at_q1():
    delta = delta_series(5)
    lhs = serre_derivative_12x(delta, k=12, n_max=5)
    assert lhs[1] == 0


def test_delta_is_not_trivially_zero():
    """Delta coefficients are not all zero — extremality is non-trivial."""
    delta = delta_series(5)
    assert delta[1] == 1
    assert delta[2] == -24


# ----------------------------------------------------------------------
# eta^c Serre flatness for positive powers (integer series).
# ----------------------------------------------------------------------
def test_eta_positive_power_serre_c1():
    r = verify_eta_positive_power_serre(1, n_max=25)
    assert r["all_zero"] is True


def test_eta_positive_power_serre_c2():
    r = verify_eta_positive_power_serre(2, n_max=25)
    assert r["all_zero"] is True


def test_eta_positive_power_serre_c4():
    r = verify_eta_positive_power_serre(4, n_max=25)
    assert r["all_zero"] is True


def test_eta_positive_power_serre_c8():
    r = verify_eta_positive_power_serre(8, n_max=25)
    assert r["all_zero"] is True


def test_eta_positive_power_serre_c12():
    r = verify_eta_positive_power_serre(12, n_max=25)
    assert r["all_zero"] is True


def test_eta_positive_power_serre_c24():
    """c=24 is the Euler function cubed... no wait, it is prod(1-q^n)^24 = Delta
    (without q prefactor).  Serre flatness is an anchor."""
    r = verify_eta_positive_power_serre(24, n_max=25)
    assert r["all_zero"] is True


def test_eta_power_c24_equals_delta_without_prefactor():
    """g_24 = prod(1-q^n)^{24} has the same coefficients as Delta SHIFTED by
    one (since Delta = q * g_24).  So delta[n+1] == g_24[n]."""
    g24 = eta_positive_power_series(24, 6)
    delta = delta_series(7)
    for n in range(6):
        assert delta[n + 1] == g24[n]


# ----------------------------------------------------------------------
# Rankin-Cohen bracket.
# ----------------------------------------------------------------------
def test_rankin_cohen_E4_E6_equals_minus_3456_delta():
    r = verify_rankin_cohen_E4_E6_is_minus_3456_delta(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_rankin_cohen_coefficient_is_minus_3456():
    r = verify_rankin_cohen_E4_E6_is_minus_3456_delta(n_max=5)
    assert r["coefficient"] == -3456
    assert r["k"] == 12


def test_rankin_cohen_equals_minus_2_times_E4cubed_minus_E6sq():
    r = verify_rankin_cohen_via_E4_cubed_minus_E6_sq(n_max=25)
    assert r["all_match"] is True


def test_rankin_cohen_q1_is_minus_3456():
    """[q^1] Delta = 1, so [q^1] [E_4, E_6]_1 = -3456."""
    e4 = e4_series(5)
    e6 = e6_series(5)
    bracket = rankin_cohen_bracket_1(e4, 4, e6, 6, 5)
    assert bracket[1] == -3456


def test_rankin_cohen_q0_is_zero():
    """Constant term of Delta is 0, so bracket q^0 coefficient is 0."""
    e4 = e4_series(5)
    e6 = e6_series(5)
    bracket = rankin_cohen_bracket_1(e4, 4, e6, 6, 5)
    assert bracket[0] == 0


# ----------------------------------------------------------------------
# W(3,3) valency appearances.
# ----------------------------------------------------------------------
def test_w33_valency_in_serre_denominator():
    s = w33_valency_signatures()
    assert s["k"] == 12
    assert s["serre_denominator"] == 12


def test_w33_valency_is_delta_weight():
    s = w33_valency_signatures()
    assert s["delta_weight_killed_by_D_k"] == 12


def test_w33_valency_cubed_is_rc_coefficient_magnitude():
    s = w33_valency_signatures()
    assert s["rankin_cohen_coefficient_minus_2_k3"] == -3456
    assert s["rankin_cohen_coefficient_equals_minus_3456"] is True


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_eight_pins():
    s = derive_all(n_max=20)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
