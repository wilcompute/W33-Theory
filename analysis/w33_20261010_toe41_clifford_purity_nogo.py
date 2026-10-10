"""TOE41: full finite symplectic/Clifford twirl of two-qutrit purity.

Finite Clifford-invariant purity is a constant, hence cannot by itself
stabilize a genus-two period matrix or furnish CP spontaneous breaking.
All 90 symplectic (nonisotropic) 2-planes in F_3^4 are enumerated exactly.
"""
import itertools,sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261010_toe40_four_controls import theta
OUT=ROOT/"data/w33_20261010_toe41_clifford_purity_no_go.json"
V=list(itertools.product(range(3),repeat=4))
def negate(v):return tuple(-t%3 for t in v)
def canon(v):return min(v,negate(v))
def symp(x,y):return (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
pts=sorted({canon(v) for v in V if any(v)})
assert len(pts)==40
planes=set()
for i,p in enumerate(pts):
 for q in pts[i+1:]:
  if symp(p,q)==0:continue
  pl=frozenset(tuple((a*p[j]+b*q[j])%3 for j in range(4))
               for a,b in itertools.product(range(3),repeat=2) if a or b)
  assert len(pl)==8
  planes.add(pl)
assert len(planes)==90
occ={v:sum(v in pl for pl in planes) for v in V if any(v)}
assert set(occ.values())=={9}
w=np.exp(2j*np.pi/3);I=np.eye(3,dtype=complex)
X=np.roll(I,1,axis=0);Z=np.diag([1,w,w*w])
P=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a,b in itertools.product(range(3),repeat=2)]
W={}
for v in V:
 W[v]=np.kron(np.linalg.matrix_power(X,v[0])@np.linalg.matrix_power(Z,v[2]),
             np.linalg.matrix_power(X,v[1])@np.linalg.matrix_power(Z,v[3]))
def record(A):
 psi=A.reshape(9)/np.linalg.norm(A)
 coeff={v:float(abs(np.vdot(psi,W[v]@psi))**2) for v in V if any(v)}
 assert abs(sum(coeff.values())-8)<1e-10
 pur=[(1+sum(coeff[v] for v in pl))/3 for pl in planes]
 assert all(1/3-1e-10<=z<=1+1e-10 for z in pur)
 av=float(np.mean(pur));assert abs(av-0.6)<1e-12
 return dict(mean=av,min=float(min(pur)),max=float(max(pur)),
             variance=float(np.var(pur)),total_nonidentity_pauli_power=sum(coeff.values()))
base=theta(.173+1.07j,.286+1.29j,0)
entangled=theta(.173+1.07j,.286+1.29j,1)
rng=np.random.default_rng(413)
cases={"product_theta":record(base),"CZ_sheared_theta":record(entangled),
       "nonseparable_theta":record(theta(.173+1.07j,.286+1.29j,.12)),
       "generic_random":record(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))}
assert max(x["mean"] for x in cases.values())-min(x["mean"] for x in cases.values())<1e-12
assert abs(cases["generic_random"]["variance"]-cases["product_theta"]["variance"])>1e-4
out=dict(status="PASS_NO_GO",projective_points=len(pts),nondegenerate_planes=len(planes),
         incidence_per_nonzero_pauli=sorted(set(occ.values())),
         universal_clifford_twirl_purity=0.6,cases=cases,
         derivation="Each of 90 nondegenerate symplectic 2-planes has 8 nonidentity Pauli operators. Each of 80 nonidentity Paulis lies in 9 such planes. For normalized pure 9-state sum_{v!=0}|<W_v>|^2=8. Thus mean reduced-factor purity=(1+(9/90)*8)/3=3/5 exactly.",
         boundary="Finite Sp(4,3) / Clifford-frame invariant. Does not identify a full Siegel modular function or construct a CP-breaking potential. A nonconstant modular vacuum observable requires more than this averaged quartic purity.")
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
