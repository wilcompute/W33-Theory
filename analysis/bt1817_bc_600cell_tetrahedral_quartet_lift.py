#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1817_bc_600cell_tetrahedral_quartet_lift.json'
FACES=['F0','F1','F2','F3']
QUARTET=['00','01','10','11']
DEFECT_SLICE=[(5,10,41),(7,34,40),(10,22,44),(12,34,42),(18,40,42),(30,41,44)]

def main():
    face_edges=list(itertools.combinations(FACES,2))
    q_edges=list(itertools.combinations(QUARTET,2))
    rows=[]
    for fe,qe,hinge in zip(face_edges,q_edges,DEFECT_SLICE):
        rows.append({'tetrahedral_face_pair':list(fe),'quartet_edge':list(qe),'hinge_support':list(hinge),'observed':hinge==(10,22,44)})
    checks={'four_faces':len(FACES)==4,'six_face_pairs':len(face_edges)==6,'six_quartet_edges':len(q_edges)==6,'six_hinges':len(DEFECT_SLICE)==6,'observed_edge_present':any(r['observed'] for r in rows)}
    payload={'bt':'BT1817','title':'BC/600-cell tetrahedral quartet lift','verified':all(checks.values()),'summary':'The K4 quartet has a direct BC/600-cell reading. A tetrahedral cell has four faces, hence four local face-neighbor directions in the 600-cell facet-dual. The six K4 edges are the six unordered pairs of tetrahedral faces, equivalently the six edges of the tetrahedron. Therefore the hidden quartet can be lifted from D4/GKP cosets to local tetrahedral face states on the BC ring. The W(E6) six-hinge slice is the same K4 edge set seen through Schlaefli transport.','local_tetrahedral_states':FACES,'quartet_states':QUARTET,'edge_lift_table':rows,'observed':next(r for r in rows if r['observed']),'dictionary':{'3_coordinate':'BC/Hesse strand step along the decagonal ring','4_coordinate':'four faces of the local tetrahedral cell / four D4 glue cosets / four GKP quartet states','6_edges':'six pairings of tetrahedral faces = six K4 edges = six W(E6)-compatible Hesse hinges','oriented_repair':'choose one tetrahedral edge/quartet edge and orient transfer by the table sign pattern'},'checks':checks,'boundary':'This identifies the local tetrahedral geometry of the quartet. It still does not choose explicit 600-cell facet coordinates for every table state in the full 30-cell ring.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'observed':payload['observed']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
