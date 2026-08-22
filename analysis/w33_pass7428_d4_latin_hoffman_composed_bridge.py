#!/usr/bin/env python3
"""Pass7428: compose the new D4 16-A2 rook geometry with the exact Pass5300 Hoffman/Latin bridge.

No q=5 Hoffman search is repeated here.  Pass5300 already certified H/Z(H) ~= L+,
where L+ is the even-parastrophe subgroup of the Klein V4 Latin autoparatopy group.
This pass supplies the previously missing E8/D4 degree-16 carrier: the Klein cell
'different row, column and symbol' graph is explicitly conjugate to the D4 A2
root-disjointness graph L_2(4).
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7428_D4_LATIN_HOFFMAN_COMPOSED_BRIDGE.json'

def neg(v):return tuple(-x for x in v)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def d4graph():
 R=[]
 for i,j in itertools.combinations(range(4),2):
  for a in (1,-1):
   for b in (1,-1):
    v=[0]*4;v[i]=a;v[j]=b;R.append(tuple(v))
 R=sorted(set(R));RS=set(R);A=set()
 for a,b in itertools.combinations(R,2):
  if dot(a,b)!=-1:continue
  c=tuple(a[i]+b[i] for i in range(4))
  if c in RS:A.add(frozenset((a,neg(a),b,neg(b),c,neg(c))))
 A=sorted(A,key=lambda x:tuple(sorted(x)));G=nx.Graph();G.add_nodes_from(range(16))
 for i,j in itertools.combinations(range(16),2):
  if not(A[i]&A[j]):G.add_edge(i,j)
 return G,A
def v4graph():
 cells=[(r,c,r^c) for r in range(4) for c in range(4)];G=nx.Graph();G.add_nodes_from(range(16))
 for i,j in itertools.combinations(range(16),2):
  if all(cells[i][k]!=cells[j][k] for k in range(3)):G.add_edge(i,j)
 return G,cells
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1

def latin_autoparatopies(cells):
 S4=list(itertools.permutations(range(4)));S3=list(itertools.permutations(range(3)));allp=set();even=set()
 for pi in S3:
  for a in S4:
   for b in S4:
    mp={};cell=[0]*16;ok=True
    for r in range(4):
     for c in range(4):
      old=(r,c,r^c);R=a[old[pi[0]]];C=b[old[pi[1]]];t=old[pi[2]];s=R^C
      if t in mp and mp[t]!=s:ok=False;break
      mp[t]=s;cell[4*r+c]=4*R+C
     if not ok:break
    if ok and len(mp)==4 and len(set(mp.values()))==4:
     q=tuple(cell);allp.add(q)
     if parity(pi)==0:even.add(q)
 return allp,even

def main():
 GD,A=d4graph();GL,cells=v4graph();assert GD.number_of_edges()==GL.number_of_edges()==48
 for G in (GD,GL):
  assert set(dict(G.degree()).values())=={6}
  lam=set();mu=set()
  for i,j in itertools.combinations(range(16),2):
   z=len(set(G[i])&set(G[j]));(lam if G.has_edge(i,j) else mu).add(z)
  assert lam==mu=={2}
 gm=nx.algorithms.isomorphism.GraphMatcher(GL,GD);iso=next(gm.isomorphisms_iter())
 allp,even=latin_autoparatopies(cells);assert len(allp)==576 and len(even)==288
 # Every autoparatopy preserves the V4 cell graph, hence transports to the D4 A2 graph.
 assert all(all(GL.has_edge(i,j)==GL.has_edge(p[i],p[j]) for i,j in itertools.combinations(range(16),2)) for p in allp)
 # Full automorphism group size of L2(4) is 1152; enumerate to certify index two.
 aut_count=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(GD,GD).isomorphisms_iter());assert aut_count==1152
 # Eight graph K4s are V4 Latin transversals in this realization.
 k4=[frozenset(C) for C in itertools.combinations(range(16),4) if all(GL.has_edge(i,j) for i,j in itertools.combinations(C,2))];assert len(k4)==8
 assert all(len({cells[i][0] for i in C})==len({cells[i][1] for i in C})==len({cells[i][2] for i in C})==4 for C in k4)
 out={'schema':'w33.pass7428.d4_latin_hoffman_composed_bridge.v1','status':'PASS',
  'D4_A2_graph':'L2(4)=SRG(16,6,2,2)','Klein_V4_cell_graph_rule':'adjacent iff row, column and symbol are all different',
  'explicit_graph_isomorphism_V4_cells_to_D4_A2_indices':{str(k):v for k,v in sorted(iso.items())},
  'V4_autoparatopy_order':576,'V4_even_parastrophe_order':288,'full_D4_A2_graph_aut_order':1152,
  'Latin_group_index_in_D4_graph_aut':2,'eight_K4s':'the eight V4 Latin transversals, transported to the eight D4=A2+A2+A2+A2 root partitions',
  'Pass5300_input':'Pass5300 already proves the q=5 Hoffman cover stabilizer H has order 576, H is not the full Latin autoparatopy group, but H/Z(H) is explicitly GL(4,2)-conjugate to the even-parastrophe subgroup L+ of order 288.',
  'composed_bridge':'H/Z(H) ~= L+ < AutPar(V4 Latin) < Aut(D4 A2 disjointness graph), with orders 288 < 576 < 1152.',
  'theorem':'The order-four Latin object in the Hoffman bridge is now realized inside E8: its 16-cell SRG is exactly the root-disjointness graph on the 16 A2 subsystems of any D4. The eight Latin transversals are exactly the eight partitions of the 24 D4 roots into four A2 hexagons.',
  'firewall':'H itself remains non-isomorphic to the full Latin autoparatopy group as proved in Pass5300. The E8 bridge is through the degree-16 Latin carrier and the central quotient, not equality of the two order-576 groups.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','orders':[288,576,1152]}))
if __name__=='__main__':main()
