import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,json,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
P=np.array([[1,0,0],[0,0,1],[0,1,0]])
odd=lambda v: np.linalg.norm(v-P@v)/2
rng=np.random.default_rng(1)
# lemma check: random unitary U_e; nu basis with odd nu2
nu=np.array([[2,1,0],[-1,1,1],[-1,1,-1]],float); nu/=np.linalg.norm(nu,axis=0)   # cols nu1 (even), nu3? -> set cols: nu1 even, nu2 odd, nu3 even
nu=np.column_stack([nu[:,0],nu[:,2],nu[:,1]])
viol=0
for _ in range(2000):
    A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)); Ue,_=np.linalg.qr(A)
    U=Ue.conj().T@nu
    for a in range(3):
        viol=max(viol, abs(U[a,1])-odd(Ue[:,a]))
print('lemma max violation (should be <=0):',viol)
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c; Om=np.array([[tau,ed],[ed,td]])
    UL=np.linalg.svd(P42.normalised(Om,(0,6*zd)).T)[0]   # tau, mu, e
    Ud=np.linalg.svd(P42.normalised(Om,(0,zd)))[2].conj().T   # right (5bar) vectors of down: b, s, d
    Uq=np.linalg.svd(P42.normalised(Om,(0,zd)))[0]           # left (10) vectors of down
    print(k,'charged-lepton odd fractions (tau,mu,e):',np.round([odd(UL[:,i]) for i in range(3)],3),' down-left (b,s,d):',np.round([odd(Uq[:,i]) for i in range(3)],3))
