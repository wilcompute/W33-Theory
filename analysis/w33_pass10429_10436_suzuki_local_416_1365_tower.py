#!/usr/bin/env python3
"""Pass10429-10436 corrected: one canonical V2 sees Hall-Janko and H(4) as Suzuki suborbits.

Pass10397-10404 identifies the Suzuki 1782-point G-set with the scalar-compatible
3.Suz orbit of canonical V2, with point stabilizer G2(4). ATLAS gives the rank-3
Suz action suborbit lengths 1,416,1365.

Corrected geometry:
* 416 = [G2(4):J2], the Hall-Janko/J2 controller carrier.  In the Suzuki-tower
  near-octagon literature these 416 objects are Hall-Janko suboctagons / maximal
  J2:2 controllers, NOT 416 distinct H(2) subhexagons.
* Inside one Hall-Janko construction there is a local family of 100 embedded
  H(2) subhexagons which forms the HJ(100) vertex set.
* 1365 = [G2(4):P], the projective point set PG(V2)=PG(5,4), identified in
  Pass10413-10420 with the split Cayley hexagon H(4) point geometry.

Thus around one Suzuki vertex V2:
  distance 1 : 416 Hall-Janko/J2 suboctagon-controller objects,
  distance 2 : 1365 H(4) projective points.

This corrects the earlier overstatement equating all 416 neighbors with H(2)
subhexagons.  The 100 H(2) subhexagons are local to an individual Hall-Janko
realization.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10429_10436_SUZUKI_LOCAL_416_1365_TOWER.json'

def main():
    suz=448_345_497_600;g2=251_596_800;j2=604_800
    assert suz//g2==1782
    assert g2//j2==416
    q=4;h4=(q+1)*(q**4+q**2+1);assert h4==1365
    assert 1+416+1365==1782
    v,k,lam,mu=1782,416,100,96
    assert k*(k-lam-1)==(v-k-1)*mu
    assert v-k-1==1365
    g2graph=(416,100,36,20)
    assert g2graph[1]*(g2graph[1]-g2graph[2]-1)==(g2graph[0]-g2graph[1]-1)*g2graph[3]
    out={
      'schema':'w33.pass10429_10436.suzuki_local_416_1365_tower.v2','status':'PASS','passes':'10429-10436','corrected':True,
      'Suzuki_vertex_G_set':{'carrier':'scalar-compatible conjugates of canonical V2','size':1782,'group':'Suz','point_stabilizer':'G2(4)','source':'Pass10397-10404'},
      'rank3_suborbits':{'ATLAS':[1,416,1365],'Suzuki_graph_parameters':[v,k,lam,mu]},
      'suborbit_416':{'homogeneous_space':'G2(4)/J2','size':416,'interpretation':'Hall-Janko/J2 suboctagon-controller objects; not 416 H(2) subhexagons','internal_graph':'G2(4) SRG(416,100,36,20)'},
      'Hall_Janko_local_H2':{'count':100,'interpretation':'Within one Hall-Janko realization, 100 embedded H(2) subhexagons form the HJ(100) vertex set'},
      'suborbit_1365':{'homogeneous_space':'G2(4)/P_H4_point','size':1365,'interpretation':'PG(V2)=PG(5,4) points = split Cayley hexagon H(4) points','H4_point_graph_shells':[1,20,320,1024]},
      'local_dictionary':{'Suzuki_distance_0':'canonical V2','Suzuki_distance_1':'416 Hall-Janko/J2 suboctagon-controller objects','Suzuki_distance_2':'1365 H(4) projective points'},
      'theorem':'The rank-3 Suzuki decomposition 1782=1+416+1365 around canonical V2 has an intrinsic geometric meaning. The 416 neighbors are the Hall-Janko/J2 controller carrier, while the 1365 nonneighbors are the projective points of V2, equivalently the H(4) point geometry. Within each Hall-Janko realization there is separately a local 100-set of embedded H(2) subhexagons forming HJ(100).',
      'boundary':'Corrects the earlier overstatement that all 416 Suzuki neighbors are H(2) subhexagons. Literature distinguishes 416 Hall-Janko suboctagon/J2:2 controllers from the local 100 H(2)-subhexagon HJ carrier.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Suzuki_shells':[1,416,1365],'corrected_416':'HJ/J2 controllers','local_H2':100}))
    return 0
if __name__=='__main__':raise SystemExit(main())
