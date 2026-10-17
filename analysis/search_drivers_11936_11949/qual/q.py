import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau=c[0]; eu=c[2]
    phis=np.linspace(0,2*np.pi,73)[:-1]; S=[]
    for p in phis:
        e=eu*np.exp(1j*p); S.append(np.linalg.svd(P42.theta(np.array([[tau,e],[e,tau]])),compute_uv=False))
    S=np.array(S)
    for i,n in enumerate(('top','charm','up')):
        v=S[:,i]; amp=(v.max()-v.min())/(2*v.mean())
        # Fourier content
        F=np.abs(np.fft.rfft(v-v.mean()))/len(v)*2/v.mean()
        print(k,n,'relative modulation %.3e'%amp,' dominant harmonics',np.argsort(F)[::-1][:2],np.round(F[np.argsort(F)[::-1][:2]],10))
    print(k,'|eps_u| %.5f (6 pi eps)^2 = %.3e'%(abs(eu),(6*np.pi*abs(eu))**2))
