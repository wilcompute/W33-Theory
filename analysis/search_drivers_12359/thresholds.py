"""12359d: can large-volume string thresholds rescue k_Y = 5/3 unification for SM_2913_v6?  Kaplunovsky / Dixon-Kaplunovsky-Louis form,
4 pi / alpha_a(mu) = k_a 4 pi / alpha_s + b_a^low ln(M_s^2 / mu^2) + sum_i c_i b_a^(i) x_i,  x_i ~ (pi/3) T2^(i) (large volume, with
c_i = |G_i|/|G|: 1/3 for the theta^3-fixed torus e3e4, 1/2 for the theta^2-fixed torus e5e6), M_s = 0.527 g_s 1e18 GeV.
b_a^(i) = the 6D massless content (Wilson lines off: the linear-in-T2 growth counts every KK level, shifted or not).  Low-energy b: SM
only (exotics at M_s) or the full massless spectrum.  Unknowns 1/alpha_s and x_i; x_i >= 0 required (large volume), torus e5e6 also
limited by its 6D tachyons (12359b: R5 < sqrt(3/8)).  Argued, not computed: the DKL form for this non-SUSY orbifold (the large-volume
linear term is field-theoretic -- power-law KK running -- so its coefficient is robust; the constant and log parts are not)."""
import json, math
import numpy as np
from fractions import Fraction as F
b6 = json.load(open('beta.json'))
bA = [float(F(b6['sub3_noW34'][k])) for k in ('bY', 'b2', 'b3')]
bB = [float(F(b6['sub2_noW5'][k])) for k in ('bY', 'b2', 'b3')]
MZ = 91.1876; ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
ainv = [ainv_em * (1 - s2), ainv_em * s2, 1 / as_]
k = [5 / 3, 1, 1]
lows = dict(SM=[41 / 6, -19 / 6, -7], full=[float(F(b6['parent'][x])) for x in ('bY', 'b2', 'b3')])
out = {}
for name, bl in lows.items():
    for mode in ('A', 'B', 'AB'):
        u = 1 / 0.04
        for _ in range(200):
            gs = math.sqrt(4 * math.pi / u); Ms = 0.527 * gs * 1e18; L = math.log(Ms / MZ)
            cols = [[kk for kk in k]]
            if 'A' in mode: cols.append([bA[a] / 3 / (4 * math.pi) for a in range(3)])
            if 'B' in mode: cols.append([bB[a] / 2 / (4 * math.pi) for a in range(3)])
            M = np.array(cols).T; rhs = np.array([ainv[a] - bl[a] / (2 * math.pi) * L for a in range(3)])
            sol, res, rk, _ = np.linalg.lstsq(M, rhs, rcond=None)
            u = max(sol[0], 1.0)
        resid = rhs - M @ sol
        out[f'{name}_{mode}'] = dict(inv_alpha_s=sol[0], x=list(sol[1:]), max_resid_inv_alpha=float(np.abs(resid).max()), Ms=Ms,
                                     feasible=bool(np.abs(resid).max() < 0.05 and all(x >= 0 for x in sol[1:]) and sol[0] > 0))
        print(name, mode, {kk: (round(v, 3) if isinstance(v, float) else [round(t, 3) for t in v] if isinstance(v, list) else v) for kk, v in out[f'{name}_{mode}'].items()})
# no-threshold control: the same machinery with x = 0 must reproduce the k_Y mismatch (residual large)
json.dump(dict(b_6D_e3e4=bA, b_6D_e5e6=bB, fits=out), open('thresholds.json', 'w'), indent=1)
