#!/usr/bin/env python3
"""BT1732: bounded split-Cayley cocycle search boundary after BT1729."""
from __future__ import annotations
from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1732_girth8_obstruction_search.json'
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
W=[459,595,363,694,87,39,347,839,561]
def systems():
 autos=[]
 for p in permutations(range(7)):
  if {frozenset(p[x] for x in L) for L in BASESETS}==BASESETS: autos.append(p)
 rots=[(0,1,2),(1,2,0),(2,0,1),(0,2,1),(2,1,0),(1,0,2)]
 out=[]
 for p in autos:
  for r in rots:
   sys=[tuple(p[t[i]] for i in r) for t in BASE]
   if all(sorted(t[k] for t in sys)==list(range(7)) for k in range(3)): out.append(sys)
 return out
def hesse_lines():
 H=[]
 for y in range(3): H.append([(x,y) for x in range(3)])
 for x in range(3): H.append([(x,y) for y in range(3)])
 for b in range(3): H.append([(t,(t+b)%3) for t in range(3)])
 return H
def graph(choices=W):
 S=systems(); H=hesse_lines(); G=nx.Graph(); cells=[(x,y) for x in range(3) for y in range(3)]
 G.add_nodes_from(('p',a,h) for a in range(7) for h in cells)
 for hi,hline in enumerate(H):
  sys=S[choices[hi]]
  for ti,tr in enumerate(sys):
   l=('l',hi,ti); G.add_node(l)
   for k in range(3): G.add_edge(('p',tr[k],hline[k]),l)
 return G,len(S)
def girth(G):
 best=10**9
 for s in G.nodes:
  dist={s:0}; par={s:None}; q=[s]
  for v in q:
   for w in G[v]:
    if w not in dist:
     dist[w]=dist[v]+1; par[w]=v; q.append(w)
    elif par[v]!=w and par[w]!=v: best=min(best,dist[v]+dist[w]+1)
 return None if best==10**9 else best
def cycles(G,bound=10):
 D=nx.DiGraph()
 for u,v in G.edges(): D.add_edge(u,v); D.add_edge(v,u)
 seen=set()
 for cyc in nx.simple_cycles(D,length_bound=bound):
  if len(cyc)<3: continue
  n=len(cyc); reps=[]
  for seq in (cyc,list(reversed(cyc))):
   for i in range(n): reps.append(tuple(seq[i:]+seq[:i]))
  seen.add(min(reps,key=str))
 return dict(Counter(map(len,seen)))
def main():
 G,nsys=graph(); cyc=cycles(G,10); g=girth(G)
 checks={'fano_systems_1008':nsys==1008,'connected_cubic':nx.is_connected(G) and set(dict(G.degree()).values())=={3},'counts_63_63_189':sum(1 for n in G if n[0]=='p')==63 and sum(1 for n in G if n[0]=='l')==63 and G.number_of_edges()==189,'girth_8':g==8,'no_4_or_6_cycles':cyc.get(4,0)==0 and cyc.get(6,0)==0,'remaining_8_cycles_54':cyc.get(8,0)==54,'remaining_10_cycles_75':cyc.get(10,0)==75}
 payload={'theorem':'BT1732 split-Cayley girth-8 obstruction search boundary','verified':all(checks.values()),'summary':'The best stored cocycle witness remains a connected cubic 63/63/189 graph with girth 8. It has zero 4-cycles, zero 6-cycles, exactly 54 8-cycles and 75 10-cycles under the bounded cycle census. This records the obstruction layer the next search must eliminate.','witness':W,'profile':{'girth':g,'diameter':nx.diameter(G),'cycle_counts_le_10':cyc,'components':nx.number_connected_components(G),'cycle_rank':G.number_of_edges()-G.number_of_nodes()+1},'next_search_contract':['preserve 63 points, 63 lines, 189 incidences','preserve cubic incidence','preserve connectedness','preserve no 4/6 cycles','eliminate 54 eight-cycles before targeting the 75 ten-cycles'],'checks':checks,'boundary':'This is a verified boundary and search contract, not a claim that girth 12 has been found.'}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
 print(json.dumps({'verified':payload['verified'],'girth':g,'cycles':cyc},indent=2))
 return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
