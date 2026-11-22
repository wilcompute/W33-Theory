#!/usr/bin/env python3
"""Max-cut MILP for rank-2 causal Hasse orientation on W33 adjacency."""
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
from toe_20261122_round6_causal_graph_no_go import w33

def solve(sec=30):
 pts,edges,triangles=w33();ne=len(edges);nv=len(pts)
 C=lil_matrix((2*ne, nv+ne),dtype=float)
 for k,(i,j) in enumerate(edges):
  C[2*k,i]=-1;C[2*k,j]=-1;C[2*k,nv+k]=1
  C[2*k+1,i]=1;C[2*k+1,j]=1;C[2*k+1,nv+k]=1
 lo=np.full(2*ne,-np.inf);hi=np.array([0,2]*ne)
 cost=np.r_[np.zeros(nv),-np.ones(ne)]
 bounds=Bounds(np.zeros(nv+ne),np.r_[np.ones(nv+ne)]);bounds.ub[0]=0
 out=milp(cost,integrality=np.r_[np.ones(nv),np.zeros(ne)],bounds=bounds,constraints=LinearConstraint(C.tocsr(),lo,hi),options={'time_limit':sec,'mip_rel_gap':0.0})
 print(out.message,'primal',-out.fun if out.fun is not None else None,'dual',-out.mip_dual_bound if out.mip_dual_bound is not None else None,'gap',out.mip_gap)
 if out.x is not None:
   group=np.rint(out.x[:nv]).astype(int)
   cut=sum(group[i]!=group[j] for i,j in edges)
   print('actual cut',cut,'partition',np.bincount(group).tolist(),'code',group.tolist())
 return out
if __name__=='__main__':solve()
