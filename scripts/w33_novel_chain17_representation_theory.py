"""
W33 Theory — Chain 17: Representation Theory of SL/GL/PSL over F_q
===================================================================
The orders of the linear groups over F_3 are exact W33 constants.
"""
from math import factorial
from fractions import Fraction
import math

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12

def test_SL2_order_equals_f():
    """  |SL(2,F_3)| = q*(q^2-1) = 24 = f."""
    assert q*(q**2-1) == f
    print(f"PASS  |SL(2,F_3)| = q*(q^2-1) = {f} = f")

def test_PSL2_order_equals_k_reg():
    """  |PSL(2,3)| = f/gcd(2,q-1) = f/2 = 12 = k_reg ≅ A_4."""
    assert f // math.gcd(2, q-1) == k_reg
    print(f"PASS  |PSL(2,3)| = f/2 = {k_reg} = k_reg ≅ A_4")

def test_SL2_irrep_count_equals_Phi6():
    """SL(2,F_3) has exactly 7 = Phi6 irreducible representations."""
    irrep_dims = [1,1,1,2,2,2,3]
    assert len(irrep_dims) == Phi6
    assert sum(d**2 for d in irrep_dims) == f   # Peter-Weyl
    assert max(irrep_dims) == q
    print(f"PASS  |Irr(SL(2,3))| = {len(irrep_dims)} = Phi6, sum_sq = f = {f}")

def test_GL2_order_equals_2f():
    """  |GL(2,F_3)| = (q^2-1)(q^2-q) = 8*6 = 48 = 2*f."""
    assert (q**2-1)*(q**2-q) == 2*f
    print(f"PASS  |GL(2,F_3)| = {(q**2-1)*(q**2-q)} = 2*f")

def test_PGL3_order():
    """  |PGL(3,F_3)| = 5616 = 2^4*q^3*Phi3, and /f = 234 = 2*q^2*Phi3."""
    order = (q**3-1)*(q**3-q)*(q**3-q**2)//(q-1)
    assert order == 5616 == 2**4 * q**3 * Phi3
    assert 5616 // f == 234 == 2 * q**2 * Phi3
    print(f"PASS  |PGL(3,3)| = {order} = 2^4*q^3*Phi3")
    print(f"PASS  |PGL(3,3)|/f = 234 = 2*q^2*Phi3")

if __name__ == "__main__":
    print("=" * 55)
    print("W33 Chain 17: Representation Theory")
    print("=" * 55)
    test_SL2_order_equals_f()
    test_PSL2_order_equals_k_reg()
    test_SL2_irrep_count_equals_Phi6()
    test_GL2_order_equals_2f()
    test_PGL3_order()
    print("\nALL 5 TESTS PASS")
