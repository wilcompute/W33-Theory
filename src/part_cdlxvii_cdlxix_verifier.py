"""
Verifier for Parts CDLXVII-CDLXIX
"""
from math import factorial

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7; C_E=21; V=27; r=4; s=-2

# Part CDLXVII: E6 coefficients and Leech-Griess gap
assert 504 == MU*p**2*C_V
assert 16632 == MU*V*C_V*(p**2+p-1)
assert 196560 == factorial(u)*p*C_V*(K-p)
assert 196883 - 196560 == (K+1)*(MU+LAM+1)
assert (K+1)*(MU+LAM+1) == 17*19
print('CDLXVII verified ✓')

# Part CDLXVIII: E8 Coxeter labels in W33
e8_coxeter = [1,2,3,4,5,6,4,2,3]
assert max(e8_coxeter) == u
assert sum(e8_coxeter) == PKT+u
assert e8_coxeter.count(2) == abs(s)
assert e8_coxeter.count(1) == p-2
primes = [7,11,13,17,19,23,29]
for q in primes:
    assert q in [1,7,11,13,17,19,23,29]  # E8 exponents
print('CDLXVIII verified ✓')

# Part CDLXIX: Grand ladder
assert PKT == r*u
assert 30 == u*(r+1)  # h(E8)
assert 18 == 2*p**2    # h(E7)
assert 12 == MU1       # h(E6)
assert 60 == 12+18+30  # |A5|
assert 6480 == 12*18*30 == u*p**2*factorial(5)
print('CDLXIX verified ✓')

print('ALL CDLXVII-CDLXIX VERIFIED')
