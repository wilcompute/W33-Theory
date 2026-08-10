#!/usr/bin/env python3
"""Pass 4763 -- reconstruct SRG(45,32,22,24) directly from support-12 minima.

No protected coordinates are imported.  Starting only from W33 apartments, their
12-line thickenings, and the unique overlap-8 partner relation of Pass4762, form
the 45 distinct 16-line partner unions.  Two unions meet in either 7 or 4 W33
lines.  Declaring intersection 7 adjacent gives SRG(45,32,22,24).

For the 45x40 0/1 grid-line incidence T:

  TT^T = 12 I_45 + 3 A_45 + 4 J_45,
  T^T T = 12 I_40 + 3 A_dual + 6 J_40.

Thus rank_Q(T)=25.  Over F2 rank(T)=24, while TT^T=A_45 has rank 14 and
T^TT=A_dual has rank 10.  This independently recovers the exceptional 45-object
transport graph from the support-12 code shell.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4763_SUPPORT12_RECONSTRUCTS_SRG45.json'

def rank2_matrix(M):
    piv={}
    for row in np.asarray(M,dtype=np.uint8):
        x=0
        for j,b in enumerate(row):
            if int(b)&1:x|=1<<j
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def main()->int:
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]];eidx={e:k for k,e in enumerate(edges)}
    through=[set() for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:through[p].add(li)
    th=[];em=[]
    for ap in apartments:
        corners=set()
        for i,j in itertools.combinations(ap,2):
            z=lines[i]&lines[j]
            if z:corners|=set(z)
        T=set()
        for p in corners:T|=through[p]
        T=frozenset(T);th.append(T);m=0
        for i,j in itertools.combinations(sorted(T),2):
            if A[i,j]:m|=1<<eidx[(i,j)]
        em.append(m)
    partner=[None]*1620
    for i in range(1620):
        for j in range(i+1,1620):
            if (em[i]&em[j]).bit_count()==8:
                assert partner[i] is None and partner[j] is None;partner[i]=j;partner[j]=i
    Gset={frozenset(th[i]|th[partner[i]]) for i in range(1620)};assert len(Gset)==45
    grids=sorted(Gset,key=lambda U:tuple(sorted(U)))
    A45=np.zeros((45,45),dtype=np.uint8);inter=Counter()
    for i,j in itertools.combinations(range(45),2):
        z=len(grids[i]&grids[j]);inter[z]+=1
        if z==7:A45[i,j]=A45[j,i]=1
    assert inter==Counter({7:720,4:270}) and set(map(int,A45.sum(axis=1)))=={32}
    ac=set();nc=set()
    for i,j in itertools.combinations(range(45),2):
        c=int(np.dot(A45[i],A45[j]));(ac if A45[i,j] else nc).add(c)
    assert ac=={22} and nc=={24}

    T=np.zeros((45,40),dtype=np.uint8)
    for i,U in enumerate(grids):
        for x in U:T[i,x]=1
    assert set(map(int,T.sum(axis=1)))=={16} and set(map(int,T.sum(axis=0)))=={18}
    TT=T.astype(int)@T.astype(int).T;TtT=T.astype(int).T@T.astype(int)
    J45=np.ones((45,45),dtype=int);J40=np.ones((40,40),dtype=int)
    assert np.array_equal(TT,12*np.eye(45,dtype=int)+3*A45.astype(int)+4*J45)
    assert np.array_equal(TtT,12*np.eye(40,dtype=int)+3*A.astype(int)+6*J40)
    # SRG(45,32,22,24) eigenvalues are 32^1,2^24,(-4)^20.
    # Hence TT^T has 288^1,18^24,0^20 and rational rank 25.
    rT2=rank2_matrix(T);rA45=rank2_matrix(A45);rA40=rank2_matrix(A)
    assert (rT2,rA45,rA40)==(24,14,10)
    assert np.array_equal(TT%2,A45) and np.array_equal(TtT%2,A)
    out={'pass':4763,'support12_quotient':{'objects':45,'pair_intersections':{'7':720,'4':270},'adjacency_rule':'intersection 7'},
      'transport_graph':{'parameters':'SRG(45,32,22,24)','eigenvalues':{'32':1,'2':24,'-4':20}},
      'grid_line_incidence':{'shape':[45,40],'row_weight':16,'column_weight':18,'rank_Q':25,'rank_F2':rT2,
        'TTt':'12 I45 + 3 A45 + 4 J45','TtT':'12 I40 + 3 A_dual + 6 J40','rank_F2_A45':rA45,'rank_F2_A_dual':rA40},
      'theorem':'The support-12 minimum shell alone reconstructs the 45-object SRG(45,32,22,24). Its 45x40 grid-line incidence has exact Gram identities and ranks 25 over Q and 24 over F2.',
      'boundary':'The 40-coordinate graph here is the W33 line-intersection graph (dual GQ(4,3)), not the nonisomorphic point graph.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
