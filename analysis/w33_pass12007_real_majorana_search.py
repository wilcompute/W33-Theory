"""Reproduce12007 realMajorana witness; no independent complexphase."""
import json,sys,numpy as np
from pathlib import Path
from scipy.optimize import least_squares
sys.path.insert(0,str(Path(__file__).resolve().parent))
from w33_pass12007_shared_theta_leptons import joint_observables
_,_,charged,A=joint_observables()
OUTPUT=Path(__file__).resolve().parents[1]/"data/w33_pass12007_neutrino_search_record.json"
target=np.array([.304,.573,.02219,7.42e-5/.002511]);rng=np.random.default_rng(120073)
_,ue=np.linalg.eigh(charged.conj()@charged.T)
def obs(p):
 L=np.array([[np.exp(p[0]),0,0],[p[2],np.exp(p[1]),0],[p[3],p[4],1.]])
 n=L@L.T;nu=A.T@n@A;_,sv,vh=np.linalg.svd(nu);order=np.argsort(sv);ss=sv[order];U=ue.conj().T@vh.conj().T[:,order];Q=abs(U)**2
 o=np.array([Q[0,1]/(1-Q[0,2]),Q[1,2]/(1-Q[0,2]),Q[0,2],(ss[1]**2-ss[0]**2)/(ss[2]**2-ss[0]**2)])
 return o,n,U,ss
best=1e9
for j in range(30):
 fit=least_squares(lambda p:np.log(obs(p)[0]/target),np.r_[rng.uniform(-2,2,2),rng.normal(size=3)],bounds=([-6,-6,-10,-10,-10],[6,6,10,10,10]),max_nfev=1000,xtol=1e-12,ftol=1e-12,gtol=1e-12)
 err=np.linalg.norm(fit.fun)
 if err<best:
  best=err;print(j,err,fit.x,flush=True)
  if err<1e-7:
   o,n,U,ss=obs(fit.x);J=float((U[0,0]*U[1,1]*U[0,1].conj()*U[1,0].conj()).imag);m3=np.sqrt(.002511/(1-(ss[0]/ss[2])**2));json.dump(dict(x=fit.x.tolist(),real_bare_Majorana=n.tolist(),obs=o.tolist(),J=J,masses_eV=(ss/ss[2]*m3).tolist()),open(OUTPUT,'w'),indent=2)
 if err<1e-7:break
