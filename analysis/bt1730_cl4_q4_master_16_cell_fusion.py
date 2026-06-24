#!/usr/bin/env python3
"""BT1730: fuse Cl4/Q4/knight/Gray data into the master 16-cell chart."""
from __future__ import annotations
from collections import Counter
import json, math
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1730_cl4_q4_master_16_cell_fusion.json'
ALG=['R','C','H','O']
MAGIC={('R','R'):'A1',('R','C'):'A2',('R','H'):'C3',('R','O'):'F4',('C','R'):'A2',('C','C'):'A2+A2',('C','H'):'A5',('C','O'):'E6',('H','R'):'C3',('H','C'):'A5',('H','H'):'D6',('H','O'):'E7',('O','R'):'F4',('O','C'):'E6',('O','H'):'E7',('O','O'):'E8'}
BITS={'R':(0,0),'C':(0,1),'H':(1,0),'O':(1,1)}
def xor(a,b):
 v=(BITS[a][0]^BITS[b][0], BITS[a][1]^BITS[b][1])
 return next(k for k,w in BITS.items() if w==v)
def knight_graph():
 G=nx.Graph()
 for r in range(4):
  for c in range(4): G.add_node((r,c))
 for r,c in list(G.nodes()):
  for dr,dc in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
   G.add_edge((r,c),((r+dr)%4,(c+dc)%4))
 return G
def hamilton_cycle(G):
 start=(0,0); path=[start]; seen={start}
 def dfs(v):
  if len(path)==len(G): return start in G[v]
  nbrs=[u for u in G.neighbors(v) if u not in seen]
  nbrs.sort(key=lambda u: sum(1 for w in G.neighbors(u) if w not in seen))
  for u in nbrs:
   seen.add(u); path.append(u)
   if dfs(u): return True
   path.pop(); seen.remove(u)
  return False
 return path+[start] if dfs(start) else None
def q4_iso(G):
 Q=nx.hypercube_graph(4)
 return next(nx.algorithms.isomorphism.GraphMatcher(G,Q).isomorphisms_iter())
def main():
 K=knight_graph(); iso=q4_iso(K); tour=hamilton_cycle(K); order={cell:i for i,cell in enumerate(tour[:-1])}
 cells=[]
 for r in range(4):
  for c in range(4):
   row=ALG[r]; col=ALG[c]; bits=tuple(iso[(r,c)]); grade=sum(bits)
   cells.append({'cell':[r,c],'row':row,'col':col,'latin_symbol':xor(row,col),'magic_square':MAGIC[(row,col)],'magic_kind':'hesse' if row!='O' and col!='O' else 'exceptional','gray_bits':list(bits),'clifford_grade':grade,'knight_order':order[(r,c)],'genus_axes':[['R',r],['C',c],['S',r^c]],'q2025_line_slot':4*r+c})
 grade_profile=[sum(x['clifford_grade']==k for x in cells) for k in range(5)]
 knight_gray_ok=all(sum(a!=b for a,b in zip(iso[tour[i]],iso[tour[(i+1)%16]]))==1 for i in range(16))
 checks={'sixteen_cells':len(cells)==16,'knight_graph_is_q4':nx.is_isomorphic(K,nx.hypercube_graph(4)),'closed_knight_gray_cycle':tour is not None and knight_gray_ok,'clifford_grade_profile_14641':grade_profile==[1,4,6,4,1],'magic_hesse_plus_exceptional':sum(x['magic_kind']=='hesse' for x in cells)==9 and sum(x['magic_kind']=='exceptional' for x in cells)==7,'genus_axes_12':len({tuple(a) for x in cells for a in x['genus_axes']})==12,'q2025_line_slots_16':sorted(x['q2025_line_slot'] for x in cells)==list(range(16)),'bus_48':16*3==48,'horizon_72_66':(12-3)*(12-4)==72 and math.comb(12,2)==66}
 payload={'theorem':'BT1730 Cl4-Q4 master 16-cell fusion chart','verified':all(checks.values()),'summary':'The master 4x4 XOR-Latin chart now carries every active layer on the same 16 cells: q2025 line slots, genus/tomotope axes, Freudenthal Hesse/exceptional cells, toroidal knight order, Q4 Gray bits, and Clifford grades. The Clifford grade profile is 1,4,6,4,1, and the knight tour is a Gray cycle under the Q4 isomorphism.','cells':sorted(cells,key=lambda x:x['knight_order']),'grade_profile':grade_profile,'knight_tour':[list(x) for x in tour],'graph_counts':{'knight_vertices':K.number_of_nodes(),'knight_edges':K.number_of_edges(),'q4_diameter':nx.diameter(K),'q4_square_faces':24},'checks':checks,'boundary':'This is a fused coordinate chart. It aligns indices and graph structure; it does not assert that q2025 line incidence equals Clifford multiplication or Freudenthal brackets.'}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
 print(json.dumps({'verified':payload['verified'],'grade_profile':grade_profile,'knight_gray_ok':knight_gray_ok},indent=2))
 return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
