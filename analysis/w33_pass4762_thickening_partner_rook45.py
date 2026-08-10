#!/usr/bin/env python3
"""Pass 4762 -- the support-12 minimum shell contains a canonical 45-object rook-grid quotient.

Use the Pass4761 28-edge image of each of the 1620 apartment thickenings.  Every
minimum has exactly one other minimum sharing eight induced edges.  This defines
a fixed-point-free partner involution.  The 810 partner pairs have 16-line unions,
but those unions collapse 18-to-1 onto exactly 45 supports.  Every support induces
SRG(16,6,2,2) and has eight K4s, hence is the 4x4 rook graph L_2(4), not Shrikhande.

The decisive comparison is literal: rebuilding the Pass4585 protected 45 from the
135 singular apartment fibers gives exactly the same 45 subsets of the 40 W33 lines.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4762_THICKENING_PARTNER_ROOK45.json'

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
        T=frozenset(T);assert len(T)==12;th.append(T)
        m=0
        for i,j in itertools.combinations(sorted(T),2):
            if A[i,j]:m|=1<<eidx[(i,j)]
        assert m.bit_count()==28;em.append(m)
    assert len(set(th))==1620

    dist=Counter();partner=[None]*1620
    for i in range(1620):
        for j in range(i+1,1620):
            z=(em[i]&em[j]).bit_count();dist[z]+=1
            if z==8:
                assert partner[i] is None and partner[j] is None
                partner[i]=j;partner[j]=i
    expected={0:375840,1:259200,2:239760,6:77760,7:272160,8:810,12:64800,16:14580,21:6480}
    assert dict(sorted(dist.items()))==expected and all(x is not None for x in partner)
    pairs=[(i,partner[i]) for i in range(1620) if i<partner[i]];assert len(pairs)==810
    grids=defaultdict(list)
    for i,j in pairs:
        assert len(th[i]&th[j])==8 and set(apartments[i]).isdisjoint(apartments[j])
        U=frozenset(th[i]|th[j]);assert len(U)==16;grids[U].append((i,j))
    assert len(grids)==45 and set(map(len,grids.values()))=={18}

    for U in grids:
        G=nx.Graph();G.add_nodes_from(U)
        for i,j in itertools.combinations(U,2):
            if A[i,j]:G.add_edge(i,j)
        assert set(dict(G.degree()).values())=={6}
        ca=set();cn=set()
        for i,j in itertools.combinations(U,2):
            c=len(set(G[i])&set(G[j]));(ca if G.has_edge(i,j) else cn).add(c)
        assert ca==cn=={2}
        K4=[C for C in nx.find_cliques(G) if len(C)==4];assert len(K4)==8

    # Rebuild the old protected 45 exactly as Pass4585/4662: apartment fibers in V8.
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if A[i,k]])
    V=set(span(B9));all40=(1<<40)-1;rep=lambda x:min(int(x),int(x)^all40)
    def af(ap):
        x=0
        for i in ap:x^=cols[int(i)]
        return rep(x)
    fibers=defaultdict(list)
    for ap in apartments:fibers[af(ap)].append(ap)
    assert len(fibers)==135 and set(map(len,fibers.values()))=={12}
    protected={frozenset().union(*(set(ap) for ap in F)) for F in fibers.values()}
    assert len(protected)==45 and set(map(len,protected))=={16}
    assert set(grids)==protected

    out={'pass':4762,'minimum_shell':{'thickenings':1620,'edge_image_weight':28,'pairwise_edge_overlap_distribution':{str(k):v for k,v in sorted(dist.items())}},
      'partner_involution':{'fixed_points':0,'pairs':810,'partner_overlap':8,'partner_apartments_disjoint':True},
      'rook_quotient':{'distinct_16_line_unions':45,'partner_pairs_per_union':18,'induced_graph':'SRG(16,6,2,2)=L_2(4) rook graph','maximal_K4_per_union':8},
      'protected45_comparison':{'old_apartment_fibers':135,'old_protected_supports':45,'literal_set_equality':True,'target':'Pass4585/4616 protected E6-tritangent/center-quad 45'},
      'theorem':'The support-12 minimum shell has a canonical overlap-8 partner involution. Its 810 pairs collapse 18-to-1 onto 45 sixteen-line rook grids, and these 45 supports are literally the previously protected E6/center-quad 45.',
      'boundary':'Exact finite set/graph equality. The partner involution is defined on support-12 minima; no dynamical meaning is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
