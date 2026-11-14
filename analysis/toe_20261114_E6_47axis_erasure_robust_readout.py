#!/usr/bin/env python3
"""47-axis one-sensor-erasure-resilient full E6 charge+qubit tomography.

The split architecture has 27 J-even charge observables and 20 J-odd
logical-qubit observables. It recovers any of 180 charge labels and
the entire CP1 Bloch state after ANY one global-axis failure.
Only 21 even + 3 odd axes need be queried per reconstructed state.

Optimality applies only to separated even-charge / odd-logical
Pauli sensor menus, not arbitrary informationally complete POVMs.
"""
from pathlib import Path
from itertools import product,combinations
import json,sys
import numpy as np
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261114_E6_180charge_minimal_even_readout as O
OUT=ROOT/"data/toe_20261114_E6_47axis_erasure_robust_readout.json"
FIXED20=(1,3,12,13,14,15,21,22,24,25,36,38,40,41,42,43,49,50,62,63)

def main():
    c=O.main()
    pauli,quad,odd,triads=E.pauli_data()
    assert len(odd)==36 and len(quad)==27
    assert len(FIXED20)==20 and set(FIXED20).issubset(set(odd))
    classes={}
    for tri in sorted(triads):
        opts=[v for v in odd if all(E.omega(v,u)==0 for u in tri)]
        groups=sorted({tuple(sorted({v,v^tri[0],v^tri[1],v^tri[2]})) for v in opts})
        assert len(groups)==3 and all(len(g)==4 for g in groups)
        classes[tri]=groups
    assert len(classes)==45
    assert all(sum(v in FIXED20 for v in g)>=2 for gg in classes.values() for g in gg)

    # Independent proof-producing optimization: test whether 19
    # J-odd sensors can hit all 135 logical cosets twice.
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=8
    solver.parameters.max_time_in_seconds=90.
    m=cp_model.CpModel()
    variables={v:m.NewBoolVar(f"sensor_{v}") for v in odd}
    for groups in classes.values():
        for g in groups:m.Add(sum(variables[v] for v in g)>=2)
    m.Add(sum(variables.values())<=19)
    status=solver.Solve(m)
    assert status==cp_model.INFEASIBLE,("20-axis optimality not certified",status,solver.ResponseStats())

    dic=json.loads((ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json").read_text())
    mp={int(i):int(v) for i,v in dic["coordinate_to_pauli_label"].items()}
    flipped=set(dic["coordinate_negative_sign_indices"])
    P=[(-1 if i in flipped else 1)*pauli[mp[i]] for i in range(27)]
    _,source,_,_,_=R.load()
    charges=[]
    for tri,s in source.items():
        for p in product((-1,1),repeat=3):
            if np.prod(p)!=s:continue
            z=[0]*27
            for i,v in zip(tri,p):z[i]=v
            charges.append(tuple(z))
    assert len(charges)==180
    no_erasure_sixer=set(c["unselected_sixer"])
    # Any absent even sensor belongs to some sixer; choose that
    # sixer as the unmeasured set to retain 21 available sensors.
    sixers=[]
    import networkx as nx
    G=nx.Graph()
    G.add_nodes_from(range(27))
    for tri in source:G.add_edges_from(combinations(tri,2))
    sixers=sorted(tuple(sorted(cl)) for cl in nx.find_cliques(nx.complement(G)) if len(cl)==6)
    for i in range(27): assert any(i in U for U in sixers)
    rng=np.random.default_rng(20261114)
    I=np.eye(8,dtype=complex)
    max_res=0.
    scenarios=0
    for lost_kind,lost in [("even",i) for i in range(27)]+[("odd",j) for j in FIXED20]:
        U=next((set(s) for s in sixers if lost_kind=="even" and lost in s),no_erasure_sixer)
        chosen=tuple(i for i in range(27) if i not in U)
        assert len(chosen)==21
        assert lost_kind!="even" or lost not in chosen
        left20=set(FIXED20)-({lost} if lost_kind=="odd" else set())
        reps={}
        for tri,groups in classes.items():
            axes=[next(v for v in g if v in left20) for g in groups]
            assert len(set(axes))==3
            reps[tri]=axes
        lookup={tuple(z[i] for i in chosen):z for z in charges}
        assert len(lookup)==180
        for z in charges:
            X=sum((z[i]*P[i] for i in range(27)),np.zeros((8,8),complex))
            Pi=(I+X)/4
            assert np.max(abs(Pi@Pi-Pi))<1e-12
            vec=np.linalg.eigh(Pi)[1][:,-2:]
            psi=vec@(rng.normal(size=2)+1j*rng.normal(size=2))
            psi/=np.linalg.norm(psi)
            rho=np.outer(psi,psi.conj())
            measurements=tuple(int(round(np.vdot(psi,P[i]@psi).real)) for i in chosen)
            assert lookup[measurements]==z
            native_support=tuple(sorted(mp[i] for i,x in enumerate(z) if x))
            ax=reps[native_support]
            logical=[Pi@pauli[v]@Pi for v in ax]
            r=[float(np.vdot(psi,pauli[v]@psi).real) for v in ax]
            got=(Pi+sum((r0*L for r0,L in zip(r,logical)),np.zeros((8,8),complex)))/2
            max_res=max(max_res,float(np.max(abs(got-rho))))
            assert max_res<1e-11
            scenarios+=1
    assert scenarios==47*180
    result=dict(status="PASS_47_GLOBAL_AXES_ANY_ONE_SENSOR_ERASURE_FULL_180_FIBER_TOMOGRAPHY",
        J_even_installed_charge_axes=27,J_odd_installed_qubit_axes=20,
        global_installed_axes_total=47,
        minimal_odd_two_cover_verified_CPSAT_no19=True,
        optimality_scope="Separated even-only charge ID and odd-only logical tomography, each tolerating any one axis loss; arbitrary joint POVMs are not covered",
        failed_global_sensor_cases=47,charge_fibers_per_case=180,
        full_state_reconstructions_under_axis_failure=scenarios,
        selected_charge_observables_per_state=21,
        selected_odd_observables_per_state=3,
        selected_total_observables_per_state=24,
        max_density_matrix_reconstruction_residual=max_res,
        fixed_twenty_odd_pauli_labels=list(FIXED20),
        proof="Even branch: with any nonempty unmeasured set, one neighboring selected sensor failure hides two coordinates in a tritangent. Hence install all 27. Odd branch: each of 135 logical four-cosets must be hit at least twice; 20 construction, <=19 CP-SAT infeasible.",
        limitations="All claims assume an unknown state within 180 minimal E6 charge fibers, ideal expectation values, independent repeated preparations, and one unavailable axis. Does not correct noisy readings or photon losses during quantum evolution.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in (
      "status","global_installed_axes_total","minimal_odd_two_cover_verified_CPSAT_no19",
      "full_state_reconstructions_under_axis_failure","selected_total_observables_per_state",
      "max_density_matrix_reconstruction_residual")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
