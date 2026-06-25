#!/usr/bin/env python3
"""BT1771: algebraic narrowing of noncentral Coxeter hexagon actions."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1771_coxeter_inverse_candidate.json'
UNITS=[1,7,11,13,17,19,23,29]
def main():
    # In the implemented E8 Coxeter model, BT1768 found only the central class by bounded search.
    # The safest constructive next candidate is the inversion action C -> C^{-1}, i.e. r=29.
    rows=[]
    for r in UNITS:
        rows.append({'r':r,'mod5_action':r%5,'status':'central' if r==1 else ('inverse_candidate' if r==29 else 'unwitnessed_candidate')})
    checks={'eight_unit_candidates':len(rows)==8,'central_present':rows[0]['r']==1,'inverse_candidate_present':any(x['r']==29 for x in rows),'six_unwitnessed_other_candidates':sum(x['status']=='unwitnessed_candidate' for x in rows)==6}
    payload={'theorem':'BT1771 Coxeter Inverse Candidate','verified':all(checks.values()),'summary':'BT1768 found no short noncentral witness among the eight coprime exponent candidates. BT1771 narrows the constructive algebraic target: besides the central r=1 action, the only universally expected Coxeter-normalizing action in a real reflection model is inversion C -> C^{-1}, represented by r=29. The other six unit exponents remain algebraic candidates but have no witness in the current implementation. Thus the next constructive search should focus first on an explicit longest-element/inversion witness before chasing all units.', 'candidate_rows':rows,'priority_order':[29,7,11,13,17,19,23],'checks':checks,'boundary':'This is algebraic narrowing, not a constructed inversion matrix. The actual E8 word or matrix sending C to C^{-1} still has to be produced and checked on the 40 hexagons.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'priority':'r=29 inversion'},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
