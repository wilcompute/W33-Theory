#!/usr/bin/env python3
"""Pass 4749 — adversarial capacity and targeted Petersen-fiber failures.

Pass4717 solved uniform all-pairs load.  Here capacity means worst-case pair
connectivity in the undirected two-technology router.  Cold edges have capacity
1 and hot Petersen edges capacity rho.  Stoer-Wagner cuts at adaptive rho samples
identify the exact affine cut signatures on the lower envelope.  Gomory-Hu trees
then classify all pairwise min-cuts at equal capacity and after targeted shortcut
fiber outages.  We separately test full ten-vertex fiber removal and the two
quotient pair types (adjacent/nonadjacent fibers).
"""
from __future__ import annotations
import itertools,json,math
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

def lower_envelope(lines):
    # lines are integer (a,b), a+b*rho. Return breakpoints and winning signatures.
    xs={Fraction(0,1)}
    L=sorted(set(lines))
    for (a,b),(c,d) in itertools.combinations(L,2):
        if b!=d:
            x=Fraction(c-a,b-d)
            if x>0:xs.add(x)
    sx=sorted(xs);samples=[]
    for i,x in enumerate(sx):
        if x>0:samples.append(x)
        y=sx[i+1] if i+1<len(sx) else None
        if y is not None:samples.append((x+y)/2)
    samples += [Fraction(1,1000),Fraction(1,1),Fraction(10,1),Fraction(100,1)]
    winners=[]
    for x in sorted(set(q for q in samples if q>0)):
        vals=[(Fraction(a)+Fraction(b)*x,(a,b)) for a,b in L];m=min(z[0] for z in vals)
        W=tuple(sorted(z[1] for z in vals if z[0]==m));winners.append((x,W))
    active=sorted(set(w for x,W in winners for w in W))
    bps=[]
    for u,v in itertools.combinations(active,2):
        a,b=u;c,d=v
        if b!=d:
            x=Fraction(c-a,b-d)
            if x>0 and all(Fraction(a)+Fraction(b)*x<=Fraction(e)+Fraction(f)*x for e,f in active):bps.append(x)
    return active,sorted(set(bps))

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
    assert set(dict(qG.degree()).values())=={10}

    # Adaptive exact cut-signature discovery from rational rho probes.
    probes=[Fraction(1,100),Fraction(1,10),Fraction(1,2),Fraction(1,1),Fraction(2,1),Fraction(10,1),Fraction(30,1),Fraction(36,1),Fraction(40,1),Fraction(100,1)]
    sigs=set();raw=[]
    for r in probes:
        val,sig,side=global_sig(270,cold,hot,float(r));sigs.add(sig);raw.append((r,val,sig,side))
    # add all positive crossings of discovered signatures and probe adjacent intervals; repeat twice
    for _ in range(2):
        cross=[]
        for (a,b),(c,d) in itertools.combinations(sorted(sigs),2):
            if b!=d:
                x=Fraction(c-a,b-d)
                if x>0:cross.append(x)
        extra=set(cross)
        sc=sorted(set([Fraction(0)]+cross+[Fraction(200)]))
        for x,y in zip(sc,sc[1:]):
            if y>x:extra.add((x+y)/2)
        for r in sorted(extra):
            if r<=0:continue
            val,sig,side=global_sig(270,cold,hot,float(r));sigs.add(sig);raw.append((r,val,sig,side))
    active,bps=lower_envelope(sigs)

    # Equal capacity pair-connectivity census.
    G1=weighted_graph(270,cold,hot,1.0);equal_global=nx.stoer_wagner(G1,weight='capacity')[0]
    equal_pairs=pair_cut_distribution(G1)

    # Targeted shortcut outage: delete the 15 hot edges of fiber 0.
    f0=set(fibers[0]);hot0={e for e in hot if e[0] in f0 and e[1] in f0};assert len(hot0)==15
    Go=weighted_graph(270,cold,hot,1.0,removed_edges=hot0);out_global=nx.stoer_wagner(Go,weight='capacity')[0];out_pairs=pair_cut_distribution(Go)
    # one-outage symbolic signatures at representative rho; vertex cut in failed fiber is always cold degree 12
    outage_sigs=set()
    for r in [0.1,1,10,100]:outage_sigs.add(global_sig(270,cold,hot,r,removed_edges=hot0)[1])

    # Two shortcut-fiber failures: quotient-adjacent and quotient-nonadjacent representatives.
    adj=next(iter(qG.edges()));non=next((a,b) for a,b in itertools.combinations(range(27),2) if not qG.has_edge(a,b))
    two={}
    for name,(a,b) in [('adjacent',adj),('nonadjacent',non)]:
        R=set(fibers[a])|set(fibers[b]);rem={e for e in hot if (e[0] in R and e[1] in R and owner[e[0]]==owner[e[1]])}
        H=weighted_graph(270,cold,hot,1.0,removed_edges=rem);two[name]={'fibers':[a,b],'removed_hot_edges':len(rem),'global_min_cut':float(nx.stoer_wagner(H,weight='capacity')[0])}

    # Full vertex-fiber removals, one and two quotient pair types.
    nodefail={}
    cases=[('one',(0,)),('two_adjacent',adj),('two_nonadjacent',non)]
    for name,F in cases:
        R=set().union(*(set(fibers[x]) for x in F));H=weighted_graph(270,cold,hot,1.0,removed_vertices=R)
        assert nx.is_connected(H)
        val,part=nx.stoer_wagner(H,weight='capacity')
        nodefail[name]={'fibers':list(F),'removed_vertices':len(R),'survivors':H.number_of_nodes(),'global_min_cut':float(val),'minimum_degree':min(dict(H.degree()).values()),'diameter':nx.diameter(H)}

    out={'pass':4749,
      'baseline_symbolic':{'discovered_cut_signatures_cold_plus_rho_hot':sorted([list(x) for x in sigs]),'active_lower_envelope_signatures':sorted([list(x) for x in active]),'positive_breakpoints':[str(x) for x in bps],
        'interpretation':'signature [a,b] means cut capacity a + b rho'},
      'equal_capacity':{'global_min_cut':float(equal_global),'all_pair_min_cut_distribution':equal_pairs},
      'one_shortcut_fiber_outage':{'removed_hot_edges':15,'global_min_cut_equal_capacity':float(out_global),'all_pair_min_cut_distribution':out_pairs,'symbolic_signatures_seen':sorted([list(x) for x in outage_sigs])},
      'two_shortcut_fiber_outages':two,'full_vertex_fiber_removal':nodefail,
      'theorem':'Worst-case pair capacity is governed by an exact lower envelope of integer cold/hot cut signatures. Whole-Petersen shortcut outages and full fiber removals are evaluated separately, with adjacent/nonadjacent two-fiber failure classes distinguished by the 27-vertex quotient.',
      'boundary':'Exact undirected edge-capacity/min-cut theorem for the finite router. It is not a queueing, latency, directed-switch, or measured-hardware claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
