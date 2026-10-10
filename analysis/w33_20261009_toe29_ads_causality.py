"""Round29 test the NEW Pass11831-11833 finite AdS4 tangent cone.
Reconstruct the 81 Minkowski analogy vectors without full group
enumeration; calculate graph heat dimension and an exact time-order
obstruction for finite translation-invariant causal relations.
"""
import sys,json,math
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11831_11833_finite_ads4 as F
OUT=ROOT/'data/w33_20261009_toe29_finite_ads_causality_test.json'
def run():
 k0=next(k for k in F.PTS if F.Q[k]==2)
 subset=[k for k in F.PTS if F.beta(k,k0)==0]
 zero=F.vec_key(np.zeros((4,4),dtype=np.int64))
 states={zero}
 for k in subset:
  for s in (1,2):states.add(F.vec_key(s*F.JM[k]))
 states=sorted(states);assert len(states)==81
 mat=[np.array(v,dtype=np.int64).reshape(4,4) for v in states]
 iq={v:i for i,v in enumerate(states)}
 norm=[F.scalar_of(F.m(M,M)) for M in mat]
 assert {v:norm.count(v) for v in set(norm)}=={0:21,1:30,2:30}
 A=np.zeros((81,81),dtype=np.int16)
 for i,X in enumerate(mat):
  for j,Y in enumerate(mat):
   Z=(X-Y)%3
   if i!=j and F.scalar_of(F.m(Z,Z))==0:A[i,j]=1
 assert np.all(A==A.T) and np.all(A.sum(1)==20)
 assert np.array_equal(A@A,20*np.eye(81,dtype=int)+A+6*(np.ones((81,81),dtype=int)-np.eye(81,dtype=int)-A))
 eig=np.linalg.eigvalsh(A.astype(float))
 for val,mul in ((20,1),(2,60),(-7,20)):
  assert sum(abs(eig-val)<1e-7)==mul
 def dim(t):
  terms=[(1,0.),(60,.9),(20,1.35)]
  heat=sum(m*math.exp(-t*lam) for m,lam in terms)/81
  moment=sum(m*lam*math.exp(-t*lam) for m,lam in terms)/81
  return heat,2*t*moment/heat
 records=[dict(t=t,heat_trace=dim(t)[0],spectral_dimension=dim(t)[1]) for t in (.25,.5,1,2,3,4,6,8,12,20)]
 assert abs(records[0]['heat_trace']-1)<.25
 # No translation-invariant nonempty STRICT time order on a finite
 # group: x -> x+v repeated 3 times closes cycle (all v have order3).
 # Both 20 null steps and any supposed timelike step fail transitivity
 # plus irreflexivity if future oriented by a fixed cone.
 assert not np.any(np.diag(A))
 for i,j in np.argwhere(A):
  if i!=j:
   X=mat[i];V=(mat[j]-X)%3
   # x, x+v, x+2v, x+3v=x is cyclic: no time-orientation
   assert F.vec_key(X+3*V)==F.vec_key(X)
   break
 out=dict(status='PASS',
  prior='Pass11831-11833 already established five-dimensional traceless bivectors, 40+45+36 orbit, Kramers observer SL2(F9) Lorentz analogy, and Brouwer-Haemers 81-vertex null graph SRG(81,20,1,6). Those results are NOT discoveries of this pass.',
  exact_reconstructed_graph='SRG(81,20,1,6)',
  adjacency_spectrum={'20':1,'2':60,'-7':20},
  full_Laplacian_spectrum={'0':1,'0.9':60,'1.35':20},
  graph_diameter=2,
  heat_spectral_dimension_samples=records,
  finite_time_orientation_no_go='For an additive group V=(F3)^4, any translation-invariant nontrivial strict partial chronology is impossible. If 0 precedes a nonzero v, translation invariance and transitivity give 0<v<2v<3v=0, violating irreflexivity. The 20 nonzero null directions are symmetric v and -v and the Brouwer-Haemers Cayley graph is undirected. A globally oriented, unbounded physical time variable must be EXTRA structure, e.g. nonperiodic Z cover, clock degree of freedom or a broken translation symmetry.',
  causal_scope='The finite 81-vector tangent cone has well-defined null adjacency and finite observer stabilizer, but no causal partial order, continuum Lorentz invariance, Einstein dynamics, physical speed c or measured time scale. This refines Round28 native Levi graph wave no-go while respecting new parallel Pass11831 kinematic breakthrough.',
  mathematical_physics_context='Analogy is finite-field Spin5/Sp4 and SL2(F9). F3 has no ordered real signature. The real AdS4 geometry is a comparison, not dynamically obtained.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('ADS CONE 81/20; spectral ds',[(r['t'],round(r['spectral_dimension'],3)) for r in records],flush=True)
 return out
if __name__=='__main__':run()
