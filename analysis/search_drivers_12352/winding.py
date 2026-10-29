"""12352: tachyons away from the orbifold point for the seven three-generation models (SM_2618 v0-v3, SM_2913 v6-v8).  Integer momenta
and windings (no Scherk-Schwarz twist); winding w_a along a direction with Wilson line W_a shifts the left coset by w_a W_a.  At
n = 0 (no momentum) a winding state has level L_int + R^2-terms with L_int = R_int, so a small-radius tachyon needs a coset whose
minimal left level is <= the sector's negative right vacuum (Witten untwisted: -1/2; Witten theta^2, theta^4: -1/6).  Cosets:
k = 0: V0 + sum_a w_a W_a (all six directions); k = 2, 4: V0 + k V1 + f-labels on the rotated tori 1, 2 + w5 W5 + w6 W6 (torus 3 fixed).
Windings |w_a| <= 2.  Exact minima by E8 x E8 closest-vector decoding.  A minimum above the vacuum = channel safe; at or below =
possible tachyon (exact level / projection not checked)."""
import sys, json, itertools
from fractions import Fraction as F
sys.argv = ['x']
exec(open('../search_drivers_12322/lmin.py').read().split('def lmin(')[0])
dc = {0: F(0), 2: F(2, 9), 4: F(2, 9)}
vac = {0: F(-1, 2), 2: F(-1, 6), 4: F(-1, 6)}
res = {}
for m in ('Z6II_06_SM_20260917_2618_v0', 'Z6II_06_SM_20260917_2618_v1', 'Z6II_06_SM_20260917_2618_v2', 'Z6II_06_SM_20260917_2618_v3',
          'Z6II_23_SM_20260917_2913_v6', 'Z6II_23_SM_20260917_2913_v7', 'Z6II_23_SM_20260917_2913_v8'):
    _, rows = read(m + '.txt')
    V0, V1, W = rows[0], rows[1], rows[3:9]
    nzW = [a for a in range(6) if any(W[a])]
    out = {}
    for k in (0, 2, 4):
        best = None; worst_coset = None
        if k == 0:
            dirs = nzW; fsets = [(0, 0, 0, 0)]
        else:
            dirs = [a for a in nzW if a in (4, 5)]; fsets = list(itertools.product(range(3), repeat=4))
        for f in fsets:
            for w in itertools.product(range(-2, 3), repeat=len(dirs)):
                Vh = [V0[i] + k * V1[i] + sum(f[b] * W[b][i] for b in range(4)) + sum(w[j] * W[dirs[j]][i] for j in range(len(dirs))) for i in range(16)]
                L = (e8_min_norm_coset(Vh[:8]) + e8_min_norm_coset(Vh[8:])) / 2 - 1 + dc[k]
                if any(w) and (best is None or L < best):
                    best, worst_coset = L, (f, w)
        out[k] = dict(min_level_with_winding=str(best), vacuum=str(vac[k]), safe=(best is None or best > vac[k]), winding_dirs=[d + 1 for d in dirs],
                      at=str(worst_coset))
    res[m] = out
    print(m, {k: (v['min_level_with_winding'], 'safe' if v['safe'] else 'POSSIBLE TACHYON', v['winding_dirs']) for k, v in out.items()})
json.dump(res, open('winding.json', 'w'), indent=1)
