"""12156: (a) the volume-growing (beta-sector, 10D-like) gauge thresholds are UNIVERSAL: sum over lattice vectors of (p.y)^2 on each
norm shell of E8 and of each SO(16) conjugacy class is |y|^2 x const (Weyl irreducibility), so the insertion is proportional to
k_a = 2|y_a|^2 per E8 half and the two halves enter symmetrically -> cannot change sin^2 theta_W. (b) the threshold needed to
reach the measured sin^2 at the heterotic scale, for k_Y = 5/3 and 17/3."""
import json, math, itertools
import numpy as np
import sys
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import latff as LF
rng = np.random.default_rng(1)
E8 = LF.e8_upto(6).astype(float) / 2
n2 = (E8 ** 2).sum(1)
out = {'E8_shells': {}, 'D8_classes': {}}
for N in (2, 4, 6):
    P = E8[np.abs(n2 - N) < 1e-9]
    vals = []
    for _ in range(5):
        y = rng.normal(size=8)
        vals.append(((P @ y) ** 2).sum() / (y @ y))
    out['E8_shells'][N] = dict(count=len(P), ratio=[float(v) for v in vals], expected=len(P) * N / 8)
# D8 conjugacy classes (SO(16) lattice decomposition): integer vectors with even sum (0), odd sum (v), half-integer even/odd # of minus (s, c)
for name, cond in [('0', lambda v: np.all(v == np.round(v)) and round(v.sum()) % 2 == 0), ('v', lambda v: np.all(v == np.round(v)) and round(v.sum()) % 2 == 1),
                   ('s', lambda v: np.all(v != np.round(v)) and (v < 0).sum() % 2 == 0), ('c', lambda v: np.all(v != np.round(v)) and (v < 0).sum() % 2 == 1)]:
    pts = []
    for half in (0.0, 0.5):
        rngs = [x + half for x in range(-3, 3)] if half else list(range(-2, 3))
        for v in itertools.product(rngs, repeat=8):
            v = np.array(v, float)
            if v @ v <= 4.0 + 1e-9 and cond(v):
                pts.append(v)
    P = np.array(pts)
    res = {}
    for N in sorted(set(np.round((P ** 2).sum(1), 6))):
        Q = P[np.abs((P ** 2).sum(1) - N) < 1e-9]
        r = []
        for _ in range(4):
            y = rng.normal(size=8)
            r.append(((Q @ y) ** 2).sum() / (y @ y))
        res[str(N)] = dict(count=len(Q), spread=float(max(r) - min(r)), ratio=float(np.mean(r)), expected=len(Q) * N / 8)
    out['D8_classes'][name] = res
iso = all(abs(v['spread']) < 1e-8 for c in out['D8_classes'].values() for v in c.values()) and all(max(s['ratio']) - min(s['ratio']) < 1e-8 for s in out['E8_shells'].values())
out['isotropic'] = bool(iso)
# (b) needed thresholds at the heterotic scale (Kaplunovsky), 1/alpha_a(MZ) = k_a/alpha_U + b_a/2pi ln(Ms/MZ) + Delta_a/(4 pi)
MZ, aem, a3, s2 = 91.1876, 1 / 127.951, 0.1180, 0.23122
bY, b2, b3 = 41 / 6, -19 / 6, -7.0
Ms = 2.6919905818218077e17
L = math.log(Ms / MZ)
iaU = 1 / a3 - b3 * L / (2 * math.pi)
need = {}
for kY in (5 / 3, 17 / 3):
    ia2m, iaYm = s2 / aem, (1 - s2) / aem
    d2 = 4 * math.pi * (ia2m - (iaU + b2 * L / (2 * math.pi)))
    dY = 4 * math.pi * (iaYm - (kY * iaU + bY * L / (2 * math.pi)))
    need['%.4f' % kY] = dict(Delta_2=d2, Delta_Y=dY, Delta_Y_minus_kY_Delta_2=dY - kY * d2, relative_to_kY_over_alphaU=(dY - kY * d2) / (4 * math.pi) / (kY * iaU))
out['needed_thresholds_heterotic_Ms'] = need
print(json.dumps(out['needed_thresholds_heterotic_Ms'], indent=1), 'isotropic', iso)
print({k: {n: (v['count'], round(v['ratio'], 4), v['expected']) for n, v in c.items()} for k, c in out['D8_classes'].items()})
json.dump(out, open('thresh.json', 'w'), indent=1, default=str)
