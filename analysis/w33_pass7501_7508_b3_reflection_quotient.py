#!/usr/bin/env python3
"""Pass7501-7508: conceptual E8 reflection quotient = B3(3) dual polar graph.

Uses the explicit Pass7465 Q+(7,3) realization.  For a nonsingular root r and
one generator family X, the quotient object is U_X=X cap r^perp.  The root
reflection swaps generator families while fixing r^perp pointwise, so the
reflection matching is objectwise, not a graph-isomorphism guess.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS7501_7508_B3_REFLECTION_QUOTIENT.json'

def radical(R,S):
    vals=set()
    for i,j in itertools.combinations(sorted(S),2):
        if E.dot(R[i],R[j])==-4:vals.add(E.canon3(tuple(R[i][k]-R[j][k] for k in range(8))))
    assert len(vals)==1
    return next(iter(vals))
def dot3(a,b):return sum(x*y for x,y in zip(a,b))%3

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();rad=[radical(R,S) for S in A2]
    assert len(set(rad))==1120
    r=E.canon3(E.SIMPLES[0]);assert dot3(r,r)==2
    Hpts={i for i,v in enumerate(rad) if dot3(v,r)==0};assert len(Hpts)==364
    plus=[i for i,p in enumerate(parity) if p==0];s=lgens[0]
    assert len(plus)==1120 and all(s[s[i]]==i and parity[s[i]]==(parity[i]^1) for i in range(2240))
    U={x:frozenset(leaves[x]&Hpts) for x in plus}
    assert set(map(len,U.values()))=={13} and len(set(U.values()))==1120
    assert all(frozenset(leaves[x]&leaves[s[x]])==U[x] for x in plus)
    rep=Counter(a for S in U.values() for a in S);assert set(rep)==Hpts and set(rep.values())=={40}
    pos={x:i for i,x in enumerate(plus)};Adj=[set() for _ in plus];mismatch=0
    for ii,x in enumerate(plus):
        for y in plus[ii+1:]:
            z=len(U[x]&U[y]);qadj=len(leaves[x]&leaves[s[y]])==13;badj=z==4
            mismatch+=qadj!=badj
            if badj:
                jj=pos[y];Adj[ii].add(jj);Adj[jj].add(ii)
    assert mismatch==0 and {len(x) for x in Adj}=={39}
    dist=[-1]*1120;dist[0]=0;dq=deque([0])
    while dq:
        v=dq.popleft()
        for w in Adj[v]:
            if dist[w]<0:dist[w]=dist[v]+1;dq.append(w)
    assert Counter(dist)==Counter({0:1,1:39,2:351,3:729})
    layers=[{i for i,d in enumerate(dist) if d==k} for k in range(4)];rows=[]
    for L in layers:
        C=Counter(tuple(len(Adj[v]&layers[j]) for j in range(4)) for v in L);assert len(C)==1;rows.append(next(iter(C)))
    assert rows==[(0,39,0,0),(1,2,36,0),(0,4,8,27),(0,0,13,26)]
    out={'schema':'w33.pass7501_7508.b3_reflection_quotient.v1','status':'PASS','passes':'7501-7508',
      'ambient':{'model':'E8/3E8 = Q+(7,3)','fixed_hyperplane':'r^perp','singular_points':364},
      'object_map':'plus generator X -> U_X=X intersect r^perp, a maximal totally singular 3-space of Q(6,3)',
      'targets':1120,'projective_points_per_target':13,'point_replication':40,
      'reflection_pair_law':'X intersect s_r(X)=X intersect r^perp',
      'adjacency_equivalence':'X meets s_r(Y) in 13 projective points iff U_X meets U_Y in 4 projective points',
      'dual_polar_graph':'B3(3)','degree':39,'distance_distribution':[1,39,351,729],
      'intersection_array':'{39,36,27;1,4,13}','transition_rows':[list(x) for x in rows],
      'correction':'The earlier C3(3) candidate was only an intersection-array match. Over odd q B3 and C3 need not be isomorphic; the explicit reflection-hyperplane construction selects B3(3).',
      'claim_boundary':'Finite E8/orthogonal-polar-space theorem only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','B3_vertices':1120,'mismatches':mismatch}))
if __name__=='__main__':main()
