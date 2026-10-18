import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
# up home on the CP o SS fixed set: Omega = R45 diag(e^{ia},e^{ib}) R45^T  (Omega conj Omega = I)
import numpy as np, sys
from scipy.optimize import least_squares
sys.path.insert(0, _ANA)
from w33_pass12004_cp_real_bare_theta_no_fit import theta_c
T=(0.620/168.26,1.23e-3/0.620)
def up(a,b):
    lp,lm=np.exp(1j*a),np.exp(1j*b); tau=(lp+lm)/2; e=(lp-lm)/2
    return np.array([[tau,e],[e,tau]])
def r(p):
    O=up(*p); s=np.linalg.svd(theta_c(O,np.zeros(2,complex)),compute_uv=False)
    return [np.log(s[1]/s[0]/T[0]),np.log(s[2]/s[1]/T[1])]
if __name__=="__main__":
    best=[]
    for a0 in np.linspace(0.05,3.09,25):
      for b0 in np.linspace(0.05,3.09,25):
        if a0<=b0: continue
        try:
          x=least_squares(r,[a0,b0],bounds=([1e-3,1e-3],[np.pi-1e-3]*2)).x
          c=np.sum(np.square(r(x))); best.append((c,tuple(np.round(x,6))))
        except Exception: pass
    best=sorted(set(best))[:8]
    for c,x in best:
        O=up(*x); print('%.2e'%c, x, 'tau=',np.round(O[0,0],5),'eps=',np.round(O[0,1],6), '|tau|^2+|e|^2=',round(abs(O[0,0])**2+abs(O[0,1])**2,8))
