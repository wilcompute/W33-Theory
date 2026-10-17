import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
rng = np.random.default_rng(2)
for phi in [np.pi, 0.0, 1.0484]:
    s = np.array([0, 1, np.exp(1j*phi)])/np.sqrt(2)
    for t in [0.01, 0.1, 1.0]:
        c = np.r_[1, t*s]; c /= np.linalg.norm(c)
        Om, res, g = lib.V.invert(c, rng, None); Om = lib.S.siegel_reduce(Om)
        th = lib.theta_null_2(Om, N=40)
        sv = np.linalg.svd(th.reshape(3,3), compute_uv=False)
        print('phi %.3f t %g res %.0e ImOm %s sv %s' % (phi, t, res, np.round(np.diag(Om).imag,4), np.round(sv/sv[0],8)), flush=True)
