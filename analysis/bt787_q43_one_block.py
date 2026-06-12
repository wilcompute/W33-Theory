#!/usr/bin/env python3
"""BT787: one Q43 apartment block check."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from bt760_q43_duo_transport_harness import build_q43, enumerate_apartments, reverse_orientation
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_BT787_Q43_ONE_BLOCK_summary.json"

def partner(i:int)->int:
    b,r=divmod(i,12); d,p=divmod(r,6); return b*12+(1-d)*6+p

def main():
    qpts,qlines=build_q43(); apts=enumerate_apartments(qpts,qlines)
    a0=apts[0]; m0=reverse_orientation(a0)
    rows=[]
    for i in range(48):
        b,r=divmod(i,12); d,p=divmod(r,6)
        rows.append((i,b,p,d,0,a0 if d==0 else m0,partner(i)))
    errors=[]
    by={r[0]:r for r in rows}
    for i,b,p,d,aid,fr,pi in rows:
        pr=by[pi]
        if pr[6]!=i: errors.append("not_order_two")
        if pr[4]!=aid: errors.append("aid_changed")
        if pr[5]!=reverse_orientation(fr): errors.append("mirror_bad")
        if pr[3]==d or pr[1]!=b or pr[2]!=p: errors.append("local_bad")
    checks={
        "q43_points_40":len(qpts)==40,
        "q43_lines_40":len(qlines)==40,
        "apartment_exists":len(apts)>0,
        "rows_48":len(rows)==48,
        "partner_rules":not errors,
        "duo_counts":Counter(r[3] for r in rows)==Counter({0:24,1:24}),
        "branch_counts":Counter(r[1] for r in rows)==Counter({0:12,1:12,2:12,3:12}),
        "phase_counts":Counter(r[2] for r in rows)==Counter({0:8,1:8,2:8,3:8,4:8,5:8}),
    }
    result={"theorem":"BT787 Q43 one-block mirror check","summary":{"rows":len(rows),"q43_points":len(qpts),"q43_lines":len(qlines),"apartments":len(apts)},"checks":checks,"all_checks_pass":all(checks.values()),"boundary":"One apartment block only; no global table is claimed."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["all_checks_pass"]: raise SystemExit(1)
if __name__=="__main__": main()
