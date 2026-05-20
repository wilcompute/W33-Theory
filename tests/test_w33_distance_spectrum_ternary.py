"""Tests for W(3,3) distance-2 spectrum and ternary eigenvalue identity (MCL)."""
from fractions import Fraction
from analysis.w33_distance_spectrum_ternary import distance_spectrum_ternary_packet


def _frac(entry):
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def test_multiplicity_formulae():
    p = distance_spectrum_ternary_packet()
    m = p["multiplicity_formulae"]
    assert m["m_r"] == 24
    assert m["m_s"] == 15
    assert m["sum_is_v_minus_1"]
    assert _frac(m["m_r_exact"]) == Fraction(24, 1)
    assert _frac(m["m_s_exact"]) == Fraction(15, 1)


def test_multiplicity_gap_equals_q2():
    p = distance_spectrum_ternary_packet()
    m = p["multiplicity_formulae"]
    q = p["parameters"]["q"]
    assert m["gap_m_r_minus_m_s"] == q ** 2
    assert m["multiplicity_gap_is_q2"]


def test_distance_2_ternary_spectrum():
    p = distance_spectrum_ternary_packet()
    d = p["distance_2_eigenvalues"]
    q = p["parameters"]["q"]
    assert d["on_r_eigenspace"] == -q
    assert d["on_s_eigenspace"] == q
    assert d["a2_r_equals_neg_q"]
    assert d["a2_s_equals_pos_q"]
    assert d["ternary_spectrum_verified"]


def test_B_matrix_eigenvalues():
    p = distance_spectrum_ternary_packet()
    B = p["B_matrix"]
    q = p["parameters"]["q"]
    assert _frac(B["b_principal"]) == Fraction(q ** 2, 1)
    assert _frac(B["b_on_r"]) == Fraction(-1, 1)
    assert _frac(B["b_on_s"]) == Fraction(1, 1)
    assert B["b_principal_equals_q2"]


def test_trace_B_zero():
    p = distance_spectrum_ternary_packet()
    B = p["B_matrix"]
    assert _frac(B["trace_B"]) == Fraction(0, 1)
    assert B["trace_B_zero"]


def test_frobenius_norm_A():
    p = distance_spectrum_ternary_packet()
    F = p["frobenius_norms"]
    assert F["frobenius_A_identity"]
    assert F["frobenius_A_2edges"]
    assert F["norm_A_sq"] == F["norm_A_kv"] == F["norm_A_2edges"]


def test_frobenius_norm_A2():
    p = distance_spectrum_ternary_packet()
    F = p["frobenius_norms"]
    q = p["parameters"]["q"]
    v = p["parameters"]["v"]
    assert F["frobenius_A2_identity"]
    assert F["norm_A2_sq"] == q ** 3 * v
    assert F["norm_A2_q3v"] == q ** 3 * v


def test_frobenius_ratio():
    p = distance_spectrum_ternary_packet()
    F = p["frobenius_norms"]
    q = p["parameters"]["q"]
    assert F["ratio_identity"]
    assert _frac(F["ratio"]) == Fraction(q ** 2, q + 1)


def test_bm_algebra_square():
    p = distance_spectrum_ternary_packet()
    bm = p["bm_algebra_square"]
    assert bm["principal_check"]
    assert bm["nonprincipal_check"]
    assert bm["B2_minus_I_equals_2J"]
    assert _frac(bm["B2_minus_I_coeff"]) == Fraction(2, 1)


def test_annihilator_properties():
    p = distance_spectrum_ternary_packet()
    an = p["annihilator_properties"]
    assert an["A2_plus_q_on_r_eigenspace"] == 0
    assert an["A2_minus_q_on_s_eigenspace"] == 0
    assert an["A2_plus_q_kills_r_eigenspace"]
    assert an["A2_minus_q_kills_s_eigenspace"]


def test_all_master_identities():
    p = distance_spectrum_ternary_packet()
    ids = p["master_identities_summary"]
    for name, val in ids.items():
        assert val, f"MCL master identity failed: {name}"
