#!/usr/bin/env python3
"""Independent OR-Tools CP-SAT *necessary-condition relaxation* for
five-qubit size-eight unextendible Pauli MUB.

Fix 0, infinity, I, one S2 representative (two S3 classes).
Seek four additional nonsingular symmetric 5x5 binary matrices whose
'singularity neighborhoods' COVER all 2336 remaining eligible matrices,
without requiring those four themselves to be pairwise disjoint.

If this relaxation is INFEASIBLE on BOTH reps, size-eight impossible.
If FEASIBLE or UNKNOWN, does NOT settle size-eight; explicitly test the
candidate's missing compatibility. Fail closed on 25s cap per class.
"""
from pathlib import Path
import json,sys,time
import numpy as np
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_five_qubit_size8_dlx as D
OUT=ROOT/"data/toe_20261113_fivequbit_size8_cpsat_cover_relaxation.json"

def one(rep,pre,limit=25):
    pos,sing,ns,I,cand,reps=pre
    universe=ns[~sing[ns^I]&~sing[ns^rep]&(ns!=I)&(ns!=rep)]
    assert len(universe)==2336
    n=len(universe)
    model=cp_model.CpModel()
    x=[model.NewBoolVar("c"+str(i)) for i in range(n)]
    model.Add(sum(x)==4)
    t0=time.monotonic()
    deg=[]
    for code in universe:
        killers=np.flatnonzero(sing[universe^code] | (universe==code))
        deg.append(len(killers))
        model.AddBoolOr([x[int(i)] for i in killers])
    build=time.monotonic()-t0
    solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=limit
    solver.parameters.num_search_workers=6
    solver.parameters.random_seed=20261113
    status=solver.Solve(model)
    name=solver.StatusName(status)
    choice=[]
    compat_pairs=None
    if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        choice=[int(universe[i]) for i in range(n) if solver.Value(x[i])]
        assert len(choice)==4
        incompat=sum(bool(sing[a^b]) for p,a in enumerate(choice) for b in choice[p+1:])
        compat_pairs=int(incompat==0)
        assert all(any(sing[t^v] or t==v for v in choice) for t in universe)
    result={"class_representative":rep,"status":name,
            "relaxation_is_necessary_not_sufficient":True,
            "build_wall_s":round(build,2),"solve_wall_s":round(solver.WallTime(),2),
            "solver_best_bound":float(solver.BestObjectiveBound()),
            "exact_coverage_constraints":n,
            "num_candidates":n,
            "killer_degree_min_median_max":[int(min(deg)),float(np.median(deg)),int(max(deg))],
            "candidate_four_matrix_codes":choice,
            "candidate_pairwise_compatible":bool(compat_pairs) if compat_pairs is not None else None,
            "interpretation":"INFEASIBLE proves no size-eight for this representative; FEASIBLE unless compatible is only cover (and does not prove a MUB), UNKNOWN is not a proof."}
    return result

def main():
    pre=D.prep(5)
    assert pre[-1]==[692,693,694,695,700,701,702,703]
    results=[]
    for rep in (692,694):
        x=one(rep,pre)
        results.append(x)
        print("RELAX",rep,x["status"],"build",x["build_wall_s"],"solve",x["solve_wall_s"],
              "pairwise",x["candidate_pairwise_compatible"],flush=True)
    if any(x["candidate_pairwise_compatible"] for x in results):
        status="EXISTS_REQUIRES_FULL_INDEPENDENT_WITNESS_VALIDATION"
    elif all(x["status"]=="INFEASIBLE" for x in results):
        status="NO_SIZE8_UNDER_CERTIFIED_TWO_CLASS_REDUCTION"
    else:
        status="UNDECIDED_SIZE8"
    out={"schema":"toe.5qubit.8MUB.CPSAT.relaxation.v1",
         "status":status,
         "results":results,
         "scope":"No negative result unless CP-SAT proves INFEASIBLE for both exact covering relaxations, and no positive result unless independent full-spread verification of compatible example."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("FINAL",status,flush=True)
    return out
if __name__=="__main__":main()
