#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'data'/'bt1718_toroidal_coordinate_parser_scaffold.json'
def genus_num(n): return (n-3)*(n-4)
def build():
 cs={'V':7,'E':21,'F':14}; sz={'V':14,'E':21,'F':7}; tet={'V':4,'E':6,'F':4}
 checks={'csaszar_euler_torus':cs['V']-cs['E']+cs['F']==0,'szilassi_euler_torus':sz['V']-sz['E']+sz['F']==0,'tet_euler_sphere':tet['V']-tet['E']+tet['F']==2,'csaszar_uses_V7':genus_num(cs['V'])==12,'szilassi_uses_F7':genus_num(sz['F'])==12,'tetra_primal_zero':genus_num(tet['V'])==0,'tetra_dual_zero':genus_num(tet['F'])==0,'dual_swap':cs['V']==sz['F'] and cs['F']==sz['V'],'edge_carrier_21':cs['E']==sz['E']==math.comb(7,2)}
 return {'theorem':'BT1718 Toroidal Coordinate Parser Scaffold','verified':all(checks.values()),'summary':'The parser scaffold records the exact primal-dual invariants needed before loading concrete coordinates: Csaszar uses V=7 in the complete-graph genus numerator, Szilassi uses F=7, and tetrahedron works in both variables with zero numerator. The coordinate parser target is now to attach actual 3D embeddings to these invariant slots.','polyhedra':{'csaszar':cs,'szilassi':sz,'tetrahedron':tet},'genus_numerators':{'csaszar_V':12,'szilassi_F':12,'tetra_V':0,'tetra_F':0},'parser_contract':['read vertices/faces from coordinate source','verify Euler characteristic','verify complete K7 adjacency or complete K7 face adjacency','emit 21-edge carrier and 7-realization scheduler label'],'checks':checks}
def main():
 cert=build(); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n'); print(cert['theorem'],cert['verified']); return 0 if cert['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
