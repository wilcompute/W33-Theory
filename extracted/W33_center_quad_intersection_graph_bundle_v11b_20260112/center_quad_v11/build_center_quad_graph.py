#!/usr/bin/env python3
"""Build the W33 center-quad intersection graph (v11).

Reads:
- W33_N12_58_triad_alignment_bundle_20260112.zip -> inputs/W33_line_phase_map.csv

Writes:
- center_quad_nodes.csv
- center_quad_edges_intersection1.csv
- center_quad_intersection1_graph.gexf
- stats.json
"""
import zipfile, io, json
from itertools import combinations
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx

ztri = Path('/mnt/data/W33_N12_58_triad_alignment_bundle_20260112.zip')
with zipfile.ZipFile(ztri,'r') as zf:
    w33 = pd.read_csv(io.BytesIO(zf.read('inputs/W33_line_phase_map.csv')))

lines=[tuple(map(int,s.split())) for s in w33['point_ids'].astype(str)]
col=[set() for _ in range(40)]
for L in lines:
    for i in range(4):
        for j in range(i+1,4):
            a,b=L[i],L[j]
            col[a].add(b); col[b].add(a)

# enumerate four-center triads and collect center quads
quads=set()
for a,b,c in combinations(range(40),3):
    if (b in col[a]) or (c in col[a]) or (c in col[b]): 
        continue
    C=tuple(sorted(col[a]&col[b]&col[c]))
    if len(C)==4:
        quads.add(C)
quads=sorted(quads)
assert len(quads)==90

quad_sets=[set(C) for C in quads]
hist=Counter()
edges=[]
for i in range(90):
    for j in range(i+1,90):
        inter=len(quad_sets[i]&quad_sets[j])
        hist[inter]+=1
        if inter==1:
            edges.append((i,j))

deg=[0]*90
for u,v in edges:
    deg[u]+=1; deg[v]+=1
assert min(deg)==max(deg)==32

# common neighbors
A=np.zeros((90,90), dtype=np.int8)
for u,v in edges:
    A[u,v]=A[v,u]=1

lam=Counter(); mu=Counter()
for i in range(90):
    for j in range(i+1,90):
        cn=int(np.dot(A[i],A[j]))
        if A[i,j]==1:
            lam[cn]+=1
        else:
            mu[cn]+=1

nodes_df=pd.DataFrame([{'quad_id':i,'quad_points':' '.join(map(str,quads[i]))} for i in range(90)])
nodes_df.to_csv('center_quad_nodes.csv', index=False)
pd.DataFrame([{'u':u,'v':v} for u,v in edges]).to_csv('center_quad_edges_intersection1.csv', index=False)

G=nx.Graph()
for i in range(90):
    G.add_node(i, quad=nodes_df.loc[i,'quad_points'])
for u,v in edges:
    G.add_edge(u,v)
nx.write_gexf(G, 'center_quad_intersection1_graph.gexf')

stats={
    'n_nodes':90,
    'n_edges':len(edges),
    'degree':32,
    'intersection_pair_histogram': {str(k):int(v) for k,v in hist.items()},
    'common_neighbors_adjacent': dict(lam),
    'common_neighbors_nonadjacent_hist': dict(mu),
}
with open('stats.json','w') as f:
    json.dump(stats, f, indent=2)
print('Wrote nodes/edges/gexf/stats')
