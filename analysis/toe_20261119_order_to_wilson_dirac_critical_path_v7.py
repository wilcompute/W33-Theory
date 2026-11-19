#!/usr/bin/env python3
"""Causet -> order-only circle incidence -> conditional local Wilson fermion.

New-to-repository constructive dependency bridge. Geometry / Lorentzian
generative spacetime, antichain, cover scale, Wilson kinetic rule, spin
holonomy, gauge group and matter are still PROVIDED, not derived TOE data.
"""
from __future__ import annotations
import json,math,sys
from collections import defaultdict
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_causal_nerve_transfer_interference_flavor_v6 as prev
OUT=ROOT/"data"/"toe_20261119_causal_order_wilson_dirac_dependency_v7.json"


def recover_circle_graph_from_order(R,n,require_H1=True):
    """Only R and selected antichain size n are passed, no x coordinates.
    Witness pair affinity = cardinality of common past-shadow events.
    Retain maximal positive off-diagonal affinities to reconstruct a cycle.
    """
    R=np.asarray(R,dtype=np.uint8)
    if R.shape!=(2*n,2*n):raise ValueError("expected two equal causal layers")
    incidence=R[:n,n:].astype(np.int64)
    C=incidence.T@incidence
    homology=prev.betti_from_nerve_order(R,n)
    b0,b1=homology["betti_H0_H1_mod2"]
    if require_H1 and (b0,b1)!=(1,1):
        raise ValueError("no connected H1=1 persistence candidate; reject operator")
    off=C.copy();np.fill_diagonal(off,0)
    maximum=int(np.max(off))
    if maximum<=0:raise ValueError("disconnected witness shadows")
    edge_pairs=[(i,j) for i in range(n) for j in range(i+1,n)
                if off[i,j]==maximum]
    graph=defaultdict(set)
    for a,b in edge_pairs:
        graph[a].add(b);graph[b].add(a)
    if any(len(graph[i])!=2 for i in range(n)):
        raise ValueError("maximal-incidence affinity is not a simple circle")
    # A 2-regular connected graph with n vertices is an n-cycle.
    path=[0]
    prev_vertex=None
    for _ in range(n-1):
        options=sorted(graph[path[-1]]-{prev_vertex}) if prev_vertex is not None else sorted(graph[path[-1]])
        if not options:raise ValueError("early cycle closure")
        nxt=options[0]
        if nxt in path:raise ValueError("disconnected short cycle")
        prev_vertex=path[-1];path.append(nxt)
    if path[0] not in graph[path[-1]]:raise ValueError("not a closed n-cycle")
    assert len(set(path))==n and len(edge_pairs)==n
    return {"causal_incidence":incidence,"common_past_witness_matrix":C,
            "nerve_homology":homology,"max_offdiagonal_common_past":maximum,
            "edges":edge_pairs,"cycle_order":path}


def wilson_operator_on_recovered_cycle(reconstruction,mass,twist):
    """D=(1+m)I - T, where T follows inferred cyclic graph edges."""
    cycle=reconstruction["cycle_order"]
    n=len(cycle)
    T=np.zeros((n,n),complex)
    for k in range(n-1):
        T[cycle[k+1],cycle[k]]=1
    T[cycle[0],cycle[-1]]=np.exp(-1j*twist)
    D=(1+mass)*np.eye(n)-T
    return D


def one_case(n,r):
    R=prev.causal_ring_order(n,r)
    topo=prev.betti_from_nerve_order(R,n)
    if topo["betti_H0_H1_mod2"]!=[1,1]:
        rejected=False
        try:recover_circle_graph_from_order(R,n)
        except ValueError:rejected=True
        assert rejected
        # A max-overlap reconstruction without the topological filter can
        # return a spurious 1D cycle even if the nerve is contractible.
        spurious=False
        try:
            recovered=recover_circle_graph_from_order(R,n,require_H1=False)
            spurious=(len(recovered["edges"])==n)
        except ValueError:pass
        return {"n":n,"shadow_radius":r,"H1":topo["betti_H0_H1_mod2"][1],
           "topology_filter_rejected":rejected,
           "unfiltered_max_overlap_graph_spurious_cycle":spurious}
    rec=recover_circle_graph_from_order(R,n)
    outputs=[]
    for mass in (0.,.01,.1):
        for twist in (0.,np.pi):
            D=wilson_operator_on_recovered_cycle(rec,mass,twist)
            measured=np.linalg.det(D)
            expected=(1+mass)**n-np.exp(-1j*twist)
            assert abs(measured-expected)<1e-8
            nzero=int(np.sum(np.linalg.svd(D,compute_uv=False)<1e-9))
            outputs.append({"mass":mass,"twist":float(twist),
                "numeric_det_real":float(measured.real),
                "numeric_det_imag":float(measured.imag),
                "closed_form_det_real":float(expected.real),
                "closed_form_det_imag":float(expected.imag),
                "zero_modes":nzero})
    return {"n":n,"shadow_radius":r,
        "H0_H1":rec["nerve_homology"]["betti_H0_H1_mod2"],
        "max_affinity":rec["max_offdiagonal_common_past"],
        "edges_recovered":len(rec["edges"]),
        "all_degrees_two":True,
        "circle_order":rec["cycle_order"],
        "fermion_determinant_checks":outputs}


