#!/usr/bin/env python3
"""BT1764: check the 30 selector completions against the BC helix/600-cell count."""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1764_bc_helix_completion_bridge.json'
MULTI=[0,0,2,2,3]
REMAIN=[(0,0),(0,2),(1,2),(2,0),(2,2)]
CROSS={(0,1),(1,0),(1,1),(2,1)}
OBS=[[0,4,0],[4,4,2],[2,4,3]]
def main():
    comps=[]
    for vals in sorted(set(itertools.permutations(MULTI))):
        T=[[None]*3 for _ in range(3)]
        for f,p in CROSS: T[f][p]=4
        for (f,p),v in zip(REMAIN,vals): T[f][p]=v
        comps.append((vals,T))
    pair01=defaultdict(int)
    pos3=Counter()
    for vals,T in comps:
        zeros=tuple(i for i,v in enumerate(vals) if v==0)
        twos=tuple(i for i,v in enumerate(vals) if v==2)
        three=vals.index(3)
        pair01[zeros]+=1; pos3[three]+=1
    checks={'thirty_completions':len(comps)==30,'ten_zero_pair_classes':len(pair01)==10 and all(v==3 for v in pair01.values()),'five_single_three_positions':len(pos3)==5 and all(v==6 for v in pos3.values()),'observed_selector_in_completions':any(T==OBS for _,T in comps)}
    payload={'theorem':'BT1764 BC-Helix Completion Bridge','verified':all(checks.values()),'summary':'The 30 BT1763 self-frame selector completions have the same primary count as one Boerdijk-Coxeter helix ring in the 600-cell: 30 tetrahedral cells/vertices per ring. More structurally, the completions factor as 10 zero-pair choices times 3 residual arrangements, a 10x3 stratification matching the BC ring description as three great-decagon strands. This is a real count/stratification resonance, not yet an incidence/geometric isomorphism.', 'completion_count':len(comps),'factorizations':{'30':'5!/(2!*2!)','10x3':'choose two zero-slots among five, then choose which remaining pair carries line 2'},'zero_pair_classes':{str(k):v for k,v in sorted(pair01.items())},'single_3_position_classes':{str(k):v for k,v in sorted(pos3.items())},'observed_selector':OBS,'checks':checks,'boundary':'BC relation is a falsifiable bridge: count and 10x3 strand structure match a 600-cell BC ring, but no 600-cell coordinate embedding or tetrahedral adjacency map is constructed here.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'completion_count':len(comps),'zero_pair_classes':len(pair01)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
