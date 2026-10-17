import sys,ast,numpy as np
sys.path.insert(0,'.'); from th40 import theta
from scipy.optimize import least_squares
DATA=dict(mc_mt=0.620/168.26, mu_mc=1.23e-3/0.620, ms_mb=0.053/2.86, md_ms=2.67e-3/0.053, Vus=0.2250, Vcb=0.0411, Vub=0.00382, J=3.08e-5)
def obs(x):
    c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,z2=c
    if tau.imag<0.03 or td.imag<0.005 or np.linalg.eigvalsh(np.array([[tau,ed],[ed,td]]).imag).min()<0.003: return {k:1e-30 for k in DATA}
    Yu=theta(np.array([[tau,eu],[eu,tau]])); Yd=theta(np.array([[tau,ed],[ed,td]]),(0,z2))
    if not (np.isfinite(Yu).all() and np.isfinite(Yd).all()): return {k:1e-30 for k in DATA}
    Uu,su,_=np.linalg.svd(Yu); Ud,sd,_=np.linalg.svd(Yd); V=(Uu.conj().T@Ud)[::-1,::-1]
    J=abs(np.imag(V[0,0]*V[1,1]*np.conj(V[0,1])*np.conj(V[1,0])))
    return dict(mc_mt=su[1]/su[0],mu_mc=su[2]/su[1],ms_mb=sd[1]/sd[0],md_ms=sd[2]/sd[1],Vus=abs(V[0,1]),Vcb=abs(V[1,2]),Vub=abs(V[0,2]),J=J)
out=[]
for s in (41,43,45,46):
    t=open(f'hy2_{s}.txt').read(); x0=np.array(ast.literal_eval(t[t.index(' x ')+3:].strip()))
    r=least_squares(lambda x:[np.log(obs(x)[k]/DATA[k]) for k in DATA],x0,method='trf',xtol=1e-14,ftol=1e-14,max_nfev=300)
    c=r.x[0::2]+1j*r.x[1::2]; tau,td,eu,ed,z2=c
    sd=np.linalg.svd(theta(np.array([[tau,ed],[ed,td]]),(0,z2)),compute_uv=False)
    line=f'seed {s} maxres {np.abs(r.fun).max():.1e} z_d {np.round(z2,4)} :'
    for rat in (-1.5,0,6,1.5,-6):
        se=np.linalg.svd(theta(np.array([[tau,ed],[ed,td]]),(0,rat*z2)).T,compute_uv=False)
        line+=f' | r={rat}: {se[1]/se[0]:.4f} {se[2]/se[1]:.5f} yb/yt {sd[0]/se[0]:.3f}'
    print(line, flush=True); out.append(r.x.tolist())
import json; json.dump(out,open('hy2_polished.json','w'))
