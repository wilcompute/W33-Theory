#!/usr/bin/env python3
"""Independent puncture census on the proven five-qubit nine-basis rank-code
witness. Strictly NOT an exhaustive exclusion of eight bases.
"""
from __future__ import annotations
import json,itertools
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/w33_five_qubit_size9_verify.json"
OUT=ROOT/"data/toe_20261113_five_qubit_nine_puncture_census.json"
def rank2(M):
    n=5
    rows=[sum(M[i][j]<<j for j in range(n)) for i in range(n)]
    r=0
    for j in range(n):
        p=next((i for i in range(r,n) if rows[i]>>j&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(n):
            if i!=r and rows[i]>>j&1: rows[i]^=rows[r]
        r+=1
    return r
def test_code(code):
    pos=list(itertools.combinations_with_replacement(range(5),2))
    mat=[[0]*5 for _ in range(5)]
    for j,(a,b) in enumerate(pos):
        if code>>j&1:mat[a][b]=mat[b][a]=1
    return rank2(mat)==5
def verify():
    ex=json.loads(SRC.read_text(encoding="utf-8"))["example"]
    assert len(ex)==7
    nonsing=np.array([test_code(x) for x in range(32768)],dtype=bool)
    ns=np.flatnonzero(nonsing)
    assert len(ns)==13888
    assert all(nonsing[a] for a in ex)
    assert all(nonsing[a^b] for a,b in itertools.combinations(ex,2))
    full=np.array([nonsing[ns^s] for s in ex])
    assert not full.all(axis=0).any()
    rows=[]
    for i,s in enumerate(ex):
        compatible=np.logical_and.reduce(np.delete(full,i,axis=0),axis=0)
        E=ns[compatible]
        assert s in E and len(E)>=1
        # If removing s yields size eight, these are exactly the
        # currently unblocked extension matrices; no conclusion about
        # unrelated eight-sets follows.
        pair_edges=sum(bool(nonsing[int(a)^int(b)]) for a,b in itertools.combinations(E,2))
        rows.append({"removed_code":s,"extendible_candidates":len(E),
                    "puncture_can_be_extended_back":True,
                    "induced_pairwise_compatible_edges":pair_edges})
    out={"status":"PASS_EXACT_NINE_WITNESS_PUNCTURE_CENSUS",
         "seven_nonsingular_codes":ex,"full_nine_bases_verified":True,
         "nonsingular_candidate_matrices_checked":len(ns),
         "puncture_rows":rows,
         "status_eight":"still undecided; deletion of the nine-witness is not an exhaustive search",
         "lesson":"a size-eight counterexample, if any, must be independently maximal; no deduction from this one nine-set puncture census"}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return out
if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
