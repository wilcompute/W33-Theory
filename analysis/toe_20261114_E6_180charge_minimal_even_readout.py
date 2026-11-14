#!/usr/bin/env python3
"""Exact minimal unknown-charge readout for all 180 signed E6 HP3 fibers.

New theorem: 21 of 27 J-even Pauli expectations suffice and are
necessary to distinguish all 180 signed minimal charges nonadaptively.
The 72 optimal menus are complements of the 72 Schlaefli sixers.
One arbitrary axis dropout requires all 27. Adaptivity reduces the
observed number of queried axes while using the same 21-menu.

Proof: on each signed cubic triple, its four allowed sign patterns
differ in every chosen two-coordinate sign flip; hence the unmeasured
set must be an independent set in the Schlaefli 135-edge graph.
Its independence number is six. Conversely if unmeasured is
independent, each triple retains at least two measured coordinates,
and two different supports cannot share two coordinates because
each graph edge lies in exactly one triple.
"""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import json,math,sys
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261114_E6_180charge_minimal_even_readout.json"

def main():
    _,signed,_,_,_=R.load()
    assert len(signed)==45
    H=nx.Graph()
    H.add_nodes_from(range(27))
    edge_in={}
    for triple,s in signed.items():
        for u,v in combinations(triple,2):
            e=tuple(sorted((u,v)))
            assert e not in edge_in
            edge_in[e]=tuple(sorted(triple))
            H.add_edge(*e)
    assert (H.number_of_nodes(),H.number_of_edges())==(27,135)
    assert set(dict(H.degree()).values())=={10}
    sixers=sorted(tuple(sorted(c)) for c in nx.find_cliques(nx.complement(H)) if len(c)==6)
    assert len(sixers)==72
    assert max(len(c) for c in nx.find_cliques(nx.complement(H)))==6
    charges=[]
    for tri,s in signed.items():
        for signs in product((-1,1),repeat=3):
            if signs[0]*signs[1]*signs[2]!=s:continue
            z=[0]*27
            for i,x in zip(tri,signs):z[i]=x
            charges.append(tuple(z))
    assert len(charges)==len(set(charges))==180

    signatures_by_sixer=[]
    menus=[]
    for U in sixers:
        assert not any(H.has_edge(u,v) for u,v in combinations(U,2))
        selected=tuple(i for i in range(27) if i not in U)
        assert len(selected)==21
        compressed={tuple(z[i] for i in selected) for z in charges}
        assert len(compressed)==180
        menus.append(selected)
        signatures_by_sixer.append(len(compressed))
    # Every one of 72 menus is optimal. A one-erasure counterexample
    # exists for every such proper menu: an unselected u and its
    # selected neighbor v can be flipped together within one triple.
    counterexamples=0
    for U,selected in zip(sixers,menus):
        u=U[0]
        v=next(w for w in selected if H.has_edge(u,w))
        tri=edge_in[tuple(sorted((u,v)))]
        witness=next(z for z in charges if set(i for i,a in enumerate(z) if a)==set(tri))
        partner=list(witness)
        partner[u]*=-1;partner[v]*=-1;partner=tuple(partner)
        assert partner in charges and partner!=witness
        assert tuple(witness[i] for i in selected if i!=v)==tuple(partner[i] for i in selected if i!=v)
        counterexamples+=1
    assert counterexamples==72
    # If any proper selected set S distinguishes all charges, its
    # unselected complement U is independent. Pick u in U and any
    # neighbor v, necessarily in S: failing axis v creates ambiguity.
    # Conversely all 27 measured coordinates tolerate one failure.

    def decision_tree(menu):
        histogram=Counter()
        def recurse(indices,available,depth):
            if len(indices)==1:
                histogram[depth]+=1
                return
            assert available
            candidate=[]
            for a in available:
                buckets=Counter(charges[j][a] for j in indices)
                if len(buckets)==1:continue
                sz=len(indices)
                entropy=math.log(sz)-sum(n/sz*math.log(n) for n in buckets.values())
                candidate.append((-entropy,max(buckets.values()),a))
            assert candidate
            a=min(candidate)[2]
            updated=tuple(v for v in available if v!=a)
            for outcome in (-1,0,1):
                subgroup=tuple(j for j in indices if charges[j][a]==outcome)
                if subgroup: recurse(subgroup,updated,depth+1)
        recurse(tuple(range(180)),tuple(menu),0)
        assert sum(histogram.values())==180
        return histogram
    h=decision_tree(menus[0])
    expected=sum(depth*count for depth,count in h.items())/180
    maxdepth=max(h)
    assert maxdepth<=21
    alpha=.05
    def shot_bound(eta):
        n=math.ceil(8/(eta*eta)*math.log(2*21/alpha))
        assert 2*21*math.exp(-n*eta*eta/8)<=alpha
        return dict(per_observable_shots=n,prepared_copies_for_21_fixed_axes=21*n,
                    visibility=eta,familywise_error_bound=.05,
                    error_model="independent +/-1 Pauli shots, per-axis mean eta*z_i",
                    classification="round mean/eta to -1,0,+1 at halfway thresholds")
    q=json.loads((ROOT/"data/toe_20261114_hidden_qubit_12_pauli_global_tomography.json").read_text())
    assert q["global_menu_size"]==12 and q["ortools_CP_SAT_global_size_le_11"]=="INFEASIBLE"
    result=dict(status="PASS_OPTIMAL_21_OF_27_E6_CHARGE_READOUT_AND_ERASURE_NO_GO",
        signed_cubic_triples=45,Schlaefli_edges=135,
        charge_fibers=180,
        maximum_unmeasured_independent_set_size=6,
        optimal_even_observables_required=21,
        optimal_fixed_charge_readout_menu_count=72,
        each_optimal_menu_identifies_all_180=True,
        single_any_axis_failure_optimal_even_menu_size=27,
        explicit_axis_failure_witnessed_for_all_72_optimal_menus=counterexamples,
        selected_even_coordinates=menus[0],
        unselected_sixer=sixers[0],
        adaptive_greedy_axis_queries_depth_histogram={str(k):v for k,v in sorted(h.items())},
        adaptive_greedy_axis_queries_expected=expected,
        adaptive_greedy_axis_queries_worst=maxdepth,
        full_global_PAULI_menu_even_odd=21+12,
        fixed_nonadaptive_experiment_settings_per_charge_fiber=21+3,
        adaptive_greedy_expected_experiment_settings_including_qubit=expected+3,
        adaptive_greedy_worst_experiment_settings_including_qubit=maxdepth+3,
        even_Pauli_measurement_shot_bounds={"eta_1":shot_bound(1),"eta_0_8":shot_bound(.8)},
        classification_requires_known_calibrated_visibility=True,
        limitations="21 lower bound is for a fixed set of J-even Pauli expectations (not arbitrary POVMs or combined J-odd strategy). Exact patterns +/-1,0 rely on ideal 180 integral charge ensemble. 27 erasure bound is for worst-case one unavailable J-even observable; adaptive protocols with arbitrary combined observables not excluded.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in (
        "status","optimal_even_observables_required","optimal_fixed_charge_readout_menu_count",
        "single_any_axis_failure_optimal_even_menu_size",
        "adaptive_greedy_axis_queries_expected","adaptive_greedy_axis_queries_worst",
        "full_global_PAULI_menu_even_odd","fixed_nonadaptive_experiment_settings_per_charge_fiber",
        "even_Pauli_measurement_shot_bounds")},indent=2),flush=True)
    return result

if __name__=="__main__":main()
