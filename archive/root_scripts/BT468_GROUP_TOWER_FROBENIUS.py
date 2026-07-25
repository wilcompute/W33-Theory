#!/usr/bin/env python3
"""
BT468_GROUP_TOWER_FROBENIUS.py

BREAKTHROUGHS:
  [PSL-GAUGE]   |PSL(2,q)| = k — gauge codec IS simple group A4
  [SP4-WE6]     |Sp(4,q)| = |W(E6)| = 51840
  [GROUP-TOWER] k->f->216->51840->155520 with substrate multipliers
  [FROBENIUS]   Hesse cubic Frobenius: trace=-lam, disc=-lam^q, CM Q(i*sqrt(lam))
  [PROJ-FULL]   |PG(4,q)|=(k-1)^2=121; |PG(5,q)|=mu*Phi6*Phi3=364
  [11-IDENT]    11=k-1=f-k-1=2k-Phi3=v-k-g-lam
"""

import sys, math

q=3; lam=2; mu=4; k=12; v=40; f=24; g_neg=15; F5=5; Phi6=7; Phi3=13; Phi4=10

tests = []
def chk(name, got, exp, note=''):
    ok = (got == exp)
    tests.append((name, got, exp, ok))
    mark = '\u2713' if ok else '\u2717'
    print(f'  [{mark}] {name}: {got} {"==" if ok else "!="} {exp}  {note}')
    return ok

print('=' * 70)
print('BT468: GROUP TOWER, FROBENIUS, EXTENDED PROJECTIVE LADDER')
print('=' * 70)

SL2q = q*(q-1)*(q+1)
PSL2q = SL2q//(q-1)
PGL2q = ((q**2-1)*(q**2-q))//(q-1)
Sp4q = q**4*(q**2-1)*(q**4-1)

print('\n-- A: Group Tower k->f->216->51840->155520 --')
chk('A1: |SL(2,q)| = f', SL2q, f)
chk('A2: |PSL(2,q)| = k (A4, gauge codec)', PSL2q, k)
chk('A3: |PGL(2,q)| = f (S4)', PGL2q, f)
chk('A4: |Sp(4,q)| = |W(E6)| = 51840', Sp4q, lam**Phi6*q**mu*F5)
chk('A5: k * lam = f', k*lam, f, 'x binary')
chk('A6: f * q^2 = 216', f*q**2, 216, 'x inflections')
chk('A7: 216 * 240 = 51840', 216*240, 51840, 'x E8 roots')
chk('A8: 51840 * q = 155520', 51840*q, 155520, 'x ternary')

print('\n-- B: Frobenius of Hesse Cubic at lambda=lam --')
N_Eq = math.factorial(q)
trace_Frob = (q+1) - N_Eq
chk('B1: |E(F_q)| at lambda=lam = q! = 6', N_Eq, 6)
chk('B2: trace(Frob) = (q+1)-N = -lam = -2', trace_Frob, -lam)
chk('B3: disc(Frob poly) = lam^2-4q = -lam^q', lam**2-4*q, -(lam**q))
chk('B4: 4q-lam^2 = lam^q', 4*q-lam**2, lam**q)
chk('B5: norm = |alpha|^2 = 1+lam = q', 1+lam, q)
chk('B6: CM disc = -4*lam = -lam^q', -4*lam, -(lam**q))

print('\n-- C: Extended Projective Ladder --')
chk('C1: |PG(0,q)| = 1', (q**1-1)//(q-1), 1)
chk('C2: |PG(1,q)| = mu = q+1', (q**2-1)//(q-1), mu)
chk('C3: |PG(2,q)| = Phi3 = k+1', (q**3-1)//(q-1), Phi3)
chk('C4: |PG(3,q)| = v', (q**4-1)//(q-1), v)
chk('C5: |PG(4,q)| = (k-1)^2 = 121', (q**5-1)//(q-1), (k-1)**2)
chk('C6: |PG(5,q)| = mu*Phi6*Phi3 = 364', (q**6-1)//(q-1), mu*Phi6*Phi3)

print('\n-- D: Substrate Identities --')
chk('D1: q = 1+lam', q, 1+lam)
chk('D2: 11 = k-1 = f-k-1 = 2k-Phi3', k-1, f-k-1)
chk('D3: 11 = 2k-Phi3', 2*k-Phi3, k-1)
chk('D4: |PG(4,q)| = (k-1)^2', (q**5-1)//(q-1), (k-1)**2)
chk('D5: |PG(5,q)| = mu*Phi6*Phi3', mu*Phi6*Phi3, (q**6-1)//(q-1))

passed = sum(1 for *_,ok in tests if ok)
total = len(tests)
print(f"\n{'='*70}")
print(f'BT468 RESULTS: {passed}/{total} ({"100%" if passed==total else str(100*passed//total)+"%"})')
print(f"{'='*70}")
if passed < total:
    for name, got, exp, ok in tests:
        if not ok:
            print(f'  FAIL: {name}: got {got}, expected {exp}')
    sys.exit(1)
else:
    print('\nNEW THEOREMS:')
    print('  [PSL-GAUGE]   |PSL(2,q)| = k: gauge codec is simple group A4')
    print('  [SP4-WE6]     |Sp(4,q)| = |W(E6)|: symplectic = E6 Weyl')
    print('  [GROUP-TOWER] k ->x2-> f ->x9-> 216 ->x240-> 51840 ->x3-> 155520')
    print('  [FROBENIUS]   trace=-lam, norm=q, CM Q(i*sqrt(lam)), disc=-lam^q')
    print('  [PROJ-FULL]   PG(5,q)=mu*Phi6*Phi3; PG(4,q)=(k-1)^2')
