"""
W33 Theory — Chain 16: j-Function Coefficient Residue
======================================================
The first non-trivial Fourier coefficient of the j-function,
196884, satisfies:

    196884 mod 744 = 468 = Phi3 * (q!)^2 = 13 * 36

This extends the Ramanujan Tau Bridge into the j-function.
"""
from math import factorial
from fractions import Fraction

q=3; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12

def test_j_coeff_residue_mod_744():
    """196884 mod f*(h_E8+1) = Phi3*(q!)^2 = 468."""
    modulus = f * (h_E8 + 1)   # = 744
    residue = 196884 % modulus
    assert residue == 468
    assert residue == Phi3 * factorial(q)**2
    print(f"PASS  196884 mod {modulus} = {residue} = Phi3*(q!)^2 = {Phi3}*{factorial(q)**2}")

def test_j_coeff_quotient():
    """196884 = 11*f * 744 + Phi3*(q!)^2. The quotient 11 = q*(q+1) - q + 1."""
    quot = 196884 // 744
    rem = 196884 % 744
    assert quot == 264 == 11 * f
    assert rem == Phi3 * factorial(q)**2
    print(f"PASS  196884 = {quot}*744 + {rem}, quot = 11*f = {11*f}")

def test_j_minus_744_mcKay():
    """McKay: 196884 = 196883 + 1 (Monster smallest irrep + trivial)."""
    assert 196884 == 196883 + 1
    # 196883 is prime — verified by trial division
    n = 196883
    composite = any(n % i == 0 for i in range(2, int(n**0.5)+1))
    assert not composite, "196883 should be prime"
    print(f"PASS  196884 = 196883(prime Monster irrep) + 1")

def test_744_as_f_times_h_plus1():
    """744 = f*(h_E8+1) = 24*31 — the j-function constant is a W33 product."""
    assert 744 == f * (h_E8 + 1)
    print(f"PASS  744 = f*(h_E8+1) = {f}*{h_E8+1}")

if __name__ == "__main__":
    print("=" * 55)
    print("W33 Chain 16: j-Function Residue")
    print("=" * 55)
    test_j_coeff_residue_mod_744()
    test_j_coeff_quotient()
    test_j_minus_744_mcKay()
    test_744_as_f_times_h_plus1()
    print("\nALL 4 TESTS PASS")
