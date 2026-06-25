#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1780_inversion_hexagon_exact_map.json'
CYCLES=[[0,7,6,13,27],[1,21,15,5,2],[3,12,17,34,4],[8,26,33,11,38],[9,24,18,35,10],[14,23,36,28,20],[16,29,32,30,22],[19,39,37,31,25]]
HMAP={0:27,7:13,6:6,13:7,27:0,1:1,21:2,15:5,5:15,2:21,3:12,12:3,17:4,34:34,4:17,8:33,26:26,33:8,11:38,38:11,9:24,24:9,18:10,35:35,10:18,14:14,23:20,36:28,28:36,20:23,16:29,29:16,32:22,30:30,22:32,19:31,39:37,37:39,31:19,25:25}
def main():
    rows=[]; ok=True
    for ci,cyc in enumerate(CYCLES):
        row=[]
        for p,x in enumerate(cyc):
            y=HMAP[x]; cj=next(j for j,c in enumerate(CYCLES) if y in c); q=CYCLES[cj].index(y)
            row.append({'from_hexagon':x,'from_phase':p,'to_hexagon':y,'to_cycle':cj,'to_phase':q})
            ok = ok and cj==ci
        rows.append({'cycle':ci,'map':row})
    checks={'forty_hexagons':len(HMAP)==40,'involution':all(HMAP[HMAP[k]]==k for k in HMAP),'preserves_each_5cycle_set':ok}
    payload={'theorem':'BT1780 exact inversion map on Coxeter hexagons','verified':all(checks.values()),'summary':'BT1777 classified the inversion witness as a D5-type operation. BT1780 gives the exact 40-hexagon map. Important refinement: with the current BT1750 cycle/phase labels, the witness preserves each of the eight Coxeter 5-cycles setwise but reflects each cycle about a cycle-dependent center; it is not a single global phase map p -> -p for all eight cycles under these labels. The correct invariant statement is cyclewise dihedral reflection.', 'coxeter_5cycles':CYCLES,'hexagon_map':{str(k):v for k,v in sorted(HMAP.items())},'cyclewise_maps':rows,'checks':checks,'boundary':'This corrects the phase-only simplification. To recover a uniform p -> -p law one must rephase the eight 5-cycles independently.'}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'mode':'cyclewise reflection'},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
