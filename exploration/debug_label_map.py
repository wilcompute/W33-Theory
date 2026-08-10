import json
from pathlib import Path
import networkx as nx

ROOT=Path('c:/Repos/Theory of Everything')
edge_to_root = json.loads((ROOT/'artifacts'/'edge_to_e8_root.json').read_text(encoding="utf-8"))
edges=[]
for k,v in edge_to_root.items():
    i,j=[int(x.strip()) for x in k.strip()[1:-1].split(',')]
    if i<j: edges.append((i,j))

build_w33 = __import__('scripts.e8_embedding_group_theoretic',fromlist=['build_w33']).build_w33
n, vertices, adj_list, _ = build_w33()
G_adj=nx.Graph();G_adj.add_nodes_from(range(40))
for i,nb in enumerate(adj_list):
    for j in nb:
        if i<j: G_adj.add_edge(i,j)

G_root=nx.Graph();G_root.add_nodes_from(range(40))
for i,j in edges:
    if i<j: G_root.add_edge(i,j)

gm=nx.algorithms.isomorphism.GraphMatcher(G_adj,G_root)
label_map=next(gm.isomorphisms_iter())
print('label_map',label_map)

neighbors0=[i for i in range(40) if i in adj_list[0]]
print('adj neighbors0',neighbors0)
print('mapped neighbors0',[label_map[n] for n in neighbors0])

phi_neighbors=[j for (i,j) in edges if i==0] + [i for (i,j) in edges if j==0]
print('phi neighbors0 from edge_to_root',sorted(phi_neighbors))
