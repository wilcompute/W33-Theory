#!/usr/bin/env python3
"""BT1766: orientation balance constraint count for the BT1760 selector."""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1766_orientation_balance_constraint.json'
TARGET=[0,4,0,4,4,2,2,4,3]
OBS=['R','R','C','C','C','C','C','R','R']
def main():
    all_assign=list(itertools.product(['C','R'], repeat=9))
    global54=[a for a in all_assign if a.count('C')==5]
    line4bal=[a for a in global54 if [a[i] for i,t in enumerate(TARGET) if t==4].count('C')==2]
    line0bal=[a for a in line4bal if [a[i] for i,t in enumerate(TARGET) if t==0].count('C')==1]
    observed_fiber=[a for a in line0bal if all(a[i]=='C' for i,t in enumerate(TARGET) if t==2) and all(a[i]=='R' for i,t in enumerate(TARGET) if t==3)]
    checks={'all_512':len(all_assign)==512,'global_5_4_count_126':len(global54)==126,'line4_balance_count_60':len(line4bal)==60,'line4_line0_balance_count_36':len(line0bal)==36,'observed_target_fiber_count_12':len(observed_fiber)==12,'observed_assignment_in_fiber':tuple(OBS) in observed_fiber}
    payload={'theorem':'BT1766 Orientation Balance Constraint','verified':all(checks.values()),'summary':'For the BT1760 target selector, orientation is not forced by the selector alone: 512 cyclic/reversed assignments exist. The global 5/4 split leaves 126; balancing line 4 leaves 60; balancing lines 4 and 0 leaves 36; requiring the observed target-fiber rule (line 2 cyclic-only and line 3 reversed-only) leaves 12 assignments, including the incumbent. Thus BT1761 balance is a strong constraint but not yet unique.','target_sequence':TARGET,'observed_orientation':OBS,'counts':{'all':len(all_assign),'global_5C_4R':len(global54),'line4_balanced':len(line4bal),'line4_and_line0_balanced':len(line0bal),'observed_target_fiber':len(observed_fiber)},'checks':checks,'boundary':'No-4/no-6 graph admissibility was not recomputed over these 12 orientations here; this is the pure target-selector orientation-count layer.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'counts':payload['counts']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
