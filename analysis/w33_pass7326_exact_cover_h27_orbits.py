#!/usr/bin/env python3
"""Pass7326: classify the 200 nine-tritangent exact covers by H27 deletion type."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
from w33_pass4992_4999_common import build_base,build_group
import w33_pass7186_e8_matter_h27_cayley as h

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7326_EXACT_COVER_H27_ORBITS.json'

def covers_of_27(tris):
    byv={v:[] for v in range(27)}
    for i,t in enumerate(tris):
        for v in t:byv[v].append(i)
    out=[]
    def rec(chosen,used):
        if len(used)==27:out.append(tuple(sorted(chosen)));return
        v=min(set(range(27))-used,key=lambda x:sum(not (set(tris[i])&used) for i in byv[x]))
        for i in byv[v]:
            T=set(tris[i])
            if not(T&used):rec(chosen+[i],used|T)
    rec([],set());return sorted(set(out))

def h27_graph():
    V=[(u,z) for u in h.F for z in range(3)];G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        u,z=V[i];v,w=V[j]
        if u!=v and w==(z+h.coc(u,v))%3:G.add_edge(i,j)
    return G

def main():
    b=build_base();G27=b['G27'];tris=b['tritangents'];assert len(tris)==45
    covers=covers_of_27(tris);assert len(covers)==200
    target=h27_graph();types=[];reps=[]
    derived=[]
    for C in covers:
        H=G27.copy()
        for i in C:
            for e in itertools.combinations(tris[i],2):H.remove_edge(*e)
        assert set(dict(H.degree()).values())=={8} and H.number_of_edges()==108
        hit=next((k for k,R in enumerate(reps) if nx.is_isomorphic(H,R)),None)
        if hit is None:reps.append(H);hit=len(reps)-1
        types.append(hit);derived.append(H)
    hist=Counter(types);assert len(hist)==2 and sorted(hist.values())==[40,160]
    ht=next(k for k,R in enumerate(reps) if nx.is_isomorphic(R,target));assert hist[ht]==40
    other=1-ht
    aut=[]
    for R in reps:aut.append(sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(R,R).isomorphisms_iter()))
    assert aut[ht]==1296
    # PSp orbits on exact covers are exactly the two graph-isomorphism classes.
    grp=build_group(b);Tidx={frozenset(t):i for i,t in enumerate(tris)}
    def act_cover(C,g):
        return tuple(sorted(Tidx[frozenset(g[v] for v in tris[i])] for i in C))
    allset=set(covers);orbits=[];rem=set(covers)
    while rem:
        C=next(iter(rem));O={act_cover(C,g) for g in grp['gp']};assert O<=allset;orbits.append(O);rem-=O
    assert sorted(map(len,orbits))==[40,160]
    orbit_type=[]
    cmap={C:types[i] for i,C in enumerate(covers)}
    for O in orbits:
        z={cmap[C] for C in O};assert len(z)==1;orbit_type.append((len(O),next(iter(z))))
    assert any(n==40 and t==ht for n,t in orbit_type)
    out={'schema':'w33.pass7326.exact_cover_h27_orbits.v1','status':'PASS','exact_covers':200,
      'deletion_graph_isomorphism_types':2,'type_sizes':{str(k):v for k,v in sorted(hist.items())},
      'H27_type':ht,'H27_type_count':40,'H27_automorphism_order':1296,'other_type_count':160,'other_automorphism_order':aut[other],
      'PSp_cover_orbits':sorted(map(len,orbits)),'PSp_orbits_equal_deletion_types':True,
      'theorem':'The old 200 nine-tritangent exact covers split 40+160 exactly by the isomorphism type of the degree-8 graph left after deleting their nine K3s from the complement-Schlaefli graph. The 40-point-cover orbit is precisely the H27 distance-transitive deletion type.',
      'bridge':'This identifies the Pass5014 40 W33 point-covers with the 40 H27 refinements of the E6 complement-Schlaefli graph; the 160 incidence-cover orbit is the second deletion type.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','types':dict(hist),'aut':aut}))
if __name__=='__main__':main()
