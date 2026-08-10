import json,pathlib
import networkx as nx

ROOT=pathlib.Path('c:/Repos/Theory of Everything')
# reuse code from driver to rebuild cycles quickly

# load adjacency
lines=[l.strip() for l in (ROOT/'W33_adjacency_matrix.txt').read_text(encoding="utf-8").splitlines() if l.strip()]
adj={i:[j for j,v in enumerate(line.split()) if v=='1'] for i,line in enumerate(lines)}
G=nx.Graph()
G.add_nodes_from(range(40))
for i in range(40):
    for j in adj[i]:
        if i<j: G.add_edge(i,j)

# read p_line etc from output JSON maybe not needed
# replicate earlier cycle building to examine structure

# we can call outer_twist_rootword_cocycle_defect to build cycle_list but easier to replicate portion

from collections import deque

# compute Tx,Ty only by reusing enumeration from prior script? easier: import function? maybe just read from previous run if stored? Not stored.
# Instead skip computing Tx,Ty and take cycle_list from earlier output? The JSON output did not store cycles. Let's modify script to store cycles for inspection next time.

print('No cycles stored, cannot inspect here')
