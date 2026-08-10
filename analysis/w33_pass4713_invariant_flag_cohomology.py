#!/usr/bin/env python3
"""Pass 4713 — a genuinely PSp-invariant apartment C2 cohomology class.

Pass 4683 correctly observed that the earlier five-generator labelled Schreier
base was not preserved by full PSp(4,3).  Here the base is instead a self-paired
orbital graph of the full PSp action on the 810 selected point-line flags.
We choose the smallest connected self-paired orbital, lift it equivariantly to
1620 apartments, and exhibit a closed base triangle whose lift changes sheets.
The PGSp outer similitude preserves both base and lift, so the deck class spans
an honest one-dimensional trivial PGSp submodule of H^1.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict, deque
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, perm_group, transvection_matrix,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4713_INVARIANT_FLAG_COHOMOLOGY_REGEN.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry()
    Astar=np.asarray(Astar,dtype=np.uint8); apartments=sorted(tuple(map(int,a)) for a in apartments)
    j=(1<<40)-1; cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    V=set(span(B9)); rep=lambda x:min(int(x),int(x)^j)
    def fib(ap):
        x=0
        for i in ap:x^=cols[i]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments}); assert len(selected)==270
    flag_lifts=defaultdict(list)
    for ap in apartments:
        L=aline(ap);x=fib(ap);assert x in L;flag_lifts[(L,x)].append(ap)
    flags=sorted(flag_lifts); assert len(flags)==810 and Counter(map(len,flag_lifts.values()))==Counter({2:810})
    findex={f:i for i,f in enumerate(flags)};aindex={a:i for i,a in enumerate(apartments)}
    lift_index={}
    for fi,f in enumerate(flags):
        for bit,ap in enumerate(sorted(flag_lifts[f])):lift_index[aindex[ap]]=(fi,bit)

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    assert len(G)==25920
    def actv(x,g):return rep(pmask(rep(x),g))
    def actL(L,g):return tuple(sorted(actv(x,g) for x in L))
    def actf(f,g):L,x=f;return (actL(L,g),actv(x,g))
    def acta(ap,g):return tuple(sorted(g[i] for i in ap))
    def afi(i,g):return findex[actf(flags[i],g)]
    def aai(i,g):return aindex[acta(apartments[i],g)]

    H=[g for g in G if afi(0,g)==0]; assert len(H)==32
    unseen=set(range(810));suborbits=[]
    while unseen:
        x=min(unseen);O=sorted({afi(x,h) for h in H});suborbits.append(O);unseen-=set(O)
    candidates=[]
    for O in suborbits:
        if 0 in O:continue
        y=min(O);E={tuple(sorted((afi(0,g),afi(y,g)))) for g in G}
        B=nx.Graph();B.add_nodes_from(range(810));B.add_edges_from(E)
        if len(E)==810*len(O)//2 and set(dict(B.degree()).values())=={len(O)} and nx.is_connected(B):
            candidates.append((len(O),y,E,B))
    candidates.sort(key=lambda z:(z[0],z[1]));valency,y,base_edges,B=candidates[0]
    assert valency==16 and len(base_edges)==6480 and nx.diameter(B)==5

    # Lexicographic lift seed.  Its full G-orbit gives exactly two lift edges
    # over each base edge and a connected 16-regular graph on 1620 apartments.
    lifts0=sorted(aindex[a] for a in flag_lifts[flags[0]])
    liftsy=sorted(aindex[a] for a in flag_lifts[flags[y]])
    a0,ay=lifts0[0],liftsy[0]
    LE={tuple(sorted((aai(a0,g),aai(ay,g)))) for g in G}
    L=nx.Graph();L.add_nodes_from(range(1620));L.add_edges_from(LE)
    assert len(LE)==12960 and set(dict(L.degree()).values())=={16} and nx.is_connected(L)
    projected=Counter(tuple(sorted((lift_index[u][0],lift_index[v][0]))) for u,v in LE)
    assert len(projected)==6480 and Counter(projected.values())==Counter({2:6480})

    mate=lifts0[1]
    path=nx.shortest_path(L,a0,mate); proj=[lift_index[z][0] for z in path]
    assert len(path)-1==3 and proj[0]==proj[-1]==0

    # PGSp outer similitude preserves the orbital and its chosen lift orbit.
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx)
    base_outer={tuple(sorted((afi(u,outer),afi(v,outer)))) for u,v in base_edges}
    lift_outer={tuple(sorted((aai(u,outer),aai(v,outer)))) for u,v in LE}
    assert base_outer==base_edges and lift_outer==LE

    out={
      'pass':4713,
      'group':{'PSp_order':25920,'flag_stabilizer_order':32,'PGSp_outer_preserves_base':True,'PGSp_outer_preserves_lift':True},
      'base':{'vertices':810,'valency':16,'edges':6480,'diameter':5,'connected':True,'betti_1':5671,'construction':'smallest connected self-paired PSp orbital'},
      'lift':{'vertices':1620,'valency':16,'edges':12960,'connected':True,'edges_per_base_edge':2,'deck_group':'C2'},
      'nonzero_cycle':{'length':3,'projected_flag_cycle':proj,'changes_sheet':True},
      'cohomology':{'group':'H^1(base;F2)','dimension':5671,'deck_class_nonzero':True,'PGSp_invariant':True,'generated_submodule_dimension':1,'module':'trivial'},
      'theorem':'The smallest connected self-paired PSp orbital on the 810 flags is 16-regular. Its equivariant apartment lift is a connected C2 double cover with nonzero deck class; PGSp preserves the cover, so that class spans an honest one-dimensional trivial PGSp submodule of H^1.',
      'boundary':'Exact finite graph-cover/cohomology theorem; no optical phase is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
