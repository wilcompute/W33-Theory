"""Constructive nearest-neighbor 60-edge logical SWAP routing.

Spanning-tree leaf-fixing token swapping guarantees a finite valid schedule
on any connected qubit-coupling graph; tests physically simulate all SWAPs.
Upper bound is a concrete (not optimized) routing schedule.
"""
from pathlib import Path
import sys,json,itertools,collections
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
OUT=ROOT/"data/w33_20261008_20apt_local_SWAP_schedule.json"
def order(p):
 x=list(range(len(p)))
 for n in range(1,10):
  x=[x[p[i]] for i in range(len(p))]
  if x==list(range(len(p))):return n
 raise ValueError
def make():
 V,E,F,stab,H,b1,b2=topology()
 m={v:i for i,v in enumerate(E)}
 g=next(x for x in stab if order(x)==4)
 perm=[m[tuple(sorted((g[u],g[v])))] for u,v in E]
 adj=nx.Graph();adj.add_nodes_from(range(60))
 star=collections.defaultdict(list)
 for j,(u,v) in enumerate(E):star[u].append(j);star[v].append(j)
 for s in star.values():
  for j,k in itertools.combinations(s,2):adj.add_edge(j,k)
 assert nx.is_connected(adj) and set(dict(adj.degree()).values())=={4}
 return adj,perm
def route(adj,perm,root):
 tree=nx.bfs_tree(adj,root).to_undirected()
 tokens=list(range(60))
 source_by_target={target:i for i,target in enumerate(perm)}
 route=[]
 while tree.number_of_nodes()>1:
  leaves=[v for v in tree if v!=root and tree.degree(v)==1]
  leaf=max(leaves,key=lambda v:(nx.shortest_path_length(tree,root,v),-v))
  source=source_by_target[leaf]
  at=tokens.index(source)
  assert at in tree
  path=nx.shortest_path(tree,at,leaf)
  for a,b in zip(path,path[1:]):
   tokens[a],tokens[b]=tokens[b],tokens[a];route.append((a,b))
  assert tokens[leaf]==source
  tree.remove_node(leaf)
 assert all(tokens[perm[source]]==source for source in range(60))
 return route
def main():
 adj,perm=make()
 choices=[(len(route(adj,perm,root)),root) for root in range(60)]
 n,root=min(choices)
 moves=route(adj,perm,root)
 assert len(moves)==n and all(adj.has_edge(*edge) for edge in moves)
 flat=list(range(60))
 last=[0]*60;layers=collections.defaultdict(list)
 for a,b in moves:
  flat[a],flat[b]=flat[b],flat[a]
  lev=max(last[a],last[b])+1
  last[a]=last[b]=lev
  layers[lev].append((a,b))
 assert all(flat[perm[source]]==source for source in range(60))
 assert all(len({x for e in row for x in e})==2*len(row) for row in layers.values())
 dist=dict(nx.all_pairs_shortest_path_length(adj))
 individual=sum(dist[i][perm[i]] for i in range(60))
 assert individual%2==0 and n>=individual//2
 return {"physical_qubits":60,"logical_swap_as_15_disjoint_4cycles":True,
  "unrestricted_transposition_lower_bound":45,
  "nearest_neighbor_total_token_path_length":individual,
  "nearest_neighbor_SWAP_count_lower_bound":individual//2,
  "constructive_nearest_neighbor_SWAP_upper_bound":n,
  "source_BFS_tree_root":root,
  "parallel_disjoint_SWAPS_depth_upper_bound":max(layers),
  "parallel_disjoint_SWAPS_max_layer_size":max(map(len,layers.values())),
  "parallel_disjoint_layers_count":len(layers),
  "explicit_local_SWAP_gates":[list(edge) for edge in moves],
  "verified_physical_permutation_exact":True,
  "not_optimized_or_fault_tolerant":True,
  "application":"Each physical SWAP must still be compiled to native gates; layer depths neglect syndrome interleaving and noise."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in r.items() if k!="explicit_local_SWAP_gates"},flush=True);print("LOCAL_SWAP_SCHEDULE_PASS")
