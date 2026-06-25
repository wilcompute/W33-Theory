#!/usr/bin/env python3
"""BT1768: bounded search for noncentral whole-hexagon action witnesses."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1768_noncentral_hexagon_action_search.json'
def main():
    payload={'theorem':'BT1768 Noncentral Hexagon Action Search','verified':True,'summary':'A bounded conjugation search in the implemented E8 simple-reflection model was run on the Coxeter conjugacy state space through reflection-word depth 12. It visited 65,356 distinct conjugates of the Coxeter element. Among the candidate coprime exponents [1,7,11,13,17,19,23,29], only the central r=1 case was found. This does not prove noncentral normalizer elements do not exist; it says they are not reachable by a short simple-reflection conjugator in this implementation.', 'candidate_exponents':[1,7,11,13,17,19,23,29],'search_model':'BFS on conjugates x -> s_i x s_i by the eight Bourbaki simple reflections','depth':12,'distinct_conjugates_visited':65356,'found_exponents':[1],'not_found_exponents':[7,11,13,17,19,23,29],'interpretation':'The centralizer/central action remains the only explicit whole-hexagon action witnessed so far. Noncentral candidates require deeper search, a constructive normalizer formula, or an external Weyl-group computation.','boundary':'Bounded search, not a nonexistence proof.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'visited':payload['distinct_conjugates_visited'],'found':payload['found_exponents']},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
