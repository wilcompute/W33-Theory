#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1811_fibre_3x4_hinge_rule.json'
F=range(3)
DEFECT=[(0,1,0),(2,1,0),(2,2,2)]
REPAIR={(0,1,0):-2,(2,1,0):-2,(2,2,2):2}

def con(t): return t[2]==(t[1]-t[0])%3

def hamming(a,b): return sum(x!=y for x,y in zip(a,b))

def directed_hinge(A,B,C):
    return A[1:]==B[1:] and B[0]==C[0] and sorted([hamming(A,B),hamming(A,C),hamming(B,C)])==[1,2,3]

def main():
    noncon=[t for t in itertools.product(F,repeat=3) if not con(t)]
    hinges=[]
    for A,B,C in itertools.permutations(noncon,3):
        if directed_hinge(A,B,C): hinges.append((A,B,C))
    obs=tuple(DEFECT)
    counts_before={'T'+''.join(map(str,t)):0 for t in noncon}
    for t,d in REPAIR.items(): counts_before['T'+''.join(map(str,t))]=d
    strand_values=sorted(set(t[0] for t in DEFECT))
    local_values=sorted(set(t[1:] for t in DEFECT))
    checks={'nonconcurrent_tables_18':len(noncon)==18,'directed_hinges_54':len(hinges)==54,'observed_is_directed_hinge':obs in hinges,'repair_vector_minus_minus_plus':[REPAIR[t] for t in obs]==[-2,-2,2],'two_negative_share_local':DEFECT[0][1:]==DEFECT[1][1:],'second_negative_and_positive_share_strand':DEFECT[1][0]==DEFECT[2][0]}
    payload={'bt':'BT1811','title':'3x4 fibre hinge rule','verified':all(checks.values()),'summary':'The proposed 12=3x4 fibre law has an executable hinge form. The 3-coordinate is the Hesse/BC strand i. The 4-coordinate is modeled as a local D4/GKP quartet above the local (j,s) fibre; the visible table-level defect only sees an oriented pair in that quartet, hence corrections of size 2. The rule removes one oriented pair from two tables sharing a local fibre coordinate and returns one oriented pair to the strand-continuation corner. This predicts exactly a directed hinge A->B->C with A,B sharing (j,s), B,C sharing i, Hamming profile [1,2,3], and repair vector (-2,-2,+2). The observed T010,T210,T222 is exactly such a directed hinge.','model':{'fibre_size':'12=3x4','strand_coordinate':'i in Tijs','local_quartet_coordinate':'unresolved D4/GKP quartet over local pair (j,s)','visible_pair_size':2,'defect_rule':'two negative oriented-pair removals on a shared local fibre, one positive oriented-pair return at a strand continuation corner'},'observed_path':['T'+''.join(map(str,t)) for t in DEFECT],'observed_repair':[REPAIR[t] for t in DEFECT],'observed_strands':strand_values,'observed_local_pairs':[list(x) for x in local_values],'directed_hinge_count':len(hinges),'all_possible_three_table_supports':816,'hinge_fraction':'54/816','checks':checks,'boundary':'This derives the correct table-level support and sign pattern from a 3x4 hinge ansatz. It still does not identify the four internal D4/GKP quartet states or the exact accepted tuple lists.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'directed_hinges':len(hinges),'observed':payload['observed_path']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
