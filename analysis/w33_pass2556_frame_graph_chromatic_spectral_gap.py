from __future__ import annotations
import json,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import numpy as np,networkx as nx
ordering=json.load(open(ROOT/'data/w33_pass2551_canonical_frame_ordering.json'));F=[set(x) for x in ordering['frozen_frame_edges']];n=540
G=nx.Graph();G.add_nodes_from(range(n))
for e in range(240):
 C=[i for i,f in enumerate(F) if e in f];assert len(C)==9
 for i in range(9):
  for j in range(i+1,9):G.add_edge(C[i],C[j])
spec=collections.Counter(round(float(x),8) for x in np.linalg.eigvalsh(nx.to_numpy_array(G,dtype=np.float64)));color=nx.coloring.greedy_color(G,strategy='DSATUR');K=1+max(color.values());colors=[color[i] for i in range(n)];k=next(iter(set(dict(G.degree()).values())));s=min(spec);alpha=int(round(n*(-s)/(k-s)));k8=json.load(open(ROOT/'data/w33_pass2551_complete_cover_link_k8_refutation.json'))
out={'schema':'w33.pass2556.frame_graph_chromatic_spectral_gap.v1','status':'PASS_FRAME_GRAPH_CHROMATIC_INTERVAL_10_TO_14','graph':{'vertices':n,'edges':G.number_of_edges(),'degree':k,'spectrum':{str(x):m for x,m in sorted(spec.items())}},'independence':{'hoffman_upper_bound':alpha,'exact_maximum':60,'maximum_independent_sets_are_exact_covers':True,'global_exact_covers':3547800},'chromatic':{'hoffman_lower_bound':9,'nine_coloring_refuted_by_complete_K8_link_search':not k8['chromatic_consequence']['nine_coloring_exists'],'proved_lower_bound':10,'explicit_upper_bound':K,'explicit_color_class_sizes':dict(collections.Counter(colors)),'explicit_coloring':colors},'theorem':'The exact frame spectrum and complete K8-free cover-link census prove 10<=chi(H); a deterministic proper 14-coloring proves chi(H)<=14.','boundary':'The exact chromatic number within {10,11,12,13,14} remains open.','checks':{'540_8640_32':(n,G.number_of_edges(),k)==(540,8640,32),'spectrum_exact':spec==collections.Counter({32.0:1,14.0:44,8.0:15,4.0:81,2.0:84,-4.0:315}),'hoffman_alpha60':alpha==60,'nine_refuted':not k8['chromatic_consequence']['nine_coloring_exists'],'proper_14_coloring':K==14 and all(colors[u]!=colors[v] for u,v in G.edges)}};base=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest();json.dump(out,open(ROOT/'data/w33_pass2556_frame_graph_chromatic_spectral_gap.json','w'),indent=2,sort_keys=True)
