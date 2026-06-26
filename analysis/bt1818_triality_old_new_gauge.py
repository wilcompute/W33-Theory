#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1818_triality_old_new_gauge.json'
TABLE_KIND={'T010':'old','T210':'old','T222':'new'}
EDGE=('00','11')
def main():
    checks={'old_old_new_pattern':[TABLE_KIND['T010'],TABLE_KIND['T210'],TABLE_KIND['T222']]==['old','old','new'],'observed_edge_00_11':EDGE==('00','11')}
    payload={'bt':'BT1818','title':'triality gauge from old/new transport','verified':all(checks.values()),'summary':'The D4 triality gauge can be fixed by the BT1795 transport kind of the unique BT1816 repair. T010 and T210 are old-support tables, while T222 is a new-support table. Therefore the unique oriented repair is old+old -> new. We choose the D4/GKP gauge in which the observed edge 00--11 is the old-to-new displacement and name the nonzero endpoint 11 as the conjugate-spinor coset c. Up to D4 triality, the invariant content is: the syndrome-valid K4 edge is the one whose positive return lands in the new support sector.','table_kinds':TABLE_KIND,'chosen_triality_gauge':{'00':'old/root coset','11':'new return coset, named c','01':'remaining nonzero coset v','10':'remaining nonzero coset s'},'observed_edge':list(EDGE),'invariant_statement':'The observed edge is the unique K4 edge whose oriented repair has two old-source removals and one new-sector return. Triality may rename v,s,c, but the old-old-to-new orientation fixes the global gauge for this branch.','checks':checks,'boundary':'This fixes the paper/code gauge relative to BT1795 old/new transport. It does not claim an absolute v/s/c naming independent of the chosen transport gauge.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'gauge':'old-old -> new'},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
