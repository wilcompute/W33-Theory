"""Pin the Rankin-Cohen bracket tower layer.

This layer shows two constructions of Delta:

    [E_4, E_6]_1 = -3456 * Delta  (weight-1 RC bracket),
    [E_4, E_4]_2 =  4800 * Delta  (weight-2 RC bracket).

The tests verify the coefficient identities, an explicit form for the
second bracket, and a short driver-chain that asserts all pins pass.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from math import comb

from w33_rankin_cohen_tower import (
    bracket_q1_calculations,
    d_power,
    delta_coefficients_first_five,
    derive_all,
    rankin_cohen_bracket,
    structural_interpretation,
    verify_rc_E4_E4_2,
    verify_rc_E4_E4_2_explicit_form,
    verify_rc_E4_E6_1,
)
from w33_ramanujan_system import (
    delta_series,
    e4_series,
    e6_series,
    q_d_dq,
    series_mul,
)


# ----------------------------------------------------------------------
# Rankin-Cohen bracket identities
# ----------------------------------------------------------------------
def test_rc_E4_E4_2_holds():
    r = verify_rc_E4_E4_2(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_rc_E4_E4_2_explicit_form_holds():
    r = verify_rc_E4_E4_2_explicit_form(n_max=25)
    assert r["all_match"] is True


def test_rc_E4_E6_1_holds():
    r = verify_rc_E4_E6_1(n_max=25)
    assert r["all_match"] is True
    assert r["mismatches"] == []


def test_structural_interpretation():
    s = structural_interpretation()
    assert s["rc_2_equals_4800"] is True
    assert s["rc_1_equals_minus_3456"] is True


def test_q1_bracket_spot_checks():
    q = bracket_q1_calculations()
    assert q["[E_4,E_4]_2 at q1"] == 4800
    assert q["[E_4,E_6]_1 at q1"] == -3456


def test_rc_E4_E4_2_coefficient():
    r = verify_rc_E4_E4_2(n_max=5)
    assert r["coefficient"] == 4800


def test_rc_E4_E6_1_coefficient():
    r = verify_rc_E4_E6_1(n_max=5)
    assert r["coefficient"] == -3456


def test_rc_E4_E4_2_q1_is_4800():
    """4800 * Delta[1] = 4800 * 1."""
    e4 = e4_series(5)
    bracket = rankin_cohen_bracket(e4, 4, e4, 4, 2, 5)
    assert bracket[1] == 4800


def test_rc_E4_E4_2_q2_is_minus_115200():
    """4800 * Delta[2] = 4800 * (-24)."""
    e4 = e4_series(5)
    bracket = rankin_cohen_bracket(e4, 4, e4, 4, 2, 5)
    assert bracket[2] == -115200


def test_rc_E4_E4_2_q3_is_1209600():
    """4800 * Delta[3] = 4800 * 252."""
    e4 = e4_series(5)
    bracket = rankin_cohen_bracket(e4, 4, e4, 4, 2, 5)
    assert bracket[3] == 1209600


def test_rc_1_formula_minus_2_k_cubed():
    k = 12
    assert -2 * k ** 3 == -3456


def test_rc_2_formula_2_C_five_two_times_240():
    assert 2 * comb(5, 2) * 240 == 4800


def test_d_power_zero_is_identity():
    f = [1, 2, 3, 4, 5]
    assert d_power(f, 0) == f


def test_d_power_one_is_q_d_dq():
    f = [1, 2, 3, 4, 5]
    assert d_power(f, 1) == q_d_dq(f)


def test_d_power_two_nested():
    f = [1, 2, 3, 4, 5]
    assert d_power(f, 2) == q_d_dq(q_d_dq(f))


def test_rankin_cohen_bracket_n0_is_product():
    """[f, g]_0 = f * g  since the sum has a single term with unit binomials."""
    e4 = e4_series(5)
    e6 = e6_series(5)
    bracket = rankin_cohen_bracket(e4, 4, e6, 6, 0, 5)
    product = series_mul(e4, e6, 5)
    assert bracket == product


def test_delta_first_three_coefficients():
    info = delta_coefficients_first_five()
    assert info["Delta_q1"] == 1
    assert info["Delta_q2"] == -24
    assert info["Delta_q3"] == 252


def test_rc_E4_E4_2_divides_by_delta_exactly():
    """[E_4, E_4]_2 / 4800 equals Delta coefficient-wise."""
    e4 = e4_series(10)
    delta = delta_series(10)
    bracket = rankin_cohen_bracket(e4, 4, e4, 4, 2, 10)
    for n in range(11):
        assert bracket[n] == 4800 * delta[n]


def test_structural_k_and_E8_roots():
    s = structural_interpretation()
    assert s["k_w33_valency"] == 12
    assert s["E8_root_count"] == 240


# ----------------------------------------------------------------------
# Driver chain
# ----------------------------------------------------------------------
def test_driver_all_eight_pins():
    s = derive_all(n_max=20)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
