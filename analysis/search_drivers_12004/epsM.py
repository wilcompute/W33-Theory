import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
import sys,numpy as np
sys.path.insert(0,_ANA); from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2
from scipy.optimize import brentq
tau=1+0.8744555j
D21,D31=7.42e-5,2.511e-3
def Y(e): return theta_null_2(np.array([[tau,e],[e,tau]]),N=60).reshape(3,3)
def m1_for(eM,phD=0.0,phM=0.0):
    # choose eps_D so that the seesaw spectrum matches Dm21/Dm31 (normal ordering), then report m1
    def spec(eD):
        m=Y(eD*np.exp(1j*phD))@np.linalg.inv(Y(eM*np.exp(1j*phM)))@Y(eD*np.exp(1j*phD))
        s=np.sort(np.linalg.svd(m,compute_uv=False))  # m1<m2<m3 relative
        return s/s[2]
    def f(eD):
        s=spec(eD); return (s[1]**2-s[0]**2)/(1-s[0]**2)-D21/D31
    grid=np.logspace(-4,-0.5,60); vals=[f(g) for g in grid]
    for i in range(len(grid)-1):
        if vals[i]*vals[i+1]<0:
            eD=brentq(f,grid[i],grid[i+1]); s=spec(eD); m3=np.sqrt(D31/(1-s[0]**2)); return eD, 1e3*s[0]*m3
    return None,None
for eM in (1e-3,3e-3,1e-2,3e-2,5e-2):
    out=[m1_for(eM,phD,phM) for phD,phM in ((0,0),(1.0,0),(0,1.0),(2.0,0.7))]
    print('eps_M %.0e'%eM,' m1 (meV) over phases:',[round(o[1],3) if o[1] else None for o in out], ' eps_D',[round(o[0],4) if o[0] else None for o in out])
