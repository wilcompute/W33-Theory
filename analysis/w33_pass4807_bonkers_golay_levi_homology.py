#!/usr/bin/env python3
"""Pass 4807 bonkers — global triangle CSS filtration by 27 punctured Golay blocks and Levi H1.

Let C=row_3(B) for the 45x270 point/triangle matrix.  Partition the 270
triangles into the ten triangles of each of the 27 GQ(4,2) K5 lines.  For a
line ell let K_ell be the local [10,6,4]_3 kernel of its 5x10 incidence matrix
(Pass4806 identifies it as punctured ternary Golay), and let L=direct sum K_ell.

This producer verifies C <= L <= C^perp with dimensions 44 <= 162 <= 226.
It then constructs the canonical quotient map to the GQ Levi graph: on each
line, multiply local triangle coefficients by the 5x10 incidence matrix.  The
result is a value on each of the 135 point-line incidences.  Line-boundaries
vanish because every triangle has three points (3=0 in F3); point-boundaries
vanish exactly when x is in C^perp.  The kernel is L.  Conversely each Levi
cycle has line-local sum zero, the exact image of the rank-4 local incidence
matrix, so it lifts.  Hence C^perp/L is canonically H_1(Levi;F3), dimension 64.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4807_GOLAY_LEVI_HOMOLOGY.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x):return tuple((x>>i)&1 for i in range(6))

def rref(M,p=3):
    A=np.array(M,dtype=int)%p;r=0;piv=[]
    for c in range(A.shape[1]):
        s=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if s is None:continue
        A[[r,s]]=A[[s,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
    return A,piv

def rank(M,p=3):return len(rref(M,p)[1])

def nullspace(M,p=3):
    R,piv=rref(M,p);free=[c for c in range(R.shape[1]) if c not in piv];out=[]
    for f in free:
        x=np.zeros(R.shape[1],dtype=int);x[f]=1
        for i,c in enumerate(piv):x[c]=(-R[i,f])%p
        out.append(x)
    return np.array(out,dtype=int)

def main()->int:
    qp=[x for x in range(1,64) if Qm(bits(x))==0];assert len(qp)==27
    ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});assert len(ql)==45
    K5=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp];assert len(set(K5))==27 and {len(C) for C in K5}=={5}
    T=sorted({tuple(sorted(t)) for C in K5 for t in itertools.combinations(C,3)});assert len(T)==270
    tid={t:i for i,t in enumerate(T)};B=np.zeros((45,270),dtype=int)
    for j,t in enumerate(T):B[list(t),j]=1
    rC=rank(B,3);assert rC==44 and not np.any((B@B.T)%3)
    local=[];S=np.zeros((135,270),dtype=int);edge=0
    # S rows are Levi incidences (ell,p); local block maps triangle coefficients to point sums.
    for ell,C5 in enumerate(K5):
        ids=[tid[tuple(sorted(t))] for t in itertools.combinations(C5,3)]
        M=B[list(C5)][:,ids];assert rank(M,3)==4
        N=nullspace(M,3);assert N.shape==(6,10)
        for v in N:
            g=np.zeros(270,dtype=int);g[ids]=v;local.append(g)
        for p in C5:
            S[edge]=B[p];S[edge,[j for j in range(270) if j not in ids]]=0
            edge+=1
    assert edge==135
    L=np.array(local,dtype=int);rL=rank(L,3);assert rL==162
    assert rank(np.vstack([L,B]),3)==162  # C <= L
    rCp=270-rC;assert rCp==226
    assert np.all((B@L.T)%3==0)          # L <= C^perp
    assert rank(S,3)==108 and 270-rank(S,3)==162  # ker S = L
    # Oriented Levi boundary: 45 point vertices + 27 line vertices, 135 edges.
    D=np.zeros((72,135),dtype=int);e=0
    for ell,C5 in enumerate(K5):
        for p in C5:
            D[p,e]=1;D[45+ell,e]=-1;e+=1
    assert rank(D,3)==71
    h1dim=135-rank(D,3);assert h1dim==64
    # S maps C^perp into cycles: D S x =0 whenever Bx=0.  Algebraically D S has
    # point block B and identically-zero line block.
    DS=(D@S)%3
    assert np.array_equal(DS[:45],B%3) and not np.any(DS[45:])
    quotient_dim=rCp-rL;assert quotient_dim==h1dim==64
    local_logical_dim=rL-rC;assert local_logical_dim==118
    out={'pass':4807,'stabilizer_code_dim':44,'local_golay_sum_dim':162,'dual_dim':226,
      'filtration':'C_[270,44,18] <= G10^27_[270,162,4] <= C^perp_[270,226,4]',
      'local_logical_quotient_dim':118,'global_quotient_dim':64,
      'Levi_vertices':72,'Levi_edges':135,'Levi_boundary_rank_F3':71,'Levi_H1_dim_F3':64,
      'canonical_isomorphism':'C^perp / (direct_sum_27 G10) ~= H_1(Levi(GQ(4,2));F3)',
      'theorem':'The qutrit logical space has a canonical local-to-global filtration. The 27 punctured ternary Golay fibers form a 162-dimensional intermediate code containing the 44-dimensional stabilizer row code; the remaining 64-dimensional quotient is canonically the first homology of the GQ(4,2) Levi graph.',
      'boundary':'The short exact sequence 0 -> L/C -> C^perp/C -> H_1(Levi;F3) -> 0 is canonical from incidence. A direct-sum splitting of the 182 logical dimensions is not promoted as canonical.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
