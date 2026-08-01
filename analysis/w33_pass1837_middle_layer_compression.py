#!/usr/bin/env python3
"""Pass 1837: exact partial-spread/duad compression of the 45-octet graph."""
from __future__ import annotations
import collections, hashlib, json
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys_path=str(ROOT/'analysis')
import sys
sys.path.insert(0,sys_path)
from w33_pass1801_1805_common import build_geometry
d0=build_geometry();octets=d0['octets'];A=np.zeros((45,45),dtype=np.int8)
for i in range(45):
 si=set(octets[i][0])|set(octets[i][1])
 for j in range(i+1,45):
  sj=set(octets[j][0])|set(octets[j][1])
  if len(si&sj)==2:A[i,j]=A[j,i]=1
C=1-np.eye(45,dtype=np.int8)-A
OUT=ROOT/'data'/'w33_pass1837_middle_layer_compression.json'
G=nx.from_numpy_array(C)
lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==5)
assert len(lines)==27
L=nx.Graph();L.add_nodes_from(range(27))
for i in range(27):
 for j in range(i+1,27):
  if set(lines[i]).isdisjoint(lines[j]):L.add_edge(i,j)
maximal=[tuple(sorted(c)) for c in nx.find_cliques(L)]
omega=max(map(len,maximal));packs=sorted(c for c in maximal if len(c)==omega)
assert omega==6 and len(packs)==72
inc=collections.Counter(i for p in packs for i in p);assert set(inc.values())=={16}
pack=[lines[i] for i in packs[0]]
covered=set().union(*(set(x) for x in pack));residual=sorted(set(range(45))-covered)
R=G.subgraph(residual).copy();deg=sorted(dict(R.degree()).values())
assert len(residual)==15 and set(deg)=={6} and R.number_of_edges()==45
RA=nx.to_numpy_array(R,nodelist=residual,dtype=int)
assert set((RA@RA)[np.triu_indices(15,1)][RA[np.triu_indices(15,1)]==1])=={1}
assert set((RA@RA)[np.triu_indices(15,1)][RA[np.triu_indices(15,1)]==0])=={3}
duads=list(__import__('itertools').combinations(range(6),2));KG=nx.Graph();KG.add_nodes_from(range(15))
for i in range(15):
 for j in range(i+1,15):
  if set(duads[i]).isdisjoint(duads[j]):KG.add_edge(i,j)
iso=nx.algorithms.isomorphism.GraphMatcher(R,KG);assert iso.is_isomorphic();mapping=iso.mapping
pair_matchings=[]
for i in range(6):
 for j in range(i+1,6):
  edges=[(u,v) for u in pack[i] for v in pack[j] if C[u,v]]
  assert len(edges)==5 and len({u for u,v in edges})==5 and len({v for u,v in edges})==5
  pair_matchings.append({'i':i,'j':j,'matching':[list(x) for x in sorted(edges)]})
line_residual=[]
for i,line in enumerate(pack):
 sparse_degrees_res=[sum(C[v,u] for u in line) for v in residual]
 sparse_degrees_line=[sum(C[v,u] for u in residual) for v in line]
 assert set(sparse_degrees_res)=={1} and set(sparse_degrees_line)=={3}
 line_residual.append({'line':i,'residual_to_line_degree':1,'line_to_residual_degree':3})
eigs=np.linalg.eigvalsh(RA);spec=collections.Counter(int(round(x)) for x in eigs)
out={
 'schema':'w33.pass1837.middle_layer_compression.v1','status':'PASS',
 'dense_octet_graph':[45,32,22,24],'sparse_complement_graph':[45,12,3,3],
 'five_clique_lines':27,'nine_line_spread_exists':False,'maximum_disjoint_lines':omega,
 'maximum_partial_spreads':len(packs),'partial_spreads_per_line':16,
 'canonical_six_line_pack':[list(x) for x in pack],'covered_vertices':30,'residual_vertices':residual,
 'residual_srg':[15,6,1,3],'residual_spectrum':{str(k):v for k,v in sorted(spec.items())},
 'residual_is_KG_6_2':True,'residual_to_duad_index':{str(k):int(v) for k,v in sorted(mapping.items())},
 'line_pair_perfect_matchings':pair_matchings,'line_residual_biregularity':line_residual,
 'compression':'The 45 coordinates split as six 5-point GQ lines plus a 15-point KG(6,2) duad residual. Between line fibers the sparse graph is a perfect matching; between each line and the residual it is (3,1)-biregular.',
 'boundary':'This exact 6x5+15 decomposition replaces the false 9x5 spread ansatz. It supplies a separator/gain-graph architecture but does not by itself complete the middle-layer weight enumerator.'
}
raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();out['sha256']=hashlib.sha256(raw).hexdigest()
OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps({'status':'PASS','omega':omega,'packings':len(packs),'residual':'SRG(15,6,1,3)=KG(6,2)','sha256':out['sha256']},indent=2))
