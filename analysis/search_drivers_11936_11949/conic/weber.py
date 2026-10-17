import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np, mpmath as mp
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
from w33_pass11869_11873_siegel_level3_two_qutrits import j_of_tau
eta=lambda t: complex(mp.exp(2j*mp.pi*t/24)*mp.qp(mp.exp(2j*mp.pi*t)))
weber=lambda t: np.exp(-1j*np.pi/24)*eta((t+1)/2)/eta(t)
def Rnum(t1,t2,eps):
    Om=np.array([[t1,eps],[eps,t2]]); sv=np.linalg.svd(lib.theta_null_2(Om,N=60).reshape(3,3),compute_uv=False)
    return sv[0]*sv[2]/sv[1]**2
rng=np.random.default_rng(3); errs=[]
for _ in range(10):
    t1,t2=[rng.uniform(-1,1)+1j*rng.uniform(0.5,2) for _ in range(2)]
    eps=1e-4*np.exp(1j*rng.uniform(0,6.28))
    pred=abs(weber(t1)*weber(t2))**8/4; errs.append(abs(Rnum(t1,t2,eps)/pred-1))
    x=weber(t1)**24; j=j_of_tau(t1); errs_c=abs((x-16)**3-j*x)/abs(j*x)
    print('%.3e  cubic %.1e' % (errs[-1], errs_c))
