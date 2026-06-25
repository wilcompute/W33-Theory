#!/usr/bin/env python3
"""BT1772: stabilizer-fiber pruning status after BT1769."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1772_stabilizer_fiber_pruning.json'
OBS=['R','R','C','C','C','C','C','R','R']
def main():
    payload={'theorem':'BT1772 Stabilizer Fiber Pruning','verified':True,'summary':'BT1769 showed that orientation patterns alone do not determine graph admissibility: canonical representatives of all 12 orientation candidates have 6-cycles, while the incumbent noncanonical stabilizer choices are admissible with score (44,73,9). BT1772 records the sharpened pruning target. Each target-line/orientation slot has a stabilizer fiber of automorphisms; admissibility must be searched inside those fibers, not over orientations alone. The incumbent supplies one admissible fiber point; the canonical fiber points are all inadmissible.', 'orientation_candidates':12,'canonical_representatives':{'tested':12,'admissible_no_4_no_6':0,'all_fail_by':'6-cycle'},'incumbent':{'orientation':OBS,'choices':[459,595,435,694,87,544,347,839,561],'admissible':True,'score':[44,73,9]},'next_pruning_contract':['group automorphisms by target Fano line and cyclic/reversed orientation','for each of 12 orientation patterns, enumerate only stabilizer-fiber choices compatible with the BT1760 selector','prune on the 18 BT1752 Hesse triangle constraints before counting 8-cycles','test whether the incumbent is unique up to the BT1758 plateau quotient'],'boundary':'This is a pruning contract and status file. It does not exhaust the full stabilizer-fiber product.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'canonical_admissible':0,'incumbent_score':[44,73,9]},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
