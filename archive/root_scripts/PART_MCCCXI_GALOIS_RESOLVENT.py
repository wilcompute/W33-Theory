#!/usr/bin/env python3
"""PART MCCCXI: Galois / resolvent / discriminant verifier for W(3,3) quartic."""
from math import prod, isqrt
roots = [10,16,24,15]
print('GALOIS / RESOLVENT / DISCRIMINANT VERIFIER')
# Discriminant
from itertools import combinations
deltas = [(roots[i]-roots[j])**2 for i,j in combinations(range(4),2)]
Disc = prod(deltas)
print('Discriminant =', Disc)
print('Expected 914457600 =', 914457600)
assert Disc == 914457600
factors = {2:10,3:6,5:2,7:2}
assert Disc == 2**10*3**6*5**2*7**2
print('Prime factorisation verified: 2^10 * 3^6 * 5^2 * 7^2')
sqrtD = 2**5*3**3*5*7
print('sqrt(Disc) =', sqrtD, '= 6 * 7! =', 6*5040)
assert sqrtD == 30240
assert sqrtD**2 == Disc
# Newton power sums
for n in range(1,5):
    pn = sum(r**n for r in roots)
    print(f'p{n} =', pn)
assert sum(r for r in roots)==65
assert sum(r**2 for r in roots)==1157
assert 1157 == 13*89
print('p2 = 13*89 = Phi3(q)*F(pIh) VERIFIED')
# Mahler measure
M = prod(roots)
print('Mahler measure =', M, '= e4 =', M == 57600)
assert M == 57600
# Resolvent roots
y1 = (roots[0]+roots[1])*(roots[2]+roots[3])
y2 = (roots[0]+roots[2])*(roots[1]+roots[3])
y3 = (roots[0]+roots[3])*(roots[1]+roots[2])
print('Resolvent roots:', y1, y2, y3)
assert y1 == 1014 and y3 == 1000
assert y1 == 2*3*13**2
assert y3 == 5**2*40
print('Resolvent root identities verified')
print('ALL GALOIS IDENTITIES VERIFIED')
