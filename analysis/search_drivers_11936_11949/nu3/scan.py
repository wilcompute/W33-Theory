import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA)
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2
Pm=np.array([[1,0,0],[0,0,1],[0,1,0]]); o=np.array([0,1,-1])/np.sqrt(2)
rng=np.random.default_rng(0); hits=[]; n=0
for _ in range(20000):
    tau=rng.uniform(-0.5,0.5)+1j*rng.uniform(0.3,2.5); w=rng.uniform(-0.5,0.5)+1j*rng.uniform(-1,1)*tau.imag*0.95
    Om=np.array([[tau,w],[w,tau]])
    if np.linalg.eigvalsh(Om.imag).min()<0.05: continue
    Y=theta_null_2(Om,N=25).reshape(3,3); n+=1
    U,s,_=np.linalg.svd(Y)
    oddness=[abs(np.vdot(o,U[:,i])) for i in range(3)]
    k=int(np.argmax(oddness))
    if k==0:
        hits.append((s[1]/s[0],s[2]/s[1],tau,w))
print('valid',n,'odd heaviest',len(hits))
if hits:
    H=np.array([(h[0],h[1]) for h in hits]); print('m2/m3 range',H[:,0].min(),H[:,0].max(),' m1/m2 range',H[:,1].min(),H[:,1].max())
    good=[h for h in hits if 0.1<h[0]<0.3]
    print('with m2/m3 in 0.1-0.3:',len(good)); [print(np.round(h[0],3),np.round(h[1],3),np.round(h[2],3),np.round(h[3],3)) for h in good[:8]]
R=0.0296
rat=[ (h[0]**2*(1-h[1]**2))/(1-h[0]**2*h[1]**2) for h in hits]
print('Dm21/Dm31 over odd-heaviest homes: min %.3f max %.3f (data %.4f)'%(min(rat),max(rat),R))
