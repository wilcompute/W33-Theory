#!/usr/bin/env python3
"""Pass 4688 — the apartment deck cohomology does not directly sign routing edges.

Project the 4050 labelled edges of the frozen Pass4656 five-factor Schreier
base from flags (selected line, selected point) to their selected-line endpoints.
Every projected pair is distance THREE in the selected270 routing graph.  Hence
none is one of the 1620 base routing edges or 405 Petersen shortcut edges.

The 4050 labelled edges collapse to 1275 distance-three line pairs, with
multiplicity 3 on 1200 pairs and 6 on 75 pairs.  Therefore a map from the deck
voltage to a routing-edge signing requires an additional path/transgression rule;
there is no canonical direct hot/cold bias to test.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4688_VOLTAGE_ROUTING_PROJECTION_OBSTRUCTION_REGEN.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]]);rep=lambda x:min(int(x),int(x)^j)
    def fib(ap):
        x=0
        for i in ap:x^=cols[i]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});selidx={L:i for i,L in enumerate(selected)};sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    Al=N.T@N-3*np.eye(270,dtype=np.int64);adj=[list(np.flatnonzero(Al[i])) for i in range(270)]
    dist=np.full((270,270),99,dtype=np.int16)
    for s in range(270):
        dist[s,s]=0;Q=deque([s])
        while Q:
            u=Q.popleft()
            for v in adj[u]:
                if dist[s,v]==99:dist[s,v]=dist[s,u]+1;Q.append(v)

    # Frozen Pass4656 five cyclic transvection factors.
    alltrans=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[alltrans[i] for i in [0,1,4,5,13]]
    def actv(x,g):return rep(pmask(rep(x),g))
    def actL(L,g):return tuple(sorted(actv(x,g) for x in L))
    flags=sorted((L,x) for L in selected for x in L);fidx={f:i for i,f in enumerate(flags)};assert len(flags)==810
    projected=[]
    per_factor=[]
    for g in gens:
        seen=set();P=[]
        for fi,f in enumerate(flags):
            fj=fidx[(actL(f[0],g),actv(f[1],g))];e=(min(fi,fj),max(fi,fj))
            if e in seen:continue
            seen.add(e);a=selidx[flags[e[0]][0]];b=selidx[flags[e[1]][0]];P.append(tuple(sorted((a,b))))
        assert len(seen)==810;per_factor.append(len(set(P)));projected.extend(P)
    assert len(projected)==4050
    assert Counter(int(dist[a,b]) for a,b in projected)==Counter({3:4050})
    C=Counter(projected);assert len(C)==1275 and Counter(C.values())==Counter({3:1200,6:75})
    routing={tuple(sorted((u,v))) for u in range(270) for v in adj[u] if u<v};assert len(routing)==2025
    assert not(set(C)&routing)

    old=json.loads((ROOT/'data/PART_W33_PASS4656_APARTMENT_C2_VOLTAGE_COHOMOLOGY.json').read_text(encoding='utf-8'))
    assert old['cohomology']['deck_class_nonzero'] is True
    out={'pass':4688,
      'source_cohomology':{'base':'Pass4656 five-factor labelled Schreier graph','labelled_edges':4050,'deck_class_nonzero':True},
      'projection_to_selected270':{'projected_edges':4050,'all_selected270_distance':3,'unique_distance3_pairs':1275,'pair_multiplicity_profile':{'3':1200,'6':75},'routing_edge_intersection':0,'base_edge_hits':0,'Petersen_shortcut_edge_hits':0},
      'signing_obstruction':{'canonical_direct_routing_signing':False,'reason':'the cohomology cochain lives on flag-Schreier edges whose line projection is distance three, not on selected270 routing edges','extra_data_required':'a choice of length-three routing path/transgression for each projected Schreier edge'},
      'theorem':'The nonzero apartment deck cohomology does not directly bias or sign either selected270 routing edge orbit: every supporting Schreier edge projects to distance three. Any hot/cold signing would require a noncanonical path-transgression choice.',
      'boundary':'Exact graph-projection obstruction. No claim is made about couplings after an explicitly specified transgression rule.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
