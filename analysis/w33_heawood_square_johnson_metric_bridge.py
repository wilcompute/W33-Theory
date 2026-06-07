#!/usr/bin/env python3
"""BT496: Heawood-Square Johnson Metric Bridge Theorem.

BT494: distance-2(Heawood)=K7 disjoint union K7.
BT495: Csaszar K7 edge metrics decompose by T(7)=L(K7) as 1+6+14.

This welds them into one exact adjacency-algebra chain:
    Heawood A_H -> A_H^2 - 3I -> K7 -> L(K7)=T(7) -> 1+6+14.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import networkx as nx
import sympy as sp

FANO_LINES=[(0,1,3),(0,2,5),(0,4,6),(1,2,4),(1,5,6),(2,3,6),(3,4,5)]

def fano_incidence_matrix() -> sp.Matrix:
    B=sp.zeros(7,7)
    for li,line in enumerate(FANO_LINES):
        for p in line:
            B[p,li]=1
    return B

def graph_from_adjacency(A: sp.Matrix) -> nx.Graph:
    g=nx.Graph(); n=A.shape[0]; g.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1,n):
            if A[i,j] != 0:
                g.add_edge(i,j)
    return g

def main() -> dict:
    x=sp.Symbol('x')
    B=fano_incidence_matrix(); I7=sp.eye(7); J7=sp.ones(7,7)
    assert B*B.T == 2*I7 + J7
    AH=sp.zeros(14,14); AH[:7,7:]=B; AH[7:,:7]=B.T
    H=graph_from_adjacency(AH)
    assert nx.is_isomorphic(H,nx.heawood_graph())
    A2=AH**2
    assert A2[:7,:7]-3*I7 == J7-I7
    assert A2[7:,7:]-3*I7 == J7-I7
    K7=graph_from_adjacency(J7-I7)
    T7=nx.line_graph(K7)
    assert T7.number_of_nodes()==21
    assert T7.number_of_edges()==105
    assert sorted(dict(T7.degree()).values())==[10]*21
    edges=list(combinations(range(7),2))
    M=sp.zeros(21,7)
    for i,(u,v) in enumerate(edges):
        M[i,u]=1; M[i,v]=1
    AT=M*M.T-2*sp.eye(21)
    assert sp.factor(AT.charpoly(x).as_expr()) == (x-10)*(x-3)**6*(x+2)**14
    one=sp.ones(21,1)
    P1=one*one.T/21
    PM=M*(M.T*M).inv()*M.T
    P6=sp.simplify(PM-P1)
    P14=sp.simplify(sp.eye(21)-PM)
    assert (P1.rank(),P6.rank(),P14.rank()) == (1,6,14)
    assert P1+P6+P14 == sp.eye(21)
    D2=nx.Graph(); D2.add_nodes_from(H.nodes())
    for u,v in combinations(H.nodes(),2):
        if nx.shortest_path_length(H,u,v)==2:
            D2.add_edge(u,v)
    comps=[D2.subgraph(c).copy() for c in nx.connected_components(D2)]
    assert sorted(c.number_of_nodes() for c in comps)==[7,7]
    assert all(nx.is_isomorphic(c,nx.complete_graph(7)) for c in comps)
    line_union=nx.disjoint_union(nx.line_graph(comps[0]), nx.line_graph(comps[1]))
    assert line_union.number_of_nodes()==42
    assert line_union.number_of_edges()==210
    results={
        'theorem':'BT496 Heawood-Square Johnson Metric Bridge Theorem',
        'pipeline':['Heawood/Szilassi adjacency A_H','A_H^2-3I on bipartitions = K7 disjoint union K7','line graph of recovered K7 = T(7)','T(7) metric projector split = 1+6+14'],
        'certificates':{
            'heawood_vertices_edges':[H.number_of_nodes(),H.number_of_edges()],
            'distance2_components':[c.number_of_nodes() for c in comps],
            'distance2_total_edges':sum(c.number_of_edges() for c in comps),
            'T7_nodes_edges_degree':[T7.number_of_nodes(),T7.number_of_edges(),10],
            'T7_spectrum':'10^1, 3^6, (-2)^14',
            'projector_ranks':{'scalar':1,'vertex_potential':6,'G2_residual':14},
            'line_graph_union_nodes_edges':[line_union.number_of_nodes(),line_union.number_of_edges()]},
        'interpretation':{'BT494':'Szilassi/Heawood squared recovers Csaszar K7','BT495':'Csaszar K7 metrics decompose by Johnson T(7)','BT496':'Metric decomposition is induced by the squared Szilassi carrier'},
        'substrate_reading':{'A_H':'face-complete Szilassi observable','A_H_squared':'vertex-complete Csaszar observable','T7':'edge-metric operator with eigenvalues E1,q,-r','1+6+14':'scalar + G2-positive selector + dim(G2) residual'}}
    out=Path('data/PART_BT496_HEAWOOD_SQUARE_JOHNSON_METRIC_BRIDGE_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))
    return results
if __name__=='__main__': main()
