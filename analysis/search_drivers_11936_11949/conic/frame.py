import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
rng=np.random.default_rng(5)
s=np.array([0,1,-1])/np.sqrt(2); e1=np.array([1,0,0],complex)
import inspect; print(inspect.getsource(lib.V.invert)[:1500])
for th,t in [(0.1,0.01),(0.1,0.3),(0.0,0.3)]:
    u=np.cos(th)*s+np.sin(th)*e1; c=np.r_[1,t*u]; c/=np.linalg.norm(c)
    Om,res,g=lib.V.invert(c,rng,None); Omr=lib.S.siegel_reduce(Om)
    for O in (Om,Omr):
        sv=np.linalg.svd(lib.theta_null_2(O,N=40).reshape(3,3),compute_uv=False); print(th,t,np.round(O,4).tolist(), np.round(sv/sv[0],7))
