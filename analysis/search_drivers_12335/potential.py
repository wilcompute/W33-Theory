"""12335: truncated one-loop potential along R_6 (alpha' = 1) for the SM_810 brother (v9).  Species with e6 momentum: the brother's
even-Z6-power-sector states (integer tower, from its dump) and the parent's even-sector states with V_h.lam odd (half-integer tower,
12334: 52 fermions + 16 tachyons at internal level -1/6).  Odd-sector states are localised on torus 3 (R_6-independent constant).
V(R) = -sum_s (-1)^F_s d_s I_s(R),  I_s = int_F d^2tau / tau2^3  exp(-4 pi tau2 l_s) sum_{n in Z+q_s, w in Z} exp(-pi tau2 (n^2/R^2 + w^2 R^2))
cos(2 pi tau1 n w)   (overall positive constant dropped).  Truncation: massive internal levels omitted; level matching of the circle
modes enters only through cos(2 pi tau1 n w).  The tachyon term converges iff R^2 < 3/8 (control on the window edge)."""
import re, json, math, collections, sys
import numpy as np
sys.path.insert(0, '../search_drivers_12334')
exec(open('../search_drivers_12334/split.py').read().split('res = {}')[0])
from mirage import read
b = '../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__'
_, prow = read(b + 'ctrl.txt'); _, brow = read(b + 'w6odd.txt'); lam = brow[8]
V0l, V1l = dot(prow[0], lam), dot(prow[1], lam); Wl = [dot(prow[3 + k], lam) for k in range(6)]
par = fields(b + 'ctrl.nsoq'); bro = fields(b + 'w6odd.nsoq')
vhl = lambda f: f['mm'] * V0l + f['n'] * V1l + sum(f['lat'][k] * Wl[k] for k in range(6))
cls = lambda m: 'T' if m in (21, 22, 23, 24) else ('F' if m in (19, 20) else 'B')
dim = lambda key: math.prod(abs(int(re.match(r'-?\d+', x).group(0))) for x in key[4].split(',')) if key[4] else 1
species = collections.Counter()
for f in bro:
    if f['n'] % 2 == 0:
        species[('int', cls(f['m']))] += dim(f['key'])
for f in par:
    if f['n'] % 2 == 0 and vhl(f) % 2 != 0:
        species[('half', cls(f['m']))] += dim(f['key'])
print('species (tower, class): components', dict(species))
# fundamental-domain quadrature
t1 = np.linspace(-0.5, 0.5, 401)
def integral(q, ell, R, nmax=8, T=40.0):
    tot = 0.0
    ns = np.arange(-nmax, nmax + 1) + q; ws = np.arange(-nmax, nmax + 1)
    for a in t1:
        lo = math.sqrt(max(1 - a * a, 0.0))
        t2 = np.geomspace(lo, T, 600)
        s = np.zeros_like(t2)
        for n in ns:
            for w in ws:
                # exponents combined before exp (the tachyon factor exp(+2 pi tau2 / 3) alone overflows at large tau2)
                s += np.exp(-math.pi * t2 * (n * n / R ** 2 + w * w * R ** 2) - 4 * math.pi * t2 * ell) * math.cos(2 * math.pi * a * n * w)
        f = s / t2 ** 3
        tot += np.trapezoid(f, t2) * (t1[1] - t1[0])
    return tot
out = dict(species={str(k): v for k, v in species.items()}, V={})
for R in (0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.58, 0.6):
    V = 0.0
    for (tw, c), d in species.items():
        q = 0.0 if tw == 'int' else 0.5
        ell = -1 / 6 if c == 'T' else 0.0
        sgn = -1 if c == 'F' else 1
        V -= sgn * d * integral(q, ell, R)
    out['V'][R] = V
    print(f'R = {R:.2f}  V = {V:.4f}', flush=True)
json.dump(out, open('potential.json', 'w'), indent=1)
