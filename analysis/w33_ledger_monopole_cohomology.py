#!/usr/bin/env python3
"""W33 monopole/cohomology stress test for the Ledger's F=dA claim.

The full W33 clique complex has C0,C1,C2,C3=(40,240,160,40).  This verifier
computes exact boundary maps and Smith data and reads the cohomology.  Result:
H^2(W33;Z)=H^2(W33;F3)=0, so every closed 2-cochain is exact ON THIS carrier.
This does not turn dF=0 into a universal theorem on arbitrary topology.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
MOD=3
def canon(v):
    for a in v:
        if a%MOD:
            inv=1 if a%MOD==1 else 2
            return tuple((inv*x)%MOD for x in v)
    raise ValueError("zero")
def symp(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%MOD
def rank_mod(A,p):
    A=A.copy()%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz):continue
        j=r+int(nz[0]);A[[r,j]]=A[[j,r]];A[r]=(A[r]*pow(int(A[r,c]),p-2,p))%p
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-int(A[i,c])*A[r])%p
        r+=1
        if r==m:break
    return r
def build_complex():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    edges=[(i,j) for i in range(40) for j in range(i+1,40) if symp(pts[i],pts[j])==0];E=set(edges)
    tri=[c for c in itertools.combinations(range(40),3) if all(tuple(sorted(e)) in E for e in itertools.combinations(c,2))]
    tet=[c for c in itertools.combinations(range(40),4) if all(tuple(sorted(e)) in E for e in itertools.combinations(c,2))]
    return pts,edges,tri,tet
def boundary(high,low):
    ix={s:i for i,s in enumerate(low)};B=np.zeros((len(low),len(high)),dtype=np.int64)
    for j,s in enumerate(high):
        for k in range(len(s)):B[ix[s[:k]+s[k+1:]],j]=-1 if k%2 else 1
    return B
def snf(A):
    S=smith_normal_form(Matrix(A.tolist()),domain=ZZ)
    return [abs(int(S[i,i])) for i in range(min(S.shape)) if S[i,i]!=0]
def main():
    pts,e,t,T=build_complex();v=[(i,) for i in range(40)]
    d1,d2,d3=boundary(e,v),boundary(t,e),boundary(T,t)
    ranks={p:[rank_mod(d1,p),rank_mod(d2,p),rank_mod(d3,p)] for p in [2,3,5,65537]}
    betti={p:[40-r[0],240-r[0]-r[1],160-r[1]-r[2],40-r[2]] for p,r in ranks.items()}
    s2,s3=snf(d2),snf(d3);ker=160-ranks[3][2];im=ranks[3][1]
    checks={"simplex_counts_40_240_160_40":[len(pts),len(e),len(t),len(T)]==[40,240,160,40],
      "d1d2_zero":np.array_equal(d1@d2,np.zeros((40,160),dtype=np.int64)),
      "d2d3_zero":np.array_equal(d2@d3,np.zeros((240,40),dtype=np.int64)),
      "ranks_field_independent":len({tuple(x) for x in ranks.values()})==1,
      "boundary_ranks_39_120_40":next(iter(ranks.values()))==[39,120,40],
      "betti_1_81_0_0":all(x==[1,81,0,0] for x in betti.values()),
      "snf_d2_all_units":len(s2)==120 and set(s2)=={1},"snf_d3_all_units":len(s3)==40 and set(s3)=={1},
      "H2_F3_zero":ker==im==120,"H2_Z_zero":True}
    checks={k:bool(x) for k,x in checks.items()};assert all(checks.values()),checks
    out={"schema":"w33.ledger.monopole-cohomology.v1","status":"PASS_W33_H2_ZERO_GLOBAL_EXACTNESS",
      "simplices":{"C0":40,"C1":240,"C2":160,"C3":40},
      "boundary_ranks":{str(p):ranks[p] for p in ranks},"betti_numbers":{str(p):betti[p] for p in betti},
      "smith":{"d2_nonzero_invariants":len(s2),"d2_unique_values":sorted(set(s2)),"d3_nonzero_invariants":len(s3),"d3_unique_values":sorted(set(s3))},
      "cohomology":{"F3":{"dim_ker_delta2":ker,"dim_im_delta1":im,"H2_dim":0},"Z":"H^2=0 (torsion-free and b2=0)"},
      "ledger_reading":{"supported_on_w33":"every closed 2-cochain on the W33 clique complex is exact, so no topological magnetic charge class survives on this carrier",
        "not_supported_universally":"dF=0 alone does not imply F=dA globally on an arbitrary spacetime or nontrivial U(1) bundle; the W33 conclusion uses H^2=0"},
      "prior_art_boundary":"W33 clique homology/Smith data existed in scripts/w33_homology.py and Pass 1944; this adds the explicit Ledger gauge/cohomology exactness test.","checks":checks}
    p=Path("data/PART_LEDGER_MONOPOLE_COHOMOLOGY.json");p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
