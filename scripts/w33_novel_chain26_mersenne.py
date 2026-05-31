"""
W33 Theory — Chain 26: Mersenne Primes & Perfect Numbers
=========================================================
Mersenne primes and perfect numbers evaluated at W33 indices.

Key: M_q = Phi6  (Mersenne at q is Phi6)
     M_5 = h_E8+1  (5th Mersenne prime = Coxeter number + 1)
"""

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12

M = lambda p: 2**p - 1   # Mersenne number
P = lambda p: 2**(p-1) * (2**p - 1)  # Even perfect number (when M_p prime)

def test_Mersenne_q_equals_Phi6():
    """M_q = 2^3-1 = 7 = Phi6."""
    assert M(q) == Phi6
    print(f"PASS  M_q = 2^{q}-1 = {M(q)} = Phi6 = {Phi6}")

def test_Mersenne_5_equals_h_E8_plus_1():
    """M_5 = 2^5-1 = 31 = h_E8+1."""
    assert M(5) == h_E8 + 1
    print(f"PASS  M_5 = 31 = h_E8+1 = {h_E8+1}")

def test_Mersenne_Phi6_mod_h_E8():
    """M_Phi6 = 127, and 127 mod h_E8 = 7 = Phi6 (self-reference mod Coxeter)."""
    assert M(Phi6) % h_E8 == Phi6
    print(f"PASS  M_Phi6 = {M(Phi6)}, {M(Phi6)} mod h_E8 = {M(Phi6)%h_E8} = Phi6")

def test_perfect_q_equals_f_plus_mu():
    """P(q) = 4*7 = 28 = f+mu."""
    assert P(q) == f + mu
    print(f"PASS  P(q) = {P(q)} = f+mu = {f}+{mu}")

def test_perfect_5_equals_2_pow_4_times_h_plus_1():
    """P(5) = 16*31 = 496 = 2^4*(h_E8+1)."""
    assert P(5) == 2**4 * (h_E8 + 1)
    print(f"PASS  P(5) = {P(5)} = 2^4*(h_E8+1) = 16*{h_E8+1}")

if __name__ == "__main__":
    print("="*55)
    print("W33 Chain 26: Mersenne Primes & Perfect Numbers")
    print("="*55)
    test_Mersenne_q_equals_Phi6()
    test_Mersenne_5_equals_h_E8_plus_1()
    test_Mersenne_Phi6_mod_h_E8()
    test_perfect_q_equals_f_plus_mu()
    test_perfect_5_equals_2_pow_4_times_h_plus_1()
    print("\nALL 5 TESTS PASS")
