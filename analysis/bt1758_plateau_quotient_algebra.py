#!/usr/bin/env python3
"""BT1758: quotient algebra of the BT1755 fixed-rotation plateau."""
from __future__ import annotations
from itertools import permutations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1758_plateau_quotient_algebra.json'
BASE=[(i,(i+1)%7,(i+3)%7) for i in range(7)]
BASESETS={frozenset(t) for t in BASE}
BASE_LINE=(0,1,3)
AUTO=[76,99,72,115,14,90,57,139,93]
PLATEAU={0:[15,28,50,119,133,166],1:[23,33,53,84,129,165],2:[4,47,55,114,132,163],3:[0,29,58,87,140,144],4:[25,52,91,111,141,152],5:[3,46,48,104,137,159],6:[22,40,78,105,123,162],7:[8,43,54,81,116,145],8:[11,38,49,113,128,151]}
def autos():
    out=[]
    for p in permutations(range(7)):
        if {frozenset(p[x] for x in L) for L in BASESETS}==BASESETS: out.append(p)
    return out
def main():
    A=autos(); lines=sorted(BASESETS,key=lambda s:tuple(sorted(s)))
    def image_line(ai): return frozenset(A[ai][i] for i in BASE_LINE)
    rows=[]; checks={'aut_group_168':len(A)==168,'nine_positions':len(PLATEAU)==9}
    all_ok=True
    for pos,vals in PLATEAU.items():
        base=image_line(AUTO[pos]); imgs=[image_line(v) for v in vals]
        missing=[tuple(sorted(L)) for L in lines if L not in imgs]
        all_ok = all_ok and len(set(imgs))==6 and base not in imgs and missing==[tuple(sorted(base))]
        rows.append({'position':pos,'incumbent_auto':AUTO[pos],'incumbent_base_line_image':tuple(sorted(base)),'plateau_autos':vals,'plateau_target_lines':[tuple(sorted(x)) for x in imgs],'missing_target_line':missing[0]})
    checks['each_plateau_is_six_other_target_lines']=all_ok
    checks['plateau_quotient_size_7_per_position']=all(len(r['plateau_target_lines'])+1==7 for r in rows)
    payload={'theorem':'BT1758 Fixed-Rotation Plateau Quotient Algebra','verified':all(checks.values()),'summary':'BT1755 plateau moves are not arbitrary. For each Hesse position, the six same-score plateau automorphisms send the base Fano line (0,1,3) to exactly the six Fano lines different from the incumbent target line. Thus the fixed-rotation plateau quotient per position is the seven-line Fano pencil of target-line images: one incumbent target plus six same-score alternatives. This explains the 54 = 9*(7-1) plateau count.', 'base_line':BASE_LINE,'positions':rows,'plateau_count_formula':'54 = 9 positions * 6 non-incumbent Fano target lines','checks':checks,'boundary':'This quotients the one-position plateau by target-line image. Stabilizer/orientation data inside each target-line fiber remains to be derived.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'formula':payload['plateau_count_formula']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
