#!/usr/bin/env python3
"""Molien symmetric-cube/four invariant dimensions of the irreducible W33 24D
PSp4(3) carrier, exact traces from the 40-point permutation action.

Independent of existing qutrit-state Molien work (Pass 11491).
"""
import sys,json
from pathlib import Path
from collections import deque
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_route_216_cubic_tomography import geometry
from w33_20261102_five_deeper_fronts import route_frame
def main():
 pts,lines,N,idx,norm,omega=geometry()
 A=N@N.T-4*np.eye(40,dtype=int)
 assert np.array_equal(A@A,8*np.eye(40,dtype=int)-2*A+4*np.ones((40,40),dtype=int))
 bas=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
      (1,0,1,0),(0,1,0,1),(1,1,1,0),(0,1,1,1)]
 gens=[bytes(idx[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts) for a in bas]
 ident=bytes(range(40));seen={ident};front=[ident];group=[]
 while front:
  nxt=[]
  for p in front:
   group.append(p)
   for g in gens:
    t=bytes(g[p[i]] for i in range(40))
    if t not in seen:seen.add(t);nxt.append(t)
  front=nxt
 assert len(group)==len(seen)==25920
 def comp(p,q):return bytes(p[q[i]] for i in range(40))
 def ch(p):
  fix=sum(p[i]==i for i in range(40))
  adjacency=sum(int(A[i,p[i]]) for i in range(40))
  assert (adjacency+4*fix-16)%6==0
  return (adjacency+4*fix-16)//6
 s2=s3=s4=0;χdist={}
 for p in group:
  p2=comp(p,p);p3=comp(p2,p);p4=comp(p3,p)
  a,b,c,d=map(ch,(p,p2,p3,p4))
  χdist[str(a)]=χdist.get(str(a),0)+1
  s2+=a*a+b
  s3+=a*a*a+3*a*b+2*c
  s4+=a**4+6*a*a*b+3*b*b+8*a*c+6*d
 assert s2%(2*25920)==0
 assert s3%(6*25920)==0
 assert s4%(24*25920)==0
 inv={2:s2//(2*25920),3:s3//(6*25920),4:s4//(24*25920)}
 # Test whether prior 216-route cubic has nonzero projection to E+.
 Z,_=route_frame()
 x=5*A[:,0].astype(int)+20*np.eye(40,dtype=int)[:,0]-2*np.ones(40,dtype=int)
 assert np.array_equal(A@x,2*x)
 v=Z@x
 C=int(np.sum(v.astype(np.int64)**3))
 P=5*A+20*np.eye(40,dtype=int)-2*np.ones((40,40),dtype=int)
 rng=np.random.default_rng(20261105)
 cubic_probes=[];point_cubic_probes=[]
 for i in range(20):
  w=P@rng.integers(-2,3,40)
  assert np.array_equal(A@w,2*w)
  cubic_probes.append(int(np.sum((Z@w).astype(np.int64)**3)))
  point_cubic_probes.append(int(np.sum(w.astype(np.int64)**3)))
 assert any(cubic_probes),(cubic_probes,'zero restricted cubic')
 witness=None
 for i in range(20):
  for j in range(i):
   det=point_cubic_probes[i]*cubic_probes[j]-point_cubic_probes[j]*cubic_probes[i]
   if det:
    witness={'sample_i':i,'sample_j':j,'exact_2x2_determinant':str(det)};break
  if witness:break
 assert witness is not None,'unexpected dependence of point and route cubics'
 out={'status':'PASS_EXACT_24D_MOLIEN_INVARIANT_COUNTS',
   'group_order':25920,'irrep_dimension':24,
   'symmetric_power_invariant_dimensions':{str(k):int(val) for k,val in inv.items()},
   'character_value_histogram':χdist,
   'projected_W33_route_cubic_at_integer_24D_vector':C,
   'projected_vector_squared_norm':int(x@x),
   'cubic_nonzero_on_24D':any(cubic_probes),
   'sampled_integer_24D_cubic_values':cubic_probes,
   'sampled_integer_24D_point_cubic_values':point_cubic_probes,
   'two_invariant_cubic_basis_independence_witness':witness,
   'cubic_basis':'C_point(x)=sum_{i=1}^{40}x_i^3; C_route(x)=sum_{s=1}^{216}(Z_s dot x)^3, for x in V24. Both invariant and independent, hence span 2D invariant Sym3 space.',
   'interpretation':'The irreducible real 24D PSp4(3) carrier admits TWO cubic invariants, not a unique one. Any W33-to-Albert cubic compatibility must choose a linear combination and verify multiplication/norm identities; dimension matching is insufficient.',
   'exact_method':'E+=(A+4I-2J/5)/6, χ24(g)=(sum_i A[i,g(i)]+4#fixed(g)-16)/6, Newton character formulas for Sym2,3,4; full 25920 symplectic transvection group.',
   'scope':'Symmetric invariant polynomial count for W33 24D point module, distinct from Pass11491 (Hesse-qutrit time-odd Molien) and prior 27D cubic.'}
 p=ROOT/'data/w33_20261103_w33_24_molien_cubic.json'
 p.write_text(json.dumps(out,indent=2)+'\n')
 print('MOLIEN24',json.dumps(out)[:4500],flush=True)
 return out
if __name__=='__main__':main()
