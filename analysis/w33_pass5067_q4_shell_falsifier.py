#!/usr/bin/env python3
"""Pass5067: symmetry-reduced q=4 minimum-shell solver contract.

Default mode reconstructs the exact 256-dimensional chamber-star generator
space and reports the gauge-fixed model dimensions.  Use --solve-seconds N to
run the bounded HiGHS MILP.  TIME_LIMIT_NO_INCUMBENT is explicitly UNKNOWN.
"""
from __future__ import annotations
import argparse
import numpy as np
from scipy import sparse
from scipy.optimize import Bounds, LinearConstraint, milp
from analysis.w33_pass5056_q4_theta_apartment_code import build_geometry

def independent_rows(rows, nbits):
    piv={}; keep=[]
    for i,r0 in enumerate(rows):
        r=int(r0)
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;keep.append(i);break
    return keep

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--solve-seconds',type=float,default=0.0);args=ap.parse_args()
    G=build_geometry();napt=len(G['apartments']);nflag=len(G['flags'])
    assert (napt,nflag)==(13600,425)
    # Chamber-star generator rows: one bit for every apartment containing flag f.
    stars=[]
    for f in range(nflag):
        z=0
        bit=1<<f
        for a,row in enumerate(G['apartment_cycle_rows']):
            if row&bit:z|=1<<a
        assert z.bit_count()==256
        stars.append(z)
    keep=independent_rows(stars,napt);assert len(keep)==256
    # Transitivity fixes apartment 0. Exactly its eight chamber stars need exclusion.
    through0=[f for f,z in enumerate(stars) if z&1];assert len(through0)==8
    print({'apartments':napt,'chambers':nflag,'chamber_generator_rank':len(keep),
           'generator_kernel_dimension':nflag-len(keep),'fixed_apartment_star_exclusions':len(through0)})
    if args.solve_seconds<=0:return 0
    # Sparse apartment x independent-generator incidence.
    rr=[];cc=[];vv=[]
    for j,f in enumerate(keep):
        z=stars[f]
        while z:
            l=z&-z;a=l.bit_length()-1;rr.append(a);cc.append(j);vv.append(1.0);z^=l
    M=sparse.coo_matrix((vv,(rr,cc)),shape=(napt,256)).tocsr()
    # Variables [u_256 binary, x_13600 binary, t_13600 integer].
    nu=256;nx=napt;nt=napt;offx=nu;offt=nu+nx;nvar=nu+nx+nt
    A=sparse.hstack([M,-sparse.eye(nx),-2*sparse.eye(nx)],format='csr')
    Aeq=sparse.vstack([A,sparse.csr_matrix(([1.0]*nx,([0]*nx,list(range(offx,offx+nx)))),shape=(1,nvar))],format='csr')
    beq=np.r_[np.zeros(nx),256.0]
    constraints=[LinearConstraint(Aeq,beq,beq)]
    for f in through0:
        idx=[a for a in range(nx) if (stars[f]>>a)&1]
        row=sparse.csr_matrix(([1.0]*len(idx),([0]*len(idx),[offx+a for a in idx])),shape=(1,nvar))
        constraints.append(LinearConstraint(row,-np.inf,255.0))
    c=np.zeros(nvar);lb=np.zeros(nvar);ub=np.r_[np.ones(nu+nx),np.full(nt,4.0)]
    lb[offx]=ub[offx]=1.0
    integ=np.ones(nvar,dtype=np.int8)
    res=milp(c=c,integrality=integ,bounds=Bounds(lb,ub),constraints=constraints,
             options={'time_limit':args.solve_seconds,'mip_rel_gap':0.0})
    incumbent=getattr(res,'x',None) is not None
    verdict='SAT' if res.success else ('UNKNOWN_TIME_LIMIT_NO_INCUMBENT' if not incumbent else 'UNKNOWN_WITH_INCUMBENT')
    print({'status':int(res.status),'message':str(res.message),'incumbent':incumbent,'verdict':verdict})
    return 0
if __name__=='__main__':raise SystemExit(main())
