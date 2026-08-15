#!/usr/bin/env python3
"""Pass5333: identify the base-point constituent inside the q=5 K0 shell module.

The 2340 minimum-shell labels are (p,{l1,l2}), with 15 labels over each of the
156 W(3,5) points.  Pass5332 found seven central simple blocks, including two
nonisomorphic 65-dimensional constituents.  Here the natural base-fiber quotient
separates them exactly.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5332_q5_k0_orbital_wedderburn import build_action
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5333_Q5_K0_BASE_FIBER_CONSTITUENT.json'

# The generic central element used in Pass5332, in its deterministic orbital order.
CENTER=np.array([1,288,288,-2,-2,-2,4,-3,-3,-3,4,-3,-3,-3,4,5,-6,-6,7,7,7],dtype=np.int64)

def relation_matrix(garr,orbs):
    n=2340
    sub=np.empty(n,dtype=np.uint8)
    for i,O in enumerate(orbs):sub[O]=i
    invs=[]
    for a in garr:
        z=np.empty(n,dtype=np.uint16);z[a]=np.arange(n,dtype=np.uint16);invs.append(z)
    parent=np.full(n,-1,dtype=np.int32);pgen=np.full(n,-1,dtype=np.int8);parent[0]=0;Q=[0]
    for x in Q:
        for gi,a in enumerate(garr):
            y=int(a[x])
            if parent[y]<0:parent[y]=x;pgen[y]=gi;Q.append(y)
    assert len(Q)==n
    maps=np.empty((n,n),dtype=np.uint16);maps[0]=np.arange(n,dtype=np.uint16)
    for x in Q[1:]:maps[x]=maps[parent[x]][invs[pgen[x]]]
    R=np.empty((n,n),dtype=np.uint8)
    for x in range(n):R[x]=sub[maps[x]]
    return R

def main():
    garr,orbs=build_action();R=relation_matrix(garr,orbs);Z=CENTER[R]
    # Base-fiber quotient: every point fiber has exactly C(6,2)=15 shell labels.
    Q=np.empty((156,156),dtype=np.int64)
    for p in range(156):
        ref=15*p
        for q in range(156):Q[p,q]=Z[ref,15*q:15*q+15].sum()
        for x in range(15*p,15*p+15):
            assert all(Z[x,15*q:15*q+15].sum()==Q[p,q] for q in range(156))
    # W(3,5) point adjacency.
    G=build_W(5);A=np.zeros((156,156),dtype=np.int64)
    for L in G['lines']:
        L=sorted(L)
        for i in L:
            for j in L:
                if i!=j:A[i,j]=1
    assert np.all(A.sum(axis=1)==30)
    J=np.ones((156,156),dtype=np.int64);I=np.eye(156,dtype=np.int64)
    assert np.array_equal(Q,476*I-87*A+77*J)
    assert Counter(map(int,Q.ravel()))==Counter({77:19500,-10:4680,553:156})
    # Exact eigenvalue multiplicities follow from W(3,5): 30^1, 4^90, (-6)^65.
    evals={
      'on_30_trivial':476-87*30+77*156,
      'on_4_dim90':476-87*4,
      'on_minus6_dim65':476+87*6,
    }
    assert evals=={'on_30_trivial':9878,'on_4_dim90':128,'on_minus6_dim65':998}
    out={'pass':5333,'status':'THEOREM_Q5_K0_BASE_FIBER_QUOTIENT_IDENTIFIES_POINT_65_BLOCK',
      'shell_vertices':2340,'base_points':156,'fiber_size':15,
      'central_quotient_formula':'Q = 476 I - 87 A_W + 77 J',
      'entry_histogram':{'553_diagonal':156,'-10_collinear':4680,'77_noncollinear':19500},
      'W35_point_spectrum':{'30':1,'4':90,'-6':65},
      'central_spectrum_on_base_fiber_space':{'9878':1,'128':90,'998':65},
      'conclusion':'The multiplicity-one 65-dimensional Pass5332 block at central eigenvalue 998 is the canonical W(3,5) point -6 constituent pulled back through the 15-to-1 shell projection. The other 65-dimensional block (central eigenvalue -352, multiplicity two) is not this point constituent.',
      'footprint_bridge':'The q5 footprint map has rank 65, so its nonzero point-module quotient lives on this same canonical 65-dimensional point constituent; this removes the equal-dimension ambiguity left by Pass5332.',
      'boundary':'This identifies the point/footprint constituent at the representation level. It does not identify the second 65-dimensional irreducible with any footprint object.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
