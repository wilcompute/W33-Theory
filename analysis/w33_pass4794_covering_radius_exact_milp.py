#!/usr/bin/env python3
"""Supplement to Pass4794: symmetry-broken exact decision for rho(H10).

Pass4794 already proves 14 <= rho <= 15.  A distance-15 coset, if it exists,
has odd parity because H10 is even.  Since the all-one vector is in H10, the
same coset has a representative of weight at most 20, hence weight 15, 17, or
19.  The automorphism group is coordinate-transitive, so a nonzero support
coordinate may be moved to coordinate 0.  We therefore solve three exact MILPs:
wt(x)=15,17,19 and x_0=1, with all 1024 distance constraints.

Any feasible branch proves rho=15.  If all three branches are infeasible,
rho=14.  A timeout/unknown branch leaves the certified 14..15 bracket intact.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy import sparse
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4794_COVERING_RADIUS_EXACT_MILP.json'

def basis(vals):
    piv={};B=[]
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;B.append(y);break
    return B
def span(B):
    V=[0]
    for b in B:V += [x^b for x in V]
    return V

def main()->int:
    _,_,_,A,_,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    rows=[sum(1<<j for j in np.flatnonzero(A[i])) for i in range(40)]
    B=basis(rows);assert len(B)==10;C=span(B);assert len(C)==1024
    assert all(c.bit_count()%2==0 for c in C)
    assert (1<<40)-1 in C
    rr=[];cc=[];dd=[];lb=[]
    for r,c in enumerate(C):
        w=c.bit_count();lb.append(15-w)
        for i in range(40):
            rr.append(r);cc.append(i);dd.append(1. if not ((c>>i)&1) else -1.)
    M=sparse.coo_matrix((dd,(rr,cc)),shape=(1024,40)).tocsr()
    branches=[];winner=None
    for target_weight in (15,17,19):
        E=np.zeros((2,40),dtype=float);E[0,0]=1.;E[1,:]=1.
        MM=sparse.vstack([M,sparse.csr_matrix(E)]).tocsr()
        lo=np.concatenate([np.array(lb,dtype=float),[1.,float(target_weight)]])
        hi=np.concatenate([np.full(1024,np.inf),[1.,float(target_weight)]])
        R=milp(np.zeros(40),integrality=np.ones(40),
          bounds=Bounds(np.zeros(40),np.ones(40)),constraints=LinearConstraint(MM,lo,hi),
          options={'presolve':True,'time_limit':900})
        rec={'representative_weight':target_weight,'status':int(R.status),'message':str(R.message)}
        if R.status==0:
            x=sum((1<<i) for i,v in enumerate(R.x) if v>.5)
            d=min((x^c).bit_count() for c in C);assert x.bit_count()==target_weight and d>=15
            rec.update({'witness':x,'witness_coset_minimum':d});winner=rec;branches.append(rec);break
        branches.append(rec)
    out={'pass':4794,'solver':'scipy.optimize.milp / HiGHS','target_minimum':15,
      'symmetry_reduction':'H10 is even and contains all-one; choose representative weight 15/17/19. Coordinate transitivity fixes x0=1.',
      'branches':branches}
    if winner is not None:
        out.update({'decision':'feasible','witness':winner['witness'],'witness_weight':winner['representative_weight'],
          'witness_coset_minimum':winner['witness_coset_minimum'],'exact_covering_radius':15,
          'theorem':'A distance-15 H10 coset exists. Combined with Pass4794 upper bound rho<=15, rho(H10)=15.'})
    elif all(b['status']==2 for b in branches) and len(branches)==3:
        out.update({'decision':'infeasible','exact_covering_radius':14,
          'theorem':'All symmetry-reduced distance-15 branches are infeasible. Combined with the explicit distance-14 witness, rho(H10)=14.'})
    else:
        out.update({'decision':'unresolved','exact_covering_radius':None,
          'theorem':'At least one exact branch did not terminate decisively; only the certified 14<=rho(H10)<=15 bracket is retained.'})
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
