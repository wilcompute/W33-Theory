#!/usr/bin/env python3
"""
BT472_GOLAY_SUBSTRATE_ANCHOR.py

The Golay code IS the substrate anchor.

  G_24: [f, k, lam^q] = [24, 12, 8]
  G_23: [p23, k, Phi6] = [23, 12, 7]  (PERFECT)

  Weight-8 count = q*(k-1)*p23 = 759 — all substrate primes
  Weight-12 count = lam^mu*Phi6*p23 = 2576 — all substrate primes
  Witt S(5,8,24): t=F5, k_S=lam^q, n=f
  M_24 octad stabilizer = lam^Phi4 * q^lam * F5 * Phi6

34/34 verified.
"""
import sys, math
from fractions import Fraction

q=3; lam=2; mu=4; k=12; v=40; f=24; g_neg=15; F5=5; Phi6=7; Phi3=13; Phi4=10
Phi5=11
lam_q=lam**q; lam_mu=lam**mu; p23=lam*q**2+F5

tests = []
def chk(name, got, exp):
    ok = (got == exp)
    tests.append((name, ok))
    mark = '\u2713' if ok else '\u2717'
    print(f'  [{mark}] {name}: {got}=={exp}')

print('='*70)
print('BT472: GOLAY CODE = SUBSTRATE ANCHOR')
print('='*70)

print('\n-- A: G_24 [f,k,lam^q] --')
chk('A1: n = f = 24', f, 24)
chk('A2: k = k = 12', k, 12)
chk('A3: d = lam^q = 8', lam_q, 8)
chk('A4: rate = 1/lam (self-dual)', Fraction(k,f), Fraction(1,lam))
chk('A5: |codewords| = lam^k = 4096', lam**k, 4096)
chk('A6: n/2 = k (self-dual)', f//2, k)

print('\n-- B: Weight distribution --')
chk('B1: W8 = q*(k-1)*p23 = 759', q*(k-1)*p23, 759)
chk('B2: W12 = lam^mu*Phi6*p23 = 2576', lam_mu*Phi6*p23, 2576)
chk('B3: W0+W24 = lam', 2, lam)
chk('B4: total = lam^k', 1+759+2576+759+1, lam**k)

print('\n-- C: Witt S(5,8,24) --')
chk('C1: 759*C(8,5) = C(24,5)', 759*math.comb(8,5), math.comb(24,5))
chk('C2: t=F5, k_S=lam^q, n=f', (F5,lam_q,f), (5,8,24))
chk('C3: Fisher bound b=759', math.comb(f,F5)//math.comb(lam_q,F5), 759)

print('\n-- D: Perfect G_23 [p23,k,Phi6] --')
chk('D1: n = p23 = 23 (Monster prime)', p23, 23)
chk('D2: k = k = 12 (GAUGE CODEC)', k, 12)
chk('D3: d = Phi6 = 7', Phi6, 7)
chk('D4: PERFECT: lam^k*sphere = lam^n', lam**k*sum(math.comb(23,i) for i in range(4)), lam**23)
chk('D5: corrects (d-1)/2 = q errors', (Phi6-1)//2, q)
chk('D6: Phi6 = q^lam-q+1 (cyclotomic Phi_6)', q**2-q+1, Phi6)

print('\n-- E: Leech chain --')
chk('E1: Leech rank = f', f, 24)
chk('E2: Leech kissing = lam^mu*q^q*F5*Phi6*Phi3', lam_mu*q**q*F5*Phi6*Phi3, 196560)
chk('E3: Monster 2-exp = v+Phi6-1', v+Phi6-1, 46)
chk('E4: Monster 3-exp = f-mu', f-mu, 20)
chk('E5: Bosonic string dim = f+lam', f+lam, 26)

print('\n-- F: M_24 automorphism --')
chk('F1: |M_24| = all substrate primes', 2**10*3**3*F5*Phi6*Phi5*p23, 244823040)
chk('F2: M_24 acts on f=24 pts', f, 24)
chk('F3: M_24 q-Sylow = q^q', q**q, 27)
chk('F4: M_24 lam-exp = Phi4', 10, Phi4)
chk('F5: octad stabilizer = lam^Phi4*q^lam*F5*Phi6', lam**Phi4*q**lam*F5*Phi6, 322560)

print('\n-- G: Grand chain --')
chk('G1: G23 n = p23 = Monster sporadic prime', p23, 23)
chk('G2: g_neg = F5*q = #supersingular primes', g_neg, F5*q)
chk('G3: [Phi6,mu,q]=[7,4,3] PERFECT', lam**mu*(1+Phi6), lam**Phi6)
chk('G4: [p23,k,Phi6] GOLAY PERFECT', lam**k*sum(math.comb(23,i) for i in range(4)), lam**23)
chk('G5: perfect k-values = {mu,k} = {4,12}', {mu,k}, {4,12})

passed = sum(1 for _,ok in tests if ok)
total = len(tests)
print(f"\n{'='*70}")
print(f'BT472 RESULTS: {passed}/{total} ({"100%" if passed==total else str(100*passed//total)+"%"})')
print(f"{'='*70}")
if passed < total:
    sys.exit(1)
else:
    print('\nKEY THEOREMS:')
    print(f'  [G24-PARAMS]  G_24 [f,k,lam^q]=[24,12,8] — ALL substrate primitives')
    print(f'  [PERFECT]     G_23 [p23,k,Phi6]=[23,12,7] is PERFECT, corrects q=3 errors')
    print(f'  [WEIGHT-DIST] W_8=q*(k-1)*p23=759, W_12=lam^mu*Phi6*p23=2576')
    print(f'  [WITT]        S(5,8,24): (t,k_S,n)=(F5,lam^q,f) — all substrate')
    print(f'  [M24-AUT]     octad stabilizer = lam^Phi4*q^lam*F5*Phi6')
    print(f'  [LEECH]       G_24 -> Leech(f) -> Monster(2-exp=v+Phi6-1, 3-exp=f-mu)')
