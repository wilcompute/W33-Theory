#!/usr/bin/env python3
"""Pass 4798 bonkers — a self-orthogonal [270,44] qutrit triangle-incidence code.

For the intrinsic GQ(4,2) 270-triangle carrier, let B be 45 x 270 point-triangle
incidence.  Each point lies in 18 triangles; adjacent points occur together in
3 triangles; nonadjacent points in 0.  Thus BB^T=18I+3A and vanishes over F3.
The only F3 row dependency is the global all-point sum, so rank_F3(B)=44.
Over F2 and F5 the local 3-subset equations force zero, hence rank 45.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4798_TRIANGLE_QUTRIT_CODE.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1
def bits(x):return tuple((x>>i)&1 for i in range(6))
def rank_mod(M,p):
    A=[[int(x)%p for x in row] for row in M];r=0
    for c in range(len(A[0])):
        s=next((i for i in range(r,len(A)) if A[i][c]),None)
        if s is None:continue
        A[r],A[s]=A[s],A[r];z=pow(A[r][c],-1,p);A[r]=[(z*x)%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]:
                z=A[i][c];A[i]=[(a-z*b)%p for a,b in zip(A[i],A[r])]
        r+=1
    return r

def main()->int:
    pts=[x for x in range(1,64) if Qm(bits(x))==0];assert len(pts)==27
    lines=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(pts,2) if (a^b) in pts});assert len(lines)==45
    A=np.zeros((45,45),dtype=int)
    for i,j in itertools.combinations(range(45),2):
        if set(lines[i])&set(lines[j]):A[i,j]=A[j,i]=1
    # Maximal K5s are point-stars of Q^-(5,2): all five singular lines through a singular point.
    K5=[]
    for p in pts:
        C=tuple(i for i,L in enumerate(lines) if p in L);assert len(C)==5;K5.append(C)
    assert len(set(K5))==27
    triangles=sorted({tuple(sorted(T)) for C in K5 for T in itertools.combinations(C,3)});assert len(triangles)==270
    B=np.zeros((45,270),dtype=int)
    for j,T in enumerate(triangles):B[list(T),j]=1
    assert set(B.sum(1))=={18} and set(B.sum(0))=={3}
    assert np.array_equal(B@B.T,18*np.eye(45,dtype=int)+3*A)
    ranks={p:rank_mod(B.tolist(),p) for p in (2,3,5)}
    assert ranks=={2:45,3:44,5:45}
    assert not np.any((B@B.T)%3)
    assert np.all(B.sum(0)%3==0)  # global all-row dependency
    out={'pass':4798,'matrix':'45 x 270 GQ(4,2) point-triangle incidence',
      'row_weight':18,'column_weight':3,'pair_overlap_adjacent':3,'pair_overlap_nonadjacent':0,
      'Gram_identity':'B B^T = 18 I + 3 A45',
      'ranks':{'F2':45,'F3':44,'F5':45},
      'F3_code':{'length':270,'dimension':44,'self_orthogonal':True,'dual_dimension':226,'known_codeword_weight_upper_bound_for_minimum':18},
      'unique_row_dependency_F3':'sum of all 45 point rows = 0; locally all triple-sum equations force equal coefficients on each K5, and GQ connectedness makes the coefficient global',
      'theorem':'The intrinsic 270-triangle carrier supports a characteristic-3 self-orthogonal incidence code of length 270 and dimension 44. The rank defect is exactly one and occurs at characteristic 3; the same 45 rows are independent over F2 and F5.',
      'boundary':'Minimum distance of the [270,44]3 code is not determined here; the displayed point rows only prove d<=18. No quantum-code parameters are inferred without a second commuting check family.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
