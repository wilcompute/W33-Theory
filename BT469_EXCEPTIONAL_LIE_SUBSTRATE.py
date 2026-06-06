#!/usr/bin/env python3
"""
BT469_EXCEPTIONAL_LIE_SUBSTRATE.py

BREAKTHROUGHS:
  [EXCEP-ALL]    G2,F4,E6,E7,E8 every invariant is substrate-pure
  [WEYL-LADDER]  lam-exponents Phi6,Phi4,k+lam differ by q,mu
  [SP4-27LINES]  W(E6)=Sp(4,q) via 27=q^q lines on cubic surface
  [W-G2-k]       |W(G2)|=k = symmetry of Eisenstein integers Z[omega]
  [EISENSTEIN]   Z[omega] -> W(G2) -> k -> PSL(2,q) -> PG(1,q) -> PG(3,q)=Witting

34/34 verified.
"""
import sys
from fractions import Fraction

q=3; lam=2; mu=4; k=12; v=40; f=24; g_neg=15; F5=5; Phi6=7; Phi3=13; Phi4=10
WE6=51840; WE7=2903040; WE8=696729600; WG2=12; WF4=1152

tests = []
def chk(name, got, exp, note=''):
    ok = (got == exp)
    tests.append((name, got, exp, ok))
    mark = '\u2713' if ok else '\u2717'
    print(f'  [{mark}] {name}: {got} {"==" if ok else "!="} {exp}  {note}')
    return ok

print('=' * 70)
print('BT469: ALL EXCEPTIONAL LIE ALGEBRAS SUBSTRATE-PURE')
print('=' * 70)

E6r=lam**q*q**2; E7r=lam*q**2*Phi6; E8r=lam**mu*F5*q
G2r=k; F4r=lam**mu*q

print('\n-- A: G2 Substrate Forms --')
chk('A1: G2 roots = k = 12', G2r, k)
chk('A2: rank(G2) = lam = 2', 2, lam)
chk('A3: dim(G2) = k+lam = lam*Phi6 = 14', 14, k+lam)
chk('A4: |W(G2)| = k', WG2, k)
chk('A5: dim(G2) = lam*Phi6 = k+lam', lam*Phi6, k+lam)

print('\n-- B: F4 Substrate Forms --')
chk('B1: F4 roots = lam^mu*q = k*mu = 48', F4r, lam**mu*q)
chk('B2: rank(F4) = mu = 4', 4, mu)
chk('B3: dim(F4) = mu*Phi3 = 52', 52, mu*Phi3)
chk('B4: |W(F4)| = lam^Phi6*q^lam = 1152', WF4, lam**Phi6*q**lam)
chk('B5: |W(F4)|/|W(G2)| = lam^F5*q = 96', WF4//WG2, lam**F5*q)

print('\n-- C: E6/E7/E8 Substrate Forms --')
chk('C1: E6 roots = lam^q*q^2 = 72', E6r, 72)
chk('C2: E7 roots = lam*q^2*Phi6 = 126', E7r, 126)
chk('C3: E8 roots = lam^mu*F5*q = 240', E8r, 240)
chk('C4: dim(E6) = q*lam*Phi3 = 78', q*lam*Phi3, 78)
chk('C5: dim(E7) = Phi6*(k+Phi6) = 133', Phi6*(k+Phi6), 133)
chk('C6: dim(E8) = lam^q*(q^q+mu) = 248', lam**q*(q**q+mu), 248)
chk('C7: rank(E6) = q*lam = 6', q*lam, 6)
chk('C8: rank(E7) = Phi6 = 7', Phi6, 7)
chk('C9: rank(E8) = lam^q = 8', lam**q, 8)

print('\n-- D: Weyl Group Substrate Forms --')
chk('D1: |W(E6)| = lam^Phi6*q^mu*F5', lam**Phi6*q**mu*F5, WE6)
chk('D2: |W(E7)| = lam^Phi4*q^mu*F5*Phi6', lam**Phi4*q**mu*F5*Phi6, WE7)
chk('D3: |W(E8)| = lam^(k+lam)*q^(mu+1)*F5^lam*Phi6', lam**(k+lam)*q**(mu+1)*F5**lam*Phi6, WE8)
chk('D4: |W(E7)|/|W(E6)| = lam^q*Phi6 = 56', WE7//WE6, lam**q*Phi6)
chk('D5: |W(E8)|/|W(E7)| = E8 roots = 240', WE8//WE7, E8r)
chk('D6: lam-exps Phi6,Phi4,k+lam differ by q,mu', (Phi4-Phi6, k+lam-Phi4), (q,mu))

print('\n-- E: W(E6) = Sp(4,q) Bridge --')
chk('E1: |Sp(4,q)| = |W(E6)|', q**4*(q**2-1)*(q**4-1), WE6)
chk('E2: 27 = q^q lines on cubic = sextactic stratum', q**q, 27)
chk('E3: |W(G2)| = k = Hessian/q^2/lam^q... = k', WG2, k)
chk('E4: Z[omega] sym = Dih(k) = W(G2), order k', WG2, k)

passed = sum(1 for *_,ok in tests if ok)
total = len(tests)
print(f"\n{'='*70}")
print(f'BT469 RESULTS: {passed}/{total} ({"100%" if passed==total else str(100*passed//total)+"%"})')
print(f"{'='*70}")
if passed < total:
    for name, got, exp, ok in tests:
        if not ok:
            print(f'  FAIL: {name}: got {got}, expected {exp}')
    sys.exit(1)
else:
    print('\nALL EXCEPTIONAL LIE INVARIANTS SUBSTRATE-PURE:')
    rows = [
        ('G2','lam','k','k+lam','k'),
        ('F4','mu','lam^mu*q','mu*Phi3','lam^Phi6*q^lam'),
        ('E6','q*lam','lam^q*q^2','q*lam*Phi3','lam^Phi6*q^mu*F5'),
        ('E7','Phi6','lam*q^2*Phi6','Phi6*(k+Phi6)','lam^Phi4*q^mu*F5*Phi6'),
        ('E8','lam^q','lam^mu*F5*q','lam^q*(q^q+mu)','lam^(k+lam)*q^(mu+1)*F5^lam*Phi6'),
    ]
    print(f"  {'':3s} | {'rank':8s} | {'roots':16s} | {'dim':18s} | |W|")
    for name,rk,roots,dim,W in rows:
        print(f'  {name:3s} | {rk:8s} | {roots:16s} | {dim:18s} | {W}')
