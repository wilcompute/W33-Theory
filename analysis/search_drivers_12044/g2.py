import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
F=np.exp(2j*np.pi*np.outer(range(3),range(3))/3)/np.sqrt(3); I3=np.eye(3)
def act(M,Om,z):
    A,B,C,D=M[:2,:2],M[:2,2:],M[2:,:2],M[2:,2:]
    W=C@Om+D; Om2=(A@Om+B)@np.linalg.inv(W); z2=np.linalg.inv(W).T@z
    return Om2,z2
Z2=np.zeros((2,2))
S_full=np.block([[Z2,-np.eye(2)],[np.eye(2),Z2]])
S_1=np.block([[np.diag([0,1]),np.diag([-1,0])],[np.diag([1,0]),np.diag([0,1])]])
rng=np.random.default_rng(1)
def rand():
    X=rng.uniform(-.4,.4,(2,2)); X=(X+X.T)/2; A=rng.normal(size=(2,2)); Y=A@A.T*0.1+np.diag(rng.uniform(.7,1.3,2))
    return X+1j*Y, np.array([0,0])+0.0j, np.array([0.05+0.03j,0.1-0.02j])
for name,M,L,R in (('S x S',S_full,F,F),('S x 1',S_1,F,I3)):
    for withz in (False,True):
        Om,z0,z1=rand(); z=z1 if withz else z0
        Om2,z2=act(M,Om,z)
        Y=P42.theta(Om,z); Y2=P42.theta(Om2,z2)
        best=1e9
        for LL in (L,L.conj()):
            for RR in (R,R.conj()):
                T=LL@Y@RR.T; r=Y2/T; best=min(best,np.abs(r-r.mean()).max()/abs(r.mean()))
        print(name,'with Wilson' if withz else 'no Wilson','| entrywise ratio spread vs (F)Y(F)^T:',f'{best:.2e}')
