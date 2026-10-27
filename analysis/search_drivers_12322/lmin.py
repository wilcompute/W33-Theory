"""12322: minimal left-moving internal level L_min = min_P P^2/2 - 1 + dc in the Witten-twisted theta^2 (and theta^4) sectors of the
SM_810 lineage, P in E8 x E8 + V_h(f), V_h = V0 + k V1 + sum_b f_b W_b over fixed points f of theta^k on the rotated tori 1, 2
(W3 = W4 on torus 2; torus 3 fixed by theta^2; brother's W6 = lam in the lattice, irrelevant), exact E8 closest-vector decoding
(Conway-Sloane: nearest of D8 and D8 + 1/2).  dc(theta^2) = dc(theta^4) = 2/9.  The small-R tachyon channel (n w = 1/2 at
R = sqrt(alpha'/2)) needs L_int = -2/3: it is closed if L_min > -2/3 (oscillators only raise the level)."""
import sys, json, itertools
from fractions import Fraction as F
sys.path.insert(0, '../search_drivers_12267')
from mirage import read
def d8_closest(x):
    r = [round(v) for v in x]
    if sum(r) % 2:
        i = max(range(8), key=lambda j: abs(x[j] - r[j]))
        r[i] += 1 if x[i] > r[i] else -1
    return r
def e8_min_norm_coset(v):
    # minimal |p + v|^2 over p in E8 (v rational, 8 entries): closest lattice point to -v
    x = [-float(t) for t in v]
    c1 = d8_closest(x)
    c2 = [t + 0.5 for t in d8_closest([t - 0.5 for t in x])]
    best = None
    for c in (c1, c2):
        p = [F(c[i]).limit_denominator(2) for i in range(8)]
        n = sum((p[i] + v[i]) ** 2 for i in range(8))
        best = n if best is None or n < best else best
    return best
def lmin(model):
    _, rows = read(model)
    V0, V1 = rows[0], rows[1]; W = rows[3:9]
    out = {}
    for k in (2, 4):
        best = None
        # theta^k rotates tori 1 and 2 (by 120 / 240 deg on torus 1, 240 / 120 on torus 2): fixed-point labels f in {0,1,2}^4 on e1..e4
        for f in itertools.product(range(3), repeat=4):
            Vh = [V0[i] + k * V1[i] + sum(f[b] * W[b][i] for b in range(4)) for i in range(16)]
            n2 = e8_min_norm_coset(Vh[:8]) + e8_min_norm_coset(Vh[8:])
            L = n2 / 2 - 1 + F(2, 9)
            best = L if best is None or L < best else best
        out[k] = best
    return out
res = {}
for v in ('v9', 'v4', 'v0'):
    for tag in ('ctrl', 'w6odd'):
        p = f'../search_drivers_12281/bro/Z6II_60_SM_20260917_810_{v}__{tag}.txt'
        try:
            r = lmin(p)
        except FileNotFoundError:
            r = lmin(p.replace('12281', '12302'))
        res[f'{v}_{tag}'] = {str(k): str(x) for k, x in r.items()}
        print(v, tag, res[f'{v}_{tag}'])
json.dump(res, open('lmin.json', 'w'), indent=1)
