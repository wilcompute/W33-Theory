"""TOE43 front 1: targeted elementary-abelian two-qutrit SIC search.

This is intentionally a *bounded numerical counterexample search*, not a
certificate of nonexistence. The group is F3^4 (80 Weyl displacements),
NOT the cyclic Z9^2 Weyl-Heisenberg group.
"""
from pathlib import Path
import itertools,json
import numpy as np
from scipy.optimize import least_squares
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe43_sic_search.json"
rng=np.random.default_rng(43001)
w=np.exp(2j*np.pi/3);I=np.eye(3,dtype=complex)
X=np.roll(I,1,axis=0);Z=np.diag([1,w,w*w])
point=lambda v:min(v,tuple(-x%3 for x in v))
P=sorted({point(v) for v in itertools.product(range(3),repeat=4) if any(v)})
assert len(P)==40
W=np.stack([np.kron(np.linalg.matrix_power(X,v[0])@np.linalg.matrix_power(Z,v[2]),
                     np.linalg.matrix_power(X,v[1])@np.linalg.matrix_power(Z,v[3])) for v in P])
def residual(x):
 v=x[:9]+1j*x[9:]
 v=v/np.linalg.norm(v)
 z=np.einsum("i,pij,j->p",v.conj(),W,v,optimize=True)
 return abs(z)**2-.1
results=[]
best=(float("inf"),None)
for i in range(48):
 seed=rng.normal(size=18)
 fit=least_squares(residual,seed,max_nfev=200,ftol=1e-12,xtol=1e-12,gtol=1e-12)
 r=residual(fit.x);sq=float(np.dot(r,r))
 results.append({"sum_sq_over_40":sq,"max_abs_residual":float(max(abs(r))),
                 "iterations":int(fit.nfev),"status":int(fit.status)})
 if sq<best[0]:best=(sq,fit.x.copy())
 if i%12==11:print("SIC run",i+1,"best",best[0],flush=True)
val,v=best
z=v[:9]+1j*v[9:];z/=np.linalg.norm(z)
q=2*(.1+residual(v))
assert abs(sum(q)-8)<1e-9
var=float((sum(q*q)-8/5)/135)
assert var>=-1e-11 and var<8/75
out={"status":"NO_FIDUCIAL_FOUND_NOT_A_PROOF",
"field":"F3^4 tensor-product Pauli group; distinguishes Z9^2 cyclic",
"search_restarts":48,"target_nontrivial_projective_overlap_sq":.1,
"residuals":results,"best_sum_squared_residual":val,
"best_max_absolute_overlap_sq_deviation":float(max(abs(residual(v)))),
"best_purity_variance":var,
"best_state":[[float(x.real),float(x.imag)] for x in z],
"mathematical_endpoint":"All 40 projective overlap squares =1/10 iff zero W33 90-frame purity variance iff elementary-abelian Pauli covariant SIC fiducial",
"boundary":"48 nonconvex numerical searches are neither a global bound nor SIC nonexistence proof. A cyclic d=9 SIC is not the same displacement group."}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k not in ["residuals","best_state"]}))
