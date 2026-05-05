from fractions import Fraction

from exploration.PART_CCCXIX_EMPIRICAL_CLOSURE_FALSIFICATION_COMPILER import (
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
    TRIANGLES,
    TR_A3,
    TREE_EXP_2,
    TREE_EXP_5,
    RESOURCE_LADDER,
    CLIFFORD_QUOTIENTS,
    PROJECTIVE_OBSERVABLES,
    FULL_STABILIZER_WEIGHT,
    FUSION_P,
    CRITICAL_EDGE_HALF,
    CRITICAL_MEAN_DEGREE,
    CRITICAL_DEGREE_VARIANCE,
    CRITICAL_STABILIZER_WEIGHT,
    EXPECTED_FULL_CLUSTER_TRIALS,
    CRITICAL_TRIANGLE_TRACE,
    GUT_WEAK_MIXING_TARGET,
    KOIDE_TARGET,
    KLM_TARGET,
    empirical_layers,
    empirical_predictions,
    empirical_closure_audit,
)


def test_finite_atoms_and_tree_factor():
    assert (q, lam, mu, V, K, E, DIRECTED) == (3, 2, 4, 40, 12, 240, 480)
    assert TREE_EXP_2 == H1 == 81
    assert TREE_EXP_5 == Phi3 + Phi4 == 23


def test_directly_testable_finite_emulator_predictions():
    assert PROJECTIVE_OBSERVABLES == V == 40
    assert E == 240
    assert FULL_STABILIZER_WEIGHT == Phi3 == 13
    assert FUSION_P == Fraction(lam, mu) == Fraction(1, 2)
    assert CRITICAL_EDGE_HALF == 120
    assert CRITICAL_MEAN_DEGREE == 2 * q == 6
    assert CRITICAL_DEGREE_VARIANCE == q == 3
    assert CRITICAL_STABILIZER_WEIGHT == Phi6 == 7
    assert EXPECTED_FULL_CLUSTER_TRIALS == DIRECTED == 480
    assert CRITICAL_TRIANGLE_TRACE == E // 2 == 120


def test_resource_and_clifford_ladders():
    assert RESOURCE_LADDER == [120, 240, 480, 960]
    assert CLIFFORD_QUOTIENTS == [432, 216, 108, 54]
    assert TR_A3 == 960
    assert TRIANGLES == 160


def test_candidate_dimensionless_targets():
    assert GUT_WEAK_MIXING_TARGET == Fraction(3, 8)
    assert KOIDE_TARGET == Fraction(2, 3)
    assert KLM_TARGET == Fraction(1, mu) == Fraction(1, 4)


def test_layers_and_predictions_present():
    layers = empirical_layers()
    predictions = empirical_predictions()
    assert [layer.tier for layer in layers] == ["T0", "T1", "T2", "T3"]
    assert len(predictions) >= 9
    assert any(pred.id == "T1-P6" and pred.exact_value == "480" for pred in predictions)
    assert any(pred.id == "T2-P1" and pred.exact_value == "3/8" for pred in predictions)


def test_threshold_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = empirical_closure_audit()
    assert all(audit["checks"].values())
    assert "scale-setting rule" in audit["closure_requirements"]
