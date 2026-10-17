import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
from scipy.optimize import minimize_scalar
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c
    Yd=P42.normalised(np.array([[tau,ed],[ed,td]]),(0,zd))
    st=lambda p: np.linalg.svd(P42.theta(np.array([[tau,eu*np.exp(1j*p)],[eu*np.exp(1j*p),tau]])),compute_uv=False)[0]
    tb=lambda p: np.angle(np.linalg.det(P42.theta(np.array([[tau,eu*np.exp(1j*p)],[eu*np.exp(1j*p),tau]])))*np.linalg.det(Yd))
    tbu=lambda p: np.angle(np.linalg.det(P42.theta(np.array([[tau,eu*np.exp(1j*p)],[eu*np.exp(1j*p),tau]]))))
    for lab,f in (('min m_t',st),('max m_t',lambda p:-st(p))):
        for p0 in (0,np.pi/2):
            r=minimize_scalar(f,bounds=(p0,p0+np.pi/2+1e-9),method='bounded',options=dict(xatol=1e-10))
            print(k,lab,'phi*=%.4f arg(eps*)=%.4f  thetabar=%.4f  arg det Yu=%.4f'%(r.x,np.angle(eu*np.exp(1j*r.x)),tb(r.x),tbu(r.x)))
