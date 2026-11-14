#!/usr/bin/env python3
"""Optimal 12-Pauli global J-odd menu for all 180 integral HP3 twistor fibers.

For each 45 tritangent supports the 12 J-odd Pauli labels commuting
with its two commuting J-even stabilizers partition into three
disjoint four-label logical cosets. Each coset gives one Bloch axis.
A global menu M recovers every integral fiber iff it intersects each
of 135 logical cosets. MILP+CP-SAT independently find and certify the
minimum |M|=12; all 180 quaternionic projectors and 720 random pure
states are reconstructed using only three axes from that menu.
"""
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_hidden_qubit_12_pauli_global_tomography.json"
def main():
    pauli,quad,nonquad,terms=E.pauli_data()
    triads=sorted(terms)
    assert len(triads)==45 and len(nonquad)==36
    classes=[]; tri_classes={}
    for t in triads:
        a,b,c=t
        assert a^b==c
        options=[v for v in nonquad if all(E.omega(v,u)==0 for u in t)]
        assert len(options)==12
        groups=sorted({tuple(sorted({v,v^a,v^b,v^c})) for v in options})
        assert len(groups)==3 and all(len(g)==4 for g in groups)
        assert set(sum((list(g) for g in groups),[]))==set(options)
        for x,y in combinations(groups,2):
            assert all(E.omega(u,v)==1 for u in x for v in y)
        tri_classes[t]=groups
        classes.extend(groups)
    assert len(classes)==135
    A=np.zeros((135,36),dtype=np.int64)
    for i,g in enumerate(classes):
        for v in g:A[i,nonquad.index(v)]=1
    assert np.all(A.sum(1)==4) and np.all(A.sum(0)==15)
    # Two independent exact binary optimizations. Must fail closed.
    ip=milp(c=np.ones(36),integrality=np.ones(36),
        bounds=Bounds(0,1),constraints=LinearConstraint(A,1,np.inf),
        options={"time_limit":100,"mip_rel_gap":0.0})
    assert ip.status==0 and ip.fun is not None and abs(ip.fun-12)<1e-8,ip
    milp_set=sorted(nonquad[i] for i in range(36) if ip.x[i]>.5)
    assert len(milp_set)==12 and np.all(A[:,[nonquad.index(k) for k in milp_set]].sum(1)>=1)
    mod=cp_model.CpModel()
    choose=[mod.NewBoolVar(f"q_{v}") for v in nonquad]
    for g in classes:mod.Add(sum(choose[nonquad.index(v)] for v in g)>=1)
    mod.Add(sum(choose)<=11)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=100;solver.parameters.num_search_workers=8
    stat=solver.Solve(mod)
    assert stat==cp_model.INFEASIBLE,("not yet proved 11 impossible",stat,solver.ResponseStats())
    # For every support the three cosets select logical X/Y/Z
    # operators: commute with stabilizer, anticommute pairwise.
    menu={}
    for t,groups in tri_classes.items():
        reps=[next(k for k in sorted(g) if k in milp_set) for g in groups]
        assert len(set(reps))==3
        assert all(E.omega(u,v)==1 for u,v in combinations(reps,2))
        menu[",".join(str(x) for x in t)]=reps
    I=np.eye(8,dtype=complex);rng=np.random.default_rng(20261114)
    maxerr=0.0;state_trials=0
    for t in triads:
        reps=menu[",".join(str(x) for x in t)]
        for a,b,c in product((-1,1),repeat=3):
            if a*b*c!=terms[t]:continue
            X=a*pauli[t[0]]+b*pauli[t[1]]+c*pauli[t[2]]
            Pi=(I+X)/4
            assert np.array_equal(Pi@Pi,Pi)
            assert int(round(np.trace(Pi).real))==2
            logical=[Pi@pauli[k]@Pi for k in reps]
            for k,L in zip(reps,logical):
                assert np.array_equal(L,L.conj().T)
                assert np.array_equal(L@L,Pi)
                assert np.array_equal(Pi@pauli[k],pauli[k]@Pi)
                assert abs(np.trace(L))<1e-10
            for u,v in combinations(logical,2):assert np.array_equal(u@v+v@u,np.zeros((8,8)))
            vals,basis=np.linalg.eigh(Pi)
            B=basis[:,-2:]
            assert np.max(abs(B.conj().T@B-np.eye(2)))<1e-12
            for j in range(4):
                psi=B@(rng.normal(size=2)+1j*rng.normal(size=2))
                psi/=np.linalg.norm(psi)
                r=[float(np.vdot(psi,pauli[k]@psi).real) for k in reps]
                assert abs(sum(s*s for s in r)-1)<1e-12
                reconstructed=(Pi+sum(s*L for s,L in zip(r,logical)))/2
                rho=np.outer(psi,psi.conj())
                maxerr=max(maxerr,float(np.max(abs(reconstructed-rho))))
                assert maxerr<1e-11
                state_trials+=1
    assert state_trials==720
    out=dict(status="PASS_GLOBAL_12_PAULI_MINIMUM_FOR_ALL_180_E6_TWISTOR_FIBERS",
       tritangent_supports=45,integer_charge_fibers=180,nonquadric_pauli_observables_total=36,
       logical_cosets_to_hit=135,coset_cardinality=4,cosets_containing_each_observable=15,
       global_menu_size=12,global_menu_labels=milp_set,
       exact_integer_program_36_binary_135_constraints=True,
       scipy_milp_status="OPTIMAL_12",ortools_CP_SAT_global_size_le_11="INFEASIBLE",
       orbit_local_three_axes=menu,
       pure_state_reconstruction_tests=state_trials,
       max_matrix_entry_reconstruction_error=maxerr,
       reconstruction_formula="rho=(Pi + r1 Pi P_a Pi + r2 Pi P_b Pi + r3 Pi P_c Pi)/2",
       lower_bound_per_fiber="At least 3 scalar real expectation readings for globally continuous injective S2 -> Rk; no injection for k<=2",
       caveat="Menu optimal only among fixed J-odd Pauli measurement sets for all 180 discrete integral charge fibers. Not a minimum for arbitrary POVMs or all HP3 pure charges.",
       literature="Logical qubit Pauli tomography and topology of Bloch sphere are standard. Exact 12-menu covering design is specific to this E6 180-point incidence.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:out[k] for k in ["status","global_menu_labels","global_menu_size","ortools_CP_SAT_global_size_le_11","pure_state_reconstruction_tests","max_matrix_entry_reconstruction_error"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
