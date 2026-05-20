"""Tests for W(3,3) CTQW revival spectrum (MCXLVII)."""
from fractions import Fraction
from analysis.w33_ctqw_revival_spectrum import ctqw_revival_spectrum_packet


def _frac(entry):
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def test_eigenvalue_differences():
    p = ctqw_revival_spectrum_packet()
    d = p["eigenvalue_differences"]
    assert d["k_minus_r"] == 10
    assert d["r_minus_s"] == 6
    assert d["k_minus_s"] == 16


def test_gcd_equals_r_and_lambda():
    p = ctqw_revival_spectrum_packet()
    assert p["eigenvalue_differences"]["gcd"] == 2
    assert p["gcd_triple_coincidence"]["gcd_equals_r"]
    assert p["gcd_triple_coincidence"]["gcd_equals_lam"]


def test_quantum_revival_verified():
    p = ctqw_revival_spectrum_packet()
    assert p["quantum_revival"]["exact_revival_verified"]
    assert p["quantum_revival"]["check_k"]
    assert p["quantum_revival"]["check_r"]
    assert p["quantum_revival"]["check_s"]


def test_partial_revival():
    p = ctqw_revival_spectrum_packet()
    pr = p["partial_revival"]
    assert pr["partial_revival_verified"]
    # At T*/2=pi/2: r-eigenspace has phase -1, others +1
    assert "+1" in pr["phase_k_eigenspace"]
    assert "-1" in pr["phase_r_eigenspace"]
    assert "+1" in pr["phase_s_eigenspace"]


def test_clique_power_identity():
    p = ctqw_revival_spectrum_packet()
    cp = p["clique_power_identity"]
    assert cp["omega"] == 4
    assert cp["r"] == 2
    assert cp["clique_power_verified"]
    assert cp["log2_omega_equals_r"]


def test_spectral_triple_coincidence():
    p = ctqw_revival_spectrum_packet()
    tc = p["spectral_triple_coincidence"]
    assert tc["r_equals_lambda"]
    assert tc["r_equals_log2_omega"]
    assert tc["r_equals_gcd_diffs"]
    assert tc["triple_verified"]


def test_binary_tetrahedral_match():
    p = ctqw_revival_spectrum_packet()
    pb = p["physics_bridge"]
    assert pb["mult_r"] == 24
    assert pb["sl23_order"] == 24
    assert pb["binary_tetrahedral_match"]


def test_revival_period_symbolic():
    """T* = 2*pi/r = 2*pi/2 = pi (represented as pi-coefficient = 1)."""
    p = ctqw_revival_spectrum_packet()
    coeff = _frac(p["quantum_revival"]["revival_period_rational_pi_coeff"])
    assert coeff == Fraction(1, 1)
