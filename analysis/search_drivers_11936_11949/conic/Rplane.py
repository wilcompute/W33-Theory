import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
rng=np.random.default_rng(7)
e1=np.array([1,0,0],complex)
th=0.01
for phi in [np.pi, np.pi/2, 0.0]:
    s=np.array([0,1,np.exp(1j*phi)])/np.sqrt(2)
    g=None
    for t in [0.03,0.1,0.3,1,2,4,10,100]:
        out=[]
        for pert in (e1, 1j*e1):
            u=np.cos(th)*s+np.sin(th)*pert; c=np.r_[1,t*u]; c/=np.linalg.norm(c)
            Om,res,g=lib.V.invert(c,rng,g)
            sv=np.linalg.svd(lib.theta_null_2(Om,N=40).reshape(3,3),compute_uv=False); sv/=sv[0]
            out.append((res,sv[1]/th,sv[2]/th**2,sv[2]/sv[1]**2))
        print('phi %.3f t %6g' % (phi,t), ' | '.join('res %.0e A %.4g B %.4g R %.4f' % o for o in out), flush=True)
