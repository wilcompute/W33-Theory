"""
Part CDLXVI Verifier: W33 Spectral Bridge to Moonshine
"""
from math import factorial, gcd

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7; V=27; r=4; s=-2

# Eigenvalue multiplicities: r=4 has mult u=6, s=-2 has mult 20
assert K + u*r + 20*s == 0
assert 1 + u + 20 == V
print('Eigenvalue multiplicities verified ✓')

# Spectral parameter encoding
assert LAM == r*(r+1)//2
assert MU  == r*abs(s)
assert u   == r+abs(s)
print('Spectral parameter encoding verified ✓')

# Trace chain
assert K**2 + u*(r**2) + 20*(s**2) == 2*u**3
assert K**3 + u*(r**3) + 20*(s**3) == 6*factorial(u)
assert K**4 + u*(r**4) + 20*(s**4) == PKT*MU*V*(K-p)
print('Spectral trace chain verified ✓')

# Ihara factors
assert 1-r+(K-1) == MU1
assert 1-s+(K-1) == 2*p**2
print('Ihara factors verified ✓')

# E4 bridge
assert LAM*PKT == 240
assert MU*V*LAM == 2160
print('E4 Eisenstein W33 bridge verified ✓')

# dim(Griess)
assert (LAM*r+C_V)*(5*MU1-1)*(p*PKT-1) == 196883
print('dim(Griess) via eigenvalue r verified ✓')

# Triangle count
assert V*K*LAM//6 == factorial(u)
print('Triangle count = u! verified ✓')

print('ALL CDLXVI ASSERTIONS PASSED')
