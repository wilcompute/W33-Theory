#!/usr/bin/env python3
"""Independent GF2 rank-table audit and physical 9-set witness for the
prior full 433,517,130-node five-qubit size-eight negative search.

This does NOT independently re-run 433M DFS nodes or create DRAT/FRAT;
it verifies every GF2 rank in the 2^15 symmetric-matrix model, the eight
completed O5 representatives plus two reversed completions, and the
nine-MUB positive witness with a fresh GF2 maximality verifier.
"""
from itertools import combinations
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_five_qubit_size8_dlx as D
OUT=ROOT/"data/toe_20261114_fivequbit_MUB_fullrun_independent_rank_audit.json"

def gf2rank(code,pos,n):
    rows=[0]*n
    for k,(i,j) in enumerate(pos):
        if code>>k&1:
            rows[i]^=1<<j
            if i!=j:rows[j]^=1<<i
    rank=0
    for col in range(n):
        idx=next((r for r in range(rank,n) if rows[r]>>col&1),None)
        if idx is None:continue
        rows[rank],rows[idx]=rows[idx],rows[rank]
        for r in range(n):
            if r!=rank and rows[r]>>col&1:rows[r]^=rows[rank]
        rank+=1
    return rank

def main():
    full=json.loads((ROOT/"data/w33_five_qubit_size8_dlx_full.json").read_text())
    rev=json.loads((ROOT/"data/w33_five_qubit_size8_dlx_reverse.json").read_text())
    pos,sing,ns,I,cand,reps=D.prep(5)
    assert len(pos)==15 and len(sing)==32768 and len(ns)==13888
    assert reps==[692,693,694,695,700,701,702,703]
    # Independently rebuild ALL singular/nonsingular decisions, rather
    # than trusting the original numpy precomputed sing table.
    for code in range(1<<len(pos)):
        assert bool(gf2rank(code,pos,5)<5)==bool(sing[code]),code
    rs=full["n5_size8"]
    assert rs["n"]==5 and rs["size"]==8 and rs["status"]=="none"
    assert rs["example"] is None and len(rs["per_rep"])==8
    assert [v["s2"] for v in rs["per_rep"]]==reps
    assert all(v["found"] is None and v["timeout"] is False for v in rs["per_rep"])
    assert sum(v["nodes"] for v in rs["per_rep"])==rs["nodes"]==433517130
    # Independent second traversal uses same algorithm but different
    # branching order; both S3 equivalence reps complete.
    second=rev["n5_size8"]
    assert second["status"]=="none" and second["example"] is None
    assert len(second["per_rep"])==2
    assert [v["s2"] for v in second["per_rep"]]==[692,694]
    assert all(v["found"] is None and not v["timeout"] for v in second["per_rep"])
    assert [v["nodes"] for v in second["per_rep"]]==[54001206,53942707]
    assert [v["nodes"] for v in second["per_rep"]] != [
        rs["per_rep"][0]["nodes"],rs["per_rep"][2]["nodes"]]
    # Independent 3-qubit exact combinatorial controls (no D search).
    pos3,sing3,ns3,I3,cand3,reps3=D.prep(3)
    assert len(reps3)==2
    for code in range(1<<len(pos3)):
        assert bool(gf2rank(code,pos3,3)<3)==bool(sing3[code])
    n3status={}
    for size in (5,7):
        # n3 two fixed Pauli bases (zero and infinity) plus I,
        # second matrix representative, then size-4 additional.
        existence=[]
        for s2 in reps3:
            opts=[int(v) for v in ns3 if v not in (I3,s2)
                  and gf2rank(I3^int(v),pos3,3)==3
                  and gf2rank(s2^int(v),pos3,3)==3]
            def rec(chosen,candidates,slots):
                if slots==0:
                    return not any(all(gf2rank(q^v,pos3,3)==3
                                     for q in chosen)
                                   for v in ns3 if v not in chosen)
                for j,v in enumerate(candidates):
                    if rec(chosen+[v],
                        [w for w in candidates[j+1:] if gf2rank(v^w,pos3,3)==3],
                        slots-1):return True
                return False
            existence.append(rec([I3,s2],opts,size-4))
        n3status[str(size)]=existence
    assert n3status["5"]==[True,True]
    assert n3status["7"]==[False,False]
    # Positive 9-set: the same D search finds a fast witness. Validate
    # independently via GF2 rank for all 13,888 nonsingular matrices.
    nine=D.search_rep((5,9,692,60))
    assert nine["found"] and not nine["timeout"],nine
    codes=[int(z) for z in nine["found"]]
    assert len(codes)==7 and codes[0]==I and codes[1]==692
    assert all(gf2rank(v,pos,5)==5 for v in codes)
    assert all(gf2rank(u^v,pos,5)==5 for u,v in combinations(codes,2))
    extenders=[int(t) for t in ns if t not in codes and
        all(gf2rank(int(t)^v,pos,5)==5 for v in codes)]
    assert extenders==[]
    result=dict(status="PASS_FIVE_QUBIT_MUB_SIZE8_FULLRUN_CERTIFICATE_INDEPENDENT_GF2_AUDIT",
      n5_binary_symmetric_matrix_codes=32768,all_GF2_rank_codes_independently_checked=True,
      n5_nonsingular_symmetric_codes=13888,
      n5_O5_representatives=reps,negative_fullrun_8_reps_433517130_nodes=True,
      negative_per_rep_nodes={str(v["s2"]):v["nodes"] for v in rs["per_rep"]},
      negative_fullrun_all_no_timeout=True,
      reversed_two_S3_reps_no_witness=True,
      reversed_nodes={str(v["s2"]):v["nodes"] for v in second["per_rep"]},
      independently_enumerated_n3_size5_exists_and_n3_size7_absent=n3status,
      positive_n5_size9_codes=codes,
      positive_n5_size9_pairwise_Delta_full_rank=True,
      positive_n5_size9_maximality_all_13888_checked=True,
      five_qubit_maximal_Pauli_MUB_minimum="9 (conditional on prior full eight-orbit solver exhaustiveness)",
      limits="The 433M-node exhaustive search and reversed two-rep traversals are stored complete computational runs from one solver family. No independent full n5 size8 re-execution, DRAT proof log or external certificate checker in this script. This is not non-Pauli strongly unextendible MUB no-go.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ["status","all_GF2_rank_codes_independently_checked","negative_fullrun_8_reps_433517130_nodes","reversed_two_S3_reps_no_witness","independently_enumerated_n3_size5_exists_and_n3_size7_absent","positive_n5_size9_maximality_all_13888_checked"]},indent=2),flush=True)
    return result
if __name__=="__main__":main()
