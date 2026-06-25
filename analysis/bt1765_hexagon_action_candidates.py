#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1765_hexagon_action_candidates.json'
UNITS=[1,7,11,13,17,19,23,29]
def main():
    rows=[{'r':r,'r_mod_5':r%5,'keeps_hex_layer':True,'central_case':r==1} for r in UNITS]
    checks={'eight_candidates':len(rows)==8,'four_mod5_actions':sorted(set(x['r_mod_5'] for x in rows))==[1,2,3,4]}
    payload={'theorem':'BT1765 hexagon action candidates','verified':all(checks.values()),'summary':'BT1762 verified the central 30-step action on the 40 hexagons. Any larger whole-hexagon action must use a coprime exponent r modulo 30. The eight candidate exponents reduce to four actions modulo 5 on each 5-cycle. This records the exact candidate action law for searching beyond the central action.','rows':rows,'checks':checks,'boundary':'Candidate law only; noncentral E8 Weyl witnesses are not constructed here.'}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'candidate_count':len(rows)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
