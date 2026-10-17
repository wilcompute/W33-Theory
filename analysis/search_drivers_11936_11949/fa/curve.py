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
mcmt=0.620/168.26; target=2*np.sqrt(1.23e-3*168.26/0.620**2)
ys=np.linspace(0.12,2.5,120); out=[]
for re in np.linspace(-1,1,41):
    g=[abs(weber(re+1j*y))**8-target for y in ys]
    for i in range(len(ys)-1):
        if g[i]*g[i+1]<0:
            y=brentq(lambda y: abs(weber(re+1j*y))**8-target, ys[i], ys[i+1]); tau=re+1j*y; e=1e-4
            s=np.linalg.svd(P42.theta(np.array([[tau,e],[e,tau]])),compute_uv=False); kap=s[1]/s[0]/e
            out.append((re,y,kap,MP*mcmt/kap/(3*y)))
O=np.array(out); print(len(O),'points')
for r in O[::max(1,len(O)//15)]: print('tau %+.3f%+.3fi kappa*Im %.4f f_a %.4e'%(r[0],r[1],r[2]*r[1],r[3]))
print('f_a min %.4e max %.4e'%(O[:,3].min(),O[:,3].max()), ' kappa*Im range',(O[:,2]*O[:,1]).min(),(O[:,2]*O[:,1]).max())
