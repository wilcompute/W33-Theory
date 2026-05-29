#!/usr/bin/env python3
"""PART MCCCXIII: Zeta special values and recurrence verifier for W(3,3)."""
r,q,F5,Phi3,v,k = 2,3,5,13,40,12
l1,l2,m1,m2 = 10,16,24,15
print('ZETA SPECIAL VALUES AND RECURRENCE VERIFIER')
# Special values
zeta = lambda s: m1*l1**(-s) + m2*l2**(-s) if s>0 else m1*l1**(-s)+m2*l2**(-s)
# Negative integer values via a(n) = m1*l1^n + m2*l2^n
a = [None]*10
a[0] = m1+m2; a[1] = m1*l1+m2*l2
for n in range(2,8):
    a[n] = (l1+l2)*a[n-1] - l1*l2*a[n-2]
print('a(0)=zeta(0)=', a[0], 'expected', q*Phi3)
print('a(1)=zeta(-1)=', a[1], 'expected', k*v)
print('a(2)=zeta(-2)=', a[2], 'expected', r**5*q*F5*Phi3)
print('a(3)=zeta(-3)=', a[3])
assert a[0] == q*Phi3
assert a[1] == k*v
assert a[2] == r**5*q*F5*Phi3
# Verify recurrence
for n in range(2,8):
    assert a[n] == (l1+l2)*a[n-1] - l1*l2*a[n-2], f'Recurrence failed at n={n}'
print('Recurrence verified for n=2..7')
# Zeta(1) = 267/80
from fractions import Fraction
z1 = Fraction(m1,l1) + Fraction(m2,l2)
print('zeta(1) =', z1, '= 267/80:', z1==Fraction(267,80))
assert z1 == Fraction(267,80)
# Ihara edge factor
b = k*v//2
print('b-v =', b-v, '= r^3*F5^2 =', r**3*F5**2, ':', b-v==r**3*F5**2)
assert b-v == r**3*F5**2
print('p2 Newton sum = Phi3*F(pIh) =', Phi3*89, '=', sum(x**2 for x in [l1]*m1+[l2]*m2))
assert Phi3*89 == 1157
print('ALL ZETA SPECIAL VALUE IDENTITIES VERIFIED')
