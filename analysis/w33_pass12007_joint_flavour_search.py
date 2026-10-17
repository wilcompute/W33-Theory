"""Reproduce the shared12007 charged fit from prior12005 seed; numericalsearchonly."""
import numpy as np,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from w33_pass12005_cp_real_theta_barr import FIT as PRIOR_FIT
OUTPUT=Path(__file__).resolve().parents[1]/"data/w33_pass12007_joint_search_record.json"
from scipy.optimize import root,least_squares
n=np.arange(-10,11);n1,n2=np.meshgrid(n,n,indexing='ij');v1=n1[None,None,:,:]+np.arange(3)[:,None,None,None]/3;v2=n2[None,None,:,:]+np.arange(3)[None,:,None,None]/3
D=np.exp(1j*np.pi*np.arange(3)**2/3)
def theta(y,eu,yd,ed,z,up=False):
 O11=1+1j*y;O22=O11 if up else 1j*yd;e=1j*(eu if up else ed)
 A=np.exp(3j*np.pi*(O11*v1*v1+2*e*v1*v2+O22*v2*v2)+6j*np.pi*v2*(0 if up else 1j*z)).sum(axis=(-2,-1))
 A=D.conj()[:,None]*A
 if up:A=A*D.conj()[None,:]
 assert abs(A.imag).max()<1e-8*abs(A).max()
 return A.real/np.linalg.norm(A)
Utarget=np.array([.620/168.26,1.23e-3/.620])
def f(p):
 a=np.linalg.svd(theta(p[0],p[1],0,0,0,True),compute_uv=False);return np.log(np.array([a[1]/a[0],a[2]/a[1]])/Utarget)
r=root(f,[.8745,.00552]);assert r.success;y,eu=r.x;Yu=theta(y,eu,0,0,0,True);Uu=np.linalg.svd(Yu)[0]
target=np.array([.053/2.86,2.67e-3/.053,.225,.0411,.00382,3.08e-5])
def model(p):
 yd=np.exp(p[0]);ed=p[1];zi=p[2]
 if y*yd-ed*ed<.005:return None
 m=theta(y,eu,yd,ed,zi)
 b=np.array([p[3],p[4]+1j*p[5],p[6]+1j*p[7]])
 K=np.eye(3)-np.outer(b.conj(),b)/(1+np.vdot(b,b).real)
 ev,O=np.linalg.eigh(K);A=(O*np.sqrt(ev))@O.conj().T
 Ud,sd,_=np.linalg.svd(m@A);V=(Uu.conj().T@Ud)[::-1,::-1]
 J=np.imag(V[0,0]*V[1,1]*V[0,1].conj()*V[1,0].conj())
 obs=np.array([sd[1]/sd[0],sd[2]/sd[1],abs(V[0,1]),abs(V[1,2]),abs(V[0,2]),J])
 e=theta(y,eu,yd,ed,6*zi).T
 se=np.linalg.svd(A.T@e,compute_uv=False)
 return np.r_[obs,se[1]/se[0],se[2]/se[1]],m,b

target=np.r_[target,102.718/1746.24,.48657/102.718]
def residual(p):
 try:q=model(p)
 except (AssertionError,np.linalg.LinAlgError,FloatingPointError):return np.ones(8)*100
 if q is None:return np.ones(8)*100
 obs=q[0];return np.r_[np.log(np.maximum(obs[:5],1e-30)/target[:5]),(obs[5]-target[5])/target[5],np.log(np.maximum(obs[6:],1e-30)/target[6:])]
rng=np.random.default_rng(12005);best=None
for i in range(12):
 seed=PRIOR_FIT.copy()
 p=seed if i==0 else seed+rng.normal(size=8)*np.r_[.5,.03,.03,np.ones(5)*3]
 fit=least_squares(residual,p,max_nfev=1000,ftol=1e-11,xtol=1e-11,gtol=1e-11,bounds=([-5,-.2,-.2,-30,-30,-30,-30,-30],[1,.2,.2,30,30,30,30,30]))
 if best is None or np.linalg.norm(fit.fun)<np.linalg.norm(best.fun):
  best=fit;print(i,float(np.linalg.norm(best.fun)),model(best.x)[0],flush=True)
  obs,m,b=model(best.x);json.dump(dict(y=y,eu=eu,x=best.x.tolist(),obs=obs.tolist(),residual=best.fun.tolist(),real_m=m.tolist(),B=[[v.real,v.imag] for v in b]),open(OUTPUT,'w'),indent=2)
 if np.linalg.norm(best.fun)<1e-7:break
