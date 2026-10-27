"""12330: one-loop beta coefficients of the left-right candidate's full massless spectrum (brother of SM_20260917_810_v9), with the
model's hypercharge Y = T3R + Y' (t = -1/148, 12286) evaluated per component; SU(2)_L = first A1.  b = -11/3 C_A + 2/3 sum_Weyl T +
1/3 sum_complex-scalar T (engine lists each complex scalar twice, phi and phi*: scalar entries / 2).  Running: SM below an assumed
common threshold M_X, the full spectrum above (most favourable case for k_Y: everything light).  Output: where alpha_2 = alpha_3 and
the k_Y needed there, against the model's k_Y = 8/3."""
import re, sys, json, math, itertools
import sympy as sp
sys.path.insert(0, '../search_drivers_12286')
from lr_hypercharge import solve, fermions
P = '../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
fs = fermions(P); c, eqs, sol = solve(fs); s = sol[0]
free = sorted((set(c) - set(s)) | {x for v in s.values() for x in sp.sympify(v).free_symbols}, key=str)
cv = [sp.sympify(s.get(ci, ci)).subs(free[0], sp.Rational(-1, 148)) for ci in c]
Tfund = {1: 0, 2: sp.Rational(1, 2), 3: sp.Rational(1, 2), 8: 3}            # SU(3): 3 -> 1/2, 8 -> 3; SU(2): 2 -> 1/2, 3 -> 2
def rec(kinds):
    out = []
    for l in open(P):
        m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) q=(\S*)', l)
        if m and int(m.group(1)) in kinds:
            d = [abs(int(re.match(r'-?\d+', x).group(0))) for x in m.group(2).split(',')] if m.group(2) else []
            q = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(3).split(',') if x]
            out.append(dict(d=d, y=sum(a * b for a, b in zip(cv, q))))
    return out
def T3(n): return Tfund[n] if n in Tfund else 0
def T2(n): return {1: 0, 2: sp.Rational(1, 2), 3: 2}.get(n, 0)
def contrib(r):
    d3, dL, dR, dH = r['d'][0], r['d'][1], r['d'][2], r['d'][3]
    b3 = T3(d3) * dL * dR * dH; b2 = T2(dL) * d3 * dR * dH
    tr = [sp.Rational(1, 2), -sp.Rational(1, 2)] if dR == 2 else [0]
    bY = sum((r['y'] + z) ** 2 for z in tr) * d3 * dL * dH
    return b3, b2, bY
W = rec({19}); Sc = rec({15, 16})
b = dict(b3=sp.Integer(-11), b2=sp.Rational(-22, 3), bY=sp.Integer(0))         # gauge: SU(3) -11, SU(2)_L -22/3
for r in W:
    x = contrib(r); b['b3'] += sp.Rational(2, 3) * x[0]; b['b2'] += sp.Rational(2, 3) * x[1]; b['bY'] += sp.Rational(2, 3) * x[2]
for r in Sc:
    x = contrib(r); b['b3'] += sp.Rational(1, 3) * x[0] / 2; b['b2'] += sp.Rational(1, 3) * x[1] / 2; b['bY'] += sp.Rational(1, 3) * x[2] / 2
print({k: str(v) for k, v in b.items()})
MZ = 91.1876; ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
a = dict(Y=1 / ainv_em / (1 - s2), two=1 / ainv_em / s2, three=as_)
bSM = dict(Y=41 / 6, two=-19 / 6, three=-7)
bF = dict(Y=float(b['bY']), two=float(b['b2']), three=float(b['b3']))
out = dict(b_full={k: str(v) for k, v in b.items()}, runs={})
for MX in (1e3, 1e6, 1e10):
    def inv(i, mu):
        x = 1 / a[i] - bSM[i] / (2 * math.pi) * math.log(min(mu, MX) / MZ)
        if mu > MX:
            x -= bF[i] / (2 * math.pi) * math.log(mu / MX)
        return x
    lo, hi = math.log(MX * 1.0001), math.log(1e19)
    f = lambda L: inv('two', math.exp(L)) - inv('three', math.exp(L))
    if f(lo) * f(hi) > 0:
        out['runs'][f'{MX:.0e}'] = dict(crossing=None, note='alpha_2 and alpha_3 do not meet below 1e19 GeV')
        continue
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    M = math.exp(lo)
    out['runs'][f'{MX:.0e}'] = dict(crossing=M, alpha_inv=inv('two', M), k_needed=inv('Y', M) / inv('two', M))
print(json.dumps(out, indent=1)); json.dump(out, open('beta.json', 'w'), indent=1)
