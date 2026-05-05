from fractions import Fraction

from exploration.PART_CCCXVI_MARKOV_HASHIMOTO_ENTROPY_LAW import (
    q,
    K,
    V,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    H1,
    E,
    DIRECTED,
    HASHIMOTO_BRANCH,
    EDGE_EXCESS,
    ordinary_walks,
    nonbacktracking_walks,
    walk_ratio,
    P_RETURN,
    P_FORWARD,
    HASHIMOTO_ROOT_DATA,
    LINE_SECOND_MOMENT,
    QLE,
    WIENER_INDEX,
    CRITICAL_RETAINED_DEGREE,
    CRITICAL_RETAINED_NB_BRANCH,
    TREE_EXP_2,
    TREE_EXP_5,
    markov_hashimoto_entropy_audit,
)


def test_local_branch_probabilities():
    assert K == 12
    assert HASHIMOTO_BRANCH == K - 1 == 11
    assert P_RETURN == Fraction(1, K) == Fraction(1, 12)
    assert P_FORWARD == Fraction(K - 1, K) == Fraction(11, 12)
    assert P_RETURN + P_FORWARD == 1


def test_walk_counts_and_conditioning_ratios():
    assert ordinary_walks(0) == V
    assert nonbacktracking_walks(0) == V
    assert walk_ratio(1) == 1
    assert walk_ratio(2) == Fraction(11, 12)
    assert walk_ratio(3) == Fraction(11, 12) ** 2
    assert ordinary_walks(2) == V * K**2 == 5760
    assert nonbacktracking_walks(2) == V * K * HASHIMOTO_BRANCH == 5280


def test_line_graph_and_distance_recover_branch():
    assert LINE_SECOND_MOMENT == nonbacktracking_walks(2) == 5280
    assert LINE_SECOND_MOMENT // DIRECTED == HASHIMOTO_BRANCH
    assert WIENER_INDEX // QLE == HASHIMOTO_BRANCH


def test_hashimoto_ihara_bass_spectral_circle():
    assert HASHIMOTO_ROOT_DATA["theta_12"]["roots"] == [11, 1]
    assert HASHIMOTO_ROOT_DATA["theta_2"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_2"]["imag_sq"] == HASHIMOTO_BRANCH
    assert HASHIMOTO_ROOT_DATA["theta_minus4"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_minus4"]["imag_sq"] == HASHIMOTO_BRANCH


def test_edge_excess_and_critical_fusion_echo():
    assert EDGE_EXCESS == E - V == 200 == J * V
    assert CRITICAL_RETAINED_DEGREE == 2 * q == 6
    assert 2 * CRITICAL_RETAINED_NB_BRANCH == HASHIMOTO_BRANCH


def test_tree_and_threshold_relations():
    assert TREE_EXP_2 == H1 == q**4 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == 23
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = markov_hashimoto_entropy_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["conditioning_law"] == "NB_n / RW_n = ((K-1)/K)^(n-1)"
