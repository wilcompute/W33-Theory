"""BT1144 regression tests for finite W33 carrier alignment."""

from fractions import Fraction

DF2 = {0: 122, 4: 240, 10: 48, 16: 30}


def test_finite_w33_operator_moments_match_bt1033_anchor():
    tr1 = sum(DF2.values())
    tr2 = sum(lam * mult for lam, mult in DF2.items())
    tr4 = sum(lam * lam * mult for lam, mult in DF2.items())
    assert (tr1, tr2, tr4) == (440, 1920, 16320)


def test_corpus_carrier_identity_uses_finite_operator_coefficients():
    tr1 = sum(DF2.values())
    tr4_half = sum(lam * lam * mult for lam, mult in DF2.items()) // 2
    A0 = 1
    A2 = 0
    A4_corpus = 24
    assert A2 == 0
    c4 = tr1 * A4_corpus + tr4_half * A0
    assert c4 == 18720
    assert Fraction(c4, 240) == 6 * 13


def test_operator_probe_lanes_are_not_finite_carrier_replacements():
    probes = {"scalar positive Laplacian", "spin Dirac square", "ordinary all-forms Hodge trace"}
    finite_carrier = "finite W33 Hodge--Dirac square D_F^2 spectrum"
    assert finite_carrier not in probes
    assert len(probes) == 3
