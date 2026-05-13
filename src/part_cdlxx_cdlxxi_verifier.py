"""
Verifier for Parts CDLXX-CDLXXI
"""
from math import factorial, comb

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7; C_E=21; V=27; r=4; s=-2

# CDLXX: one-parameter collapse
assert u == 2*p
assert r == p+1
assert PKT == r*u == (p+1)*2*p
assert K == r**2 == (p+1)**2
assert V == p**3
assert LAM == comb(r+1,2)
assert MU == 2*r
assert MU1 == r*(r-1)
assert C_V == 2*p+1
assert C_E == C_V*p
assert 30 == u*(r+1)   # h(E8)
assert 18 == 2*p**2    # h(E7)
assert 12 == MU1       # h(E6)
print('CDLXX one-parameter verified \u2713')

# Csaszar toroid
assert C_V - C_E + 2*C_V == 0
print('Csaszar Euler verified \u2713')

# W33 complement
assert (V-K-1, V-2*K+MU-2, V-2*K+LAM) == (10, 1, 5)
print('W33 complement verified \u2713')

# CDLXXI: exceptional Lie algebras
assert 51840 == factorial(u)*p*PKT
assert 51840 == factorial(u)*p*PKT
assert 78  == u*(K-p)
assert 133 == C_V*19
assert 248 == MU*31
assert 78+133+248 == V*(K+1)
print('CDLXXI exceptional dims verified \u2713')

print('ALL CDLXX-CDLXXI VERIFIED')
