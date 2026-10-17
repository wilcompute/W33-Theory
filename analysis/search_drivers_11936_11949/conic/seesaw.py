import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
tau = 1+0.8744555j
def Y(eps): return lib.theta_null_2(np.array([[tau,eps],[eps,tau]]), N=60).reshape(3,3)
def sv(M): s=np.linalg.svd(M,compute_uv=False); return s/s[0]
s0=sv(Y(1e-4)); R=s0[2]/s0[1]**2; kap=s0[1]/1e-4
print('R(tau) %.5f kappa %.4f' % (R,kap))
for eD,eM in [(1e-3,1e-2),(1e-3,3e-3),(3e-4,1e-3),(1e-3,1e-1),(2e-3,1e-2*np.exp(1j))]:
    mnu = Y(eD) @ np.linalg.inv(Y(eM)) @ Y(eD)
    s=sv(mnu); pred=kap*abs(eD)**2/abs(eM)
    print('eD %.0e eM %.0e : asym %.1e  R_nu %.5f (R %.5f)  s2 %.4e pred %.4e' % (abs(eD),abs(eM),np.abs(mnu-mnu.T).max()/np.abs(mnu).max(), s[2]/s[1]**2, R, s[1], pred))
