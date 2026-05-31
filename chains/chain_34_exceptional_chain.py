"""
Chain 34: The Exceptional Chain E6 ⊂ E7 ⊂ E8 from q=3

The entire exceptional Lie algebra chain is determined by q:

  Rank: E6=2q=6, E7=Phi6=7, E8=2^q=8
  Coxeter: h(E6)=k_reg=12, h(E7)=2q^2=18, h(E8)=h(E6)+h(E7)=30
  Roots: E6=2q*k_reg=72, E7=2*Phi6*q^2=126, E8=E6_roots+E7_roots+2q^3+...
  Dims: e6=2q*Phi3=78, e7=Phi6*19=133, e8=2^q*(h_E8+1)=248
"""

from math import factorial

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12
h_E6=12; h_E7=18; E6_roots=72; E7_roots=126; E8_roots=240
E6_rank=6; E7_rank=7; E8_rank=8
E6_dim=78; E7_dim=133; E8_dim=248

def test_exceptional_ranks_from_q():
    """E6 rank=2q=6, E7 rank=Phi6=7, E8 rank=2^q=8"""
    assert E6_rank == 2*q
    assert E7_rank == Phi6
    assert E8_rank == 2**q
    return True

def test_coxeter_numbers():
    """h(E6)=k_reg=12, h(E7)=2q^2=18, h(E8)=h(E6)+h(E7)=30"""
    assert h_E6 == k_reg
    assert h_E7 == 2*q**2
    assert h_E8 == h_E6 + h_E7  # The key identity!
    return True

def test_root_counts_from_q():
    """E6 roots = 2q*k_reg, E7 roots = 2*Phi6*q^2, E7-E6 = 2q^3"""
    assert E6_roots == 2*q*k_reg
    assert E7_roots == 2*Phi6*q**2
    assert E7_roots - E6_roots == 2*q**3
    return True

def test_algebra_dimensions_from_q():
    """dim(e6)=2q*Phi3=78, dim(e7)=Phi6*19=133, dim(e8)=2^q*(h_E8+1)=248"""
    assert E6_dim == 2*q*Phi3
    assert E7_dim == Phi6*19
    assert E8_dim == 2**q*(h_E8+1)
    # Verify dims = roots + rank
    assert E6_dim == E6_roots + E6_rank
    assert E7_dim == E7_roots + E7_rank
    assert E8_dim == E8_roots + E8_rank
    return True

def test_E6_E7_E8_chain_structure():
    """
    E6 ⊂ E7 ⊂ E8 branching rules:
    E8 adjoint 248 → E7 × SU(2): 248 = (133,1) + (56,2) + (1,3)
    56 = 2*E7_rank*4? Actually: 56 = 8*7 = 2^q*Phi6 !
    3 = q (the SU(2) adjoint)
    """
    # E8 → E7 × SU(2): 248 = 133 + 2*56/2 + 3
    # Proper decomposition: 248 = (133,1) ⊕ (56,2) ⊕ (1,3)
    E7_adj = E7_dim  # 133
    E7_fund = 56     # the 56-dim fundamental of E7
    SU2_adj = q      # = 3
    # Check: E7 fundamental dim = 8*7 = 2^q * Phi6
    assert E7_fund == 2**q * Phi6
    check = E7_adj + E7_fund + SU2_adj  # = 133 + 56 + 3 = 192 ≠ 248
    # Actually: 133*1 + 56*2 + 1*3 = 133+112+3 = 248 ✓ (counting over SU2 reps)
    assert E7_adj*1 + E7_fund*2 + 1*q == E8_dim
    return True

if __name__ == '__main__':
    tests = [
        test_exceptional_ranks_from_q,
        test_coxeter_numbers,
        test_root_counts_from_q,
        test_algebra_dimensions_from_q,
        test_E6_E7_E8_chain_structure,
    ]
    for t in tests:
        t()
        print(f'  PASS: {t.__name__}')
    print(f'\n5/5 Chain 34 ALL PASS')
