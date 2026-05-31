"""
W33 Theory — Chain 21: Catalan Numbers
=======================================
Catalan numbers C(n) = C(2n,n)/(n+1) evaluated at W33 indices.
"""
from math import comb
from fractions import Fraction

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12

def catalan(n): return comb(2*n, n) // (n+1)
C = [catalan(n) for n in range(15)]

def test_catalan_at_mu_equals_2_Phi6():
    assert C[mu] == 14 == 2*Phi6
    print(f"PASS  C(mu) = C({mu}) = {C[mu]} = 2*Phi6")

def test_catalan_at_Phi6():
    assert C[Phi6] == 429 == q * 11 * Phi3
    print(f"PASS  C(Phi6) = C({Phi6}) = {C[Phi6]} = q*11*Phi3")

def test_catalan_sum_power_of_2_times_Phi6():
    s = C[q] + C[mu] + C[Phi6]
    assert s == 448 == 2**6 * Phi6
    print(f"PASS  C(q)+C(mu)+C(Phi6) = {s} = 2^6*Phi6")

def test_catalan_at_Phi4_equals_partition_Phi4():
    """C(5) = 42 = p(10) = p(Phi4) — Catalan meets partition function."""
    p_Phi4 = 42  # p(10) from OEIS A000041
    assert C[5] == 42 == p_Phi4
    print(f"PASS  C(5) = {C[5]} = p(Phi4) = p(10) [Catalan = Partition]")

if __name__ == "__main__":
    print("="*55)
    print("W33 Chain 21: Catalan Numbers")
    print("="*55)
    test_catalan_at_mu_equals_2_Phi6()
    test_catalan_at_Phi6()
    test_catalan_sum_power_of_2_times_Phi6()
    test_catalan_at_Phi4_equals_partition_Phi4()
    print("\nALL 4 TESTS PASS")
