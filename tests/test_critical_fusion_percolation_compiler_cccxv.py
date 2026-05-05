from fractions import Fraction

from exploration.PART_CCCXV_CRITICAL_FUSION_PERCOLATION_COMPILER import (
    q,
    lam,
    mu,
    V,
    K,
    Phi3,
    Phi4,
    Phi6,
    J,
    J_inv,
    H1,
    E,
    DIRECTED,
    HASHIMOTO_BRANCH,
    TRIANGLES,
    TR_A3,
    p_fusion,
    p_klm,
    EXPECTED_SUCCESS_EDGES as EDGE_HALF_A,
    EXPECTED_FAILED_EDGES as EDGE_HALF_B,
    EXPECTED_ORIENTED_SUCCESS_INCIDENCES as ORIENTED_HALF_A,
    EXPECTED_RETRY_ATTEMPTS_ALL_EDGES as FULL_TRIAL_COUNT,
    EXPECTED_RETAINED_DEGREE as MEAN_DEGREE,
    RETAINED_DEGREE_VARIANCE as DEGREE_VAR,
    EXPECTED_STABILIZER_WEIGHT as MEAN_STABILIZER_WEIGHT,
    EXPECTED_RETAINED_TRIANGLES as MEAN_TRIANGLES,
    EXPECTED_RETAINED_TRIANGLE_TRACE as MEAN_TRIANGLE_TRACE,
    EDGE_COUNT_VARIANCE,
    FOUR_EDGE_VARIANCE,
    QLE,
    SEIDEL_POSITIVE_MASS,
    SEIDEL_NEGATIVE_MASS,
    SEIDEL_ENERGY,
    LINE_GRAPH_VERTICES,
    LINE_GRAPH_SECOND_MOMENT,
    TREE_EXP_2,
    TREE_EXP_5,
    DIRAC_GAP_EXPONENT,
    DIRAC_NEGATIVE_ENDPOINT_MAGNITUDE,
    critical_fusion_percolation_audit,
)


def test_photonic_probabilities_are_w33_ratios():
    assert p_fusion == Fraction(lam, mu) == Fraction(1, 2)
    assert p_klm == Fraction(1, mu) == Fraction(1, 4)


def test_balanced_edge_halves_match_seidel_balance():
    assert EDGE_HALF_A == QLE == SEIDEL_POSITIVE_MASS == 120
    assert EDGE_HALF_B == QLE == SEIDEL_NEGATIVE_MASS == 120
    assert EDGE_HALF_A + EDGE_HALF_B == E == SEIDEL_ENERGY == 240


def test_oriented_and_full_trial_counts():
    assert ORIENTED_HALF_A == E == LINE_GRAPH_VERTICES == 240
    assert FULL_TRIAL_COUNT == DIRECTED == 480


def test_critical_degree_and_stabilizer():
    assert MEAN_DEGREE == 2 * q == DIRAC_GAP_EXPONENT == 6
    assert DEGREE_VAR == q == 3
    assert MEAN_STABILIZER_WEIGHT == Phi6 == DIRAC_NEGATIVE_ENDPOINT_MAGNITUDE == 7


def test_triangle_layer():
    assert TRIANGLES == 160
    assert TR_A3 == 960
    assert MEAN_TRIANGLES == Fraction(V, 2) == 20
    assert MEAN_TRIANGLE_TRACE == QLE == 120


def test_global_variance_edge_shell():
    assert EDGE_COUNT_VARIANCE == 60
    assert FOUR_EDGE_VARIANCE == E == 240


def test_operator_companions_and_threshold():
    assert LINE_GRAPH_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH == 5280
    assert TREE_EXP_2 == H1 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == 23
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = critical_fusion_percolation_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["critical_stabilizer"] == "expected critical stabilizer weight 1+pk=Phi6=7"
