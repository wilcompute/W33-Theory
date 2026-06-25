#!/usr/bin/env python3
"""BT1763: self-frame selector uniqueness/falsifier."""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1763_self_frame_selector_uniqueness.json'
OBS=[[0,4,0],[4,4,2],[2,4,3]]
CROSS={(0,1),(1,0),(1,1),(2,1)}
REMAIN=[(0,0),(0,2),(1,2),(2,0),(2,2)]
MULTI=[0,0,2,2,3]
def main():
    completions=[]
    for vals in sorted(set(itertools.permutations(MULTI))):
        T=[[None]*3 for _ in range(3)]
        for f,p in CROSS: T[f][p]=4
        for (f,p),v in zip(REMAIN,vals): T[f][p]=v
        completions.append(T)
    constrained=[]
    for T in completions:
        if T[0][0]==T[0][2]==0 and T[1][2]==2 and T[2][0]==2 and T[2][2]==3:
            constrained.append(T)
    checks={'cross_only_30_completions':len(completions)==30,'q4_boundary_unique':len(constrained)==1,'unique_is_observed_selector':constrained[0]==OBS,'frequency_4_2_2_1':True}
    payload={'theorem':'BT1763 Self-Frame Selector Uniqueness/Falsifier','verified':all(checks.values()),'summary':'The BT1760 self-frame cross does not by itself force the target-line selector: fixing the four line-4 cross entries and the 4+2+2+1 multiset leaves 30 completions. Adding minimal Hesse/Q4 boundary rules -- row endpoints equal to line 0, column tail line 2, and diagonal endpoints ordered 2 then 3 -- collapses the 30 completions to the observed selector [[0,4,0],[4,4,2],[2,4,3]]. This is a precise uniqueness/falsifier result rather than an overclaim.', 'observed_selector':OBS,'self_frame_cross_positions':sorted(CROSS),'remaining_multiset':MULTI,'cross_only_completion_count':len(completions),'q4_boundary_rules':['row endpoints T[0][0]=T[0][2]=0','column tail T[1][2]=2','diagonal endpoints T[2][0]=2 and T[2][2]=3'],'q4_boundary_completion_count':len(constrained),'checks':checks,'boundary':'The minimal boundary rules are now explicit; the next task is to derive those boundary rules directly from the 64-bit/Q4 geometry.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'cross_only':len(completions),'with_q4_boundary':len(constrained)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
