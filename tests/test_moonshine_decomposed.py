"""Pin the mechanical proof that 196884 = 196560 + 324, and the general
   Leech-vs-oscillator decomposition of every j-coefficient.

   Master identity:
       j(tau) - 720  =  theta_Lambda(tau) / Delta(tau)  =  chi_{V_Lambda}(tau).

   Coefficient identity for n >= -1:
       [q^n] j(tau)  =  720 * delta_{n,0}  +  sum_k  N_{2k}(Lambda) * p_{24}(n - k + 1).
"""
from __future__ import annotations

import sys
from math import comb
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_moonshine_decomposed import (  # noqa: E402
    decompose_j_via_leech,
    derive_all_moonshine_decomposed,
    inv_delta_qseries,
    p24_combinatorial,
    p24_partitions,
    the_21493760_solution,
    the_324_solution,
    verify_inv_delta_equals_q_inv_times_p24,
)


# ----------------------------------------------------------------------
# 24-color partition numbers (OEIS A006922).
# ----------------------------------------------------------------------
EXPECTED_P24 = [1, 24, 324, 3200, 25650, 176256, 1073720]


@pytest.mark.parametrize("n,expected", list(enumerate(EXPECTED_P24)))
def test_p24_matches_OEIS_A006922(n, expected):
    p = p24_partitions(6)
    assert p[n] == expected


def test_p24_of_2_combinatorial():
    """p_24(2) = 24 (one part) + C(25, 2) (two parts) = 24 + 300 = 324."""
    one_part_2 = 24
    two_parts_1 = comb(25, 2)
    assert one_part_2 == 24
    assert two_parts_1 == 300
    assert one_part_2 + two_parts_1 == 324


def test_p24_combinatorial_matches_powerseries():
    p_series = p24_partitions(2)
    for n in range(3):
        assert p_series[n] == p24_combinatorial(n)


# ----------------------------------------------------------------------
# 1/Delta as 24-color partition generating function.
# ----------------------------------------------------------------------
EXPECTED_INV_DELTA = {
    -1: 1,
     0: 24,
     1: 324,
     2: 3200,
     3: 25650,
     4: 176256,
     5: 1073720,
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_INV_DELTA.items()))
def test_inv_delta_coefficients(n, expected):
    inv = inv_delta_qseries(5)
    assert inv[n] == expected


def test_inv_delta_pole_at_q_minus_one():
    inv = inv_delta_qseries(0)
    assert inv[-1] == 1


def test_inv_delta_constant_term_is_24():
    inv = inv_delta_qseries(0)
    assert inv[0] == 24


def test_inv_delta_q_one_is_324():
    inv = inv_delta_qseries(1)
    assert inv[1] == 324


def test_inv_delta_equals_p24_shifted():
    v = verify_inv_delta_equals_q_inv_times_p24(5)
    assert v["all_match"] is True


# ----------------------------------------------------------------------
# THE KEY IDENTITY:  196884 = 196560 + 324.
# ----------------------------------------------------------------------
def test_solve_324_total_is_196884():
    sol = the_324_solution()
    assert sol["j_q_coef"] == 196884
    assert sol["leech_minimum_count"] == 196560
    assert sol["oscillator_contribution"] == 324
    assert 196560 + 324 == 196884


def test_solve_324_p24_breakdown():
    sol = the_324_solution()
    bd = sol["p_24_of_2_combinatorial"]
    assert bd["one_part_of_2_in_24_colors"] == 24
    assert bd["two_parts_of_1_with_reps"] == 300
    assert bd["total"] == 324


def test_solve_324_decomposition_matches_actual_j():
    sol = the_324_solution()
    decomp = sol["convolution_explained"]
    assert decomp["match"] is True
    assert decomp["j_via_decomposition"] == 196884
    assert decomp["j_actual"] == 196884


# ----------------------------------------------------------------------
# Generalize:  21493760 = 3200 + 4717440 + 16773120.
# ----------------------------------------------------------------------
def test_q2_coefficient_decomposition():
    """[q^2] j = 21493760 splits as:
        k=0: 1       * p_24(3) = 3200
        k=2: 196560  * p_24(1) = 4717440
        k=3: 16773120* p_24(0) = 16773120
    """
    sol = the_21493760_solution()
    decomp = sol["leech_decomposition_via_CFT"]
    assert decomp["lattice_sum"] == 21493760
    assert decomp["match"] is True

    contribs = {c["k"]: c["contribution"] for c in decomp["contributions"]}
    assert contribs[0] == 3200
    assert contribs[2] == 4717440
    assert contribs[3] == 16773120
    assert contribs[0] + contribs[2] + contribs[3] == 21493760


def test_q2_coefficient_consistent_with_monster_decomposition():
    """21493760 = 1 + 196883 + 21296876  (sum of three smallest Monster irreps)."""
    assert 1 + 196883 + 21296876 == 21493760


# ----------------------------------------------------------------------
# Decomposition matches j at every q-power up to order 4.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", [-1, 0, 1, 2, 3, 4])
def test_j_coefficient_via_decomposition_matches(n):
    decomp = decompose_j_via_leech(n)
    assert decomp["match"] is True


def test_q_minus_1_decomposition_yields_1():
    """[q^-1] j = 1 = N_0(Leech) * p_24(0)."""
    decomp = decompose_j_via_leech(-1)
    assert decomp["j_via_decomposition"] == 1
    assert decomp["j_actual"] == 1


def test_q_zero_includes_constant_720():
    """[q^0] j = 744.  Decomposition: 720 * delta_{n,0} + N_0 * p_24(1) = 720 + 24."""
    decomp = decompose_j_via_leech(0)
    assert decomp["constant_720_at_n_eq_0"] == 720
    assert decomp["lattice_sum"] == 24       # only N_0=1 * p_24(1)=24
    assert decomp["j_via_decomposition"] == 744
    assert decomp["j_actual"] == 744


# ----------------------------------------------------------------------
# Driver consistency.
# ----------------------------------------------------------------------
def test_driver_chain_consistent():
    chain = derive_all_moonshine_decomposed(max_n=4)
    assert chain["inv_delta_equals_q_inv_p24"]["all_match"] is True
    assert chain["the_324_solution"]["leech_minimum_count"] == 196560
    assert chain["the_324_solution"]["oscillator_contribution"] == 324
    for n in (-1, 0, 1, 2, 3, 4):
        d = chain["all_decompositions"][f"q^{n}"]
        assert d["match"] is True
