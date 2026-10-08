"""600-cell antipodal graph vs W33 60-edge code incidence fingerprints.

Uses the actual 120 H4 coordinates/adjacency of the existing Clifford
fibration verifier, not the Boerdijk abstract tetrahedron-ring model.
"""
from pathlib import Path
import sys,json,collections,itertools
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"));sys.path.insert(0,str(ROOT))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
from w33_clifford_antipodal_spread_incidence_bridge import antipodal_pair_index
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
OUT=ROOT/"data/w33_20261008_H4_60_antipodal_incidence_obstruction.json"
def main():
 vertices=build_600cell();ad=build_adjacency(np.array(vertices),120);pairs=antipodal_pair_index()
 assert len(vertices)==120 and len(set(pairs.values()))==60
 H=nx.Graph();H.add_nodes_from(range(60))
 for u in range(120):
  for v in range(u+1,120):
   if ad[u][v]:H.add_edge(pairs[u],pairs[v])
 assert nx.number_of_nodes(H)==60
 V,E,F,stab,G,b1,b2=topology()
 W=nx.Graph();W.add_nodes_from(range(60))
 incident=collections.defaultdict(list)
 for j,(u,v) in enumerate(E):incident[u].append(j);incident[v].append(j)
 for star in incident.values():
  for x,y in itertools.combinations(star,2):W.add_edge(x,y)
 def fingerprint(g):
  return {"vertices":g.number_of_nodes(),"edges":g.number_of_edges(),
   "degree_histogram":dict(collections.Counter(dict(g.degree()).values())),
   "triangles":sum(nx.triangles(g).values())//3,
   "connected_components":nx.number_connected_components(g),
   "adjacency_spectrum_sorted":[round(float(a),7) for a in np.linalg.eigvalsh(nx.to_numpy_array(g))]}
 fH=fingerprint(H);fW=fingerprint(W)
 assert fH["degree_histogram"]!=fW["degree_histogram"]
 return {"H4_600cell_antipodal_graph":fH,
  "W33_60_edge_qubit_line_graph":fW,
  "incidence_preserving_60vertex_graph_bijection_exists":False,
  "F20_abstract_bijection_remaining_valid":True,
  "proof":"Different degree histogram; an abstract F20 equivariant bijection is not an adjacency isomorphism. Actual 600-cell antipodal vertex geometry used.",
  "unexplored":"A different 600-cell relation, a labeled association-scheme twist, or a subset of H4 adjacency may still work."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:{t:v for t,v in a.items() if t!="adjacency_spectrum_sorted"} for k,a in x.items() if isinstance(a,dict)},flush=True)
 print("H4_ADJACENCY_NO_GO_PASS")
