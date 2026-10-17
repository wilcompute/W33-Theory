import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np, mpmath as mp
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
def fk(tau,k,N=60):
    n=np.arange(-N,N+1); return np.array([np.sum((n+c/3)**k*np.exp(3j*np.pi*tau*(n+c/3)**2)) for c in range(3)])
def gam_closed(t):
    f0,f1,f2=fk(t,0),fk(t,1),fk(t,2)
    W=np.linalg.norm(np.cross(f0,f2))  # |f0 ^ f2| via cross product magnitude (complex): use Gram
    G=np.array([[np.vdot(a,b) for b in (f0,f2)] for a in (f0,f2)]); W=np.sqrt(abs(np.linalg.det(G)))
    return W/np.vdot(f1,f1).real
def gam_num(t):
    eps=1e-4; Om=np.array([[t,eps],[eps,t]]); sv=np.linalg.svd(lib.theta_null_2(Om,N=60).reshape(3,3),compute_uv=False)
    return np.sqrt(2*sv[2]*sv[0]/sv[1]**2)
for t in [1j, 1+1j, np.exp(2j*np.pi/3), 0.3+0.9j, -0.2+1.4j]:
    print(t, gam_closed(t), gam_num(t))
# eta regression
eta=lambda t: complex(mp.exp(2j*mp.pi*t/24)*mp.qp(mp.exp(2j*mp.pi*t)))
rng=np.random.default_rng(0); X=[];Y=[]
args=[0.5,1,1.5,2,3,6,1/3,2/3,1/6]
for _ in range(40):
    t=rng.uniform(-0.5,0.5)+1j*rng.uniform(0.6,1.6)
    X.append([np.log(abs(eta(a*t))) for a in args]+[1.0, np.log(t.imag)]); Y.append(np.log(gam_closed(t)))
X=np.array(X);Y=np.array(Y); c,res,*_=np.linalg.lstsq(X,Y,rcond=None)
print('coef',dict(zip(args+['const','logy'],np.round(c,4))),'resid',np.abs(X@c-Y).max())
