"""Tests for W(3,3) Kemeny spectral excess identity (MCXLIX)."""
from fractions import Fraction
from analysis.w33_kemeny_spectral_excess import kemeny_spectral_excess_packet


def _frac(entry):
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def test_kemeny_constant():
    p = kemeny_spectral_excess_packet()
    K = _frac(p["kemeny_constant"]["K"])
    assert K == Fraction(801, 20)


def test_kemeny_spectral_identity_K_equals_v_plus_r_over_v():
    p = kemeny_spectral_excess_packet()
    ks = p["kemeny_spectral_identity"]
    assert ks["K_equals_v_plus_r_over_v"]
    assert _frac(ks["formula_K"]) == Fraction(801, 20)


def test_kemeny_volume_identity_Kv_equals_v2_plus_r():
    p = kemeny_spectral_excess_packet()
    ks = p["kemeny_spectral_identity"]
    assert ks["Kv_equals_v2_plus_r"]
    assert ks["Kv"] == 1602
    assert ks["Kv_formula"] == 1602


def test_kemeny_excess_equals_r_over_v():
    p = kemeny_spectral_excess_packet()
    ks = p["kemeny_spectral_identity"]
    assert ks["kemeny_excess_identity"]
    excess = _frac(ks["K_minus_v"])
    r_over_v = _frac(ks["r_over_v"])
    assert excess == Fraction(1, 20)
    assert r_over_v == Fraction(1, 20)
    assert excess == r_over_v


def test_spectral_product_identity():
    p = kemeny_spectral_excess_packet()
    sp = p["spectral_product_identity"]
    assert sp["verified"]
    assert sp["product"] == 160
    assert sp["four_v"] == 160


def test_holographic_entropy_identities():
    p = kemeny_spectral_excess_packet()
    he = p["holographic_entropy"]
    S = _frac(he["S_from_alpha_r"])
    assert S == Fraction(20, 1)
    assert he["identity_v_half"]
    assert he["identity_BH"]
    assert _frac(he["S_from_v_half"]) == Fraction(20, 1)
    assert _frac(he["S_from_BH"]) == Fraction(20, 1)


def test_bekenstein_hawking():
    p = kemeny_spectral_excess_packet()
    bh = p["bekenstein_hawking"]
    G = _frac(bh["G_newton"])
    assert G == Fraction(3, 1)   # G = q = 3
    assert bh["G_equals_q"]
    assert bh["edges"] == 240
    assert bh["S_holo"] == 20


def test_kemeny_holographic_bridge():
    p = kemeny_spectral_excess_packet()
    kh = p["kemeny_holographic_bridge"]
    assert kh["verified"]
    assert _frac(kh["K_minus_v"]) == Fraction(1, 20)
    assert _frac(kh["one_over_S"]) == Fraction(1, 20)


def test_algebraic_proof():
    p = kemeny_spectral_excess_packet()
    ap = p["algebraic_proof"]
    assert ap["algebraic_check"]
    assert ap["num_physics_check"]
    assert ap["numerator"] == 8
    assert ap["denominator"] == 160
    assert ap["delta_ym"] == 5


def test_all_master_identities():
    p = kemeny_spectral_excess_packet()
    ids = p["master_identities_summary"]
    for name, val in ids.items():
        assert val, f"Master identity failed: {name}"
