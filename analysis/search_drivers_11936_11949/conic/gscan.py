import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
def g2(t):
    eps=1e-4
    Om = np.array([[t, eps], [eps, t]], complex)
    sv = np.linalg.svd(lib.theta_null_2(Om, N=60).reshape(3,3), compute_uv=False); sv = sv/sv[0]
    return 2*sv[2]/sv[1]**2     # gamma(t)^2
best=[]
for x in np.linspace(-1.5,1.5,31):
    for y in [0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.866,1.0,1.2,1.5]:
        best.append((g2(x+1j*y), x, y))
best.sort()
for b in best[:12]: print('gamma^2 %.5f at %.2f+%.3fi' % b)
print('max', best[-1])
