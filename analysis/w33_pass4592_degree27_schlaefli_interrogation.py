#!/usr/bin/env python3
"""Pass 4592 — interrogate the degree-27 half-spinor orbit against Schlaefli/cubic lines.

This pass is deliberately fail-closed: dimension/cardinality equality is not used as evidence.
The script reconstructs the W33-derived O+(8,2) maximal-singular generators as in Pass 4588,
extracts the unique PSp(4,3) orbit of size 27, and forms the canonical orbital graphs under
the induced action. A degree-16 orbital is accepted as Schlaefli only after the exact
SRG(27,16,10,8) identities are verified. Stabilizer order is also checked to be 960.
"""
from __future__ import annotations
import json
from collections import Counter, deque
from pathlib import Path
import numpy as np
from w33_pass4588_apartment_triality_obstruction_spread_bridge import compose, perm_group, pmask
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry, build_line_perm, transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4592_DEGREE27_SCHLAEFLI_INTERROGATION.json'

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(n) for k in range(i+1,n) if Astar[i,k]]
    B9=rank_basis_int([cols[i]^cols[k] for i,k in edges]); V9=set(span(B9)); reps={min(x,x^j) for x in V9}
    rep=lambda x:min(int(x),int(x)^j)
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in reps if x and q(x)==0)
    levels={0:{frozenset((0,))}}
    for d in range(4):
        nxt=set()
        for S in levels[d]:
            for v in singular:
                if v in S or any(polar(v,u) for u in S): continue
                T=frozenset(set(S)|{rep(u^v) for u in S})
                if len(T)==1<<(d+1) and all(q(u)==0 for u in T): nxt.add(T)
        levels[d+1]=nxt
    generators=sorted(levels[4],key=lambda S:tuple(sorted(S)))
    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for g in cand:
        if g in G: continue
        gens.append(g); G=perm_group(gens)
        if len(G)==25920: break
    assert len(G)==25920
    def act_v(x,g): return rep(pmask(rep(x),g))
    def act_gen(X,g): return frozenset(act_v(x,g) for x in X)
    remaining=set(generators); orbits=[]
    while remaining:
        X=next(iter(remaining)); O={act_gen(X,g) for g in G}; orbits.append(sorted(O,key=lambda S:tuple(sorted(S)))); remaining-=set(O)
    O27=next(O for O in orbits if len(O)==27); idx={X:i for i,X in enumerate(O27)}
    X0=O27[0]; H=[g for g in G if act_gen(X0,g)==X0]; assert len(H)==960
    suborbits=[]; rem=set(range(27))
    while rem:
        a=min(rem); O={idx[act_gen(O27[a],h)] for h in H}; suborbits.append(sorted(O)); rem-=O
    sizes=sorted(map(len,suborbits)); assert sizes==[1,10,16]
    target=next(O for O in suborbits if len(O)==16)
    A=np.zeros((27,27),dtype=np.int16)
    for i,X in enumerate(O27):
        # transport target orbital from basepoint using a group element taking X0 to X
        g=next(g for g in G if act_gen(X0,g)==X)
        for j0 in target:
            A[i,idx[act_gen(O27[j0],g)]]=1
    assert np.array_equal(A,A.T) and np.all(np.diag(A)==0) and set(map(int,A.sum(1)))=={16}
    lam=set(); mu=set()
    for i in range(27):
        for k in range(i+1,27):
            c=int(A[i]@A[k]); (lam if A[i,k] else mu).add(c)
    assert lam=={10} and mu=={8}
    ev=np.linalg.eigvalsh(A.astype(float)); spec=Counter(int(round(x)) for x in ev)
    assert spec==Counter({16:1,4:6,-2:20})
    out={
      'pass':4592,
      'group_order':25920,
      'degree27_orbit':27,
      'point_stabilizer_order':960,
      'subdegrees':[1,10,16],
      'degree16_orbital_graph':{'parameters':'SRG(27,16,10,8)','spectrum':{'16':1,'4':6,'-2':20}},
      'conclusion':'The previously unnamed degree-27 maximal-singular-generator orbit carries the Schlaefli graph under the induced PSp(4,3) action; this is an action/orbital identification, not a count match.',
      'boundary':'This identifies the finite PSp(4,3) Schlaefli/cubic-line permutation carrier. It does not identify these 27 finite objects with physical particles or fields.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
