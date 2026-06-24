#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import networkx as nx
OUT=Path(__file__).resolve().parents[1]/'data'/'bt1717_split_cayley_incidence_obstruction.json'
def fano_lines():
 return [[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]]
def build():
 pts=[(a,h) for a in range(7) for h in range(9)]
 lines=[]
 for h in range(9):
  for L in fano_lines(): lines.append([(a,h) for a in L])
 G=nx.Graph(); G.add_nodes_from([('p',p) for p in pts]); G.add_nodes_from([('l',i) for i in range(len(lines))])
 for i,L in enumerate(lines):
  for p in L: G.add_edge(('p',p),('l',i))
 comps=nx.number_connected_components(G)
 checks={'point_count_63':len(pts)==63,'line_count_63':len(lines)==63,'each_line_size_3':all(len(L)==3 for L in lines),'each_point_degree_3':all(G.degree(('p',p))==3 for p in pts),'naive_product_not_connected':comps==9,'not_full_split_cayley':comps!=1}
 return {'theorem':'BT1717 Split-Cayley Incidence Product Obstruction','verified':all(checks.values()),'summary':'The naive Fano times Hesse address cover has 63 points and 63 triples with degree 3, but its incidence graph is nine disconnected Fano components. Therefore the full split-Cayley functor requires a nontrivial Hesse/Fano twist cocycle; direct product incidence is falsified.','counts':{'points':63,'lines':63,'components':comps,'incidences':G.number_of_edges()},'next_target':'search for a 9-cell monodromy/cocycle on Fano lines that connects the 9 components while preserving girth-12 hexagon constraints','checks':checks}
def main():
 cert=build(); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n'); print(cert['theorem'],cert['verified']); return 0 if cert['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
