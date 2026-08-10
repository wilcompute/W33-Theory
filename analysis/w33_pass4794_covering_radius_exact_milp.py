#!/usr/bin/env python3
"""Supplement to Pass4794: exact MILP decision for a distance-15 H10 coset.

Forty binary variables encode x. For every one of the 1024 H10 codewords c,
wt(x+c)=wt(c)+sum_i (1-2c_i)x_i >=15. Feasibility therefore decides the only
case left by the K4 proof: feasible => rho=15, infeasible => rho=14.
A time-limit status is recorded without promotion.
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
    rr=[];cc=[];dd=[];lb=[]
    for r,c in enumerate(C):
        w=c.bit_count();lb.append(15-w)
        for i in range(40):rr.append(r);cc.append(i);dd.append(1. if not ((c>>i)&1) else -1.)
    M=sparse.coo_matrix((dd,(rr,cc)),shape=(1024,40)).tocsr()
    R=milp(np.zeros(40),integrality=np.ones(40),bounds=Bounds(np.zeros(40),np.ones(40)),
      constraints=LinearConstraint(M,np.array(lb,dtype=float),np.full(1024,np.inf)),
      options={'presolve':True,'time_limit':900})
    out={'pass':4794,'solver':'scipy.optimize.milp / HiGHS','status':int(R.status),'message':str(R.message),'target_minimum':15}
    if R.status==0:
        x=sum((1<<i) for i,v in enumerate(R.x) if v>.5);d=min((x^c).bit_count() for c in C);assert d>=15
        out.update({'decision':'feasible','witness':x,'witness_weight':x.bit_count(),'witness_coset_minimum':d,'exact_covering_radius':15,
          'theorem':'A distance-15 H10 coset exists. Combined with Pass4794 upper bound rho<=15, the exact covering radius is rho(H10)=15.'})
    elif R.status==2:
        out.update({'decision':'infeasible','exact_covering_radius':14,
          'theorem':'No distance-15 H10 coset exists. Combined with the explicit distance-14 witness, the exact covering radius is rho(H10)=14.'})
    else:
        out.update({'decision':'unresolved','exact_covering_radius':None,
          'theorem':'The exact MILP did not terminate decisively within its execution budget; only the certified 14<=rho<=15 bracket is retained.'})
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
