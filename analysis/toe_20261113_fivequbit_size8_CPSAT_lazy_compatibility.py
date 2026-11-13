#!/usr/bin/env python3
"""Full five-qubit size-8 unextendible Pauli MUB constraint generation.

Two S3 classes 692,694; exact all 2336 coverage clauses, 4 chosen
symmetric-matrix codes. Start with coverage relaxation and ITERATIVELY
insert valid pairwise incompatibility cuts for each false witness.
If any pairwise-compatible cover exists, verify all 8 Lagrangians
and unextendibility using an independent full 32^? rank-code check.
If solver is INFEASIBLE after some valid cuts, this is a complete
class no-go provided CP-SAT status is truly INFEASIBLE.
Otherwise UNKNOWN — no false proofs from timeouts.
"""
from pathlib import Path
import json,sys,time
from itertools import combinations
import numpy as np
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_five_qubit_size8_dlx as D
OUT=ROOT/"data/toe_20261113_fivequbit_size8_lazy_cpsat_full_compatibility.json"

def independently_verify(pre,rep,picks):
    pos,sing,ns,I,cand,reps=pre
    chosen=[int(I),int(rep)]+[int(z) for z in picks]
    assert len(chosen)==6 and len(set(chosen))==6
    for a,b in combinations(chosen,2):
        assert not sing[a^b],(a,b)
    for z in ns:
        if z not in chosen:
            assert any(sing[z^x] for x in chosen),int(z)
    return {"symmetric_matrices_including_I_and_S2":chosen,
            "Pauli_Lagrangians_count_including_0_and_infinity":8,
            "pairwise_disjoint_rank_codes":True,
            "all_nonsingular_symmetric_extenders_blocked":True}

def run(pre,rep,limit=55):
    pos,sing,ns,I,cand,reps=pre
    universe=ns[~sing[ns^I]&~sing[ns^rep]&(ns!=I)&(ns!=rep)]
    assert len(universe)==2336 and rep in reps
    n=len(universe)
    model=cp_model.CpModel()
    x=[model.NewBoolVar(f"s{i}") for i in range(n)]
    model.Add(sum(x)==4)
    for val in universe:
        killers=np.flatnonzero(sing[universe^val]|(universe==val))
        assert len(killers)>0
        model.AddBoolOr([x[int(k)] for k in killers])
    t0=time.perf_counter()
    cuts=set()
    rounds=0;status="UNKNOWN";witness=None;last_violation=0
    counts=[]
    while time.perf_counter()-t0<limit:
        solver=cp_model.CpSolver()
        solver.parameters.max_time_in_seconds=min(18.0,max(.25,limit-(time.perf_counter()-t0)))
        solver.parameters.num_search_workers=6
        solver.parameters.random_seed=20261113+rounds%101
        result=solver.Solve(model)
        name=solver.StatusName(result)
        if result==cp_model.INFEASIBLE:
            status="PROVED_INFEASIBLE"
            break
        if result not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            status="UNKNOWN"
            break
        indices=[i for i in range(n) if solver.Value(x[i])]
        assert len(indices)==4
        incompatible=[]
        for i,j in combinations(indices,2):
            if sing[universe[i]^universe[j]]:
                incompatible.append((i,j))
        rounds+=1;last_violation=len(incompatible)
        if not incompatible:
            witness=independently_verify(pre,rep,[universe[i] for i in indices])
            status="EXISTS_VALID_SIZE8"
            break
        for a,b in incompatible:
            edge=(a,b)
            assert edge not in cuts, "violated pair cut already imposed"
            cuts.add(edge)
            model.AddBoolOr([x[a].Not(),x[b].Not()])
        if rounds%5==0:
            print("PROGRESS",rep,"rounds",rounds,"cuts",len(cuts),"elapsed",round(time.perf_counter()-t0,1),flush=True)
    elapsed=round(time.perf_counter()-t0,2)
    return {"class_rep":int(rep),"status":status,"elapsed_seconds":elapsed,
            "modeling":"Exact 2336 covering clauses plus lazily added VALID pairwise-compatibility no-good cuts",
            "cut_iterations":rounds,"pairwise_nogood_cuts_added":len(cuts),
            "last_fake_witness_number_incompatible_pairs":last_violation,
            "valid_full_witness":witness,
            "proof_boundary":"No absence proof for UNKNOWN or non-compatible feasible examples; if both S3 representatives return PROVED_INFEASIBLE and no valid witness exists, a size-eight no-go would follow subject to an independently checkable SAT proof, which CP-SAT does not export here."}

def main():
    p=D.prep(5)
    assert p[-1]==[692,693,694,695,700,701,702,703]
    results=[]
    for rep in (692,694):
        q=run(p,rep)
        results.append(q)
        print("FINAL_REP",rep,q["status"],"iterations",q["cut_iterations"],"cuts",q["pairwise_nogood_cuts_added"],"time",q["elapsed_seconds"],flush=True)
        if q["status"]=="EXISTS_VALID_SIZE8":break
    status=("EXISTS_VALID_SIZE8" if any(r["status"]=="EXISTS_VALID_SIZE8" for r in results)
           else "PROVED_NO_SIZE8_CPSAT_TWO_CLASSES" if len(results)==2 and all(r["status"]=="PROVED_INFEASIBLE" for r in results)
           else "UNDECIDED_SIZE8")
    out={"status":status,"results":results,
         "two_S3_classes_checked":[r["class_rep"] for r in results],
         "positive_control":"A full candidate requires 0, infinity, I, S2 plus 4 candidates; every pair sum nonsingular and all nonsingular extenders blocked",
         "boundary":"A bounded lazy-cut search must NOT be relabeled as infeasibility. Full certified UNSAT would require reproducible solver settings and independent proof checks."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("OVERALL",status,flush=True)
    return out
if __name__=="__main__":main()
