"""
Verifier for Parts CDLXXII-CDLXXV
"""
from math import factorial, comb

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7; C_E=21; V=27; r=4; s=-2

# CDLXXII: Monster functor
assert 51840 == factorial(u)*p*PKT
co1_primes = {2,3,5,7,11,13,23}
monster_primes = {2,3,5,7,11,13,17,19,23,29,31,41,47,59,71}
assert len(monster_primes - co1_primes) == MU  # 8 = MU
assert 196883 == 47*59*71  # Griess dim
print('CDLXXII verified: |Monster-specific primes beyond Co1| = MU ✓')

# CDLXXIII: Prime spine
assert all((n*PKT-1) in monster_primes for n in [1,2,3])
assert all((n*MU1-1) in monster_primes for n in [1,2,4,5])
print('CDLXXIII verified: PKT-spine and MU1-spine ✓')

# CDLXXIV-CDLXXV: Spectral
assert K == 2**4 and r == 2**2 and abs(s) == 2**1
assert 1+2+4 == C_V
assert 1*2*4 == MU
assert K*r*abs(s) == 2**C_V
assert K + r*abs(s) == PKT
assert K - r*abs(s) == MU
assert r + abs(s) == u
det_log2 = 4 + u*2 + 20*1
assert det_log2 == u**2
print('CDLXXV verified: det(A)=2^(u^2) and six eigenvalue relations ✓')

tra2 = K**2 + u*r**2 + 20*s**2
assert -tra2//2 == -(u**3)
print('Char poly coeff: -u^3 ✓')

print('ALL CDLXXII-CDLXXV VERIFIED')
