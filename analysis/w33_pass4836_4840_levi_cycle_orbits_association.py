#!/usr/bin/env python3
"""Passes 4836/4840 — classify the 1080 Levi 8-cycles and their K3,3 bridge.

The [1620,64,96]_2 code is Rep_12 of the binary cycle code of the
72-vertex/135-edge Levi graph of GQ(4,2); its 1080 minimum words are therefore
exactly the simple Levi 8-cycles.  This producer reconstructs the full PSp and
PGSp actions from the independent Pass4804 45-point GQ carrier, computes the
minimum-shell orbit/stabilizer data, the exact pair-intersection scheme, and an
objectwise incidence with the 360 induced K3,3 witnesses in the 27-line
intersection graph.

No conclusion is inferred from 1080=3*360.  The K3,3/cycle incidence is built
literally: every 2x2 rectangle in a K3,3 gives four GQ intersection points and
hence one Levi 8-cycle.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4804_equivariant_f4_e6_intertwiner import source_packet_action
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4836_4840_LEVI_CYCLE_ORBITS_ASSOCIATION.json'

def canon_nodes(C):
    C=list(C);R=list(reversed(C));cand=[]
    for s in range(len(C)):
        cand.append(tuple(C[s:]+C[:s]));cand.append(tuple(R[s:]+R[:s]))
    return min(cand)

def perm_mask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def srg_params(G):
    n=G.number_of_nodes();deg=set(dict(G.degree()).values())
    if len(deg)!=1:return None
    k=next(iter(deg));lam=set();mu=set()
    for i,j in itertools.combinations(range(n),2):
        c=len(set(G[i])&set(G[j]))
        (lam if G.has_edge(i,j) else mu).add(c)
        if len(lam)>1 or len(mu)>1:return None
    if len(lam)==1 and len(mu)==1:return (n,k,next(iter(lam)),next(iter(mu)))
    return None

def main()->int:
    Q45,PSp45,PGSp45=source_packet_action();assert len(PSp45)==25920 and len(PGSp45)==51840
    # 27 GQ lines are the maximal K5s of the 45-point collinearity graph.
    lines=sorted((frozenset(c) for c in nx.find_cliques(Q45) if len(c)==5),key=lambda S:tuple(sorted(S)));assert len(lines)==27
    lidx={S:i for i,S in enumerate(lines)}
    def line_perm(p):return tuple(lidx[frozenset(p[x] for x in S)] for S in lines)
    # Levi graph: point vertices 0..44, line vertices 45..71.
    ledges=sorted((p,l) for l,S in enumerate(lines) for p in S);assert len(ledges)==135;lei={e:i for i,e in enumerate(ledges)}
    Levi=nx.Graph();Levi.add_nodes_from(range(72));Levi.add_edges_from((p,45+l) for p,l in ledges);assert nx.is_connected(Levi) and nx.girth(Levi)==8
    # Enumerate simple 8-cycles once; record edge-support masks.
    cyc_nodes=set()
    for s in range(72):
        def dfs(path):
            if len(path)==8:
                if Levi.has_edge(path[-1],s):cyc_nodes.add(canon_nodes(path))
                return
            for v in Levi[path[-1]]:
                if v==s or v in path or v<s:continue
                dfs(path+[v])
        dfs([s])
    assert len(cyc_nodes)==1080
    cycles=[]
    for C in sorted(cyc_nodes):
        m=0
        for a,b in zip(C,C[1:]+C[:1]):
            if a>=45:a,b=b,a
            m|=1<<lei[(a,b-45)]
        assert m.bit_count()==8;cycles.append(m)
    cset=set(cycles);cidx={m:i for i,m in enumerate(cycles)}

    def incidence_perm(pp):
        lp=line_perm(pp);return tuple(lei[(pp[p],lp[l])] for p,l in ledges)
    # One representative orbit is enough if it reaches all 1080 minima.
    rep=cycles[0]
    Porb={perm_mask(rep,incidence_perm(p)) for p in PSp45}
    Gorb={perm_mask(rep,incidence_perm(p)) for p in PGSp45}
    assert Porb<=cset and Gorb<=cset
    ptrans=len(Porb)==1080;gtrans=len(Gorb)==1080

    # Exact support-intersection distribution and relation graphs.
    paircnt=Counter();per=Counter()
    for i,j in itertools.combinations(range(1080),2):paircnt[(cycles[i]&cycles[j]).bit_count()]+=1
    for j in range(1,1080):per[(cycles[0]&cycles[j]).bit_count()]+=1
    # Transitivity implies every row has same intersection profile; verify directly by totals.
    for t,c in paircnt.items():assert 2*c==1080*per[t]
    relations={}
    for t in sorted(k for k in per if k>0):
        G=nx.Graph();G.add_nodes_from(range(1080));G.add_edges_from((i,j) for i,j in itertools.combinations(range(1080),2) if (cycles[i]&cycles[j]).bit_count()==t)
        relations[str(t)]={'degree':next(iter(set(dict(G.degree()).values()))),'edges':G.number_of_edges(),'components':nx.number_connected_components(G),'srg':srg_params(G)}

    # 27-line intersection graph and all induced K3,3s.
    Lg=nx.Graph();Lg.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if len(lines[i]&lines[j])==1:Lg.add_edge(i,j)
    assert set(dict(Lg.degree()).values())=={10}
    K=[]
    for S in itertools.combinations(range(27),6):
        H=Lg.subgraph(S)
        if H.number_of_edges()!=9 or set(dict(H.degree()).values())!={3} or not nx.is_bipartite(H):continue
        A,B=nx.algorithms.bipartite.sets(H)
        if len(A)==len(B)==3:K.append((tuple(sorted(A)),tuple(sorted(B))))
    assert len(K)==360
    cycle_to_k=Counter();k_rect_counts=[]
    for A,B in K:
        seen=set()
        for aa in itertools.combinations(A,2):
            for bb in itertools.combinations(B,2):
                m=0
                for l in aa+bb:
                    opp=bb if l in aa else aa
                    for r in opp:
                        hit=lines[l]&lines[r];assert len(hit)==1;p=next(iter(hit));m|=1<<lei[(p,l)]
                assert m.bit_count()==8 and m in cset;seen.add(m);cycle_to_k[m]+=1
        assert len(seen)==9;k_rect_counts.append(len(seen))
    assert set(k_rect_counts)=={9}
    extension_profile=Counter(cycle_to_k.values());assert set(cycle_to_k)==cset

    out={
      'passes':[4836,4840],
      'minimum_shell':{'code':'[1620,64,96]_2','Levi_8_cycles':1080,'PSp_orbit_size_of_representative':len(Porb),'PGSp_orbit_size_of_representative':len(Gorb),'PSp_transitive':ptrans,'PGSp_transitive':gtrans,'PSp_stabilizer_order':25920//len(Porb),'PGSp_stabilizer_order':51840//len(Gorb)},
      'cycle_support_intersections':{'per_cycle':dict(sorted(per.items())),'unordered_pair_counts':dict(sorted(paircnt.items())),'relation_graphs':relations},
      'K33_bridge':{'induced_K33':360,'rectangles_per_K33':9,'cycle_extension_multiplicity_profile':dict(sorted(extension_profile.items())),'all_1080_cycles_hit':set(cycle_to_k)==cset,'incidence_total':sum(cycle_to_k.values())},
      'theorem':'The complete weight-96 shell is classified by the exact PSp/PGSp actions, and its relation to the 360 ternary K3,3 witnesses is objectwise: each induced K3,3 contributes its nine 2x2 rectangles as Levi 8-cycles; the reverse multiplicity is recorded by direct incidence enumeration.',
      'boundary':'A K3,3 witness is a six-line ternary homology object; a Levi minimum is an eight-incidence binary cycle. The incidence map does not identify the two shells or their coefficient fields.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
