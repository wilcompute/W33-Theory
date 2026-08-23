#!/usr/bin/env python3
"""Pass9473-9480: refine the Suzuki weld by orthogonal subtype and locate the R transport obstruction."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9473_9480_SUZUKI_SIGN_R_TRANSPORT_OBSTRUCTION.json'

def main():
 ctrl=json.loads((ROOT/'data/PART_W33_PASS9101_9108_SUZUKI_QPLUS53_CONTROLLER_NO_SELECTION.json').read_text())
 twin=json.loads((ROOT/'data/PART_W33_PASS9253_9260_ORTHOGONAL_SIGN_TWIN_SELECTOR.json').read_text())
 hj=json.loads((ROOT/'data/PART_W33_PASS9085_9092_LEECH_HJ_SUZUKI_DOUBLE_COVER.json').read_text())
 assert ctrl['two_space_orbits_under_similitudes']['nondegenerate_candidate_orbits']==90
 assert ctrl['two_space_orbits_under_similitudes']['hyperbolic_orbits']==62
 assert ctrl['two_space_orbits_under_similitudes']['anisotropic_orbits']==28
 assert twin['Suzuki_selector']['nondegenerate_W33_candidates']==7371
 assert hj['Hall_Janko_copies_in_Leech20800']==416 and hj['HJ_copies_through_each_six_space']==2
 q=3;n=6
 sp=q**(n*n)
 for i in range(1,n+1):sp*=q**(2*i)-1
 u=q**(n*(n-1)//2)
 for i in range(1,n+1):u*=q**i-(-1)**i
 orbit=sp//u
 assert sp==14395932257291877030764312963579904000
 assert u==182699779456696320 and orbit==78795564505342027200
 out={'schema':'w33.pass9473_9480.suzuki_sign_r_transport_obstruction.v1','status':'PASS','passes':'9473-9480',
  'Suzuki_Qplus_candidate_orbits':{'nondegenerate_total_points':7371,'controller_orbits':90,'hyperbolic_orbits':62,'anisotropic_orbits':28},
  'orthogonal_subtype_result':'Within the certified Suzuki Q+(5,3) selector, fixing the two-space subtype is a genuine refinement but not a selector: 62 controller orbits remain in the hyperbolic sector and 28 remain in the anisotropic sector.',
  'Hall_Janko_416_carrier':{'vertices_or_HJ_copies':416,'Leech_edges':20800,'oriented_incidence_flags':41600,'HJ_endpoints_per_Leech_edge':2},
  'R_transport':{'Sp12_3_order':sp,'U6_3_centralizer_order':u,'conjugacy_orbit_of_complex_structures':orbit,'status':'NO CANONICAL TRANSPORT CERTIFIED'},
  'theorem':'Orthogonal subtype improves the marked-line Suzuki weld from 90 candidate orbits to 62 or 28, but does not select uniquely. The F9 complex structure R is stronger data, yet the repo currently has no objectwise symplectic isometry identifying the Niemeier glue phase space (K,R) with the independent Suzuki 12D module. Choosing such an isometry arbitrarily chooses one among 78,795,564,505,342,027,200 conjugate symplectic complex structures, so an R-based collapse of the 90 orbits is not invariant until a transport is constructed.',
  'cross_track':'The parallel Hall-Janko result supplies a canonical two-sheet incidence cover of the Leech 20,800 edges by their 416 Hall-Janko/G2(4)-graph endpoints. This is promising transport data, but cardinality/incidence alone does not define the missing symplectic isometry.',
  'boundary':'Exact orbit counts and group-order obstruction. This is not a theorem that no canonical transport can exist; it states that no such transport is present in the currently certified weld and quantifies the choice that must be removed.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','subtype_orbits':[62,28],'R_choices':orbit}));return 0
if __name__=='__main__':raise SystemExit(main())
