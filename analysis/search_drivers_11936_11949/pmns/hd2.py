import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
from scipy.optimize import least_squares
Pm=np.array([[1,0,0],[0,0,1],[0,1,0]]); odd=lambda v: np.linalg.norm(v-Pm@v)/2
L=P42.LEPTONS
def lep(Om,ze):
    U,s,_=np.linalg.svd(P42.normalised(Om,(0,ze)).T); return s[1]/s[0], s[2]/s[1], [odd(U[:,2]),odd(U[:,1]),odd(U[:,0])]
rng=np.random.default_rng(3)
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c; Om=np.array([[tau,ed],[ed,td]])
    sols=[]
    for s in range(300):
        p0=[rng.uniform(-1,1), rng.uniform(-0.06,0.06)]
        def res(p):
            try: a,b,o=lep(Om,6*zd-5*(p[0]+1j*p[1]))
            except Exception: return [10,10]
            return [np.log(a/L['mmu_mtau']), np.log(b/L['me_mmu'])]
        r=least_squares(res,p0,max_nfev=200)
        if r.cost<1e-10:
            ze=6*zd-5*(r.x[0]+1j*r.x[1]); ze=complex((ze.real+0.5)%1-0.5, ze.imag)   # Re periodic mod 1
            if not any(abs(ze-z)<1e-4 for z,_ in sols): sols.append((ze, lep(Om,6*zd-5*(r.x[0]+1j*r.x[1]))[2]))
    print(k,'distinct z_e solutions:',len(sols))
    for ze,o in sorted(sols,key=lambda t:(t[0].real,t[0].imag)): print('   z_e',np.round(ze,4),' odd(e,mu,tau)',np.round(o,3))
