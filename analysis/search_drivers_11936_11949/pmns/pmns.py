import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,json,numpy as np
sys.path.insert(0,_os.path.join(_DRV, 'ckm')); from th40 import theta
FITS=json.load(open(_os.path.join(_DATA, f'hy2_polished.json')))
def fk(tau,k,N=60):
    n=np.arange(-N,N+1); return np.array([np.sum((n+c/3)**k*np.exp(3j*np.pi*tau*(n+c/3)**2)) for c in range(3)])
def gs(vs):
    out=[]
    for v in vs:
        w=v.astype(complex)
        for u in out: w=w-np.vdot(u,w)*u
        out.append(w/np.linalg.norm(w))
    return np.array(out).T          # columns: heaviest, middle, lightest
def angles(U):
    s13=abs(U[0,2]); c13=np.sqrt(1-s13**2)
    return np.degrees([np.arcsin(abs(U[0,1])/c13), np.arcsin(abs(U[1,2])/c13), np.arcsin(s13)])
for lab,x in zip('AB',(FITS[0],FITS[2])):
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c; Om=np.array([[tau,ed],[ed,td]])
    Ye=theta(Om,(0,6*zd)).T          # rows L (5bar index), cols e^c
    UL,se,_=np.linalg.svd(Ye)        # columns: tau, mu, e (descending)
    Ue=UL[:,::-1]                    # e, mu, tau
    Fn=gs([fk(td,0),fk(td,1),fk(td,2)])   # nu3, nu2, nu1 (descending, NO)
    Un=Fn[:,::-1]                    # nu1, nu2, nu3
    U=Ue.conj().T@Un
    print(lab,'|U|=\n',np.round(np.abs(U),3),'\n theta12, theta23, theta13 =',np.round(angles(U),1),' (data 33.4, 49, 8.6)')
    print('  nu basis |components|:\n',np.round(np.abs(Fn),3),'\n  e basis:\n',np.round(np.abs(UL),3))
