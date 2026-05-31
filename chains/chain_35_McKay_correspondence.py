"""
Chain 35: McKay Correspondence — Binary Icosahedral Group I* and E8

The McKay correspondence maps:
  Binary icosahedral group I* ↔ E8 extended Dynkin diagram

Key identities:
  |I*| = 120 = Phi4 * k_reg = mu * h_E8
  Irrep dimensions: [1,2,3,4,5,6,4,2,3]
  Sum of irrep dims = h_E8 = 30  [THE McKAY MIRACLE]
  Max irrep dim = q! = 6
  Number of irreps = 2^q + 1 = 9
  Sum of squares of irrep dims = |I*| = 120
"""

from math import factorial

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12

I_IRREPS = [1, 2, 3, 4, 5, 6, 4, 2, 3]

def test_binary_icosahedral_order():
    """| I* | = 120 = Phi4*k_reg = mu*h_E8"""
    I_order = 120
    assert I_order == Phi4 * k_reg
    assert I_order == mu * h_E8
    assert I_order == 2**q * q * 5
    return True

def test_McKay_miracle_sum():
    """Sum of I* irrep dims = h_E8 = 30  [The McKay Miracle]"""
    s = sum(I_IRREPS)
    assert s == h_E8
    assert s == 30
    return True

def test_McKay_irrep_max():
    """Max I* irrep dim = q! = 6"""
    assert max(I_IRREPS) == factorial(q)
    return True

def test_McKay_irrep_count():
    """Number of I* irreps = 2^q + 1 = 9 (= rank(E8) + 1)"""
    n = len(I_IRREPS)
    assert n == 2**q + 1
    assert n == 9  # extended E8 Dynkin has 9 nodes
    return True

def test_McKay_sum_of_squares():
    """Sum of squares of I* irrep dims = |I*| = 120"""
    ss = sum(d**2 for d in I_IRREPS)
    assert ss == 120
    assert ss == Phi4 * k_reg
    return True

if __name__ == '__main__':
    tests = [
        test_binary_icosahedral_order,
        test_McKay_miracle_sum,
        test_McKay_irrep_max,
        test_McKay_irrep_count,
        test_McKay_sum_of_squares,
    ]
    for t in tests:
        t()
        print(f'  PASS: {t.__name__}')
    print(f'\n5/5 Chain 35 ALL PASS')
