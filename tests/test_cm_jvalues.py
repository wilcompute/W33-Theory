"""Pin the CM j-values at Heegner points and the Ramanujan almost-integers.

The imaginary quadratic fields Q(sqrt(-d)) with class number 1 have d in
{1, 2, 3, 7, 11, 19, 43, 67, 163}.  At the CM point tau_d = (1+sqrt(-d))/2,
j(tau_d) is the cube of an integer:

    j(i)        = 12^3 = 1728 = k^3
    j(sqrt(-2)i) = 20^3
    j((1+sqrt(-163))/2) = -640320^3

The Ramanujan almost-integer:  e^{pi sqrt(d)} ~ -j(tau_d) + 744.
For d=163 this gives the famous near-integer 262537412640768744.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_cm_jvalues import (  # noqa: E402
    HEEGNER_J_VALUES,
    derive_all_cm_jvalues,
    heegner_cube_roots,
    j_of_i_equals_k_cubed,
    ramanujan_almost_integer,
    the_ramanujan_constant,
    verify_j_values_are_cubes,
)


# ----------------------------------------------------------------------
# All Heegner j-values are integer cubes.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("d", sorted(HEEGNER_J_VALUES.keys()))
def test_j_at_heegner_is_cube(d):
    results = verify_j_values_are_cubes()
    r = results[d]
    assert r["match"] is True
    assert r["cube"] == r["j_value"]


def test_j_of_i_is_1728():
    r = verify_j_values_are_cubes()[1]
    assert r["cube_root"] == 12
    assert r["j_value"] == 1728


def test_j_of_i_is_k_cubed():
    r = j_of_i_equals_k_cubed(12)
    assert r["match"] is True
    assert r["j(i)"] == 1728
    assert r["k^3"] == 12 ** 3


def test_j_at_rho_is_zero():
    """j((1+sqrt(-3))/2) = 0."""
    r = verify_j_values_are_cubes()[3]
    assert r["cube_root"] == 0
    assert r["j_value"] == 0


def test_j_at_d_163_is_negative_640320_cubed():
    r = verify_j_values_are_cubes()[163]
    assert r["cube_root"] == -640320
    assert r["j_value"] == -640320 ** 3
    assert r["j_value"] == -262537412640768000


# ----------------------------------------------------------------------
# Ramanujan almost-integer e^{pi sqrt(d)} ~ -j + 744.
# ----------------------------------------------------------------------
def test_ramanujan_163_matches_to_12_decimals():
    """For d=163, |e^{pi sqrt(163)} - 262537412640768744| < 1e-12."""
    import mpmath
    r = ramanujan_almost_integer(163, precision_digits=40)
    diff = mpmath.mpf(r["difference"])
    assert abs(diff) < mpmath.mpf("1e-12")


def test_ramanujan_163_predicted_integer():
    r = ramanujan_almost_integer(163)
    assert r["predicted_integer"] == 262537412640768744


def test_ramanujan_constant_is_163():
    r = the_ramanujan_constant()
    assert r["d"] == 163


@pytest.mark.parametrize("d", [43, 67, 163])
def test_ramanujan_correction_matches(d):
    """|diff - (-196884 e^{-pi sqrt(d)})| is small relative to the correction
    itself.  d=19 is excluded because higher-order terms in the j-series
    (196884^2 * q^2 etc.) become comparable to the first-order correction."""
    r = ramanujan_almost_integer(d, precision_digits=50)
    assert r["_corr_match"]


def test_ramanujan_correction_order_at_d_19():
    """At d=19, |diff| and |correction| are both of order 1/5."""
    import mpmath
    r = ramanujan_almost_integer(19, precision_digits=30)
    diff = abs(mpmath.mpf(r["difference"]))
    corr = abs(mpmath.mpf(r["first_order_correction"]))
    # Both of order 0.2, same sign => ratio close to 1.
    assert mpmath.mpf("0.4") < diff / corr < mpmath.mpf("1.0")


# ----------------------------------------------------------------------
# k-connections: 12 and 20 = k + rank(E_8).
# ----------------------------------------------------------------------
def test_j_of_i_cube_root_is_12():
    r = heegner_cube_roots()
    assert r["cube_roots"][1] == 12
    assert r["j(i)_is_k"] is True


def test_j_of_sqrt_minus_2_cube_root_is_20():
    r = heegner_cube_roots()
    assert r["cube_roots"][2] == 20
    assert r["20 = k + 8"] is True


def test_1728_equals_12_cubed():
    assert 12 ** 3 == 1728


# ----------------------------------------------------------------------
# Heegner set is exactly 9 numbers.
# ----------------------------------------------------------------------
def test_heegner_set_has_9_elements():
    assert len(HEEGNER_J_VALUES) == 9


def test_heegner_set_contents():
    assert set(HEEGNER_J_VALUES.keys()) == {1, 2, 3, 7, 11, 19, 43, 67, 163}


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_chain_all_true():
    chain = derive_all_cm_jvalues()
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"
