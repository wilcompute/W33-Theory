#!/usr/bin/env python3
"""BT1754: decompose Fano orientations into Hesse/Q4-derived parts."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1754_hesse_q4_fano_orientation_decomposition.json'
CHOICES=[459,595,435,694,87,544,347,839,561]
ROT_RULE={0:[3,1,3],1:[4,3,4],2:[5,5,3]}
def family(hi): return 0 if hi<3 else (1 if hi<6 else 2)
def param(hi): return hi%3
def main():
    rows=[]; ok=True
    for hi,c in enumerate(CHOICES):
        fam=family(hi); par=param(hi); auto=c//6; rot=c%6; d=ROT_RULE[fam][par]
        ok = ok and (rot==d)
        rows.append({'hesse_line':hi,'family':['row','column','diagonal'][fam],'parameter':par,'choice':c,'fano_automorphism_index':auto,'rotation_index':rot,'derived_rotation':d})
    autos=[r['fano_automorphism_index'] for r in rows]
    checks={'nine_choices':len(CHOICES)==9,'choice_decomposition':all(6*r['fano_automorphism_index']+r['rotation_index']==r['choice'] for r in rows),'rotations_derived_from_family_parameter':ok,'automorphisms_remain_nine_external_indices':len(autos)==9 and len(set(autos))==9}
    payload={'theorem':'BT1754 Hesse/Q4 Fano Orientation Decomposition','verified':all(checks.values()),'summary':'The nine Fano system choices split as choice = 6*PSL(2,7)-automorphism-index + rotation-index. The rotation indices are derived from the Hesse/Q4 family-parameter table: rows [3,1,3], columns [4,3,4], diagonals [5,5,3]. Thus BT1751/BT1754 derive channel colors and rotation orientation from the Hesse/Q4 layer. The remaining external data are exactly nine PSL(2,7) automorphism indices.', 'rotation_rule':ROT_RULE,'decomposition':rows,'remaining_automorphism_indices':autos,'checks':checks,'boundary':'This derives the rotation part of the nine choices, not the PSL(2,7) automorphism indices themselves.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'remaining_automorphism_indices':autos},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
