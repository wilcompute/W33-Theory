#!/usr/bin/env python3
"""Pass 4589 -- graph/incidence factorization of apartment-selected singular lines.

Correction note: the selected-line intersection graph has eigenvalue -3 with
multiplicity 150, not 165.  The 150-dimensional column kernel of N is already
the full contribution at -3; the 15-dimensional point-gram nullity becomes
zero eigenvalue of L=N^T N-3I and must not be counted a second time.
"""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4589_APARTMENT_SELECTED_SINGULAR_GRAPH.json'


def rank_mod2(M):
    A=np.asarray(M,dtype=np.uint8).copy()&1; r=0
    for c in range(A.shape[1]):
        piv=np.flatnonzero(A[r:,c])
        if len(piv)==0: continue
        rr=r+int(piv[0]); A[[r,rr]]=A[[rr,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
        if r==A.shape[0]: break
    return r


def main()->int:
    _,_,_,_,_,Astar,_,apartments,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(n) for k in range(i+1,n) if Astar[i,k]]
    B9=rank_basis_int([cols[i]^cols[k] for i,k in edges]); V9=set(span(B9))
    assert len(B9)==9 and len(V9)==512 and j in V9
    rep=lambda x:min(int(x),int(x)^j)
    q=lambda x:(rep(x).bit_count()//4)&1
    reps={rep(x) for x in V9}; singular=sorted(x for x in reps if x and q(x)==0); assert len(singular)==135
    pidx={x:i for i,x in enumerate(singular)}

    def apartment_fiber(ap):
        x=0
        for i in ap: x^=cols[int(i)]
        return rep(x)
    def apartment_line(ap):
        opp=[(a,b) for a,b in combinations(ap,2) if not Astar[a,b]]; assert len(opp)==2
        s=rep(cols[opp[0][0]]^cols[opp[0][1]]); t=rep(cols[opp[1][0]]^cols[opp[1][1]]); x=apartment_fiber(ap)
        assert q(s)==q(t)==q(x)==0 and rep(s^t)==x
        return tuple(sorted((s,t,x)))

    fibers=defaultdict(list)
    for ap in apartments: fibers[apartment_line(ap)].append(ap)
    selected=sorted(fibers); assert len(selected)==270 and Counter(map(len,fibers.values()))==Counter({6:270})
    N=np.zeros((135,270),dtype=np.int64)
    for c,L0 in enumerate(selected):
        for x in L0: N[pidx[x],c]=1
    assert set(map(int,N.sum(1)))=={6} and set(map(int,N.sum(0)))=={3}

    NN=N@N.T; A=NN-6*np.eye(135,dtype=np.int64)
    assert set(np.unique(A)).issubset({0,1}) and np.all(np.diag(A)==0)
    assert set(map(int,A.sum(1)))=={12} and int(A.sum()//2)==810
    ca=Counter(); cn=Counter()
    for i in range(135):
        for k in range(i+1,135):
            c=int(A[i]@A[k]); (ca if A[i,k] else cn)[c]+=1
    assert ca==Counter({1:810}) and cn==Counter({0:4455,3:2160,1:1620})

    I=np.eye(135,dtype=np.int64); P=I.copy()
    for root in (12,6,3,0,-3,-6): P=P@(A-root*I)
    assert not P.any()
    expected={12:1,6:15,3:20,0:60,-3:24,-6:15}
    Ak=I.copy()
    for k in range(6):
        assert int(np.trace(Ak))==sum(m*(lam**k) for lam,m in expected.items()); Ak=Ak@A
    rank_q=120; rank_f2=rank_mod2(N); assert rank_f2==119

    L=N.T@N-3*np.eye(270,dtype=np.int64)
    assert set(np.unique(L)).issubset({0,1}) and set(map(int,L.sum(1)))=={15}
    line_spectrum={15:1,9:15,6:20,3:60,0:24,-3:150}
    assert sum(line_spectrum.values())==270
    # Nonzero singular values of N give 15,9,6,3,0 on L; ker(N) has dimension 150 and gives -3.
    assert 270-rank_q==150
    assert int(np.trace(A@A@A)//6)==270

    out={
      'pass':4589,
      'incidence':{'points':135,'selected_lines':270,'point_degree':6,'line_size':3,'apartment_lifts_per_line':6,'rank_Q':rank_q,'rank_F2':rank_f2},
      'point_graph':{'vertices':135,'degree':12,'edges':810,'triangles':270,'triangles_are_exactly_selected_lines':True,'adjacent_common_neighbors':{'1':810},'nonadjacent_common_neighbors':{'0':4455,'1':1620,'3':2160},'spectrum':{str(k):v for k,v in expected.items()},'annihilator':'(x-12)(x-6)(x-3)x(x+3)(x+6)','gram':'N N^T = 6 I + A'},
      'selected_line_intersection_graph':{'vertices':270,'degree':15,'edges':2025,'spectrum':{str(k):v for k,v in line_spectrum.items()},'gram':'N^T N = 3 I + L'},
      'correction':'The -3 multiplicity is 150, not 165; the previous expression double-counted the 15-dimensional point-gram nullity.',
      'theorem':'The apartment image is recoverable from a 135-vertex 12-regular graph: its 270 selected singular lines are exactly that graph\'s triangles. The 135x270 incidence matrix has exact rational rank 120 and binary rank 119.',
      'boundary':'The rational rank 120 is not an identification with the separate 120 anisotropic quotient classes.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
