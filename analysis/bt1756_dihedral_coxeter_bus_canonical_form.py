#!/usr/bin/env python3
"""BT1756: dihedral Coxeter-cycle canonical form for E8 bus partitions."""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1756_dihedral_coxeter_bus_canonical_form.json'
CYCLES=[[0,7,6,13,27],[1,21,15,5,2],[3,12,17,34,4],[8,26,33,11,38],[9,24,18,35,10],[14,23,36,28,20],[16,29,32,30,22],[19,39,37,31,25]]
PART=[list(range(8*g,8*g+8)) for g in range(5)]
def dnorm(w):
    w=list(w); n=len(w); vs=[]
    for s in range(n):
        r=tuple(w[s:]+w[:s]); vs.append(r); vs.append(tuple(reversed(r)))
    return min(vs)
def main():
    color={}
    for b,block in enumerate(PART):
        for h in block: color[h]=b
    words=[tuple(color[h] for h in cyc) for cyc in CYCLES]
    best=None; best_perm=None
    for perm in itertools.permutations(range(5)):
        sig=tuple(sorted(dnorm(tuple(perm[x] for x in w)) for w in words))
        if best is None or sig<best: best=sig; best_perm=perm
    checks={'eight_cycle_words':len(words)==8,'word_length_5':all(len(w)==5 for w in words),'best_signature_8_words':len(best)==8,'bus_permutation_is_identity':best_perm==(0,1,2,3,4)}
    payload={'theorem':'BT1756 Dihedral Coxeter Bus Canonical Form','verified':all(checks.values()),'summary':'BT1753 is upgraded from row/column signatures to a canonical form under bus relabeling plus independent dihedral rotations/reflections of each Coxeter 5-cycle. This is the natural combinatorial normalizer of the eight Coxeter 5-cycles on the 40 E8/Witting hexagons. The sorted BT1747 partition has canonical word signature shown here.','cycle_bus_words':[list(w) for w in words],'canonical_dihedral_signature':[list(w) for w in best],'best_bus_permutation':list(best_perm),'checks':checks,'boundary':'This is the canonical form under the Coxeter-cycle dihedral wreath model, not the full E8 Weyl normalizer.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'canonical_words':payload['canonical_dihedral_signature']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
