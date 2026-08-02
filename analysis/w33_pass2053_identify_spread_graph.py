#!/usr/bin/env python3
"""Literal identification of the 36-spread graph as NO_6^-(2)."""
from __future__ import annotations
import itertools,hashlib,json,math
from pathlib import Path
from collections import Counter
import numpy as np
import networkx as nx
from w33_pass1060_1064_core import build_w33

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2053_exact_spread_graph_identification.json'
EXPECTED='2f92d0f61995a4355167902fef4ae30da2e3ecf7758a9047ae3e9e1b1c3cd6d7'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def all_spreads(lines,npts=40):
 onpt=[[i for i,L in enumerate(lines) if p in L] for p in range(npts)];out=[]
 def rec(ch,used):
  if len(used)==npts:out.append(tuple(sorted(ch)));return
  p=next(x for x in range(npts) if x not in used)
  for li in onpt[p]:
   if set(lines[li])&used:continue
   rec(ch+[li],used|set(lines[li]))
 rec([],set());return sorted(set(out))
def rank_mod(M,p):
 a=[[int(x)%p for x in row] for row in M.tolist()];m=len(a);n=len(a[0]);r=0
 for c in range(n):
  k=next((i for i in range(r,m) if a[i][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];inv=pow(a[r][c],-1,p);a[r]=[(x*inv)%p for x in a[r]]
  for i in range(m):
   if i!=r and a[i][c]:
    f=a[i][c];a[i]=[(x-f*y)%p for x,y in zip(a[i],a[r])]
  r+=1
 return r

def main():
 w=build_w33();S=all_spreads(w.lines);assert len(S)==36
 A=np.zeros((36,36),dtype=np.uint8)
 for i,j in itertools.combinations(range(36),2):
  if len(set(S[i])&set(S[j]))==4:A[i,j]=A[j,i]=1
 assert set(map(int,A.sum(1)))=={15}
 AA=A.astype(np.int64)@A.astype(np.int64)
 assert np.array_equal(AA,9*np.eye(36,dtype=np.int64)+6*np.ones((36,36),dtype=np.int64))
 h=hashlib.sha256(A.tobytes()).hexdigest();assert h=='ef8c7005329511cfbe4f23b5cfc327b17f9779d75eecfdb936baa63c34199345'
 G=nx.from_numpy_array(A);base=0;N=sorted(G.neighbors(base));M=sorted(set(G)-{base}-set(N))
 local=G.subgraph(N);second=G.subgraph(M)
 pairs=list(itertools.combinations(range(6),2));K=nx.Graph();K.add_nodes_from(pairs)
 K.add_edges_from((a,b) for a,b in itertools.combinations(pairs,2) if set(a).isdisjoint(b))
 triples=list(itertools.combinations(range(6),3));J=nx.Graph();J.add_nodes_from(triples)
 J.add_edges_from((a,b) for a,b in itertools.combinations(triples,2) if len(set(a)&set(b))==2)
 assert nx.is_isomorphic(local,K) and nx.is_isomorphic(second,J)
 tri=int(np.trace(A.astype(np.int64)@A.astype(np.int64)@A.astype(np.int64))//6)
 common=AA;four=sum(math.comb(int(common[i,j]),2) for i in range(36) for j in range(i+1,36))//2
 ranks={str(p):rank_mod(A,p) for p in (2,3,5,7)}
 cert=json.loads(CERT.read_text());assert cert['sha256_without_hash_field']==EXPECTED==digest(cert)
 assert tri==540 and four==4725 and ranks=={'2':36,'3':15,'5':35,'7':36}
 out={'status':'PASS','identification':'NO_6^-(2) = NO_5^{-perp}(3)',
      'adjacency_sha256':h,'local':'Kneser K(6,2)','second':'Johnson J(6,3)',
      'triangles':tri,'four_cycles':four,'modular_ranks':ranks,'certificate':EXPECTED}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
