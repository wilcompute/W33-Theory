#!/usr/bin/env python3
"""BT1729: Hesse/Fano cocycle search reaches girth 8 boundary.

This improves BT1725.  The fixed witness choices were found by a deterministic
seeded local search over oriented Fano systems on the 9 selected Hesse lines.
It connects the nine product components, preserves cubic 63/63/189 incidence,
eliminates all 4- and 6-cycles, and reaches girth 8.  Therefore the remaining
split-Cayley obstruction is exactly the 8/10-cycle layer.
"""
from __future__ import annotations
from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1729_hesse_fano_girth8_cocycle.json'
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
WITNESS=[459,595,363,694,87,39,347,839,561]
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
def product_graph():
 H=[(x,y) for x in range(3) for y in range(3)]
 G=nx.Graph(); G.add_nodes_from(('p',a,h) for a in range(7) for h in H)
 for h in H:
  for i,tr in enumerate(BASE):
   l=('l',h,i); G.add_node(l)
   for a in tr: G.add_edge(('p',a,h),l)
 return G
def twist_graph(choices=WITNESS):
 S=systems(); H=hesse_lines(); G=nx.Graph(); G.add_nodes_from(('p',a,h) for a in range(7) for h in [(x,y) for x in range(3) for y in range(3)])
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
    elif par[v]!=w and par[w]!=v:
     best=min(best,dist[v]+dist[w]+1)
 return None if best==10**9 else best
def cycle_counts(G,bound=10):
 D=nx.DiGraph()
 for u,v in G.edges(): D.add_edge(u,v); D.add_edge(v,u)
 seen=set()
 for cyc in nx.simple_cycles(D,length_bound=bound):
  if len(cyc)<3: continue
  n=len(cyc); rots=[]
  for seq in (cyc,list(reversed(cyc))):
   for i in range(n): rots.append(tuple(seq[i:]+seq[:i]))
  seen.add(min(rots,key=str))
 return {str(k):v for k,v in sorted(Counter(map(len,seen)).items())}
def main():
 P=product_graph(); T,nsys=twist_graph(); cyc=cycle_counts(T,10)
 checks={'oriented_fano_systems_1008':nsys==1008,'product_components_9':nx.number_connected_components(P)==9,'twist_connected':nx.is_connected(T),'twist_counts_63_63_189':sum(1 for n in T if n[0]=='p')==63 and sum(1 for n in T if n[0]=='l')==63 and T.number_of_edges()==189,'twist_cubic':set(dict(T.degree()).values())=={3},'girth_reaches_8':girth(T)==8,'no_4_or_6_cycles':cyc.get('4',0)==0 and cyc.get('6',0)==0,'remaining_8_and_10_cycles':cyc.get('8',0)>0 and cyc.get('10',0)>0}
 payload={'theorem':'BT1729 Hesse-Fano girth-8 cocycle boundary','verified':all(checks.values()),'summary':'A deterministic Hesse/Fano cocycle witness improves the BT1725 boundary: it connects the nine disconnected Fano components, preserves the cubic 63-point/63-line/189-incidence profile, eliminates all 4- and 6-cycles, and reaches girth 8. The remaining split-Cayley obstruction is now the 8/10-cycle layer.','witness_choices':WITNESS,'product':{'components':nx.number_connected_components(P),'component_sizes':sorted(len(c) for c in nx.connected_components(P))},'twist':{'components':nx.number_connected_components(T),'diameter':nx.diameter(T),'girth':girth(T),'cycle_counts_le_10':cyc,'cycle_rank':T.number_of_edges()-T.number_of_nodes()+nx.number_connected_components(T)},'checks':checks,'boundary':'This is not yet the split-Cayley hexagon: girth is 8, not 12. It is a strictly stronger cocycle waypoint than BT1725.'}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
 print(json.dumps({'verified':payload['verified'],'girth':payload['twist']['girth'],'cycles':cyc},indent=2))
 return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
