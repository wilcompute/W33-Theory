import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
import sys, numpy as np
sys.path.insert(0, _ANA)
import w33_pass12044_s_type_cp_and_locus_stability as P
from scipy.optimize import minimize_scalar
from scipy.optimize import least_squares
for k in '+-':
    x = least_squares(lambda p: [np.log(np.linalg.svd(P.theta_c(P.up_home(*p), np.zeros(2, complex)), compute_uv=False)[1] / np.linalg.svd(P.theta_c(P.up_home(*p), np.zeros(2, complex)), compute_uv=False)[0] / P.UP['mc_mt']),
                                     np.log(np.linalg.svd(P.theta_c(P.up_home(*p), np.zeros(2, complex)), compute_uv=False)[2] / np.linalg.svd(P.theta_c(P.up_home(*p), np.zeros(2, complex)), compute_uv=False)[1] / P.UP['mu_mc'])],
                      P.UP_AB[k], xtol=1e-15, ftol=1e-15).x
    Ou = P.up_home(*x); tau = Ou[0, 0]
    for sg in (1, -1):
        A = np.concatenate([np.geomspace(1e-9, .05, 1500), np.linspace(.05, np.pi - .05, 3000), np.pi - np.geomspace(.05, 1e-9, 1500)])
        v = []
        for a in A:
            Od = P.down_home_ss(tau, a, sg)
            if Od is None or np.linalg.eigvalsh(Od.imag).min() < 1e-12: v.append(np.inf); continue
            try: v.append(P.chi_down(Ou, Od))
            except Exception: v.append(np.inf)
        v = np.array(v); i = int(np.argmin(v))
        lo, hi = A[max(i - 1, 0)], A[min(i + 1, len(A) - 1)]
        r = minimize_scalar(lambda a: P.chi_down(Ou, P.down_home_ss(tau, a, sg)) if P.down_home_ss(tau, a, sg) is not None else 1e12, bounds=(lo, hi), method='bounded', options=dict(xatol=1e-14))
        Od = P.down_home_ss(tau, r.x, sg)
        # behaviour at the ends
        ends = [(a, round(float(v[j]), 1)) for j, a in enumerate(A) if j in (0, 300, 700, 1100, len(A) - 1, len(A) - 300, len(A) - 700)]
        print(k, sg, 'min chi2 %.5g at a1=%.6e' % (r.fun, r.x), 'minEigIm %.2e' % np.linalg.eigvalsh(Od.imag).min(), 'finite', np.isfinite(v).sum(), 'ends', ends, flush=True)
