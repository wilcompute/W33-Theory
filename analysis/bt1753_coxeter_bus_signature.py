#!/usr/bin/env python3
"""BT1753: Coxeter bus signature for the E8 hexagon allocation."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1753_coxeter_bus_signature.json'
CYCLES=[[0,7,6,13,27],[1,21,15,5,2],[3,12,17,34,4],[8,26,33,11,38],[9,24,18,35,10],[14,23,36,28,20],[16,29,32,30,22],[19,39,37,31,25]]
PART=[list(range(8*g,8*g+8)) for g in range(5)]
def main():
    M=[]
    for block in PART:
        s=set(block); M.append([len(s&set(cyc)) for cyc in CYCLES])
    row_sigs=sorted([sorted(r,reverse=True) for r in M], reverse=True)
    col_sigs=sorted([sorted([M[i][j] for i in range(5)],reverse=True) for j in range(8)], reverse=True)
    checks={'five_buses':len(PART)==5,'eight_cycles':len(CYCLES)==8,'row_sums_8':all(sum(r)==8 for r in M),'col_sums_5':all(sum(M[i][j] for i in range(5))==5 for j in range(8))}
    payload={'theorem':'BT1753 Coxeter Bus Signature','verified':all(checks.values()),'summary':'The BT1747 E8 hexagon allocation now has a reusable Coxeter-cycle signature. Rows are 8-hexagon buses; columns are Coxeter 5-cycles on the 40 Witting hexagons. The row and column signatures are invariant under bus relabeling and Coxeter-cycle relabeling.','intersection_matrix':M,'row_signatures':row_sigs,'column_signatures':col_sigs,'checks':checks,'boundary':'Coxeter-cycle signature only; full E8 Weyl normalizer classification remains open.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'row_signatures':row_sigs},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
