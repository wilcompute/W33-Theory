import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,json,numpy as np
sys.path.insert(0,_os.path.join(_DRV, 'ckm')); from th40 import theta
exec(open('pmns.py').read().split('for lab,x')[0])
def fkz(tau,k,z,N=60):
    n=np.arange(-N,N+1); return np.array([np.sum((n+c/3)**k*np.exp(3j*np.pi*tau*(n+c/3)**2+6j*np.pi*(n+c/3)*z)) for c in range(3)])
TBM=np.array([[2/np.sqrt(6),1/np.sqrt(3),0],[-1/np.sqrt(6),1/np.sqrt(3),-1/np.sqrt(2)],[-1/np.sqrt(6),1/np.sqrt(3),1/np.sqrt(2)]])
for t in [0.01j,-0.0629+0.0175j,0.001+0.001j]:
    F=gs([fk(t,0),fk(t,1),fk(t,2)])[:,::-1]
    print('tau',t,'max | |F|-|TBM| | = %.2e' % np.abs(np.abs(F)-np.abs(TBM)).max())
for lab,x in zip('AB',(FITS[0],FITS[2])):
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c; Om=np.array([[tau,ed],[ed,td]])
    Ue=np.linalg.svd(theta(Om,(0,6*zd)).T)[0][:,::-1]
    for r in (0,1,2,3,-1.5,-3,6):
        Un=gs([fkz(td,0,r*zd),fkz(td,1,r*zd),fkz(td,2,r*zd)])[:,::-1]
        U=Ue.conj().T@Un
        print(lab,'z_nu/z_d =',r,' angles',np.round(angles(U),1))
