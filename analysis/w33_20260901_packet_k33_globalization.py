#!/usr/bin/env python3
"""Globalize the local K4,4 -> K3,3 quotient against the 360 Schlaefli K3,3s.

The 45 W33 K4,4 octets / E8 D4+D4 packets are the lines of GQ(2,4); each is
incident with exactly three of the 27 completion charts.  The chart collinearity
graph has 360 induced K3,3s.  This script classifies all 45*360 packet/witness
pairs under PSp(4,3), rather than promoting the numerical 45*8=360 coincidence.

Result sought: determine the stabilizer orbits of a packet on the 360 global
K3,3 witnesses and test whether an equivariant eight-witness refinement can
exist.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter,deque
from pathlib import Path

import networkx as nx

import w33_20260829_216_clifford_torsor_nogo as base

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_PACKET_K33_GLOBALIZATION.json'


def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def paired_closure(A,B,n,m):
    I=(tuple(range(n)),tuple(range(m)));S={I};D=deque([I])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(A,B):
            z=(comp(ga,a),comp(gb,b))
            if z not in S:S.add(z);D.append(z)
    return S


def main():
    pts,idx,_lines,N=base.geometry(); supports,_=base.supports_from_N(N)
    assert len(supports)==45
    padj=[set() for _ in range(45)]
    for a,b in itertools.combinations(range(45),2):
        if supports[a].isdisjoint(supports[b]):padj[a].add(b);padj[b].add(a)
    charts=sorted((tuple(sorted(C)) for C in itertools.combinations(range(45),5)
                   if all(v in padj[u] for u,v in itertools.combinations(C,2))))
    assert len(charts)==27
    cidx={frozenset(C):i for i,C in enumerate(charts)}
    CG=nx.Graph();CG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if set(charts[a])&set(charts[b]):CG.add_edge(a,b)
    K33=[]
    for S in itertools.combinations(range(27),6):
        H=CG.subgraph(S)
        if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
            A,B=nx.algorithms.bipartite.sets(H)
            if len(A)==len(B)==3:K33.append(frozenset(S))
    assert len(K33)==360
    kidx={S:i for i,S in enumerate(K33)}

    incident=[frozenset(i for i,C in enumerate(charts) if p in C) for p in range(45)]
    assert {len(x) for x in incident}=={3}
    counts=Counter(len(incident[p]&K33[k]) for p in range(45) for k in range(360))
    per_packet=[]
    for p in range(45):per_packet.append(Counter(len(incident[p]&K) for K in K33))
    assert len(set(tuple(sorted(c.items())) for c in per_packet))==1

    # Same four deterministic PSp generators used by the obstruction carrier.
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for q in pts:
                z=alpha*base.form(q,v)%3
                y=base.norm(tuple((q[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[q] for q in S)] for S in supports) for p in gens40]
    G45=[];G27=[]
    for gi in (18,62,77,10):
        p45=gens45[gi]
        p27=tuple(cidx[frozenset(p45[q] for q in C)] for C in charts)
        G45.append(p45);G27.append(p27)
    G=paired_closure(G45,G27,45,27);assert len(G)==25920
    H=[z for z in G if z[0][0]==0];assert len(H)==576

    # Packet-0 stabilizer orbits on the 360 K3,3 witnesses.
    def actK(pc,K):return kidx[frozenset(pc[x] for x in K)]
    unseen=set(range(360));orbits=[]
    while unseen:
        k=min(unseen)
        O={actK(pc,K33[k]) for _pp,pc in H}
        unseen-=O;orbits.append(sorted(O))
    orbits=sorted(orbits,key=lambda O:(len(O),O[0]))
    profile=[]
    for O in orbits:
        inter=Counter(len(incident[0]&K33[k]) for k in O)
        profile.append({'size':len(O),'intersectionHistogram':{str(a):b for a,b in sorted(inter.items())}})
    orbit_sizes=[len(O) for O in orbits]

    # An equivariant assignment of a subset of global K3,3s to each packet must
    # be a union of packet-stabilizer orbits.  Test whether cardinality eight is
    # even combinatorially possible.
    possible={0}
    for s in orbit_sizes:possible|={x+s for x in list(possible)}
    eight_possible=8 in possible

    # Edge containment gives the intersection=2 class: the three charts through
    # a packet form a GQ line/K3, and each of its three edges lies in 24 K3,3s.
    edge_class=sum(1 for K in K33 if len(incident[0]&K)==2)
    one_class=sum(1 for K in K33 if len(incident[0]&K)==1)
    zero_class=sum(1 for K in K33 if len(incident[0]&K)==0)

    out={
      'schema':'w33.20260901.packet-k33-globalization.v1','status':'PASS',
      'objects':{'packets':45,'charts':27,'globalK33':360,'packetIncidentCharts':3},
      'pairIntersectionGlobalHistogram':{str(k):v for k,v in sorted(counts.items())},
      'packet0IntersectionClassSizes':{'0':zero_class,'1':one_class,'2':edge_class},
      'packetStabilizer':{'order':576,'orbitCountOnK33':len(orbits),'orbitSizes':orbit_sizes,'orbitProfile':profile},
      'equivariantEightWitnessRefinementPossible':eight_possible,
      'theorem':(
        'The complete PSp(4,3) packet-by-global-K3,3 relation is classified by the packet stabilizer. '
        'Any equivariant witness assignment must be a union of the listed stabilizer orbits. '
        'Therefore the local K4,4 -> S4/V4 -> K3,3 quotient is not identified with eight selected members '
        'of the 360 global Schlaefli K3,3 shell unless cardinality eight is a stabilizer-orbit union.'),
      'boundary':(
        'This classifies the natural global finite-group correspondence.  It does not deny the local abstract '
        'K4,4 frame quotient; it tests whether that local K3,3 can be promoted canonically to a small subset '
        'of the distinct 360 chart-graph K3,3 witnesses.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','orbitSizes':orbit_sizes,'classes':[zero_class,one_class,edge_class],
                      'eightPossible':eight_possible},sort_keys=True))

if __name__=='__main__':main()
