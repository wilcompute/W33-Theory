#!/usr/bin/env python3
from math import isqrt
r,q,Phi3,v,g2 = 2,3,13,40,6
l1,l2 = 10,16
m1,m2 = 24,15
print('SPECTRAL COMPRESSION VERIFIER')
print('sum eigen=', l1+l2, 'expected', r*Phi3)
print('prod eigen=', l1*l2, 'expected', r*r*v)
print('gap eigen=', l2-l1, 'expected', g2)
Dspec = (l1+l2)**2 - 4*(l1*l2)
print('disc eigen=', Dspec, 'expected', g2*g2)
print('roots eigen=', ((r*Phi3-g2)//2, (r*Phi3+g2)//2))
print('sum mult=', m1+m2, 'expected', q*Phi3)
print('prod mult=', m1*m2, 'expected', q*q*v)
print('gap mult=', m1-m2, 'expected', q*q)
Dmult = (m1+m2)**2 - 4*(m1*m2)
print('disc mult=', Dmult, 'expected', q**4)
print('roots mult=', ((q*Phi3+q*q)//2, (q*Phi3-q*q)//2))
assert l1+l2 == r*Phi3
assert l1*l2 == r*r*v
assert l2-l1 == g2
assert Dspec == g2*g2
assert ((r*Phi3-g2)//2, (r*Phi3+g2)//2) == (10,16)
assert m1+m2 == q*Phi3
assert m1*m2 == q*q*v
assert m1-m2 == q*q
assert Dmult == q**4
assert ((q*Phi3+q*q)//2, (q*Phi3-q*q)//2) == (24,15)
print('ALL SPECTRAL COMPRESSION IDENTITIES VERIFIED')
