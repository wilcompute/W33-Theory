from fractions import Fraction

from exploration.PART_CCCXX_OBSERVABLE_DICTIONARY_SCALE_MAP_V1 import (
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
    ALBERT,
    E,
    DIRECTED,
    TRIANGLES,
    TR_A3,
    TARGET_SIN2_THETA_W_GUT,
    TARGET_KOIDE,
    TARGET_FUSION,
    TARGET_KLM,
    TARGET_MARKOV_CONTRACTION,
    TARGET_MARKOV_POSITIVE_MODE,
    TARGET_MARKOV_NEGATIVE_MODE,
    TARGET_NONREVERSE_PROB,
    TARGET_RETURN_PROB,
    PROJECTIVE_OBSERVABLES,
    FULL_STABILIZER_WEIGHT,
    CRITICAL_FUSION_P,
    CRITICAL_EDGE_HALF,
    CRITICAL_MEAN_DEGREE,
    CRITICAL_DEGREE_VARIANCE,
    CRITICAL_STABILIZER_WEIGHT,
    EXPECTED_FUSION_TRIALS,
    RESOURCE_LADDER,
    CLIFFORD_QUOTIENTS,
    REQUIRED_DIMENSIONFUL_ANCHORS,
    observable_dictionary,
    scale_map_rules,
    scale_map_v1_audit,
)


def test_w33_atoms_and_finite_targets():
    assert (q, lam, mu, V, K, E, DIRECTED) == (3, 2, 4, 40, 12, 240, 480)
    assert (Phi3, Phi4, Phi6, J, J_inv, H1, ALBERT) == (13, 10, 7, 5, 8, 81, 27)
    assert TRIANGLES == 160
    assert TR_A3 == 960


def test_m0_finite_emulator_predictions():
    assert PROJECTIVE_OBSERVABLES == V == 40
    assert FULL_STABILIZER_WEIGHT == Phi3 == 13
    assert CRITICAL_FUSION_P == Fraction(1, 2)
    assert CRITICAL_EDGE_HALF == 120
    assert CRITICAL_MEAN_DEGREE == 2 * q == 6
    assert CRITICAL_DEGREE_VARIANCE == q == 3
    assert CRITICAL_STABILIZER_WEIGHT == Phi6 == 7
    assert EXPECTED_FUSION_TRIALS == DIRECTED == 480


def test_m1_dimensionless_targets():
    assert TARGET_SIN2_THETA_W_GUT == Fraction(3, 8)
    assert TARGET_KOIDE == Fraction(2, 3)
    assert TARGET_FUSION == Fraction(lam, mu) == Fraction(1, 2)
    assert TARGET_KLM == Fraction(1, mu) == Fraction(1, 4)
    assert TARGET_MARKOV_CONTRACTION == Fraction(1, q) == Fraction(1, 3)
    assert TARGET_MARKOV_POSITIVE_MODE == Fraction(1, 2 * q) == Fraction(1, 6)
    assert TARGET_MARKOV_NEGATIVE_MODE == Fraction(-1, q) == Fraction(-1, 3)
    assert TARGET_NONREVERSE_PROB == Fraction(K - 1, K) == Fraction(11, 12)
    assert TARGET_RETURN_PROB == Fraction(1, K) == Fraction(1, 12)


def test_resource_clifford_and_dimensionful_requirements():
    assert RESOURCE_LADDER == [120, 240, 480, 960]
    assert CLIFFORD_QUOTIENTS == [432, 216, 108, 54]
    assert len(REQUIRED_DIMENSIONFUL_ANCHORS) == 3


def test_dictionary_and_rules_shape():
    entries = observable_dictionary()
    rules = scale_map_rules()
    assert len(entries) == 10
    assert len(rules) == 5
    assert any(entry.id == "M0-FUSION-TRIALS" and entry.w33_value == "480" for entry in entries)
    assert any(entry.id == "M2-DIMENSIONFUL-MAP" and entry.w33_value == "not fixed in v1" for entry in entries)
    assert any(rule.id == "NO_REFIT" for rule in rules)


def test_threshold_relations():
    assert (J * J_inv) % Phi3 == 1
    assert Phi6 + 1 == J_inv


def test_audit_checks_all_true():
    audit = scale_map_v1_audit()
    assert all(audit["checks"].values())
    assert audit["exact_targets"]["nonreverse_probability"] == "11/12"
