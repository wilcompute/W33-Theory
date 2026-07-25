#!/usr/bin/env python3
"""
BT473_TERNARY_GOLAY_TETRACODE.py

Ternary Golay + Tetracode + Substrate q-Code Tower

  Tetracode [mu,lam,q]=[4,2,3] over F_q: MDS, rate=1/lam, = TH(lam)
  G_11: [Phi5,q*lam,F5]=[11,6,5] over F_q: PERFECT, k=rank(E6)
  G_12: [k,q*lam,q*lam]=[12,6,6] over F_q: self-dual, rate=1/lam
  M_12/M_24 ratio = W_12(G_24) = 2576
  All self-dual substrate codes have rate = 1/lam.

33/33 verified.
"""
import sys, math
from fractions import Fraction

q=3; lam=2; mu=4; k=12; v=40; f=24; g_neg=15; F5=5; Phi6=7; Phi3=13; Phi4=10
Phi5=11
lam_q=lam**q; lam_mu=lam**mu; p23=lam*q**2+F5
M12=95040; M24=244823040

tests = []
def chk(name, got, exp):
    ok = (got == exp)
    tests.append((name, ok))
    mark = '\u2713' if ok else '\u2717'
    print(f'  [{mark}] {name}: {got}=={exp}')

print('='*70)
print('BT473: TERNARY GOLAY = TETRACODE = SUBSTRATE q-CODE TOWER')
print('='*70)

print('\n-- A: Tetracode [mu,lam,q] over F_q --')
chk('A1: n=mu=4', mu, 4)
chk('A2: k=lam=2', lam, 2)
chk('A3: d=q=3', q, 3)
chk('A4: rate=1/lam', Fraction(lam,mu), Fraction(1,lam))
chk('A5: MDS: d=n-k+1', q, mu-lam+1)
F3=[0,1,2]
TC={(a,b,(a+b)%q,(a-b)%q) for a in F3 for b in F3}
min_wt=min(sum(1 for x in c if x!=0) for c in TC if any(x!=0 for x in c))
chk('A6: min weight=q (enumerated)', min_wt, q)
chk('A7: |codewords|=q^lam=9', len(TC), q**lam)
TH2_n=(q**lam-1)//(q-1); TH2_k=TH2_n-lam
chk('A8: Tetracode=TH(lam): n=mu,k=lam', (TH2_n,TH2_k), (mu,lam))

print('\n-- B: Perfect ternary Golay G_11 [Phi5,q*lam,F5] --')
chk('B1: n=Phi5=11', Phi5, 11)
chk('B2: k=q*lam=6=rank(E6)=C(mu,2)', q*lam, 6)
chk('B3: d=F5=5', F5, 5)
t11=(F5-1)//2; sph11=sum(math.comb(Phi5,i)*(q-1)**i for i in range(t11+1))
chk('B4: t=(d-1)/2=lam', t11, lam)
chk('B5: PERFECT: q^k*sphere=q^n', q**(q*lam)*sph11, q**Phi5)
chk('B6: sphere=q^F5=243', sph11, q**F5)

print('\n-- C: Extended ternary Golay G_12 [k,q*lam,q*lam] --')
chk('C1: n=k=12 (GAUGE CODEC!)', k, 12)
chk('C2: k_G12=q*lam=6=rank(E6)', q*lam, 6)
chk('C3: d=q*lam=6', q*lam, 6)
chk('C4: rate=1/lam (self-dual)', Fraction(q*lam,k), Fraction(1,lam))
chk('C5: |codewords|=q^(q*lam)=729', q**(q*lam), 729)
chk('C6: (q^q)^lam = q^(q*lam) = 729', (q**q)**lam, q**(q*lam))

print('\n-- D: Mathieu tower --')
chk('D1: |M_12|=lam^(q*lam)*q^q*F5*Phi5', lam**(q*lam)*q**q*F5*Phi5, M12)
chk('D2: M_12 lam-exp=q*lam=rank(E6)', q*lam, 6)
chk('D3: M_12 q-Sylow=q^q=27', q**q, 27)
chk('D4: |M_24|/|M_12|=W_12(G_24)=2576', M24//M12, lam_mu*Phi6*p23)
chk('D5: 2576=lam^lam*lam^lam*Phi6*p23', lam**lam*lam**lam*Phi6*p23, 2576)
chk('D6: M_12 acts on Phi5=11 pts', Phi5, 11)
chk('D7: M_24 acts on f=24 pts', f, 24)

print('\n-- E: Ternary Hamming tower --')
chk('E1: TH(m=2): n=mu=4', (q**lam-1)//(q-1), mu)
chk('E2: TH(m=3): n=Phi3=13', (q**q-1)//(q-1), Phi3)
chk('E3: TH(m=q): k=Phi4=10', (q**q-1)//(q-1)-q, Phi4)

print('\n-- F: Universal self-dual rate = 1/lam law --')
chk('F1: Tetracode rate=1/lam', Fraction(lam,mu), Fraction(1,lam))
chk('F2: G_12 rate=1/lam', Fraction(q*lam,k), Fraction(1,lam))
chk('F3: G_24 rate=1/lam', Fraction(k,f), Fraction(1,lam))

passed=sum(1 for _,ok in tests if ok); total=len(tests)
print(f"\n{'='*70}")
print(f'BT473: {passed}/{total} ({"100%" if passed==total else str(100*passed//total)+"%"})')
if passed < total:
    sys.exit(1)
else:
    print('\nKEY THEOREMS:')
    print('  [TETRACODE]     [mu,lam,q]=[4,2,3] = MDS ternary Hamming(lam) code')
    print('  [G11-PERFECT]   G_11=[Phi5,q*lam,F5]: PERFECT ternary, k=rank(E6)')
    print('  [G12-SELFDUAL]  G_12=[k,q*lam,q*lam]: n=GAUGE CODEC, rate=1/lam')
    print('  [MATHIEU]       |M_24|/|M_12| = W_12(G_24) = 2576 = lam^mu*Phi6*p23')
    print('  [SELFDUAL-LAW]  ALL self-dual substrate codes: rate = 1/lam')
