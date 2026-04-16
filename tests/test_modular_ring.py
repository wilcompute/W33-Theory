"""Pin the modular form ring M_*(SL(2,Z)) = C[E_4, E_6].

Every modular form is a polynomial in E_4, E_6.  The dimension formula
matches the monomial count, and dim-1 spaces force identities like
E_8 = E_4^2 and E_10 = E_4*E_6.  dim S_12 = 1 forces Delta unique.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_modular_ring import (  # noqa: E402
    derive_modular_ring,
    dim_Mk,
    dim_Sk,
    eisenstein_constants_from_k,
    list_monomials,
    monomial_count,
    verify_dimension_equals_monomial_count,
    verify_E8_equals_E4_squared,
    verify_E10_equals_E4_E6,
    verify_E14_equals_E4sq_E6,
    verify_unique_cusp_form,
)


# ----------------------------------------------------------------------
# Dimension formula.
# ----------------------------------------------------------------------
EXPECTED_DIMS = {0: 1, 2: 0, 4: 1, 6: 1, 8: 1, 10: 1, 12: 2,
                 14: 1, 16: 2, 18: 2, 20: 2, 22: 2, 24: 3, 26: 2}


@pytest.mark.parametrize("k,d", sorted(EXPECTED_DIMS.items()))
def test_dim_Mk(k, d):
    assert dim_Mk(k) == d


def test_dim_Mk_odd_is_zero():
    for k in (1, 3, 5, 7, 11, 13):
        assert dim_Mk(k) == 0


def test_dim_Mk_negative_is_zero():
    assert dim_Mk(-2) == 0
    assert dim_Mk(-4) == 0


def test_dim_M2_is_zero():
    assert dim_Mk(2) == 0


def test_dim_Sk_12_is_1():
    assert dim_Sk(12) == 1


def test_dim_Sk_below_12_is_0():
    for k in range(0, 12, 2):
        assert dim_Sk(k) == 0


# ----------------------------------------------------------------------
# Monomial count = dim M_k.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("k", list(range(0, 62, 2)))
def test_monomial_count_equals_dim(k):
    assert monomial_count(k) == dim_Mk(k)


def test_dimension_table_all_match():
    results = verify_dimension_equals_monomial_count(60)
    assert all(d["match"] for d in results)


def test_monomials_weight_12():
    m = list_monomials(12)
    assert (3, 0) in m  # E_4^3
    assert (0, 2) in m  # E_6^2
    assert len(m) == 2


# ----------------------------------------------------------------------
# Forced identities from dim = 1.
# ----------------------------------------------------------------------
def test_E8_equals_E4_squared():
    r = verify_E8_equals_E4_squared()
    assert r["match"] is True
    assert r["dim_M8"] == 1


def test_E10_equals_E4_E6():
    r = verify_E10_equals_E4_E6()
    assert r["match"] is True
    assert r["dim_M10"] == 1


def test_E14_equals_E4sq_E6():
    r = verify_E14_equals_E4sq_E6()
    assert r["match"] is True
    assert r["dim_M14"] == 1


# ----------------------------------------------------------------------
# Unique cusp form.
# ----------------------------------------------------------------------
def test_unique_cusp_form_S12():
    r = verify_unique_cusp_form()
    assert r["dim_S12"] == 1
    assert r["S12_unique"] is True
    assert r["dim_M12"] == 2


# ----------------------------------------------------------------------
# Eisenstein constants encode k.
# ----------------------------------------------------------------------
def test_E4_constant_is_20k():
    r = eisenstein_constants_from_k(12)
    assert r["c_E4"] == 240
    assert r["c_E4 = 20k"] is True


def test_E6_constant_is_minus_42k():
    r = eisenstein_constants_from_k(12)
    assert r["c_E6"] == -504
    assert r["c_E6 = -42k"] is True


def test_240_equals_20_times_12():
    assert 20 * 12 == 240


def test_504_equals_42_times_12():
    assert 42 * 12 == 504


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_chain_all_true():
    chain = derive_modular_ring(12)
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"
