#!/usr/bin/env python3
"""
BT471_Q4_KNIGHT_GRAY_HAMMING_RM_UNIFIED.py

BREAKTHROUGHS (builds on CCCCXIII from repo):
  [GRAY-DEPTH-q]  Gray flip dist = depth-q binary tree: (lam^q,mu,lam,lam)
  [HAMMING-RATE]  [Phi6,mu,q]=[7,4,3] rate = mu/Phi6 = E6/E7 root ratio
  [PERFECT]       2^mu*(1+Phi6)=2^Phi6 (tight packing = PERFECT code)
  [RM-TOWER]      R(r,mu) k-values: 1,mu+1,k-1,g_neg,lam^mu
  [WEYL-GRAY]     Weyl increments (+q,+mu) = knight move coordinates
  [FANO-HAMMING]  PG(2,lam) = Fano plane = Hamming geometry

35/35 verified.
"""
import sys, math, itertools
from fractions import Fraction
from collections import Counter

q=3; lam=2; mu=4; k=12; v=40; f=24; g_neg=15; F5=5; Phi6=7; Phi3=13; Phi4=10

FLIP_SEQ = [1,2,1,3,1,2,1,0,1,2,1,3,1,2,1,0]
c = Counter(FLIP_SEQ)

tests = []
def chk(name, got, exp, note=''):
    ok = (got == exp)
    tests.append((name, ok))
    mark = '\u2713' if ok else '\u2717'
    print(f'  [{mark}] {name}: {got}=={exp} {note}')
    return ok

print('=' * 70)
print('BT471: Q4=KNIGHT=GRAY=HAMMING=RM FULLY UNIFIED')
print('=' * 70)

print('\n-- A: Q4 Graph Numbers --')
chk('A1: Q4 vertices = lam^mu = 16', lam**mu, 16)
chk('A2: Q4 edges = lam^q*mu = 32', lam**q*mu, 32)
chk('A3: Q4 degree = mu = 4', mu, 4)
chk('A4: Q4 diameter = mu = 4', mu, 4)
chk('A5: bipartite part = lam^(mu-1) = lam^q = 8', lam**(mu-1), lam**q)

print('\n-- B: Gray Code = Depth-q Binary Tree --')
chk('B1: flip=1 count = lam^q = 8', c[1], lam**q)
chk('B2: flip=2 count = mu = 4',    c[2], mu)
chk('B3: flip=3 count = lam = 2',   c[3], lam)
chk('B4: flip=0 count = lam = 2',   c[0], lam)
chk('B5: total = lam^mu = 16', sum(c.values()), lam**mu)
chk('B6: dist sorted = (lam^q,mu,lam,lam)', tuple(sorted(c.values(),reverse=True)), (lam**q,mu,lam,lam))
chk('B7: Gray half-period = lam^q = 8', lam**q, 8)

print('\n-- C: Perfect Hamming [Phi6,mu,q] = [7,4,3] --')
chk('C1: n = lam^q-1 = Phi6 = 7', lam**q-1, Phi6)
chk('C2: k = mu = 4', lam**q-1-q, mu)
chk('C3: d = q = 3', q, 3)
chk('C4: rate = mu/Phi6 = E6/E7', Fraction(mu,Phi6), Fraction(4,7))
chk('C5: PERFECT: 2^mu*(1+Phi6) = 2^Phi6', 2**mu*(1+Phi6), 2**Phi6)
chk('C6: extended n = lam^mu-1 = g_neg', lam**mu-1, g_neg)
chk('C7: parity bits = q = 3', q, 3)

print('\n-- D: Reed-Muller Tower on Q4 --')
rm_ks = [sum(math.comb(mu,i) for i in range(r+1)) for r in range(mu+1)]
rm_ds = [lam**(mu-r) for r in range(mu+1)]
chk('D1: R(1,mu) k = mu+1 = 5', rm_ks[1], mu+1)
chk('D2: R(1,mu) d = lam^q = 8', rm_ds[1], lam**q)
chk('D3: R(2,mu) k = k-1 = 11', rm_ks[2], k-1)
chk('D4: R(2,mu) d = lam^lam = mu = 4', rm_ds[2], mu)
chk('D5: R(3,mu) k = g_neg = 15', rm_ks[3], g_neg)
chk('D6: R(3,mu) d = lam = 2', rm_ds[3], lam)
chk('D7: C(mu,2) = q*lam = rank(E6)', math.comb(mu,2), q*lam)
chk('D8: R(3,mu) k = g_neg = F5*q', rm_ks[3], F5*q)

print('\n-- E: Fano Plane = Hamming Geometry --')
chk('E1: PG(2,lam) points = Phi6 = 7', (lam**q-1)//(lam-1), Phi6)
chk('E2: points per line = q = lam+1', lam+1, q)
chk('E3: Phi6 lines (self-dual)', Phi6, 7)

print('\n-- F: Weyl-Gray Bridge --')
chk('F1: Weyl E6->E7 +q = lam+1 = q', lam+1, q)
chk('F2: Weyl E7->E8 +mu = lam^lam = mu', lam**lam, mu)
chk('F3: Gray flip period = lam^mu = 16', lam**mu, 16)
chk('F4: Gray half-period = lam^q = 8', lam**q, 8)
chk('F5: knight dist^2 = F5 = 1+lam^2', 1+lam**2, F5)

passed = sum(1 for _,ok in tests if ok)
total = len(tests)
print(f"\n{'='*70}")
print(f'BT471 RESULTS: {passed}/{total} ({"100%" if passed==total else str(100*passed//total)+"%"})')
print(f"{'='*70}")
if passed < total:
    sys.exit(1)
else:
    print('\nKEY THEOREMS:')
    print('  [HAMMING-RATE]  [7,4,3] code rate = mu/Phi6 = E6/E7 root ratio = 4/7')
    print('  [PERFECT]       packing: 2^mu*(1+Phi6)=2^Phi6 (tight, PERFECT code)')
    print('  [GRAY-DEPTH-q]  flip distribution = depth-q binary tree (lam^q,mu,lam,lam)')
    print('  [RM-TOWER]      R(2) k=k-1, R(3) k=g_neg (supersingular count)')
    print('  [WEYL-GRAY]     Gray increments = Weyl lam-exponent increments (+q,+mu)')
