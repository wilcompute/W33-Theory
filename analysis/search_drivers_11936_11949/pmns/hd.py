import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
from scipy.optimize import least_squares
Pm=np.array([[1,0,0],[0,0,1],[0,1,0]]); odd=lambda v: np.linalg.norm(v-Pm@v)/2
COLS={1:(0.82,0.36,0.43),2:(0.548,0.605,0.578),3:(0.148,0.74,0.66)}
L=P42.LEPTONS
def lep(Om,ze):
    U,s,_=np.linalg.svd(P42.normalised(Om,(0,ze)).T)   # tau, mu, e
    return s[1]/s[0], s[2]/s[1], [odd(U[:,2]),odd(U[:,1]),odd(U[:,0])]   # e, mu, tau
rng=np.random.default_rng(0)
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c; Om=np.array([[tau,ed],[ed,td]])
    for col,target in COLS.items():
        def res(p):
            ze=6*zd-5*(p[0]+1j*p[1])
            try: a,b,o=lep(Om,ze)
            except Exception: return [10]*5
            return [np.log(a/L['mmu_mtau'])/0.2, np.log(b/L['me_mmu'])/0.2]+[(o[i]-target[i])/0.05 for i in range(3)]
        best=None
        for s in range(40):
            p0=[rng.uniform(-0.5,0.5), rng.uniform(-0.03,0.03)]
            r=least_squares(res,p0,max_nfev=300)
            if best is None or r.cost<best.cost: best=r
        a,b,o=lep(Om,6*zd-5*(best.x[0]+1j*best.x[1]))
        print(k,'col',col,'chi2 %.2f'%(2*best.cost),'h_d',np.round(best.x,4),'mmu/mtau %.4f me/mmu %.5f odd(e,mu,tau)'%(a,b),np.round(o,3),flush=True)
