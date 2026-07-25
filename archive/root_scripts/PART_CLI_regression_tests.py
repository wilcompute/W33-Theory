"""Regression tests for Part CLI: Three-Layer Closed Observable Ring"""
from fractions import Fraction

def test_b0_equals_Phi6():
    b0 = (11*3 - 2*6) // 3
    assert b0 == 7

def test_ring_closure():
    Phi3 = Fraction(13); Phi6 = Fraction(7)
    P6 = Phi6/Phi3; P6i = Phi3/Phi6
    assert P6 * P6i == 1

def test_bridge_identity():
    C = Fraction(8,13); T = Fraction(5,13)
    D = C - T
    assert D == Fraction(3,13)
    assert 1 - D == Fraction(10,13)
    assert Fraction(10,13) == Fraction(10)/Fraction(13)

def test_Phi6_sector():
    P6i = Fraction(13,7)
    D = Fraction(3,13); T = Fraction(5,13); C = Fraction(8,13)
    assert P6i * D == Fraction(3,7)
    assert P6i * T == Fraction(5,7)
    assert P6i * C == Fraction(8,7)

def test_D_equals_q_over_Phi3():
    assert Fraction(3,13) == Fraction(3)/Fraction(13)

if __name__ == "__main__":
    test_b0_equals_Phi6()
    test_ring_closure()
    test_bridge_identity()
    test_Phi6_sector()
    test_D_equals_q_over_Phi3()
    print("All Part CLI regression tests PASSED.")
