"""12359c: one-loop beta coefficients (SM SU(3), SU(2), Y) of the massless spectra of the parent and of the two fixed-torus sub-orbifolds,
from weights: T_a(state) = sum_w (w . alpha_a)^2 / 4 for a root alpha_a of the parent's SU(3) (resp. SU(2)) factor -- valid when the
factor sits inside a larger group of the sub-orbifold (SU(3) in SU(4) for theta^3).  Gauge bosons (m = 13) -11/3, Weyl fermions (m = 19)
2/3, scalars (m = 15, 16; a complex scalar listed twice) 1/6.  Y: the SUSY parent's exact vector (12351), sum_w Y(w)^2 with the same
weights.  Control: the parent must reproduce 12355's (19/3, 13, 338/9)."""
import json, sys
import sympy as sp
Y = [sp.Rational(x) for x in json.load(open('../search_drivers_12351/yvec.json'))['SM_20260917_2913']['Yvec']]
def roots(p):
    R = []
    for l in open(p, errors='ignore'):
        if l.startswith('FACTOR'):
            R.append([[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()] for r in l.split('|')[1:]])
    return R
par = roots('m2913v6_parent.nsoq')
a3, a2 = par[0][0], par[1][0]
def beta(p):
    w = {13: sp.Rational(-11, 3), 19: sp.Rational(2, 3), 15: sp.Rational(1, 6), 16: sp.Rational(1, 6)}
    b = dict(b3=sp.Integer(0), b2=sp.Integer(0), bY=sp.Integer(0)); cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            cur = int(l.split()[2][2:])
        elif l.startswith('W ') and cur in w:
            P = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')]
            d3 = sum(x * y for x, y in zip(P, a3)); d2 = sum(x * y for x, y in zip(P, a2)); y = sum(x * c for x, c in zip(P, Y))
            b['b3'] += w[cur] * d3 ** 2 / 4; b['b2'] += w[cur] * d2 ** 2 / 4; b['bY'] += w[cur] * y ** 2
    return {k: str(v) for k, v in b.items()}
if __name__ == '__main__':
    out = {t: beta(f'm2913v6_{t}.nsoq') for t in ('parent', 'sub2', 'sub3', 'sub2_noW5', 'sub3_noW34')}
    for k, v in out.items(): print(k, v)
    json.dump(out, open('beta.json', 'w'), indent=1)
