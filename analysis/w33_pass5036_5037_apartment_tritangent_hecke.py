#!/usr/bin/env python3
"""Pass5036-5037: labeled apartment/tritangent transport and eight FF orbitals."""
from __future__ import annotations
import itertools, json
from collections import defaultdict, deque, Counter
from pathlib import Path
import numpy as np
import networkx as nx
from analysis.w33_pass4992_4999_common import build_base, build_group, closure
ROOT=Path(__file__).resolve().parents[1]
O36=ROOT/'data/PART_W33_PASS5036_APARTMENT_TRITANGENT_TRANSPORT.json'
O37=ROOT/'data/PART_W33_PASS5037_STEINBERG_EIGHT_FF_ORBITALS.json'
def main():
 b=build_base();T=b['tritangents'];M=b['M'].astype(int);W=b['W'];L=b['L']
 AT=nx.Graph();AT.add_nodes_from(range(45))
 for i,j in itertools.combinations(range(45),2):
  if len(set(T[i])&set(T[j]))==1:AT.add_edge(i,j)
 indep=[frozenset(s) for s in itertools.combinations(range(45),3) if all(not AT.has_edge(*e) for e in itertools.combinations(s,2))]
 circuits={}
 for A in indep:
  common=set(range(45))
  for a in A:common&=set(AT.neighbors(a))
  for z in itertools.combinations(sorted(common-A),3):
   B=frozenset(z)
   if all(not AT.has_edge(*e) for e in itertools.combinations(B,2)):
    key=tuple(sorted((tuple(sorted(A)),tuple(sorted(B)))));circuits[key]=(A,B)
 assert len(circuits)==120
 steiner={tuple(sorted(s)):s for s in b['steiner']};iso=b['iso_ds_sp'];spreads=b['spreads'];line_to_circuits=defaultdict(list)
 for key,(A,B) in circuits.items():
  six=sorted(A|B);missed=tuple(sorted(d for d in range(36) if all(M[t,d]==0 for t in six)));assert missed in steiner
  common=set(range(40))
  for d in missed:common&=set(spreads[iso[d]])
  assert len(common)==1;line_to_circuits[next(iter(common))].append((A,B))
 assert all(len(line_to_circuits[l])==3 for l in range(40))
 cover_lines=defaultdict(set);opposite={}
 for l in range(40):
  cs=line_to_circuits[l];bybits={}
  for bits in itertools.product((0,1),repeat=3):
   S=frozenset().union(*(cs[i][bits[i]] for i in range(3)));assert len(S)==9;bybits[bits]=tuple(sorted(S));cover_lines[tuple(sorted(S))].add(l)
  for bits,C in bybits.items():opposite[(l,C)]=bybits[tuple(1-x for x in bits)]
 assert len(cover_lines)==200 and Counter(len(v) for v in cover_lines.values())==Counter({1:160,4:40})
 special={}
 for C,ls in cover_lines.items():
  if len(ls)==4:
   pts=set(range(40))
   for l in ls:pts&=set(L[l])
   assert len(pts)==1;special[C]=next(iter(pts))
 point_cover={p:C for C,p in special.items()};assert len(point_cover)==40
 flag_cover={}
 for C,ls in cover_lines.items():
  if len(ls)==1:
   l=next(iter(ls));op=opposite[(l,C)];assert op in special;p=special[op];assert p in L[l];flag_cover[(p,l)]=C
 flags=[(p,l) for l,Q in enumerate(L) for p in Q];assert len(flag_cover)==len(flags)==160
 ordered=[point_cover[p] for p in range(40)]+[flag_cover[f] for f in flags]
 U=np.zeros((200,45),dtype=np.int8)
 for i,C in enumerate(ordered):U[i,list(C)]=1
 assert np.linalg.matrix_rank(U.astype(float))==25 and set(map(int,U.sum(1)))=={9} and set(map(int,U.sum(0)))=={40}
 fi={f:i for i,f in enumerate(flags)};pair_line={}
 for l,Q in enumerate(L):
  for p,q in itertools.combinations(Q,2):pair_line[tuple(sorted((p,q)))]=l
 aps=[c for c in itertools.combinations(range(40),4) if W.subgraph(c).number_of_edges()==4 and set(dict(W.subgraph(c).degree()).values())=={2}];assert len(aps)==1620
 Y=np.zeros((1620,200),dtype=np.int16)
 for k,S in enumerate(aps):
  for p in S:Y[k,p]=1
  for p,q in W.subgraph(S).edges():
   l=pair_line[tuple(sorted((p,q)))];Y[k,40+fi[(p,l)]]=1;Y[k,40+fi[(q,l)]]=1
 Z=Y@U;assert Z.shape==(1620,45) and np.linalg.matrix_rank(Z.astype(float))==25 and set(map(int,Z.sum(1)))=={108} and set(map(int,Z.sum(0)))=={3888}
 G=Z.T@Z;diag=set();adj=set();non=set()
 for i in range(45):
  for j in range(i,45):
   if i==j:diag.add(int(G[i,j]))
   elif AT.has_edge(i,j):adj.add(int(G[i,j]))
   else:non.add(int(G[i,j]))
 assert (diag,adj,non)==({12672},{8496},{9540})
 Atr=nx.to_numpy_array(AT,nodelist=range(45),dtype=int);assert np.array_equal(G,3132*np.eye(45,dtype=int)-1044*Atr+9540*np.ones((45,45),dtype=int))
 ev=np.linalg.eigvalsh(G.astype(float));assert sum(np.isclose(ev,0,atol=1e-6))==20 and sum(np.isclose(ev,6264,atol=1e-6))==24 and sum(np.isclose(ev,419904,atol=1e-6))==1
 gg=build_group(b);P=closure(gg['LpP'],40);assert len(P)==25920
 line_index={frozenset(Q):l for l,Q in enumerate(L)}
 def lf(g,l):return line_index[frozenset(g[x] for x in L[l])]
 def ff(g,i):
  p,l=flags[i];return fi[(g[p],lf(g,l))]
 base=0;H=[g for g in P if ff(g,base)==base];assert len(H)==162
 unseen=set(range(160));orbs=[]
 while unseen:
  i=min(unseen);O={ff(g,i) for g in H};unseen-=O;orbs.append(sorted(O))
 Aflag=[[] for _ in flags]
 for i,(p,l) in enumerate(flags):
  for j,(q,m) in enumerate(flags):
   if i!=j and (p==q or l==m):Aflag[i].append(j)
 d=[-1]*160;d[base]=0;Qd=deque([base])
 while Qd:
  u=Qd.popleft()
  for v in Aflag[u]:
   if d[v]<0:d[v]=d[u]+1;Qd.append(v)
 cells=sorted((d[O[0]],len(O)) for O in orbs);assert cells==[(0,1),(1,3),(1,3),(2,9),(2,9),(3,27),(3,27),(4,81)]
 coeff=[(-1)**ell*3**(4-ell) for ell,n in cells];assert coeff==[81,-27,-27,9,9,-3,-3,1]
 out36={'pass':5036,'status':'PASS','U':[200,45],'rank_U':25,'Z':[1620,45],'rank_Z':25,'Z_row_sum':108,'Z_col_sum':3888,'gram':'3132 I - 1044 A_trit + 9540 J','squared_singular_spectrum':{'419904':1,'6264':24,'0':20},'image':'1+V24','V20_annihilated':True}
 out37={'pass':5037,'status':'PASS','FF_orbitals':8,'cells':[list(x) for x in cells],'coefficients':coeff,'formula':'(-1)^ell 3^(4-ell)','rank':81}
 O36.write_text(json.dumps(out36,indent=2)+'\n');O37.write_text(json.dumps(out37,indent=2)+'\n');print(json.dumps({'5036':out36,'5037':out37},indent=2))
if __name__=='__main__':main()
