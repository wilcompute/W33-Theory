"""W33 next-five-and-more reproducible regression suite.

Expensive global exhaustive witness producers are not invoked here; their
frozen certificates are checked against independent sample and identities.
"""
import json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_chamber81_commutator_graph as chamber
import w33_20261008_photon_likelihood_information as photon
import w33_20261008_polar13_hexality_smoothness_guards as guards
from w33_20261008_global_cycle_center_census import cycles
D=ROOT/"data"

def cert(name):
    return json.loads((D/name).read_text())

def test_global_noncommutation_graph_degree_and_constructed_45_maximal_clique():
    d=cert("w33_20261008_cycle_center_atlas_constructive.json")
    C=cycles(); assert len(C)==1620
    assert d["vertex_count"]==1620 and d["noncommuting_graph_degree"]==324
    assert d["noncommuting_undirected_edges"]==1620*324//2==262440
    assert d["commuting_undirected_edges"]==1048950
    assert d["noncommuting_triangle_count"]==6981120
    ix=d["largest_found_cycle_indices"]
    assert len(ix)==len(set(ix))==d["largest_found_commuting_atlas_cardinality"]==45
    pm=[];lm=[]
    for c in C:
        pm.append(sum(1<<v for v in c if v<40))
        lm.append(sum(1<<(v-40) for v in c if v>=40))
    def compatible(i,j):
        return (pm[i]&pm[j]).bit_count()==(lm[i]&lm[j]).bit_count()
    assert all(compatible(i,j) for k,i in enumerate(ix) for j in ix[k+1:])
    assert all(any(not compatible(j,i) for i in ix) for j in range(1620) if j not in ix)
    assert sum(not compatible(0,j) for j in range(1,1620))==324
    assert d["not_proven_optimal"] is True

def test_chamber81_graph_has_degree32_but_is_not_SRG():
    r=chamber.analyze()
    assert r["rank81_apartments"]==81 and r["degree_histogram"]=={32:81}
    assert r["edge_common_neighbor_histogram"]=={11:648,23:162,13:162,12:324}
    assert sum(k*v for k,v in r["edge_common_neighbor_histogram"].items())//3==5616
    assert r["is_SRG_81_32_13_12"] is False
    assert np.isclose(r["spectral_extrema"][0],-10)
    assert np.isclose(r["spectral_extrema"][1],32)
    assert sum(r["nonedge_common_neighbor_histogram"].values())==1944

def test_known_Steinberg_chamber_basis_is_not_commuting_atlas():
    r=chamber.analyze()
    assert sum(r["edge_common_neighbor_histogram"].values())==1296
    assert sum(r["nonedge_common_neighbor_histogram"].values())==1944
    assert r["intersection_signatures"]["p1_l1"]==1458

def test_permutation_invariant_optical_input_port_test():
    r=cert("w33_20261008_photon_likelihood_information.json")
    designs=r["permutation_invariant_95pct_designs"]
    assert designs["0.99"]["stages"]==72
    assert designs["0.99"]["successful_single_source_detections_sufficient_95pct"]==1075
    assert designs["0.99"]["expected_launches_under_uniform_loss_for_label_invariant_test"]==2217
    assert designs["0.98"]["stages"]==36
    assert designs["0.999"]["stages"]==144
    for depth in designs.values():
        assert depth["min_full_anonymous_sorted_linf_margin"]>0
    assert "NOT a composite-label unknown protocol" in r["bound_scope"]

def test_full_discrete_charge_anomaly_integer_bookkeeping():
    x=guards.charge_ledger()
    assert x["P6_anomaly_integer_necessary_ledgers"]=={
        "2T_SU3":18,"2T_SU2":18,"gravity":102,
        "U1Y2Z":756,"U1YZ2":288,"Z3":1854}
    assert all(v==0 for v in x["P6_mod3_checks"].values())
    assert x["dangerous_operators"]["QLDc"]["X3"]==0
    assert x["dangerous_operators"]["LLEc"]["X3"]==0
    assert x["physical_gauged_Z6_remnant_constructed"] is False

def test_natural_polar13_alt_form_has_rank2_not12():
    x=guards.polar_alternating_radical()
    assert x["polar_points"]==13
    assert x["explicit_stabilizer_invariant_alt_form_rank"]==2
    assert x["alt_form_radical_dimension"]==11
    assert x["augmentation_restriction_rank"]==0
    assert x["12D_non_degenerate_phase_space_from_13D_permutation_module"] is False

def test_complex_tetraquadric_smoothness_remains_unknown():
    x=cert("w33_20261008_polar13_hexality_smoothness_guards.json")
    for key,p in (("tetraquadric_F11",11),("tetraquadric_F13",13)):
        o=x[key]
        assert o["p"]==p
        assert o["ambient_rational_points"]==(p+1)**4
        assert o["complex_smoothness_proven"] is False
    assert x["tetraquadric_F11"]["singular_Fp_rational_points"]==2

def test_frozen_results_have_no_physical_overclaim():
    a=cert("w33_20261008_cycle_center_atlas_constructive.json")
    b=cert("w33_20261008_photon_likelihood_information.json")
    c=cert("w33_20261008_polar13_hexality_smoothness_guards.json")
    assert a["not_proven_optimal"]
    assert "no device errors" in b["interpretation"]
    assert c["discrete_P6"]["physical_gauged_Z6_remnant_constructed"] is False

def test_selected_45_apartment_atlas_has_exact_20_term_integer_relation():
    data=cert("w33_20261008_cycle_atlas_homology_rank.json")
    atlas=cert("w33_20261008_cycle_center_atlas_constructive.json")
    C=cycles()
    coefficients=data["primitive_integral_relation_coefficients"]
    assert len(coefficients)==len(atlas["largest_found_cycle_indices"])==45
    assert data["homology_ranks"]=={"F2":44,"F3":44,"F5":44,"Q":44}
    assert data["primitive_relation_support_size"]==20
    assert sorted(set(coefficients))==[-1,0,1]
    assert coefficients.count(1)==11 and coefficients.count(-1)==9
    from w33_20261008_six_toe_frontier_followthrough import levi_graph
    g=levi_graph()
    E=sorted((min(a,b),max(a,b)) for a,b in g.edges())
    eidx={e:i for i,e in enumerate(E)}
    z=[0]*160
    for weight,cid in zip(coefficients,atlas["largest_found_cycle_indices"]):
        if weight==0:continue
        cyc=C[cid]
        for u,v in zip(cyc,cyc[1:]+cyc[:1]):
            z[eidx[min(u,v),max(u,v)]]+=weight*(1 if u<40 else -1)
    assert all(w==0 for w in z)

def test_branched_20_apartment_cell_complex_has_integral_homology_of_torus():
    from w33_20261008_twenty_apartment_cell_homology import main
    x=main()
    assert x["CW_cells_V_E_F"]==[40,60,20]
    assert x["homology_betti_H0_H1_H2"]==[1,2,1]
    assert x["integral_H0_H1_H2"]==["Z","Z^2","Z"]
    assert x["euler_characteristic"]==0
    assert x["chain_boundary_ranks_over_Q"]==[39,19]
    assert x["H1_torsion_invariant_factors"]==[]
    assert x["smith_d2_nonzero_diagonal_histogram"]=={1:19}
    assert x["smith_d1_nonzero_diagonal_histogram"]=={1:39}
    assert x["octagon_edge_face_multiplicity_histogram"]=={2:40,4:20}
    assert x["skeleton_vertex_degree_histogram"]=={3:40}
    assert "non-manifold" in x["topological_type"]
