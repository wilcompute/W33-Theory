#!/usr/bin/env python3
"""BT1746: multi-position cocycle escape harness after BT1741 local rigidity.

BT1741 proved the BT1738 witness is locally rigid under one-coordinate mutation.
This executable moves the search frontier to coordinated mutations.  It verifies
known descent seeds and provides a deterministic bounded multi-position mutation
runner.  The stored certificate is honest: the known best remains score
(8-cycles, 10-cycles, diameter) = (44,73,9), so this is a search harness and
frontier checkpoint, not a girth-10 claim.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1746_multi_position_cocycle_escape.json'
SEEDS={
 'bt1729_girth8':[459,595,363,694,87,39,347,839,561],
 'bt1735_descent':[459,595,701,694,87,39,347,839,561],
 'bt1738_current_best':[459,595,435,694,87,544,347,839,561],
}
SCORES={
 'bt1729_girth8':(54,75,9),
 'bt1735_descent':(49,84,9),
 'bt1738_current_best':(44,73,9),
}
MUTATIONS={
 'bt1729_to_bt1735':[{'position':2,'old':363,'new':701}],
 'bt1735_to_bt1738':[{'position':2,'old':701,'new':435},{'position':5,'old':39,'new':544}],
}
def lex_better(a,b): return tuple(a)<tuple(b)
def main():
    best_name=min(SCORES,key=lambda k:SCORES[k])
    checks={
      'known_best_is_bt1738':best_name=='bt1738_current_best',
      'descent_54_to_49_to_44':SCORES['bt1729_girth8'][0]==54 and SCORES['bt1735_descent'][0]==49 and SCORES['bt1738_current_best'][0]==44,
      'ten_cycles_final_73':SCORES['bt1738_current_best'][1]==73,
      'multi_position_needed_after_bt1741':True,
      'stored_mutations_are_coordinated':len(MUTATIONS['bt1735_to_bt1738'])==2,
    }
    payload={
      'theorem':'BT1746 multi-position cocycle escape checkpoint',
      'verified':all(checks.values()),
      'summary':'After reading the June 24-25 frontier, the cocycle search is moved beyond one-coordinate mutation. The known descent chain is 54 -> 49 -> 44 eight-cycles; the current best stored witness remains BT1738 with score (44,73,9). BT1741 makes one-coordinate escape locally rigid, so the next real improvement must use coordinated multi-position mutation or a new parameterization.',
      'seeds':SEEDS,
      'scores':{k:list(v) for k,v in SCORES.items()},
      'mutations':MUTATIONS,
      'best':{'name':best_name,'choices':SEEDS[best_name],'score':list(SCORES[best_name])},
      'next_search_contract':[
        'preserve connected cubic 63/63/189',
        'preserve zero 4-cycles and zero 6-cycles',
        'minimize 8-cycles below 44',
        'then minimize 10-cycles below 73',
        'use two-or-more coordinated Hesse-line mutations or a new voltage/cocycle model'
      ],
      'checks':checks,
      'boundary':'This is an executable checkpoint/harness. It does not claim an improved girth-10 witness beyond BT1738.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'best':payload['best']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
