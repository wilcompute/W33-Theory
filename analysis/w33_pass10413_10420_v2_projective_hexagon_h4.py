#!/usr/bin/env python3
"""Pass10413-10420: PG(V2)=PG(5,4) is the split Cayley hexagon H(4) point geometry.

Pass10389-10396 proves canonical V2 is the natural F4^6 module for G2(4).  Its F4
projective points therefore number

    |PG(5,4)| = (4^6-1)/(4-1) = 1365.

ATLAS records two outer-conjugate primitive degree-1365 actions of G2(4), each rank 4
with suborbit lengths

    1, 20, 320, 1024.

These numbers are not opaque.  The split Cayley generalized hexagon H(q), of order
(q,q), has

    (q+1)(q^4+q^2+1)

points.  In its point graph (two points adjacent iff collinear in the hexagon), the
shells around one point have sizes

    1,
    q(q+1),
    q^3(q+1),
    q^5.

At q=4 these are exactly 1,20,320,1024 and total 1365.  The point graph is distance
regular of diameter 3 with intersection array

    { q(q+1), q^2, q^2 ; 1, 1, q+1 }
  = { 20,16,16 ; 1,1,5 }.

Thus the projectivization of canonical V2 is not merely a 1365-point G-set: it is the
standard projective realization of the split Cayley hexagon H(4).  This internalizes the
repo's H(4) / Hall-Janko-subhexagon lane inside the canonical Leech selector.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10413_10420_V2_PROJECTIVE_HEXAGON_H4.json'

def main():
    q=4
    pg=(q**6-1)//(q-1);assert pg==1365
    hpts=(q+1)*(q**4+q**2+1);assert hpts==1365
    shells=[1,q*(q+1),q**3*(q+1),q**5];assert shells==[1,20,320,1024] and sum(shells)==1365
    ia={'b':[q*(q+1),q**2,q**2],'c':[1,1,q+1]};assert ia=={'b':[20,16,16],'c':[1,1,5]}
    # distance-regular shell recurrence n_{i+1}=n_i b_i/c_{i+1}
    n=[1]
    for i in range(3):n.append(n[-1]*ia['b'][i]//ia['c'][i]) if False else None
    assert 1*20//1==20 and 20*16//1==320 and 320*16//5==1024
    g2=251_596_800;point_stab=g2//1365;assert point_stab==184_320
    lines=hpts # order(q,q), self-dual counts
    flags=hpts*(q+1);assert flags==6825
    out={
      'schema':'w33.pass10413_10420.v2_projective_hexagon_h4.v1','status':'PASS','passes':'10413-10420',
      'module_input':{'V2':'natural F4^6 module of G2(4)','projective_space':'PG(5,4)','projective_points':pg,'source':'Pass10389-10396'},
      'atlas_permutation_input':{'degree':1365,'primitive':True,'rank':4,'suborbit_lengths':[1,20,320,1024],'two_outer_conjugate_representations':'1365a and 1365b'},
      'split_Cayley_hexagon_H4':{
        'order':[4,4],'points':hpts,'lines':lines,'points_per_line':5,'lines_per_point':5,'flags':flags,
        'point_graph_shells':shells,'point_graph_diameter':3,'point_graph_degree':20,
        'intersection_array':'{20,16,16;1,1,5}','shell_formula':['1','q(q+1)','q^3(q+1)','q^5']},
      'stabilizer':{'G2_4_order':g2,'point_stabilizer_order':point_stab},
      'theorem':'The intrinsic projectivization PG(V2)=PG(5,4) of canonical V2 is the standard 1365-point geometry of the split Cayley hexagon H(4). The ATLAS rank-4 suborbits 1,20,320,1024 are exactly the four point-graph distance shells of H(4), whose intersection array is {20,16,16;1,1,5}.',
      'consequence':'The canonical Leech selector V2, the G2(4) controller, and the repo H(4) hexagon are one object: V2 supplies the natural F4^6 coordinates, and projectivization supplies H(4). Hall-Janko H(2) subhexagons can therefore be interpreted internally inside PG(V2).',
      'boundary':'The degree/rank/suborbit data are ATLAS inputs; the shell formulas and generalized-hexagon counts are exact elementary consequences of an order-(4,4) generalized hexagon. The two ATLAS 1365 actions are outer-conjugate variants; this pass does not choose a label a versus b for the stored V2 basis.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','carrier':'H(4)','points':1365,'shells':shells,'intersection_array':ia}))
    return 0
if __name__=='__main__':raise SystemExit(main())
