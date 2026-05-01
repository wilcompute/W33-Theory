from fractions import Fraction

from PART_CXLVIII_GRAMMAR_TAGGER import (
    grammar_dictionary,
    grammar_tagger_audit,
    tag_value,
    canonical_observables,
    unmatched_probe_values,
)


def test_dictionary_tags_core_mixer_values():
    d = grammar_dictionary()
    assert d[Fraction(8, 13)].grammar_class == "base/carrier"
    assert d[Fraction(5, 13)].grammar_class == "base/threshold"
    assert d[Fraction(3, 13)].grammar_class == "imbalance"


def test_dictionary_tags_complement_and_plus_branch():
    d = grammar_dictionary()
    assert d[Fraction(10, 13)].operation == "1-D"
    assert d[Fraction(16, 13)].operation == "1+D"


def test_dictionary_tags_q_lifts():
    d = grammar_dictionary()
    assert d[Fraction(24, 13)].operation == "q*C"
    assert d[Fraction(15, 13)].operation == "q*T"
    assert d[Fraction(9, 13)].operation == "q*D"


def test_dictionary_tags_inverses():
    d = grammar_dictionary()
    assert d[Fraction(13, 3)].grammar_class == "inverse/imbalance"
    assert d[Fraction(13, 10)].grammar_class == "inverse/complement"
    assert d[Fraction(13, 24)].grammar_class == "inverse/q_lift_carrier"


def test_tag_value_matches_and_rejects_exactly():
    matched = tag_value("qcd", Fraction(24, 13))
    assert matched.matched is True
    assert matched.tag_name == "qC"

    unmatched = tag_value("phi6", Fraction(7, 13))
    assert unmatched.matched is False
    assert unmatched.tag_name is None


def test_all_canonical_observables_match():
    assert all(t.matched for t in canonical_observables())


def test_probe_values_are_not_basic_grammar_tokens_yet():
    probes = {p.label: p for p in unmatched_probe_values()}
    assert probes["phi6_over_phi3"].matched is False
    assert probes["hashimoto_norm_over_phi3"].matched is False
    assert probes["k_over_phi3"].matched is False
    assert probes["phi3_over_phi6"].matched is False


def test_audit_boundary_checks():
    audit = grammar_tagger_audit()
    assert audit["checks"]["all_canonical_match"] is True
    assert audit["checks"]["phi6_over_phi3_not_yet_basic_token"] is True
    assert audit["checks"]["hashimoto_norm_over_phi3_not_yet_basic_token"] is True
    assert "not automatically promoted" in audit["theorem_statement"]
