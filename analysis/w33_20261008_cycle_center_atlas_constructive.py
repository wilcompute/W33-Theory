#!/usr/bin/env python3
"""Exact W33 C8 noncommuting-center graph and constructive commuting atlases.

All combinatorial counts are finite exact calculations. Greedy maximum is a
certified LOWER bound, not a proof of maximal cardinality.
"""
import json,sys,random
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_global_cycle_center_census import cycles
OUT=ROOT/"data"/"w33_20261008_cycle_center_atlas_constructive.json"

def census():
    c=cycles();n=len(c);assert n==1620
    pm=[];lm=[]
    for cy in c:
        p=q=0
        for v in cy:
            if v<40:p|=1<<v
            else:q|=1<<(v-40)
        pm.append(p);lm.append(q)
    adj=[set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if (pm[i]&pm[j]).bit_count()!=(lm[i]&lm[j]).bit_count():
                adj[i].add(j);adj[j].add(i)
    degree=Counter(map(len,adj))
    assert degree=={324:1620},degree
    rows=[];cols=[]
    for i in range(n):
        rows.extend([i]*len(adj[i]));cols.extend(sorted(adj[i]))
    a=csr_matrix((np.ones(len(rows),dtype=np.int8),(rows,cols)),shape=(n,n))
    assert a.nnz==1620*324
    components,lab=connected_components(a,directed=False)
    # Triangle count in noncommutation graph by edge intersection:
    triangle_six=sum(len(adj[i]&adj[j]) for i in range(n) for j in adj[i])
    assert triangle_six%6==0
    # Each local neighborhood degree of common neighbors (triangle)
    # depends on cycle intersection orbit; measure exact histogram.
    edge_common=Counter()
    for i in range(n):
        for j in adj[i]:
            if i<j:edge_common[len(adj[i]&adj[j])]+=1
    rng=random.Random(20261008)
    candidates=[]
    for iteration in range(180):
        # Randomized smallest-degree induced-subgraph greedy independent set.
        remaining=set(range(n));chosen=[]
        while remaining:
            sampled=sorted(remaining,key=lambda i:(len(adj[i]&remaining),rng.random()))
            v=sampled[0]
            chosen.append(v)
            remaining.difference_update(adj[v]);remaining.discard(v)
        assert all((j not in adj[i]) for k,i in enumerate(chosen) for j in chosen[k+1:])
        candidates.append(chosen)
    best=max(candidates,key=len)
    # Maximality (can't add a missing vertex) distinct from maximum size.
    assert all(any(j in adj[i] for i in best) for j in range(n) if j not in best)
    all_intersection=Counter()
    for x in best:
        for y in best:
            if x>=y:continue
            P=(pm[x]&pm[y]).bit_count();L=(lm[x]&lm[y]).bit_count()
            assert P==L
            all_intersection[f"{P}:{L}"]+=1
    result={
      "vertex_count":n,"noncommuting_graph_degree":324,
      "centralizers_per_C8_other_than_itself":1295,
      "noncommuting_undirected_edges":a.nnz//2,
      "commuting_undirected_edges":n*(n-1)//2-a.nnz//2,
      "connected_components":int(components),
      "edge_common_neighbor_histogram":dict(sorted(edge_common.items())),
      "noncommuting_triangle_count":triangle_six//6,
      "greedy_runs":len(candidates),
      "greedy_atlas_cardinality_histogram":dict(sorted(Counter(map(len,candidates)).items())),
      "largest_found_commuting_atlas_cardinality":len(best),
      "largest_found_cycle_indices":best,
      "largest_found_actual_cycles":[list(c[k]) for k in best],
      "largest_found_pair_overlap_signature":dict(all_intersection),
      "not_proven_optimal":True,
      "degree_324_vs_U81_V4_order324":"exact numerical equality, no group-action identification shown",
      "conclusion":"Provides explicit pairwise-central-commuting subatlas; does not solve higher cocycles or gravitational constraints"
    }
    return result

if __name__=="__main__":
    d=census()
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print({k:v for k,v in d.items() if k not in ("largest_found_cycle_indices","largest_found_actual_cycles","edge_common_neighbor_histogram","greedy_atlas_cardinality_histogram")},flush=True)
    print("CENTER_ATLAS_PASS",flush=True)
