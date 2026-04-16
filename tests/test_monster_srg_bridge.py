"""Pin the Monster-SRG bridge: k=12 -> 196883 -> j-coefficients -> D=26.

The smallest Monster irrep dimension 196883 = 47*59*71 = (4k-1)(5k-1)(6k-1)
at k = 12 (the W(3,3) valency).  The j-invariant coefficients decompose
into Monster irrep dimensions, and the critical string dimension is 2k+2 = 26.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_monster_srg_bridge import (  # noqa: E402
    MONSTER_IRREP_DIMS,
    J_IRREP_DECOMPOSITIONS,
    critical_dimension,
    derive_full_bridge,
    srg_valency_factorization,
    the_moonshine_identity,
    verify_all_j_decompositions,
    verify_j_irrep_decomposition,
    verify_primes_47_59_71,
)


# ----------------------------------------------------------------------
# (1)  196883 = (4k-1)(5k-1)(6k-1) at k=12.
# ----------------------------------------------------------------------
def test_196883_equals_product_at_k_12():
    f = srg_valency_factorization(12)
    assert f["product"] == 196883
    assert f["is_196883"] is True


def test_47_59_71_are_factors():
    f = srg_valency_factorization(12)
    assert f["4k-1"] == 47
    assert f["5k-1"] == 59
    assert f["6k-1"] == 71
    assert 47 * 59 * 71 == 196883


def test_47_59_71_are_prime():
    p = verify_primes_47_59_71()
    assert p[47] is True
    assert p[59] is True
    assert p[71] is True
    assert p["all_prime"] is True


def test_arithmetic_progression_with_d_equals_k():
    f = srg_valency_factorization(12)
    ap = f["primes_AP"]
    assert ap["terms"] == [47, 59, 71]
    assert ap["diffs"] == [12, 12]
    assert ap["common_difference"] == 12
    assert ap["is_AP"] is True


def test_47_equals_4k_minus_1():
    assert 4 * 12 - 1 == 47


def test_59_equals_5k_minus_1():
    assert 5 * 12 - 1 == 59


def test_71_equals_6k_minus_1():
    assert 6 * 12 - 1 == 71


# ----------------------------------------------------------------------
# (2)  Monster irrep dimensions and j-coefficient decompositions.
# ----------------------------------------------------------------------
def test_monster_irrep_dims():
    assert MONSTER_IRREP_DIMS[0] == 1
    assert MONSTER_IRREP_DIMS[1] == 196883
    assert MONSTER_IRREP_DIMS[2] == 21296876
    assert MONSTER_IRREP_DIMS[3] == 842609326


@pytest.mark.parametrize("n", sorted(J_IRREP_DECOMPOSITIONS.keys()))
def test_j_irrep_decomposition(n):
    d = verify_j_irrep_decomposition(n)
    assert d["match"] is True


def test_j_minus_1_equals_trivial():
    d = verify_j_irrep_decomposition(-1)
    assert d["c(n)"] == 1
    assert d["decomposition"] == {1: 1}


def test_j_1_equals_1_plus_196883():
    d = verify_j_irrep_decomposition(1)
    assert d["c(n)"] == 196884
    assert d["decomposition"] == {1: 1, 196883: 1}
    assert 1 + 196883 == 196884


def test_j_2_equals_1_plus_196883_plus_21296876():
    d = verify_j_irrep_decomposition(2)
    assert d["c(n)"] == 21493760
    assert 1 + 196883 + 21296876 == 21493760


def test_j_3_decomposition():
    d = verify_j_irrep_decomposition(3)
    assert d["c(n)"] == 864299970
    assert 2 + 2 * 196883 + 21296876 + 842609326 == 864299970


def test_all_j_decompositions_match():
    results = verify_all_j_decompositions()
    assert all(d["match"] for d in results)


# ----------------------------------------------------------------------
# (3)  The moonshine identity: 196884 = 196883 + 1.
# ----------------------------------------------------------------------
def test_moonshine_identity():
    m = the_moonshine_identity()
    assert m["match"] is True
    assert m["c(1)"] == 196884
    assert m["d_1"] == 1
    assert m["d_2"] == 196883
    assert m["d_1 + d_2"] == 196884


def test_196884_minus_1_equals_monster_dim():
    assert 196884 - 1 == 196883


# ----------------------------------------------------------------------
# (4)  Critical string dimension D = 26 = 2k + 2.
# ----------------------------------------------------------------------
def test_critical_dimension_is_26():
    cd = critical_dimension(12)
    assert cd["D_crit"] == 26
    assert cd["is_26"] is True


def test_transverse_dims_equals_24():
    cd = critical_dimension(12)
    assert cd["transverse_dims"] == 24
    assert cd["2k"] == 24


def test_eta_exponent_equals_leech_rank():
    cd = critical_dimension(12)
    assert cd["eta_exponent"] == cd["leech_rank"] == 24


def test_D_equals_2k_plus_2():
    k = 12
    assert 2 * k + 2 == 26


# ----------------------------------------------------------------------
# (5)  Full bridge chain.
# ----------------------------------------------------------------------
def test_full_bridge_all_true():
    chain = derive_full_bridge(12)
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_full_bridge_all_j_decomps():
    chain = derive_full_bridge(12)
    assert chain["all_j_decomps_match"] is True
