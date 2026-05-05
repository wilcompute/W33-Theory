from fractions import Fraction

from exploration.PART_CCCXI_NORMALIZED_MARKOV_KREIN_COMPILER import (
    q,
    V,
    K,
    lam,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    H1,
    HASHIMOTO_BRANCH,
    P_SPECTRUM,
    P_NONTRIVIAL_POS,
    P_NONTRIVIAL_NEG,
    P_TRACE,
    P_TRACE_SQ,
    P_TRACE_CUBE,
    P_SLEM,
    NL_SPECTRUM,
    NL_EIG1,
    NL_EIG2,
    NL_TRACE,
    NL_TRACE_SQ,
    NL_SUM_NONTRIVIAL,
    NL_PROD_NONTRIVIAL,
    NL_DIFF_NONTRIVIAL,
    CHEEGER_LOWER,
    KR_11_0,
    KR_22_0,
    KR_22_2,
    KREIN_VERTEX,
    KREIN_THETA,
    KREIN_FIREWALL,
    KREIN_CARRIER_SQUARE,
    TREE_EXP_2,
    TREE_EXP_5,
    normalized_markov_krein_compiler_audit,
)


def test_random_walk_q_clock_spectrum():
    assert P_SPECTRUM == [(Fraction(1), 1), (Fraction(1, 6), 24), (Fraction(-1, 3), 15)]
    assert P_NONTRIVIAL_POS == Fraction(1, 2 * q)
    assert P_NONTRIVIAL_NEG == Fraction(-1, q)
    assert P_SLEM == Fraction(1, q)
    assert P_TRACE == 0


def test_random_walk_return_moments():
    assert P_TRACE_SQ == Fraction(Phi4, q) == Fraction(10, 3)
    assert P_TRACE_CUBE == Fraction(lam * (V * K // 2) * 2 // 3, K ** 3)


def test_normalized_laplacian_spectrum_and_invariants():
    assert NL_SPECTRUM == [(Fraction(0), 1), (Fraction(5, 6), 24), (Fraction(4, 3), 15)]
    assert NL_EIG1 == Fraction(5, 6)
    assert NL_EIG2 == Fraction(4, 3)
    assert NL_TRACE == V == 40
    assert NL_TRACE_SQ == Fraction(130, 3) == Fraction(V) + Fraction(Phi4, q)


def test_normalized_nontrivial_sum_product_difference():
    assert NL_SUM_NONTRIVIAL == Fraction(Phi3, 2 * q) == Fraction(13, 6)
    assert NL_PROD_NONTRIVIAL == Fraction(Phi4, q ** 2) == Fraction(10, 9)
    assert NL_DIFF_NONTRIVIAL == Fraction(1, 2)
    assert CHEEGER_LOWER == Fraction(J, K) == Fraction(5, 12)


def test_krein_dual_agrees_with_markov_and_carrier():
    assert KREIN_VERTEX == V == 40
    assert KREIN_THETA == Phi4 == 10
    assert q * KR_22_2 == q * P_TRACE_SQ == Phi4
    assert KREIN_FIREWALL == KR_11_0 - KR_22_0 == q ** 2 == 9
    assert KREIN_CARRIER_SQUARE == J_inv ** 2 == 64


def test_global_exponents_and_threshold():
    assert TREE_EXP_2 == H1 == q ** 4 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == 23
    assert HASHIMOTO_BRANCH == 11
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = normalized_markov_krein_compiler_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["markov_q_clock"] == "A/K has nontrivial eigenvalues +1/(2q) and -1/q"
