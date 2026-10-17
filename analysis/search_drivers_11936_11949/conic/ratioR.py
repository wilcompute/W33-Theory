import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
def R(t1, t2, eps=1e-3, d=(0,1)):
    Om = np.array([[t1, 0], [0, t2]], complex); Om[0,1] = Om[1,0] = eps*np.exp(1j*d[1])
    sv = np.linalg.svd(lib.theta_null_2(Om, N=40).reshape(3,3), compute_uv=False); sv = sv/sv[0]
    return sv[1], sv[2], sv[2]/sv[1]**2
w = np.exp(2j*np.pi/3)
for t1, t2 in [(1j,1j),(w,w),(1j,w),(1j,2j),(2j,2j),(1j,1.5j),(0.5+1.2j,1j),(3j,3j)]:
    for eps in (1e-2,1e-3):
        s2,s3,r = R(t1,t2,eps)
        print(t1,t2,'eps',eps,'s2/eps %.4f s3/eps2 %.4f R %.4f' % (s2/eps, s3/eps**2, r))
    print('  phase', R(t1,t2,1e-3,(0,1.0))[2])
