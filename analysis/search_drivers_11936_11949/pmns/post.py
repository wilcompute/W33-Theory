import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_os.path.join(_DRV, 'ckm')); from th40 import theta
exec(open('pmns.py').read().split('FITS=')[0]); exec('def fk'+open('pmns.py').read().split('def fk')[1].split('for lab,x')[0])
def nth(Om,z):
    z=np.asarray(z); return theta(Om,z)*np.exp(-3*np.pi*z.imag@np.linalg.inv(Om.imag)@z.imag)
for b in (0,2):
    X=np.load(_os.path.join(_DATA, f'xs_{b}_7.npy')); A=[]
    for x in X[::6]:
        c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c; Om=np.array([[tau,ed],[ed,td]])
        Ue=np.linalg.svd(nth(Om,(0,6*zd)).T)[0][:,::-1]; Un=gs([fk(td,0),fk(td,1),fk(td,2)])[:,::-1]
        A.append(angles(Ue.conj().T@Un))
    A=np.array(A); print('branch',b,'n',len(A),'theta12 q05/50/95',np.round(np.quantile(A[:,0],[.05,.5,.95]),1),'theta23',np.round(np.quantile(A[:,1],[.05,.5,.95]),1),'theta13',np.round(np.quantile(A[:,2],[.05,.5,.95]),1))
