import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np,mpmath as mp
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
from scipy.optimize import brentq
MP=2.435e18
eta=lambda t: complex(mp.exp(2j*mp.pi*t/24)*mp.qp(mp.exp(2j*mp.pi*t)))
weber=lambda t: np.exp(-1j*np.pi/24)*eta((t+1)/2)/eta(t)
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau=c[0]; eu=c[2]
    print(k,'tau',np.round(tau,4),'|eps_u| %.5f'%abs(eu),'f_a = %.3e GeV'%(MP*abs(eu)/(3*tau.imag)))
mcmt=0.620/168.26; target=2*np.sqrt(1.23e-3*168.26/0.620**2)
rows=[]
for re in np.linspace(-0.5,0.5,21):
    try: y=brentq(lambda y: abs(weber(re+1j*y))**8-target, 0.15, 3.0)
    except ValueError: continue
    tau=re+1j*y; e=1e-4
    s=np.linalg.svd(P42.theta(np.array([[tau,e],[e,tau]])),compute_uv=False); kap=s[1]/s[0]/e
    eps=mcmt/kap; fa=MP*eps/(3*y)
    rows.append((re,y,kap,eps,fa)); print('Re tau %+.2f Im %.4f kappa %.4f |eps| %.5f f_a %.3e'%(re,y,kap,eps,fa))
F=np.array([r[4] for r in rows]); print('f_a range over Weber curve: %.3e - %.3e GeV'%(F.min(),F.max()))
