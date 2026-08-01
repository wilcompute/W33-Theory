#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,importlib.util
from collections import Counter,deque
from itertools import combinations
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/w33_pass1950_u6_collision_graph.txt'
OUT=ROOT/'data/w33_pass1950_u6_collision_graph_compression.json'
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'
def canon(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_common():
 s=importlib.util.spec_from_file_location('c',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def main():
 L=RAW.read_text().splitlines();i=L.index('VERTICES')+1;j=L.index('EDGES')
 V=[tuple(map(int,x.split())) for x in L[i:j]];E=[tuple(map(int,x.split())) for x in L[j+1:]]
 G=nx.Graph()
 for s,a,b,rec,un,dg,de,dd in V:G.add_node(s,label=(rec,un,dg,de,dd),pair=(a,b))
 for a,b,sg,ce,ds in E:G.add_edge(a,b,label=(sg,ce,ds))
 nm=nx.algorithms.isomorphism.categorical_node_match('label',None);em=nx.algorithms.isomorphism.categorical_edge_match('label',None)
 aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=nm,edge_match=em).isomorphisms_iter())
 c=load_common();D=c.build_geometry()
 def compose(p,q):return tuple(p[q[k]] for k in range(len(q)))
 idp=tuple(range(40));seen={idp:tuple(range(240))};q=deque([idp])
 while q:
  pp=q.popleft();ep=seen[pp]
  for gp,ge,*_ in D['acts']+[D['outer']]:
   np=compose(gp,pp)
   if np not in seen:seen[np]=tuple(ge[ep[k]] for k in range(240));q.append(np)
 stab=[ep for ep in seen.values() if ep[0]==0]
 pairs=set(combinations(range(1,240),2));os=[]
 while pairs:
  x=min(pairs);o={tuple(sorted((ep[x[0]],ep[x[1]]))) for ep in stab};pairs-=o;os.append(len(o))
 checks={'vertices28':len(V)==28,'complete378':len(E)==378,'cross_edges':sum(x[3] for x in E)==5_389_182,'shared_groups':sum(x[2] for x in E)==3_163_606,'labels125':len(set(x[2:5] for x in E))==125,'weighted_graph_rigid':aut==1,'edge_stabilizer216':len(stab)==216,'pair_orbits230':len(os)==230}
 out={'schema':'w33.pass1950.u6_collision_graph_compression.v1','status':'PASS_WITH_GLOBAL_U6_BOUNDARY','checks':checks,'numeric_supershard_graph':{'vertices':28,'edges':378,'complete':True,'shared_syndrome_group_pair_incidences':sum(x[2] for x in E),'cross_collision_edges':sum(x[3] for x in E),'unique_edge_weight_labels':len(set(x[2:5] for x in E)),'automorphism_group_order':aut,'raw_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest()},'symmetry_invariant_pair_charts':{'fixed_edge_stabilizer_order':len(stab),'unordered_pairs':238*239//2,'orbits':len(os),'orbit_size_distribution':{str(k):v for k,v in sorted(Counter(os).items())}},'theorem':'The 28-shard numeric-minimum collision graph is complete, has 125 distinct edge labels, and is rigid. The fixed-edge geometric stabilizer has 230 orbits on all pair charts, so the current ordering-based partition admits no meaningful orbit compression; a different global deduplication architecture is required.','boundary':'No global U6 coefficient is claimed. The 230 orbit count concerns overlapping pair charts, not a disjoint global partition.'}
 assert all(checks.values());out['sha256_without_hash_field']=canon(out);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sha':out['sha256_without_hash_field'],'checks':checks},indent=2));return out
if __name__=='__main__':main()
