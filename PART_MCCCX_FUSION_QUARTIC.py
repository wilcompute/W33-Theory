#!/usr/bin/env python3
from sympy import symbols, expand
r,q,F5,Phi3,v = 2,3,5,13,40
l1,l2 = 10,16
m1,m2 = 24,15
x = symbols('x')
print('SPECTRAL-MULTIPLICITY FUSION VERIFIER')
print('lambda1*m1 =', l1*m1)
print('lambda2*m2 =', l2*m2)
print('rqv =', r*q*v)
print('weighted trace =', l1*m1 + l2*m2, 'expected', 12*v)
print('full fused sum =', l1+l2+m1+m2, 'expected', F5*Phi3)
assert l1*m1 == l2*m2 == r*q*v
assert l1+l2+m1+m2 == F5*Phi3
assert l1*m1 + l2*m2 == 12*v
quartic = expand((x-l1)*(x-l2)*(x-m1)*(x-m2))
print(quartic)
assert quartic == x**4 - 65*x**3 + 1534*x**2 - 15540*x + 57600
assert 57600 == (r*q*v)**2
print('ratio eigen =', l1/l2)
print('ratio inv mult =', m2/m1)
assert l1*m1 == l2*m2
print('ALL FUSION IDENTITIES VERIFIED')
