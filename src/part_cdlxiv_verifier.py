"""
Part CDLXIV Verifier: Grand Master Moonshine Theorem
"""
from math import gcd

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7; V=27

# All c_g(1) W33 expressions
assert (LAM*(p+1)+C_V)*(5*MU1-1)*(p*PKT-1) == 196883
assert 196883 + 1 == 196884
assert p*(u**2-u+1)*(LAM*(p+1)+C_V) == 4371
assert 4371 + 1 == 4372
assert 4*(u**2-u+1)*(p*K-C_V)*(5*MU1-1)*(p*PKT-1) == 21296876
assert gcd(196883, 21296876) == 59*71
assert 21296876 * (LAM*(p+1)+C_V) == 196883 * 4*(u**2-u+1)*(p*K-C_V)
assert PKT*p + C_V == 79
assert (p-1)*(PKT*p-(u-1)) == 134
assert MU1*(PKT-1) == 276
assert V*(PKT+(u-1)) == 783
assert (p+1)*(LAM*(p+1)*V+(K-p)) == 4372
print('All Part CDLXIV assertions passed ✓')
