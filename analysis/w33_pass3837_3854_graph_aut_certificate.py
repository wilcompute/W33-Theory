#!/usr/bin/env python3
"""Standalone exact graph-automorphism certificate for Passes 3837-3854."""
from __future__ import annotations
import argparse,json
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name=='analysis' else Path(__file__).resolve().parent
DEFAULT=ROOT/'data'/'PART_3837_3854_GRAPH_AUT_CERTIFICATE.json'

def bits(x):return tuple((x>>i)&1 for i in range(6))
def quadratic(x):
 a=bits(x);return (a[0]*a[1]+a[2]*a[3]+a[4]+a[4]*a[5]+a[5])&1
def polar(x,y):
 a,b=bits(x),bits(y);return (a[0]*b[1]+a[1]*b[0]+a[2]*b[3]+a[3]*b[2]+a[4]*b[5]+a[5]*b[4])&1
def rooted_count(A,root=0):
 G=nx.from_numpy_array(np.asarray(A,dtype=np.uint8));H=G.copy()
 nx.set_node_attributes(G,{i:int(i==root) for i in G},'root');nx.set_node_attributes(H,{i:int(i==root) for i in H},'root')
 return sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,H,node_match=lambda x,y:x['root']==y['root']).isomorphisms_iter())
def digest(A):return sha256(np.asarray(A,dtype=np.uint8).tobytes()).hexdigest()
def build():
 singular=tuple(x for x in range(1,64) if quadratic(x)==0);ss=set(singular)
 lines=sorted({tuple(sorted((x,y,x^y))) for x,y in combinations(singular,2) if x^y in ss and polar(x,y)==0})
 assert len(lines)==45
 A45=np.zeros((45,45),dtype=np.uint8)
 for i,j in combinations(range(45),2):
  if set(lines[i]).intersection(lines[j]):A45[i,j]=A45[j,i]=1
 payload=json.loads((ROOT/'data'/'PART_3837_3854_DOUBLE_K4_INCIDENCE.json').read_text())
 B=np.asarray(payload['incidence'],dtype=np.int64)
 assert sha256(B.astype(np.uint8).tobytes()).hexdigest()==payload['incidence_sha256']
 row=B@B.T-4*np.eye(40,dtype=np.int64);col=B.T@B-4*np.eye(40,dtype=np.int64)
 r45=rooted_count(A45);rr=rooted_count(row);rc=rooted_count(col);iso=nx.is_isomorphic(nx.from_numpy_array(row),nx.from_numpy_array(col))
 assert (r45,rr,rc,iso)==(1152,1296,1296,False)
 result={'schema':'w33.pass3837_3854.graph_aut_certificate.v1','gq45_adjacency_sha256':digest(A45),'gq45_rooted_automorphisms':r45,'gq45_full_automorphism_order':45*r45,'row40_adjacency_sha256':digest(row),'column40_adjacency_sha256':digest(col),'row40_rooted_automorphisms':rr,'column40_rooted_automorphisms':rc,'row40_full_automorphism_order':40*rr,'column40_full_automorphism_order':40*rc,'row_column_isomorphic':iso,'verdict':'PASS_EXACT_GRAPH_AUTOMORPHISM_AND_NONSIMILAR_DUAL_CERTIFICATE'}
 result['semantic_sha256']=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest();return result
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=DEFAULT);a=ap.parse_args();r=build();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('PASS_3837_3854_GRAPH_AUT',r['semantic_sha256'])
if __name__=='__main__':main()
