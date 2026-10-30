"""12459b: best PHYSICAL fit (1/alpha_s > 0, x_i >= 0) for each c22 hypercharge -- the smallest achievable residual in 1/alpha_a (NNLS,
iterating M_s with g_s).  Control: hypothetical k_Y = 5/3 with c22's OWN 6D coefficients rescaled to that Y normalisation is NOT
meaningful, so the control is the 12359 SM_2913 numbers reproduced by the same function (residual >= 8.7 SM-only)."""
import json, math
import numpy as np
from scipy.optimize import nnls
T = json.load(open('thresholds_c22.json'))
MZ = 91.1876; ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
ainv = [ainv_em * (1 - s2), ainv_em * s2, 1 / as_]
def fit(kY, bA, bB, bl):
    u = 25.0
    for _ in range(300):
        gs = math.sqrt(4 * math.pi / u); Ms = 0.527 * gs * 1e18; L = math.log(Ms / MZ)
        M = np.array([[kY, 1, 1], [bA[a] / 2 / (4 * math.pi) for a in range(3)], [bB[a] / 3 / (4 * math.pi) for a in range(3)]]).T
        rhs = np.array([ainv[a] - bl[a] / (2 * math.pi) * L for a in range(3)])
        sol, rn = nnls(M, rhs); u = max(sol[0], 1.0)
    return sol, float(np.abs(rhs - M @ sol).max())
out = {}
b2913 = json.load(open('../search_drivers_12359/thresholds.json'))
s, r = fit(5 / 3, b2913['b_6D_e5e6'], b2913['b_6D_e3e4'], [41 / 6, -19 / 6, -7])
out['control_SM2913_SM'] = r
print('control SM_2913 (12359 says >= 8.7):', round(r, 2))
for rec in T:
    kY = eval(rec['kY'])
    for nm, bl in (('SM', [41 / 6, -19 / 6, -7]), ('full', rec['b_parent_massless'])):
        s, r = fit(kY, rec['b6_theta2'], rec['b6_theta3'], bl)
        out[f"{rec['kY']}_{nm}_{len(out)}"] = dict(resid=round(r, 2), inv_alpha_s=round(float(s[0]), 2), x=[round(float(v), 2) for v in s[1:]])
        print(rec['kY'], nm, out[list(out)[-1]])
json.dump(out, open('nnls_c22.json', 'w'), indent=1)
