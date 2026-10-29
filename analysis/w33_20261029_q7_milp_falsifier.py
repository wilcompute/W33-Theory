#!/usr/bin/env python3
"""Symmetry-reduced exact MILP feasibility probe for W(3,7) kernel weights 10/12.
The Sp4(7) point stabilizer has adjacent and nonadjacent second-point orbits.
A solver time-limit is INCONCLUSIVE, not a distance proof.
"""
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,hstack,vstack,eye
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261029_q7_milp_search.json"
def graph():
 q=7;pts=set()
 for a in range(q):
  for b in range(q):
   for c in range(q):
    for d in range(q):
     x=(a,b,c,d)
     if not any(x):continue
     inv=pow(next(t for t in x if t),-1,q)
     pts.add(tuple(t*inv%q for t in x))
 pts=sorted(pts)
 f=lambda x,y:(x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%q
 A=csr_matrix(np.array([[int(i!=j and not f(x,y)) for j,y in enumerate(pts)]
              for i,x in enumerate(pts)],dtype=np.int8))
 assert A.shape==(400,400) and np.all(np.asarray(A.sum(1)).ravel()==56)
 return A
def search(A,weight,adjacent,limit=20):
 n=400;neighbors=set(A[0].indices)
 other=next(j for j in range(1,n) if (j in neighbors)==adjacent)
 M=vstack([hstack([A,-2*eye(n,format="csr")],format="csr"),
    csr_matrix(np.array([[1]*n+[0]*n],dtype=np.int8))],format="csr")
 low=np.zeros(2*n);upper=np.array([1]*n+[weight//2]*n,dtype=float)
 low[0]=upper[0]=1;low[other]=upper[other]=1
 rhs=np.array([0]*n+[weight])
 start=time.time()
 result=milp(np.zeros(2*n),integrality=np.ones(2*n),
   bounds=Bounds(low,upper),constraints=LinearConstraint(M,rhs,rhs),
   options={"time_limit":limit,"mip_rel_gap":0})
 witness=result.x is not None and np.max(abs(M@result.x-rhs))<1e-5
 return {"weight":weight,"fixed_pair_adjacent":adjacent,"solver_status":int(result.status),
   "solver_message":result.message,"seconds":round(time.time()-start,3),
   "proved_infeasible":result.status==2,
   "feasible_counterexample":bool(witness),
   "scope":"Only an infeasible termination certifies nonexistence. Time limit is inconclusive."}
def main():
 A=graph();weight=int(sys.argv[1]) if len(sys.argv)>1 else 10
 results=[search(A,weight,True),search(A,weight,False)]
 OUT.write_text(json.dumps({"checks":results},indent=2)+"\n")
 print(json.dumps(results,indent=2))
if __name__=="__main__":main()
