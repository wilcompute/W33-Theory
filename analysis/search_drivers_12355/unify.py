"""12355: one-loop running for SM_2913_v6 (full massless spectrum above a common threshold M_X, SM below; Y from the SUSY parent's exact
vector, k_Y = 5/3).  b = -11/3 C_A + 2/3 sum_Weyl T + 1/3 sum_complex T (scalar entries / 2), other factors as multiplicity.  Scan M_X
from 1e3 to 1e16 GeV: k_Y needed where alpha_2 = alpha_3 at a perturbative crossing, compared with 5/3."""
import re, json, math, os, sys
import sympy as sp
yv = json.load(open('../search_drivers_12351/yvec.json')); ch = json.load(open('../search_drivers_12351/chiral.json'))
m = 'Z6II_23_SM_20260917_2913_v6'
Y = [sp.Rational(x) for x in yv['SM_20260917_2913']['Yvec']]
p = '../search_drivers_12302/bro/' + m + '__ctrl.nsoq'
if not os.path.exists(p): p = p.replace('12302', '12281')
i3, i2 = ch[m]['SU3'], ch[m]['SU2']
recs = []; cur = None
for l in open(p, errors='ignore'):
    if l.startswith('FIELD'):
        mm = re.match(r'FIELD \d+ m=(\S+) .* dim=(\S*) q=', l)
        cur = dict(m=int(mm.group(1)), d=[abs(int(re.match(r'-?\d+', x).group(0))) for x in mm.group(2).split(',')] if mm.group(2) else [], y=None)
        recs.append(cur)
    elif l.startswith('W ') and cur is not None and cur['y'] is None:
        cur['y'] = sum(a * sp.nsimplify(float(b), tolerance=1e-9, rational=True) for a, b in zip(Y, l[2:].split(',')))
T3 = {1: 0, 3: sp.Rational(1, 2), 8: 3}; T2 = {1: 0, 2: sp.Rational(1, 2), 3: 2}
b = dict(b3=sp.Integer(-11), b2=sp.Rational(-22, 3), bY=sp.Integer(0))
for r in recs:
    if r['m'] not in (19, 15, 16) or r['y'] is None:
        continue
    d = r['d']; mult = math.prod(d[j] for j in range(len(d)) if j not in (i3, i2))
    w = sp.Rational(2, 3) if r['m'] == 19 else sp.Rational(1, 6)      # Weyl 2/3; complex scalar 1/3 with each listed twice -> 1/6
    b['b3'] += w * T3.get(d[i3], 0) * d[i2] * mult
    b['b2'] += w * T2.get(d[i2], 0) * d[i3] * mult
    b['bY'] += w * r['y'] ** 2 * d[i3] * d[i2] * mult
bF = dict(Y=float(b['bY']), two=float(b['b2']), three=float(b['b3']))
MZ = 91.1876; ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
a = dict(Y=1 / ainv_em / (1 - s2), two=1 / ainv_em / s2, three=as_)
bSM = dict(Y=41 / 6, two=-19 / 6, three=-7)
rows = []
for e in [3 + 0.25 * i for i in range(53)]:
    MX = 10 ** e
    def inv(i, mu):
        x = 1 / a[i] - bSM[i] / (2 * math.pi) * math.log(min(mu, MX) / MZ)
        if mu > MX: x -= bF[i] / (2 * math.pi) * math.log(mu / MX)
        return x
    lo, hi = math.log(MZ * 1.001), math.log(1e19); f = lambda L: inv('two', math.exp(L)) - inv('three', math.exp(L))
    if f(lo) * f(hi) > 0:
        rows.append(dict(log10MX=e, crossing=None)); continue
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    M = math.exp(lo); ai = inv('two', M)
    rows.append(dict(log10MX=e, log10M=math.log10(M), alpha_inv=ai, perturbative=ai > 0 and inv('Y', M) > 0, k_needed=inv('Y', M) / ai))
pert = [r for r in rows if r.get('perturbative')]
ks = [r['k_needed'] for r in pert]
near = [r for r in pert if abs(r['k_needed'] - 5 / 3) < 0.05]
out = dict(b={k: str(v) for k, v in b.items()}, perturbative_k_range=[min(ks), max(ks)] if ks else None, near_5_3=near)
print('b =', out['b'], ' perturbative k range', out['perturbative_k_range'], ' within 0.05 of 5/3:', [(round(r['log10MX'], 2), round(r['log10M'], 2), round(r['k_needed'], 3)) for r in near])
json.dump(dict(out, rows=rows), open('unify.json', 'w'), indent=1)
