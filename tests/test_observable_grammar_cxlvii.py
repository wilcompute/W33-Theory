from fractions import Fraction

from PART_CXLVII_OBSERVABLE_GRAMMAR import (
    CARRIER,
    IMBALANCE,
    K,
    MU,
    PHI3,
    PHI4,
    Q,
    THRESHOLD,
    exact_checks,
    grammar_relations,
    grammar_tokens,
    observable_grammar_audit,
)


def test_base_mixer_tokens():
    assert CARRIER == Fraction(8, 13)
    assert THRESHOLD == Fraction(5, 13)
    assert CARRIER + THRESHOLD == 1


def test_imbalance_is_q_over_phi3():
    assert IMBALANCE == Fraction(3, 13)
    assert IMBALANCE == Fraction(Q, PHI3)


def test_complements_match_phi4_and_heavy_branch():
    assert 1 - IMBALANCE == Fraction(PHI4, PHI3)
    assert 1 + IMBALANCE == Fraction(K + MU, PHI3)


def test_q_lifts_match_expected_observables():
    assert Q * CARRIER == Fraction(24, 13)
    assert Q * THRESHOLD == Fraction(15, 13)
    assert Q * IMBALANCE == Fraction(9, 13)
    assert Q * CARRIER + Q * THRESHOLD == Q


def test_fibonacci_ratio():
    assert CARRIER / THRESHOLD == Fraction(8, 5)


def test_grammar_tokens_include_key_classifications():
    by_name = {t.name: t for t in grammar_tokens()}
    assert by_name["q_lift_carrier"].value == "24/13"
    assert by_name["imbalance"].value == "3/13"
    assert by_name["phi4_complement"].value == "10/13"
    assert by_name["heavy_plus_branch"].value == "16/13"


def test_exact_checks_all_true_and_relations_present():
    assert all(exact_checks().values())
    rel = grammar_relations()
    assert rel["qcd_bare_factor"] == "q*C = 24/13"
    assert rel["fibonacci_ratio"] == "C/T = 8/5"


def test_audit_records_finite_observable_grammar():
    audit = observable_grammar_audit()
    assert audit["base_mixer"]["carrier"] == "8/13"
    assert audit["base_mixer"]["threshold"] == "5/13"
    assert audit["base_mixer"]["imbalance"] == "3/13"
    assert "finite observable grammar" in audit["theorem_statement"]
