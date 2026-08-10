#!/usr/bin/env python3
"""Pass 4749 — exact adversarial capacity and targeted Petersen-fiber failures.

Pass4717 solved uniform all-pairs load. Here capacity means worst-case pair
connectivity in the undirected two-technology router. Cold edges have capacity
1 and hot Petersen edges capacity rho.

The exact lower envelope needs no interpolation from sampled min-cuts. The cold
selected270 graph has edge-connectivity 12; every hot Petersen fiber has
edge-connectivity 3; and the 27-vertex quotient has edge-connectivity 10. Thus
for any nontrivial cut:

  * if it splits a Petersen fiber, (cold,hot) boundary >= (12,3), attained by a
    single router vertex;
  * if it splits no Petersen fiber, it is a union of whole fibers and its cold
    boundary is 12 times a quotient cut, hence >= 120, attained by one fiber.

Therefore the exact global min-cut is min(12+3 rho, 120), with the unique
technology breakpoint rho=36. Numeric Stoer-Wagner probes are retained only as
regression diagnostics. Whole shortcut-fiber outages and full ten-vertex fiber
removals are then evaluated separately.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import networkx as nx
from w33_pass4716_selected270_bundle_connection import build_bundle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4749_ADVERSARIAL_ROUTER_CAPACITY.json'

def cut_signature(part,hotset,coldset):
    S=set(part);a=b=0
    for e in coldset:
        if (e[0] in S)^(e[1] in S):a+=1
    for e in hotset:
        if (e[0] in S)^(e[1] in S):b+=1
    return a,b

def weighted_graph(n,cold,hot,rho,removed_edges=frozenset(),removed_vertices=frozenset()):
    G=nx.Graph();G.add_nodes_from(i for i in range(n) if i not in removed_vertices)
    for u,v in cold:
        e=tuple(sorted((u,v)))
        if u not in removed_vertices and v not in removed_vertices and e not in removed_edges:G.add_edge(u,v,capacity=1.0,weight=1.0)
    for u,v in hot:
        e=tuple(sorted((u,v)))
        if u not in removed_vertices and v not in removed_vertices and e not in removed_edges:G.add_edge(u,v,capacity=float(rho),weight=float(rho))
    return G

def global_sig(n,cold,hot,rho,removed_edges=frozenset(),removed_vertices=frozenset()):
    G=weighted_graph(n,cold,hot,rho,removed_edges,removed_vertices)
    val,part=nx.stoer_wagner(G,weight='capacity')
    S,T=part
    return float(val),cut_signature(S,set(cold)-set(removed_edges),set(hot)-set(removed_edges)),min(len(S),len(T))

def pair_cut_distribution(G):
    T=nx.gomory_hu_tree(G,capacity='capacity');dist=Counter()
    nodes=sorted(G)
    for i,u in enumerate(nodes):
        for v in nodes[i+1:]:
            path=nx.shortest_path(T,u,v)
            z=min(float(T[a][b]['weight']) for a,b in zip(path,path[1:]))
            dist[round(z,9)]+=1
    return dict(sorted(dist.items()))

def main():
    X=build_bundle();hot=sorted(tuple(sorted(e)) for e in X['hot']);cold=sorted(tuple(sorted(e)) for e in X['cold']);K5=X['K5'];projected=X['projected']
    hotset=set(hot);coldset=set(cold);assert (len(hot),len(cold))==(405,1620)
    owner=[]
    for T in projected:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    fibers=[sorted(i for i,a in enumerate(owner) if a==f) for f in range(27)];assert set(map(len,fibers))=={10}
    qG=nx.Graph();qG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if K5[a]&K5[b]:qG.add_edge(a,b)
    assert set(dict(qG.degree()).values())=={10} and nx.is_connected(qG)

    coldG=nx.Graph();coldG.add_nodes_from(range(270));coldG.add_edges_from(cold)
    hotG=nx.Graph();hotG.add_nodes_from(range(270));hotG.add_edges_from(hot)
    assert nx.is_connected(coldG)
    cold_edge_connectivity=nx.edge_connectivity(coldG);assert cold_edge_connectivity==12
    quotient_edge_connectivity=nx.edge_connectivity(qG);assert quotient_edge_connectivity==10
    hot_components=[hotG.subgraph(C).copy() for C in nx.connected_components(hotG)]
    assert len(hot_components)==27 and set(H.number_of_nodes() for H in hot_components)=={10}
    hot_edge_connectivities=[nx.edge_connectivity(H) for H in hot_components];assert set(hot_edge_connectivities)=={3}

    # Every quotient edge carries exactly 12 cold physical edges.
    qmult=Counter()
    for u,v in cold:qmult[tuple(sorted((owner[u],owner[v])))]+=1
    assert len(qmult)==135 and set(qmult.values())=={12} and set(qmult)=={tuple(sorted(e)) for e in qG.edges()}

    exact={
      'cold_graph_edge_connectivity':cold_edge_connectivity,
      'hot_Petersen_edge_connectivity':3,
      'quotient_edge_connectivity':quotient_edge_connectivity,
      'cold_edges_per_quotient_edge':12,
      'split_fiber_lower_bound':'12 + 3 rho',
      'whole_fiber_union_lower_bound':'120',
      'exact_global_min_cut':'min(12 + 3 rho, 120)',
      'breakpoint_rho':36,
      'witness_below_breakpoint':'single router vertex has 12 cold + 3 hot incident edges',
      'witness_above_breakpoint':'one complete Petersen fiber has 120 cold boundary edges and zero hot boundary edges'
    }
    for r in [Fraction(1,100),Fraction(1,10),Fraction(1,1),Fraction(10,1),Fraction(35,1),Fraction(36,1),Fraction(37,1),Fraction(100,1)]:
        val,sig,side=global_sig(270,cold,hot,float(r))
        target=min(12+3*float(r),120.0)
        assert abs(val-target)<1e-7

    # Equal capacity pair-connectivity census.
    G1=weighted_graph(270,cold,hot,1.0);equal_global=nx.stoer_wagner(G1,weight='capacity')[0]
    assert abs(equal_global-15.0)<1e-8
    equal_pairs=pair_cut_distribution(G1)

    # Targeted shortcut outage: delete the 15 hot edges of fiber 0. Cold graph remains,
    # so every cut has capacity >=12; a single failed-fiber vertex attains 12.
    f0=set(fibers[0]);hot0={e for e in hot if e[0] in f0 and e[1] in f0};assert len(hot0)==15
    outage_diag={}
    for r in [Fraction(1,100),Fraction(1,1),Fraction(10,1),Fraction(100,1)]:
        val,sig,side=global_sig(270,cold,hot,float(r),removed_edges=hot0);assert abs(val-12.0)<1e-7
        outage_diag[str(r)]={'min_cut':val,'signature':list(sig),'smaller_side':side}
    Go=weighted_graph(270,cold,hot,1.0,removed_edges=hot0);out_pairs=pair_cut_distribution(Go)

    # Two shortcut-fiber failures: quotient-adjacent and quotient-nonadjacent representatives.
    adj=next(iter(qG.edges()));non=next((a,b) for a,b in itertools.combinations(range(27),2) if not qG.has_edge(a,b))
    two={}
    for name,(a,b) in [('adjacent',adj),('nonadjacent',non)]:
        R=set(fibers[a])|set(fibers[b]);rem={e for e in hot if owner[e[0]] in (a,b) and owner[e[0]]==owner[e[1]]}
        H=weighted_graph(270,cold,hot,1.0,removed_edges=rem);val=float(nx.stoer_wagner(H,weight='capacity')[0])
        assert val==12.0
        two[name]={'fibers':[a,b],'removed_hot_edges':len(rem),'global_min_cut_equal_capacity':val}

    # Full vertex-fiber removals, one and two quotient pair types.
    nodefail={}
    cases=[('one',(0,)),('two_adjacent',adj),('two_nonadjacent',non)]
    for name,F in cases:
        R=set().union(*(set(fibers[x]) for x in F));H=weighted_graph(270,cold,hot,1.0,removed_vertices=R)
        assert nx.is_connected(H)
        val,part=nx.stoer_wagner(H,weight='capacity')
        nodefail[name]={'fibers':list(F),'removed_vertices':len(R),'survivors':H.number_of_nodes(),'global_min_cut':float(val),'minimum_degree':min(dict(H.degree()).values()),'diameter':nx.diameter(H)}

    out={'pass':4749,
      'exact_symbolic_global_cut':exact,
      'equal_capacity':{'global_min_cut':float(equal_global),'all_pair_min_cut_distribution':equal_pairs},
      'one_shortcut_fiber_outage':{'removed_hot_edges':15,'exact_global_min_cut_all_positive_rho':12,'diagnostic_samples':outage_diag,'all_pair_min_cut_distribution_at_rho1':out_pairs},
      'two_shortcut_fiber_outages':two,'full_vertex_fiber_removal':nodefail,
      'theorem':'For cold capacity 1 and hot capacity rho>0, the exact worst-pair min-cut is min(12+3 rho,120), with breakpoint rho=36. The proof uses edge-connectivity 12 of the cold graph, edge-connectivity 3 of each Petersen fiber, edge-connectivity 10 of the 27-vertex quotient, and exactly 12 cold physical edges per quotient edge. Failure of all shortcut edges in even one Petersen fiber collapses the global min-cut to exactly 12 for every rho>0.',
      'boundary':'Exact undirected edge-capacity/min-cut theorem for the finite router. It is not a queueing, latency, directed-switch, or measured-hardware claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
