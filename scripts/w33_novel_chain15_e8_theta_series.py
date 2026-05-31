"""
W33 Theory — Chain 15: E8 Theta Series
=======================================
The theta series of the E8 lattice has coefficients a_n = 240*sigma_3(n).
Three new identities connect these coefficients to W33 constants.
"""
import math
from fractions import Fraction

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12; E8_roots=240

def sigma3(n):
    return sum(d**3 for d in range(1, n+1) if n % d == 0)

a = {n: 240 * sigma3(n) for n in range(1, 25)}

def test_theta_coeff_a1_equals_E8_roots():
    assert a[1] == E8_roots
    print(f"PASS  a_1 = {a[1]} = E8_roots")

def test_theta_coeff_a_q_divisible_by_h_E8():
    """h_E8 divides a_q: a_3 = 6720 = 224 * h_E8."""
    assert a[q] == 6720
    assert a[q] % h_E8 == 0
    assert a[q] // h_E8 == 224 == 2**5 * Phi6
    print(f"PASS  a_q = {a[q]}, a_q/h_E8 = {a[q]//h_E8} = 2^5*Phi6 = {2**5*Phi6}")

def test_theta_sum_first_q_coeffs():
    """sum(a_1 + a_2 + a_3) = 9120 = f * 380."""
    s = sum(a[n] for n in range(1, q+1))
    assert s == 9120 == f * 380
    print(f"PASS  sum(a_1..a_q) = {s} = f * 380")

def test_gosset_polytope_edges_equal_a_q():
    """4_21 Gosset polytope edges = 6720 = a_q (E8 theta coeff at index q)."""
    gosset_edges = 6720
    assert gosset_edges == a[q]
    gosset_faces = 60480
    assert gosset_faces // gosset_edges == q**2
    print(f"PASS  Gosset edges = {gosset_edges} = a_q, faces/edges = q^2 = {q**2}")

def test_e8_root_graph_regularity():
    """k_E8 = 56 = f*Phi6/q. Each E8 root has 56 neighbors at inner product 1."""
    k_E8 = 56
    assert Fraction(k_E8, f) == Fraction(Phi6, q)
    n_orth = 240 - 1 - k_E8 - k_E8 - 1
    assert n_orth == 126 == 2 * q**2 * Phi6
    print(f"PASS  k_E8 = {k_E8} = f*Phi6/q, orth roots = {n_orth} = 2*q^2*Phi6")

if __name__ == "__main__":
    print("=" * 55)
    print("W33 Chain 15: E8 Theta Series")
    print("=" * 55)
    test_theta_coeff_a1_equals_E8_roots()
    test_theta_coeff_a_q_divisible_by_h_E8()
    test_theta_sum_first_q_coeffs()
    test_gosset_polytope_edges_equal_a_q()
    test_e8_root_graph_regularity()
    print("\nALL 5 TESTS PASS")
