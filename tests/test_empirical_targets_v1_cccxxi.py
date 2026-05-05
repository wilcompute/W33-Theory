from fractions import Fraction

from exploration.PART_CCCXXI_EMPIRICAL_TARGETS_V1 import (
    q,
    lam,
    mu,
    V,
    K,
    Phi3,
    Phi6,
    J,
    J_inv,
    H1,
    E,
    DIRECTED,
    PROJECTIVE_OBSERVABLES,
    FULL_STABILIZER_WEIGHT,
    FUSION_P,
    KLM_P,
    CRITICAL_EDGE_HALF,
    CRITICAL_MEAN_DEGREE,
    CRITICAL_DEGREE_VARIANCE,
    CRITICAL_STABILIZER_WEIGHT,
    EXPECTED_FUSION_TRIALS,
    CLIFFORD_QUOTIENTS,
    SIN2_THETA_W_GUT,
    KOIDE,
    MARKOV_CONTRACTION,
    NONREVERSE_PROB,
    REVERSE_PROB,
    empirical_targets_v1,
    targets_summary,
    empirical_targets_audit,
)


def test_w33_and_finite_targets():
    assert (q, lam, mu, V, K, E, DIRECTED) == (3, 2, 4, 40, 12, 240, 480)
    assert PROJECTIVE_OBSERVABLES == V == 40
    assert FULL_STABILIZER_WEIGHT == Phi3 == 13
    assert CRITICAL_EDGE_HALF == 120
    assert CRITICAL_MEAN_DEGREE == 2 * q == 6
    assert CRITICAL_DEGREE_VARIANCE == q == 3
    assert CRITICAL_STABILIZER_WEIGHT == Phi6 == 7
    assert EXPECTED_FUSION_TRIALS == DIRECTED == 480
    assert CLIFFORD_QUOTIENTS == [432, 216, 108, 54]


def test_dimensionless_and_resource_targets():
    assert SIN2_THETA_W_GUT == Fraction(3, 8)
    assert KOIDE == Fraction(2, 3)
    assert FUSION_P == Fraction(lam, mu) == Fraction(1, 2)
    assert KLM_P == Fraction(1, mu) == Fraction(1, 4)
    assert MARKOV_CONTRACTION == Fraction(1, q) == Fraction(1, 3)
    assert NONREVERSE_PROB == Fraction(K - 1, K) == Fraction(11, 12)
    assert REVERSE_PROB == Fraction(1, K) == Fraction(1, 12)


def test_target_schema_and_statuses():
    targets = empirical_targets_v1()
    assert len(targets) == 17
    assert targets_summary(targets) == {
        "READY_EXACT": 12,
        "DATA_REQUIRED": 2,
        "EXPERIMENT_REQUIRED": 2,
        "ANCHORS_REQUIRED": 1,
    }
    assert all(t.measured_value is None for t in targets if t.status in {"DATA_REQUIRED", "ANCHORS_REQUIRED"})
    assert any(t.id == "M1_SIN2_THETA_W_GUT" and t.theory_value == "3/8" for t in targets)
    assert any(t.id == "M2_DIMENSIONFUL_ANCHORS" and t.status == "ANCHORS_REQUIRED" for t in targets)


def test_threshold_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv
    assert H1 == q**4 == 81


def test_audit_checks_all_true():
    audit = empirical_targets_audit()
    assert all(audit["checks"].values())
    assert audit["status_summary"]["DATA_REQUIRED"] == 2
    assert audit["residual_policy"]["residual"] == "measured_value - theory_value"
