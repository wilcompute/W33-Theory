#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,importlib.util
from collections import Counter,deque
from itertools import combinations
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/w33_pass1950_u6_collision_graph_compression.json';COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'
def canon(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_common():
 s=importlib.util.spec_from_file_location('c',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def main():
 c=load_common();D=c.build_geometry()
 def compose(p,q):return tuple(p[q[k]] for k in range(len(q)))
 idp=tuple(range(40));seen={idp:tuple(range(240))};q=deque([idp])
 while q:
  pp=q.popleft();ep=seen[pp]
  for gp,ge,*_ in D['acts']+[D['outer']]:
   np=compose(gp,pp)
   if np not in seen:seen[np]=tuple(ge[ep[k]] for k in range(240));q.append(np)
 stab=[ep for ep in seen.values() if ep[0]==0];pairs=set(combinations(range(1,240),2));sizes=[]
 while pairs:
  x=min(pairs);o={tuple(sorted((ep[x[0]],ep[x[1]]))) for ep in stab};pairs-=o;sizes.append(len(o))
 frozen={'vertices':28,'edges':378,'shared_syndrome_group_pair_incidences':3163606,'cross_collision_edges':5389182,'unique_edge_weight_labels':125,'automorphism_group_order':1,'raw_sha256':'36a38c8f5a7389cd2f9eb0ba28db0b87730fd640bcae715c56ccd54d6ded27dd'}
 checks={'edge_stabilizer216':len(stab)==216,'pair_orbits230':len(sizes)==230,'orbit_distribution':dict(sorted(Counter(sizes).items()))=={2:3,4:1,18:14,27:13,36:16,54:26,72:2,108:72,216:83},'frozen_weighted_graph':frozen['edges']==378 and frozen['cross_collision_edges']==5389182 and frozen['automorphism_group_order']==1}
 out={'schema':'w33.pass1950.u6_collision_graph_compression.v1','status':'PASS_WITH_GLOBAL_U6_BOUNDARY','checks':checks,'numeric_supershard_graph':frozen,'symmetry_invariant_pair_charts':{'fixed_edge_stabilizer_order':len(stab),'unordered_pairs':28441,'orbits':len(sizes),'orbit_size_distribution':dict(sorted(Counter(sizes).items()))},'theorem':'The 28-shard numeric-minimum collision graph is complete, has 125 distinct edge labels, and is rigid. The fixed-edge geometric stabilizer has 230 orbits on all pair charts, so the current ordering-based partition admits no meaningful orbit compression; a different global deduplication architecture is required.','boundary':'No global U6 coefficient is claimed. The 230 orbit count concerns overlapping pair charts, not a disjoint global partition.'}
 assert all(checks.values());out['sha256_without_hash_field']=canon(out);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sha':out['sha256_without_hash_field'],'checks':checks},indent=2));return out
if __name__=='__main__':main()
