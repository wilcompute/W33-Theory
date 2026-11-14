#!/usr/bin/env python3
"""Optimal single-sensor-failure-tolerant hidden-qubit Pauli menus.

The prior 12-observable menu hits each of 135 logical-Pauli cosets
once. For arbitrary loss of ONE globally selected observable the
menu must hit every four-label coset at least TWICE. Prove minimum
via independent SciPy/HiGHS MILP and OR-Tools CP-SAT contradiction
for one fewer, then verify every possible dropout by integers.
"""
from itertools import combinations
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_pauli_global_dropout_resilient_tomography.json"

def main():
    P,quad,nonquad,terms=E.pauli_data()
    assert len(nonquad)==36 and len(terms)==45
    classes=[]
    for a,b,c in sorted(terms):
        assert a^b==c
        opts=[g for g in nonquad if all(E.omega(g,u)==0 for u in (a,b,c))]
        groups=sorted({tuple(sorted({g,g^a,g^b,g^c})) for g in opts})
        assert len(groups)==3 and all(len(z)==4 for z in groups)
        classes+=groups
    assert len(classes)==135
    A=np.zeros((135,36),dtype=np.int64)
    for i,coset in enumerate(classes):
        for a in coset:A[i,nonquad.index(a)]=1
    assert list(sorted(set(A.sum(0))))==[15]
    results={}
    for redundancy in (1,2):
        ip=milp(c=np.ones(36),integrality=np.ones(36),
          bounds=Bounds(0,1),constraints=LinearConstraint(A,redundancy,np.inf),
          options={"time_limit":80,"mip_rel_gap":0.0})
        assert ip.status==0 and ip.fun is not None,ip
        chosen=sorted(nonquad[i] for i in range(36) if ip.x[i]>.5)
        N=len(chosen);assert abs(ip.fun-N)<1e-8
        idx=[nonquad.index(x) for x in chosen]
        coverage=A[:,idx].sum(1)
        assert coverage.min()>=redundancy
        model=cp_model.CpModel();z=[model.NewBoolVar("x"+str(i)) for i in range(36)]
        for row in A:model.Add(sum(z[j] for j,v in enumerate(row) if v)>=redundancy)
        model.Add(sum(z)<=N-1)
        solver=cp_model.CpSolver()
        solver.parameters.max_time_in_seconds=85
        solver.parameters.num_search_workers=8
        outcome=solver.Solve(model)
        assert outcome==cp_model.INFEASIBLE,(redundancy,outcome,solver.ResponseStats())
        if redundancy==2:
            for failed in chosen:
                remain=[i for i,x in enumerate(nonquad) if x in chosen and x!=failed]
                assert (A[:,remain].sum(1)>=1).all()
        results[str(redundancy)]={"minimum_menu":N,"chosen_Pauli_labels":chosen,
          "coset_hits_min":int(coverage.min()),
          "coset_hits_max":int(coverage.max()),
          "CP_SAT_menu_size_minus_one":"INFEASIBLE",
          "all_single_sensor_dropout_patterns_verified":N if redundancy==2 else None}
    assert results["1"]["minimum_menu"]==12
    out=dict(status="PASS_MINIMAL_GLOBAL_ONE_SENSOR_DROPOUT_TOLERANT_PAULI_TOMOGRAPHY",
       cosets=135,Pauli_candidate_observables=36,instances=results,
       model="Any single chosen sensor globally fails: redundant menu keeps all three logical Pauli cosets covered for every one of 180 integral charge fibers.",
       limitations="Robust to one global axis being unavailable, not qubit erasure, unknown charge, correlated readout noise, or arbitrary POVMs.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2),flush=True)
    return out
if __name__=="__main__":main()
