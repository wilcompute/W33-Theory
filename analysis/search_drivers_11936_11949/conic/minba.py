import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
rng = np.random.default_rng(int(sys.argv[1]))
state = {'guess': None}
def ba(x):
    u = x[:3]+1j*x[3:]; u = u/np.linalg.norm(u)
    c = np.r_[1, 0.005*u]; c /= np.linalg.norm(c)
    try:
        Om, res, g = lib.V.invert(c, rng, state['guess'])
    except Exception:
        return 2.0
    if res > 1e-8: return 2.0
    state['guess'] = g; Om = lib.S.siegel_reduce(Om)
    sv = np.linalg.svd(lib.theta_null_2(Om, N=40).reshape(3, 3), compute_uv=False)
    if sv[1]/sv[0] > 0.05 or sv[1]/sv[0] < 1e-6: return 2.0       # stay in the one-dimensional cusp regime
    return sv[2]/sv[1]
x0 = rng.normal(size=6)
r = minimize(ba, x0, method='Nelder-Mead', options=dict(maxiter=300, xatol=1e-4, fatol=1e-6))
u = r.x[:3]+1j*r.x[3:]; u /= np.linalg.norm(u)
print('seed', sys.argv[1], 'min b/a %.5f' % r.fun, 'nfev', r.nfev, 'M2 %.4f' % lib.H23.magic(u), 'u', np.round(u, 4).tolist(), flush=True)
