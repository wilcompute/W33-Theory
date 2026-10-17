import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys; sys.path.insert(0,'.'); from th import *
import numpy as np
import importlib.util
sys.path.insert(0, _ANA)
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2
rng=np.random.default_rng(0)
Om=np.array([[1+0.874j,0.003],[0.003,1+0.874j]]); print('conv check', np.abs(theta(Om)-theta_null_2(Om,N=40).reshape(3,3)).max())
tau=1+0.874j
for trial in range(3):
    td=rng.uniform(-.5,.5)+1j*rng.uniform(0.8,2); eu=1e-3*np.exp(1j*rng.uniform(0,6)); ed=2e-2*np.exp(1j*rng.uniform(0,6))
    V,su,sd=ckm(theta(np.array([[tau,eu],[eu,tau]])), theta(np.array([[tau,ed],[ed,td]])))
    print('no Wilson: |V| =\n', np.round(V,6))
    zd=0.05*(rng.normal()+1j*rng.normal())
    V,su,sd=ckm(theta(np.array([[tau,eu],[eu,tau]])), theta(np.array([[tau,ed],[ed,td]]),(0,zd)))
    print('right Wilson z_d: Vcb %.4f Vus %.4f Vub %.5f  ms/mb %.4f md/ms %.4f' % (V[1,0],V[2,1],V[2,0],sd[1],sd[2]/sd[1]))
