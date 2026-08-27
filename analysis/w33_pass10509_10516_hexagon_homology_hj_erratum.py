#!/usr/bin/env python3
"""Pass10509-10516: correct the Hall-Janko/H(2) provenance and freeze the q^6 Levi-homology identity.

Two distinct objects had been conflated in Pass10429-10436:
  * the 416 Suzuki neighbors are G2(4)/J2 Hall-Janko/J2 controller objects
    (Hall-Janko suboctagons in the Suzuki-tower near-octagon description);
  * inside one Hall-Janko realization, a local family of 100 embedded H(2)
    subhexagons forms the HJ(100) vertex set.

Separately, for the split Cayley hexagon H(q),
  P=(q+1)(q^4+q^2+1), E=(q+1)P,
so the first Betti number of its connected Levi graph is
  beta1=E-2P+1=q^6.
Hence beta1(H(4))=4096 and beta1(H(2))=64.
For a free C13 action on the H(4) Levi graph, the quotient has
105 point-orbits, 105 line-orbits, 525 flag-orbits and beta1=316=1+315.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10509_10516_HEXAGON_HOMOLOGY_HJ_ERRATUM.json'

def counts(q:int):
    P=(q+1)*(q**4+q**2+1)
    E=(q+1)*P
    beta=E-2*P+1
    assert beta==q**6
    return P,E,beta

def main()->int:
    P4,E4,b4=counts(4);assert (P4,E4,b4)==(1365,6825,4096)
    P2,E2,b2=counts(2);assert (P2,E2,b2)==(63,189,64)
    assert P4%13==0 and E4%13==0
    qP=P4//13;qE=E4//13
    qb=qE-2*qP+1
    assert (qP,qE,qb)==(105,525,316)
    assert qb==1+(4**6-1)//13==316
    out={
      'schema':'w33.pass10509_10516.hexagon_homology_hj_erratum.v1','status':'PASS','passes':'10509-10516',
      'provenance_correction':{
        'Suzuki_416':'G2(4)/J2 Hall-Janko/J2 controller objects; in the Suzuki-tower literature these are Hall-Janko suboctagons, not 416 H(2) subhexagons',
        'Hall_Janko_local_H2':'within one Hall-Janko realization, 100 embedded H(2) subhexagons form the HJ(100) vertex set',
        'corrected_source':'Pass10429-10436 v2'},
      'general_hexagon_identity':{
        'points_and_lines':'P=(q+1)(q^4+q^2+1)',
        'flags':'E=(q+1)P',
        'Levi_beta1':'E-2P+1=q^6'},
      'H4':{'points':P4,'lines':P4,'flags':E4,'Levi_beta1':b4,'identity':'4096=4^6=|V2|'},
      'H2':{'points':P2,'lines':P2,'flags':E2,'Levi_beta1':b2,'identity':'64=2^6'},
      'H4_mod_C13':{'point_orbits':qP,'line_orbits':qP,'flag_orbits':qE,'Levi_beta1':qb,'identity':'316=1+315'},
      'theorem':'For every split Cayley hexagon H(q), the connected Levi graph has first Betti number q^6. Thus H(4) has beta1=4096 and H(2) has beta1=64. Under the free C13 quotient of H(4), beta1 becomes 316=1+315. These homology identities are independent of the corrected Hall-Janko provenance: the 416 Suzuki neighbors are J2/Hall-Janko controller objects, while the local HJ(100) construction uses 100 embedded H(2) subhexagons.',
      'boundary':'The q^6 Betti identity is exact elementary incidence arithmetic. It does not identify H(2) cycle spaces with every one of the 416 Suzuki-neighbor controller objects, and it does not by itself identify graph homology with V2 as a full G2(4)-module beyond the C13 restriction proved in Pass10501-10508.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','beta_H4':b4,'beta_H2':b2,'beta_H4_C13':qb,'corrected_416':'HJ/J2 controllers','local_H2':100}))
    return 0
if __name__=='__main__':raise SystemExit(main())