def label_covariance_gate(n=12,r=1,seed=20261119):
    R=prev.causal_ring_order(n,r)
    rec0=recover_circle_graph_from_order(R,n)
    P=np.random.default_rng(seed).permutation(n)
    Q=np.random.default_rng(seed+1).permutation(n)
    relabel=np.r_[P,Q+n]
    RR=R[np.ix_(relabel,relabel)]
    rec1=recover_circle_graph_from_order(RR,n)
    assert rec0["nerve_homology"]["betti_H0_H1_mod2"]==rec1["nerve_homology"]["betti_H0_H1_mod2"]
    checks=[]
    for twist in (0.,np.pi):
        d0=wilson_operator_on_recovered_cycle(rec0,.07,twist)
        d1=wilson_operator_on_recovered_cycle(rec1,.07,twist)
        assert abs(np.linalg.det(d0)-np.linalg.det(d1))<1e-9
        checks.append({"twist":twist,"abs_determinant_difference":float(abs(np.linalg.det(d0)-np.linalg.det(d1)))})
    return {"status":"PASS","permuted_antichain_and_future_witness_labels":True,
            "H1":rec1["nerve_homology"]["betti_H0_H1_mod2"][1],
            "fermion_det_invariant_under_event_relabeling":checks}


def causal_to_fermions_dependency_gate():
    """Qualitatively honest dependency ordering, not claimed theorem."""
    steps=[
       {"id":"A","name":"causal order and selected antichain","status":"synthetic input",
        "prerequisites":[]},
       {"id":"B","name":"persistent nerve topology","status":"constructed from A, independently benchmarked in 3+1 external code",
        "prerequisites":["A"]},
       {"id":"C","name":"maximal-shadow-overlap 1D ring graph","status":"constructed from B + selected resolution",
        "prerequisites":["A","B"]},
       {"id":"D","name":"Wilson 1D matter kinetic determinant on inferred cycle",
        "status":"constructed from C but Wilson rule/mass/spin twist still inserted",
        "prerequisites":["C"]},
       {"id":"E","name":"relative spin and SU2 center weights",
        "status":"toy calculated conditional on a specified matter representation",
        "prerequisites":["D"]},
       {"id":"F","name":"intrinsic 3+1 Lorentzian spin/Clifford/Dirac field",
        "status":"OPEN fundamental bottleneck","prerequisites":["B"]},
       {"id":"G","name":"physically derived 3-generation chiral matter and masses",
        "status":"OPEN fundamental bottleneck","prerequisites":["F"]},
       {"id":"H","name":"physical sector selection from actual fermionic path integral",
        "status":"OPEN requires both F and G plus quantum measure","prerequisites":["E","F","G"]},
       {"id":"I","name":"unique coupled gauge/gravity/quantum history action",
        "status":"OPEN not implied by positive gauge transfer","prerequisites":["A","G"]},
       {"id":"J","name":"positive normalized decoherence functional over unlabeled histories",
        "status":"OPEN relative bad-vs-good measure","prerequisites":["I","H"]},
       {"id":"K","name":"4D Lorentzian Einstein continuum, causal scattering and observed couplings",
        "status":"OPEN ultimate test","prerequisites":["J"]}
    ]
    idx={x["id"]:i for i,x in enumerate(steps)}
    assert all(idx[p]<idx[x["id"]] for x in steps for p in x["prerequisites"])
    first_open=[x["id"] for x in steps if x["status"].startswith("OPEN") and
               not any(steps[idx[p]]["status"].startswith("OPEN") for p in x["prerequisites"])]
    assert first_open==["F"]
    return {"status":"PASS","dependencies":steps,
      "first_open_minimum_depth_front":first_open,
      "priority_argument":"Attempt an intrinsic 3+1 causal Dirac operator on the robust antichain nerve; it unlocks mass, anomaly and determinant tests. Do not waste effort asserting a selected spin sector before this.",
      "limit":"This is a scientific dependency graph and an ordinal heuristic, not a proof of fundamental uniqueness or that a Dirac operator is mathematically sufficient to derive matter."}


def run():
    cases=[one_case(12,r) for r in range(6)]
    success=[x for x in cases if x.get("H0_H1")==[1,1]]
    assert len(success)==2 and [x["shadow_radius"] for x in success]==[1,2]
    assert one_case(20,1)["H0_H1"]==[1,1]
    result={"date":"2026-11-19","status":"PASS constructive one-dimensional order-to-Wilson bridge",
      "TOE_solved":False,"emergent_3plus1_spin_Dirac_derived":False,
      "metric_and_antichain_supplied":True,"Wilson_mass_and_spin_lift_supplied":True,
      "cases_N12_all_shadow_radii":cases,
      "N20_stable_shadow_case":one_case(20,1),
      "event_relabeling":label_covariance_gate(),
      "critical_path":causal_to_fermions_dependency_gate(),
      "most_important_falsifier":"For shadow radius r>=3 the Dowker H1 is ZERO but a maximal-overlap cycle graph may still exist; require robust topology BEFORE using that graph as physical geometry.",
      "sources":[
        "https://arxiv.org/abs/2611.06102",
        "https://github.com/stelios-tsilioukas/topology-change-in-causal-set-theory",
        "https://doi.org/10.1007/s41468-026-00239-x",
        "https://doi.org/10.1007/s11005-026-02080-w"
      ]}
    return result


def main():
    r=run()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"status":"PASS",
      "radius_H1_and_gating":[[x["shadow_radius"],x.get("H1",x.get("H0_H1",[None,None])[-1]),x.get("topology_filter_rejected",False)] for x in r["cases_N12_all_shadow_radii"]],
      "first_fundamental_gap":r["critical_path"]["first_open_minimum_depth_front"],
      "output":str(OUT)}))
if __name__=="__main__":main()
