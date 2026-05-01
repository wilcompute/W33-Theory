from fractions import Fraction

from PART_CL_TWO_LAYER_OBSERVABLE_ALGEBRA import (
    PHI3,
    PHI4,
    PHI6,
    HASHIMOTO_NORM,
    K,
    D,
    intersection_tokens,
    mixer_tokens,
    projection_tokens,
    two_layer_observable_algebra_audit,
)


def test_layers_intersect_only_at_10_over_13():
    inter = intersection_tokens()
    assert len(inter) == 1
    assert inter[0]["value"] == "10/13"


def test_bridge_token_has_two_meanings():
    assert 1 - D == Fraction(10, 13)
    assert Fraction(PHI4, PHI3) == Fraction(10, 13)


def test_qcd_bare_is_mixer_only():
    m = mixer_tokens()
    p = projection_tokens()
    assert Fraction(24, 13) in m
    assert Fraction(24, 13) not in p


def test_projection_only_tokens_remain_projection_only():
    m = mixer_tokens()
    p = projection_tokens()
    for value in [Fraction(PHI6, PHI3), Fraction(HASHIMOTO_NORM, PHI3), Fraction(K, PHI3), Fraction(PHI3, PHI6)]:
        assert value in p
        assert value not in m


def test_audit_checks_all_true():
    audit = two_layer_observable_algebra_audit()
    assert all(audit["checks"].values())
    assert len(audit["intersection"]) == 1
    assert audit["intersection"][0]["value"] == "10/13"


def test_layer_word_examples_include_qcd_and_bridge():
    audit = two_layer_observable_algebra_audit()
    words = {row["observable"]: row for row in audit["layer_word_examples"]}
    assert "QCD alpha_s(M_GUT) carrier" in words
    assert "Phi4 bridge / Ko complement" in words
    assert words["Phi4 bridge / Ko complement"]["word"] == "1-D = P(Phi4)"
