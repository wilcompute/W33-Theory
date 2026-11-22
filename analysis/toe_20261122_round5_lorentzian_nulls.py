#!/usr/bin/env python3
"""Order-invariant causal-set benchmark with matched relation-count counterexamples.

1+1 Minkowski causal diamonds are simulated in light-cone coordinates
(u,v) in [0,1]^2: x<y iff both u and v increase. An all-to-all
2-layer poset is tuned to the same large-n ordering fraction ~1/2.
They differ sharply in chain height and interval contents. W33 graph
causal orientations are also compared against degree-matched null graphs.
Neither comparison proves continuum quantum gravity.
"""
from __future__ import annotations
from pathlib import Path
import json,math
import numpy as np
import networkx as nx
import toe_20261122_causal_orientation_no_go as W
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round5_lorentzian_nulls.json'

def stats(C):
    n=len(C)
    assert np.all(np.diag(C)==0)
    assert not np.any(C & C.T)
    relations=int(C.sum())
    counts=C.astype('int16')@C.astype('int16')
    nonempty=int(np.sum(C & (counts>0)))
    single=int(np.sum(C & (counts==1)))
    # DAG longest chain over arbitrary topological order.
    indeg=np.sum(C,axis=0)
    # Works for arbitrary poset order with Kahn method.
    h=np.ones(n,dtype=int)
    for i in list(nx.topological_sort(nx.from_numpy_array(C,create_using=nx.DiGraph))):
        for j in np.flatnonzero(C[i]):h[j]=max(h[j],h[i]+1)
    return dict(ordering_fraction=relations/(n*(n-1)/2),
                comparable_pairs=relations,intervals_with_positive_interior=nonempty,
                intervals_with_one_interior=single,maximum_chain_length=int(h.max()))

def diamond(n,rng):
    uv=rng.random((n,2))
    C=(uv[:,0,None]<uv[None,:,0]) & (uv[:,1,None]<uv[None,:,1])
    return C

def two_layers(n):
    assert n%2==0
    C=np.zeros((n,n),bool);C[:n//2,n//2:]=True
    return C

def graph_order(vertices,edges,rng):
    n=len(vertices)
    ordering=rng.permutation(n)
    pos=np.argsort(ordering)
    links=np.zeros((n,n),bool)
    for i,j in edges:
        if pos[i]<pos[j]:links[i,j]=1
        else:links[j,i]=1
    # closure by decreasing topological positions
    masks=[0]*n
    for i in ordering[::-1]:
        out=np.flatnonzero(links[i])
        m=0
        for j in out:m|=1<<int(j);m|=masks[int(j)]
        masks[i]=m
    C=np.array([[bool(masks[i]>>j &1) for j in range(n)] for i in range(n)])
    return C

def verify():
    rng=np.random.default_rng(22661122)
    rows=[]
    for n in (40,80,160):
        x=[stats(diamond(n,rng)) for _ in range(40)]
        y=stats(two_layers(n))
        means={key:float(np.mean([r[key] for r in x])) for key in x[0]}
        rows.append(dict(n=n,sprinkled_Minkowski_diamond_mean=means,layered_counterexample=y,
                   number_of_random_sprinklings=40))
    assert all(abs(z['sprinkled_Minkowski_diamond_mean']['ordering_fraction']-.5)<.05 for z in rows)
    assert all(z['layered_counterexample']['maximum_chain_length']==2 for z in rows)
    assert all(z['layered_counterexample']['intervals_with_positive_interior']==0 for z in rows)
    assert all(z['sprinkled_Minkowski_diamond_mean']['maximum_chain_length']>5 for z in rows)
    # Degree-matched W33 baseline: each graph 12 regular, 40 nodes, 240 links.
    _,E=W.w33();G=nx.Graph();G.add_nodes_from(range(40));G.add_edges_from(E)
    assert len(E)==240 and set(dict(G.degree()).values())=={12}
    comparison=[]
    for k in range(80):
        seed=7000+k
        rg=np.random.default_rng(seed)
        random_graph=nx.random_regular_graph(12,40,seed=seed)
        w=stats(graph_order(list(range(40)),E,rg))
        rr=stats(graph_order(list(range(40)),random_graph.edges(),np.random.default_rng(seed)))
        comparison.append((w,rr))
    metrics=['ordering_fraction','maximum_chain_length','intervals_with_one_interior']
    graph_stats={key:dict(W33=float(np.mean([z[0][key] for z in comparison])),
                          random_12_regular=float(np.mean([z[1][key] for z in comparison]))) for key in metrics}
    return dict(status='PASS_MINKOWSKI_POSSET_ORDER_INVARIANTS_WITH_MATCHED_NULLS',
      Minkowski_dimension='1+1; lightcone coordinates u,v with coordinatewise order',
      test_sizes=rows,W33_degree_matched_orientation_null=graph_stats,
      key_nonidentifiability='Ordering fraction alone does not identify Lorentzian geometry: an all-comparable two-layer poset and a 1+1 Minkowski diamond have limiting relation fraction 1/2 but distinct chains and intervals.',
      literature='Myrheim-Meyer dimension estimators in causal-set theory are established prior art; a single ordering-fraction statistic is a weak geometric diagnostic.',
      limitations='No 3+1 Lorentzian GR, Einstein-Hilbert continuum, spin-two pole, quantum dynamics, finite-density control or physical units. Random W33 orientations use an imposed external total order.')
if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status']);print(d['W33_degree_matched_orientation_null'])
