#!/usr/bin/env python3
"""Sharp 80-edge W33 repair can have height THREE, not just two.

Split one side of the proven equitable max-cut into early and late layers,
while using the opposite side as the middle layer. Every retained edge is
between adjacent layers and hence an irredundant Hasse cover. Count interval
sizes; compare to height-two null and to a 1+1 Minkowski diamond control.
"""
import json
from collections import Counter
from itertools import combinations
from collections import deque
from pathlib import Path
import numpy as np
from toe_20261122_round6_causal_graph_no_go import w33,CUT
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round7_w33_three_layer_hasse.json'

def causal_counts(rel):
   n=len(rel);counts=Counter(); longest=1
   for i in range(n):
    for j in range(n):
     if rel[i,j]:counts[int(np.dot(rel[i].astype(int),rel[:,j].astype(int)))]+=1
   dp=np.ones(n,dtype=int)
   # rel is a transitive DAG with a compatible layer topological order only here;
   # generic longest chain via repeated boolean relations.
   power=rel.copy(); height=1
   for k in range(2,n+1):
    if not power.any():break
    height=k; power=(power.astype(int)@rel.astype(int))>0
   return dict(comparable_pairs=int(rel.sum()),interval_interior_histogram={str(k):v for k,v in sorted(counts.items())},longest_chain=height,ordering_fraction=float(rel.sum()/(n*(n-1)/2)))

def verify():
   pts,edges,T=w33();colors=np.array(CUT);left=np.flatnonzero(colors==0);center=np.flatnonzero(colors==1)
   assert len(left)==len(center)==20
   # Deterministic balanced split of one side of the optimal 20/20 cut.
   early=left[:10];late=left[10:];layer=np.full(40,1,dtype=int);layer[early]=0;layer[late]=2
   assert np.bincount(layer).tolist()==[10,20,10]
   dag=np.zeros((40,40),dtype=bool)
   for i,j in edges:
    if abs(layer[i]-layer[j])==1:
     dag[i,j]=bool(layer[i]<layer[j]);dag[j,i]=bool(layer[j]<layer[i])
   assert int(dag.sum())==160
   # Any two-step reachable pair is from early to late, and has no retained direct edge.
   paths2=dag.astype(int)@dag.astype(int)
   assert np.max(paths2[dag])==0
   reach=dag | (paths2>0)
   assert not (reach & reach.T).any()
   result=causal_counts(reach)
   hist=Counter(int(paths2[i,j]) for i in early for j in late)
   assert result['longest_chain']==3
   # Every Hasse cover is retained; all possible comparabilities come from 1- or 2-step paths.
   assert result['comparable_pairs']==160+int(np.count_nonzero(paths2))
   height2=np.zeros((40,40),dtype=bool)
   for i,j in edges:
    if colors[i]!=colors[j]:
     height2[i,j]=bool(colors[i]==0);height2[j,i]=bool(colors[j]==0)
   null=causal_counts(height2)
   assert null['comparable_pairs']==160 and null['longest_chain']==2
   # Stronger construction: BFS layers of the retained 160-edge bipartite graph.
   # Every edge of a bipartite graph joins adjacent BFS layers. Orient all up.
   adjacency=[set() for _ in range(40)]
   for i,j in edges:
     if colors[i]!=colors[j]:adjacency[i].add(j);adjacency[j].add(i)
   dist={0:0};queue=deque([0])
   while queue:
     p=queue.popleft()
     for q in sorted(adjacency[p]):
       if q not in dist:dist[q]=dist[p]+1;queue.append(q)
   assert len(dist)==40
   assert max(dist.values())==3
   assert sorted(Counter(dist.values()).items())==[(0,1),(1,8),(2,19),(3,12)]
   assert all(abs(dist[i]-dist[j])==1 for i,j in edges if colors[i]!=colors[j])
   four_dag=np.zeros((40,40),dtype=bool)
   for i,j in edges:
     if colors[i]!=colors[j]:
       four_dag[i,j]=bool(dist[i]<dist[j]);four_dag[j,i]=bool(dist[j]<dist[i])
   assert four_dag.sum()==160
   four_square=(four_dag.astype(int)@four_dag.astype(int))
   assert np.max(four_square[four_dag])==0
   reach4=four_dag.copy();step=four_dag.astype(int)
   for _ in range(2,5):
     step=step@four_dag.astype(int)
     reach4|=(step>0)
   four_result=causal_counts(reach4)
   assert four_result['longest_chain']==4
   assert four_result['interval_interior_histogram'].get('0')==160
   rng=np.random.default_rng(20261122)
   uv=rng.random((40,2))
   mink=(uv[:,0,None]<uv[None,:,0]) & (uv[:,1,None]<uv[None,:,1])
   mink_result=causal_counts(mink)
   assert mink_result['longest_chain']>four_result['longest_chain']
   return dict(status='PASS_EXACT_SHARP_W33_80_EDGE_REPAIR_WITH_FOUR_CAUSAL_LAYERS_AND_INTERVALS',
      W33_vertices=40,W33_edges=240,minimum_deleted_edges_proven_prior=80,
      edges_retained_as_Hasse_covers=int(dag.sum()),maxcut_sides_20_20=[left.tolist(),center.tolist()],
      layers_10_20_10=[early.tolist(),center.tolist(),late.tolist()],
      all_retained_edges_are_irredundant_covers=True,
      three_layer_poset=result,
      early_late_pair_path_multiplicity_histogram={str(k):int(v) for k,v in sorted(hist.items())},
      height_two_control=null,
      four_layer_BFS_root=0,
      four_layer_vertex_distribution=[1,8,19,12],
      four_layer_poset=four_result,
      four_layer_Hasse_covers=160,
      seeded_40event_1plus1_Minkowski_diamond_control=mink_result,
      caveat='Height 2, 3 and 4 causal orders all retain the same 160 optimal covers. Neither four finite layers nor nonzero intervals establish manifoldlikeness, Lorentzian dynamics or a continuum. Higher dimensions must be validated against matched random regular graph and 1+1 Minkowski controls.')

if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d)
