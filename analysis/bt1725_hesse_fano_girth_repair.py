#!/usr/bin/env python3
"""BT1725: Hesse/Fano girth-repair boundary for the split-Cayley target."""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1725_hesse_fano_girth_repair.json'
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
CHOICES=[9,941,834,658,135,388,764,575,964]
CELLS=[(x,y) for x in range(3) for y in range(3)]
def systems():
 autos=[]
 for p in itertools.permutations(range(7)):
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
def graph_direct():
 G=nx.Graph(); G.add_nodes_from(('p',a,h) for a in range(7) for h in CELLS)
 for h in CELLS:
  for i,t in enumerate(BASE):
   l=('l',h,i); G.add_node(l)
   for a in t: G.add_edge(('p',a,h),l)
 return G
def graph_twist():
 S=systems(); H=hesse_lines(); G=nx.Graph(); G.add_nodes_from(('p',a,h) for a in range(7) for h in CELLS)
 for hi,hline in enumerate(H):
  sys=S[CHOICES[hi]]
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
def four_cycles(G):
 pts=[n for n in G if n[0]=='p']; total=0; bad=0
 for a,b in itertools.combinations(pts,2):
  c=len(set(G.neighbors(a))&set(G.neighbors(b)))
  if c>=2: bad+=1; total+=math.comb(c,2)
 return total,bad
def main():
 D=graph_direct(); T,nsys=graph_twist(); g=girth(T); c4,bad=four_cycles(T)
 checks={'oriented_fano_systems_1008':nsys==1008,'direct_product_nine_components':nx.number_connected_components(D)==9,'twist_connected':nx.is_connected(T),'twist_63_points_63_lines_189_edges':sum(1 for n in T if n[0]=='p')==63 and sum(1 for n in T if n[0]=='l')==63 and T.number_of_edges()==189,'twist_3_regular':set(dict(T.degree()).values())=={3},'twist_kills_4_cycles':c4==0 and bad==0,'twist_still_has_6_cycles':g==6,'split_cayley_requires_girth_12':g<12}
 payload={'theorem':'BT1725 Hesse-Fano girth-repair boundary','verified':all(checks.values()),'summary':'The Hesse/Fano monodromy twist repairs the nine disconnected Fano components into one connected 3-regular 63/63/189 incidence graph and kills all 4-cycles, but girth remains 6. Thus the next cocycle must preserve connectivity and 4-cycle-freeness while eliminating 6,8,10-cycles to reach the split-Cayley girth-12 target.','direct_product':{'components':nx.number_connected_components(D),'component_sizes':sorted(len(c) for c in nx.connected_components(D))},'twist':{'components':nx.number_connected_components(T),'diameter':nx.diameter(T),'girth':g,'four_cycles':c4,'cycle_rank':T.number_of_edges()-T.number_of_nodes()+nx.number_connected_components(T),'choices':CHOICES},'checks':checks,'boundary':'This is an upgrade from disconnected to connected and 4-cycle-free. It is not yet the split-Cayley hexagon because girth is 6 rather than 12.'}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
 print(json.dumps({'verified':payload['verified'],'girth':g,'four_cycles':c4,'diameter':payload['twist']['diameter']},indent=2))
 return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
