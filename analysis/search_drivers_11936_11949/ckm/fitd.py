import sys; sys.path.insert(0,'.'); from th import *
import numpy as np
from scipy.optimize import least_squares
EMAX=float(sys.argv[4])
DATA=dict(mc_mt=0.620/168.26, mu_mc=1.23e-3/0.620, ms_mb=0.053/2.86, md_ms=2.67e-3/0.053, Vus=0.2250, Vcb=0.0411, Vub=0.00382)
def unpack(x):
    c=x[0::2]+1j*x[1::2]
    tau,td,eu,ed,w,z1,z2=c[0],c[1],c[2],c[3],c[4],c[5],c[6]
    return tau,td,eu,ed,w,z1,z2
def obs(x):
    tau,td,eu,ed,w,z1,z2=unpack(x)
    if tau.imag<0.08 or td.imag<0.08: return None
    Yu=theta(np.array([[tau,eu],[eu,tau]]),(w,w)); Yd=theta(np.array([[tau,ed],[ed,td]]),(z1,z2))
    if not (np.all(np.isfinite(Yu)) and np.all(np.isfinite(Yd))): return None
    Om=np.array([[tau,ed],[ed,td]]).imag
    if np.linalg.eigvalsh(Om).min()<0.05: return None
    V,su,sd=ckm(Yu,Yd)
    return dict(mc_mt=su[1],mu_mc=su[2]/su[1],ms_mb=sd[1],md_ms=sd[2]/sd[1],Vus=V[2,1],Vcb=V[1,0],Vub=V[2,0])
def resid(x, keys):
    o=obs(x)
    if o is None: return np.full(len(keys)+2,30.)
    tau,td,eu,ed,w,z1,z2=unpack(x)
    pen=[10*max(0,np.log(abs(e)/EMAX)) for e in (eu,ed)]
    return np.array([np.log(max(o[k],1e-30)/DATA[k]) for k in keys]+pen)
seed=int(sys.argv[1]); keys=sys.argv[2].split(',')
rng=np.random.default_rng(seed); best=None
for s in range(int(sys.argv[3])):
    x0=np.array([rng.uniform(-.5,.5),rng.uniform(.6,1.6), rng.uniform(-.5,.5),rng.uniform(.6,2.5),
                 *(10**rng.uniform(-4,-1.5)*np.array([np.cos(a:=rng.uniform(0,6.3)),np.sin(a)])),
                 *(10**rng.uniform(-3,-0.5)*np.array([np.cos(a:=rng.uniform(0,6.3)),np.sin(a)])),
                 *rng.normal(0,0.15,6)])
    r=least_squares(resid,x0,args=(keys,),method='trf',max_nfev=400)
    if best is None or r.cost<best.cost: best=r
o=obs(best.x)
print('seed',seed,'keys',sys.argv[2],'cost %.3g'%best.cost, {k:round(float(v),5) for k,v in o.items()}, 'x',np.round(best.x,4).tolist(), flush=True)
