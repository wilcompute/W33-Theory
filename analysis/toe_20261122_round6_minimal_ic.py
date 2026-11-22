#!/usr/bin/env python3
"""Positive Witting frame polytope search (IC requires an independent rank-16 check)."""
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import hstack,csr_matrix
import toe_20261122_witting_one_phase_three_fixed as W

def get_mats():
  w=np.exp(2j*np.pi/3)
  V=np.array([[complex(float(x[0])-float(x[1])/2,float(x[1])*np.sqrt(3)/2) for x in v] for v in W.all_rays()]);V/=np.linalg.norm(V,axis=1)[:,None]
  P=np.array([np.outer(v,v.conj()) for v in V]);
  def coord(m):return np.r_[np.real(np.diag(m)),[np.real(m[i,j]) for i in range(4) for j in range(i+1,4)],[np.imag(m[i,j]) for i in range(4) for j in range(i+1,4)]]
  A=np.column_stack([coord(p) for p in P]);b=coord(np.eye(4));return P,A,b

def non_ic_minimum_identity_resolution(max_seconds=45):
  P,A,b=get_mats();n=40
  # w_j <= y_j, since each P normalized and sum=w_j Pj...=I.
  eq=csr_matrix(np.c_[A,np.zeros((16,40))]);ineq=csr_matrix(np.c_[np.eye(40),-np.eye(40)])
  cs=[LinearConstraint(eq,b,b),LinearConstraint(ineq,-np.inf,np.zeros(40))]
  c=np.r_[np.zeros(40),np.ones(40)]
  opt=milp(c,integrality=np.r_[np.zeros(40),np.ones(40)],bounds=Bounds(np.zeros(80),np.ones(80)),constraints=cs,options={'time_limit':max_seconds,'mip_rel_gap':0.0})
  print('MIP',opt.message,'status',opt.status,'objective',opt.fun,'bound',opt.mip_dual_bound,'gap',opt.mip_gap,flush=True)
  if opt.x is not None:
    ids=[int(i) for i,x in enumerate(opt.x[:40]) if x>1e-8]
    print('support',len(ids),ids,'minweight',min(opt.x[ids]),'rank',np.linalg.matrix_rank(A[:,ids]),'residual',max(abs(A@opt.x[:40]-b)),flush=True)
  return opt
def reproduce_first_16(seed=481,limit=500):
  """Deterministic randomized LP reproduces exact 16-ray support after 356 failed draws.

  WARNING: a generic positive identity resolution is NOT automatically IC.
  Rank and exact normalization are independently certified in the companion proof.
  """
  from scipy.optimize import linprog
  _,A,b=get_mats();rng=np.random.default_rng(seed)
  for k in range(limit):
    q=linprog(rng.normal(size=40),A_eq=A,b_eq=b,bounds=(0,None),method='highs')
    if not q.success:continue
    indices=tuple(int(i) for i in np.flatnonzero(q.x>1e-8))
    if len(indices)==16 and np.linalg.matrix_rank(A[:,indices])==16:
      return {'random_objective_index':k,'indices':indices,'weights':q.x[np.array(indices)].tolist()}
  return None

if __name__=='__main__':
  d=reproduce_first_16()
  assert d is not None
  print(d)

