#!/usr/bin/env python3
"""Numerical commutant-rank probe for the 15D POVM null module, with exact
PSp(4,3) action-order and stabilizer rank10 verified separately.
"""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261102_route_216_cubic_tomography import geometry
def main():
 Z,N=route_frame();K=(Z@Z.T)**2
 vals,U=np.linalg.eigh(K.astype(float))
 assert np.max(abs(vals[:15]))<1e-7
 B=U[:,:15];I=np.eye(15)
 pts,lines,NN,idx,norm,omega=geometry();pos={tuple(x):j for j,x in enumerate(Z)}
 point_basis=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
         (1,0,1,0),(0,1,0,1),(1,1,1,0),(0,1,1,1)]
 reps=[]
 for a in point_basis:
  g=np.array([idx[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts])
  pi=np.array([pos[tuple(int(z[i]) for i in np.argsort(g))] for z in Z])
  assert set(map(int,pi))==set(range(216))
  assert np.array_equal(Z[pi],Z[:,np.argsort(g)])
  R=B.T@B[pi]
  assert np.max(abs(R.T@R-I))<1e-9
  reps.append(R)
 # A matrix X commutes with each R iff the following stacked real linear
 # operator kills vec(X) (column-major order).
 D=np.vstack([np.kron(I,R)-np.kron(R.T,I) for R in reps])
 singular=np.linalg.svd(D,compute_uv=False)
 n=int(np.sum(singular<1e-8))
 assert n>=1
 rank=225-n
 print("15D_COMMUTANT",n,"smallest_singular",singular[-8:],flush=True)
 ret={"group_generators":len(reps),"stabilizer_orbital_rank":10,
      "blind_module_dimension":15,"complex_irreducibility_from_numeric_commutant":n==1,
      "commutant_numerical_dimension":n,"constraint_rank":rank,
      "smallest_singular_values":list(map(float,singular[-8:])),
      "numerical_threshold":1e-8,
      "scope":"high-confidence floating matrix linear-algebra certificate; exact rational modular proof still required for formal theorem"}
 (ROOT/"data/w33_20261102_blind_commutant_probe.json").write_text(json.dumps(ret,indent=2)+"\n")
 return ret
if __name__=="__main__":main()
