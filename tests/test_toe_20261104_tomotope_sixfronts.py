"""Exact tomotope primary-source and cross-history physics-falsifier controls."""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import numpy as np
import pytest
import sympy as sy

ROOT=Path(__file__).resolve().parents[1]

def imp(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

@pytest.fixture(scope="module")
def source():
    return imp("tomotope_primary_verify",
               "analysis/toe_20261104_tomotope_reye_flux_invariants.py")

@pytest.fixture(scope="module")
def data(source):
    return source.main()

@pytest.fixture(scope="module")
def controls():
    return imp("tomotope_toe5",
        "analysis/toe_20261104_tomotope_fivefront_controls.py").main()

def test_paper_incidences_and_21dim_cycles(data):
    s=data["spectral"]
    assert (s["edge_nodes"],s["triangle_nodes"],s["medial_incidence_edges"])==(12,16,48)
    assert s["cycle_rank"]==21
    assert s["flags_of_full_tomotope"]==192
    assert s["girth"]==6
    assert s["shortest_six_cycles_through_each_incidence_edge"]==6

def test_reye_spectrum_and_signed_rank(data):
    s=data["spectral"];h=data["hardware_flux"]
    assert s["exact_positive_gram_charpoly"]=="z^2 (z-4)^9 (z-12)"
    assert s["unsigned_incidence_rank_exact"]==10
    assert s["signed_bipartite_adjacency_spectrum"]["zero"]==8
    assert h["one_link_pi_flux_incidence_rank"]==11
    assert h["zero_eigenmodes_before"]==8 and h["zero_eigenmodes_after"]==6

def test_q4_antipodal_incidence_isomorphism(source,data):
    _,_,B,G=source.canonical_incidence()
    _,_,Q,QG=source.q4_incidence()
    assert Q.shape==B.shape==(12,16)
    assert np.sum(Q)==np.sum(B)==48
    assert data["antipodal_q4_source"]["original_edges"]==32
    assert data["antipodal_q4_source"]["original_faces"]==24
    assert data["antipodal_q4_source"]["quotient_face_classes"]==12
    assert data["antipodal_q4_source"]["quotient_edge_classes"]==16

def test_published_Gamma96_not_monodromy18432(data,source):
    pub=source.published_group()
    assert pub.order()==96
    assert pub.derived_subgroup().order()==48
    assert pub.center().order()==1
    assert data["covers"]["tomotope_monodromy_order"]==18432
    assert data["covers"]["published_minimal_regular_cover_R2_order"]==36864
    assert data["symmetry"]["Reye_bipartite_aut_color_preserving_order"]==576
    assert data["symmetry"]["accidental_extra_symmetry_index"]==6

def test_symmetry_orbits_no_full_Gamma_three_generation_choice(data,controls):
    s=data["symmetry"]
    assert s["Gamma96_orbits_on_16_triangles"]==[16]
    assert s["selected_C3_orbits_16_triangles"]==[1,3,3,3,3,3]
    assert s["selected_C3_orbits_48_medial_flags"]==[3]*16
    assert s["nontrivial_order3_elements_in_Gamma96"]==32
    assert controls["symmetry_and_flavor"]["invariant_three_triangle_subset_under_full_Gamma_exists"] is False

def test_cross_W33_160_fixedflags_to_tomotope_48_C3_free_no_go(controls):
    x=controls["symmetry_and_flavor"]
    assert x["W33_selected_C3_fixed_160_Levi_flags"]==16
    assert x["Tomotope_any_nontrivial_Gamma96_C3_fixed_48_medial_flags"]==0
    assert x["C3_equivariant_total_map_160_W33_flags_to_48_tomotope_medial_flags_exists"] is False

def test_flux_sixth_moment_real_vs_imag(source,data):
    h=data["hardware_flux"]
    assert h["moment_differences_orders_0_through_6"]==[0,0,0,0,0,0,24]
    assert h["imaginary_return_quadrature_is_exactly_zero_for_all_real_t"]
    for row in h["simulations"]:
        t=row["time"]
        assert row["imaginary_Ramsey_quadrature_difference"]==0
        assert row["real_return_amplitude_difference"]<0
        if t<=.2:
            assert abs(row["real_return_amplitude_difference"]/
                       (-t**6/30)-1)<.03

def test_reye_subdivision_1d_first_correction(controls):
    c=controls["dimension"]
    alpha=math.acos(1/math.sqrt(3))
    assert math.isclose(c["predicted_rescaled_gap"],alpha*alpha,rel_tol=1e-12)
    assert c["metric_graph_weyl_dimension"]==1
    assert abs(c["verified_results"][-1]["leading_correction_measure"]-5/12)<.001
    for row in c["verified_results"]:
        assert row["edges"]-row["nodes"]+1==21
        if "direct_sparse_gap" in row:
            assert abs(row["first_gap"]-row["direct_sparse_gap"])<1e-8

def test_reye_gravity_positive_constraint_zero_locus(controls):
    grav=controls["gravity"]
    assert grav["Reye_cycle_rank"]==21
    assert grav["Reye_node_edge_incidence_rank"]==27
    assert grav["selected_integer_cycle_basis_covers_all_48_edges"]
    assert grav["direct_rank_preserving_identification_of_81W33_cycles_inside_Reye_H1_impossible"]
    assert not grav["nonlinear_Einstein_Dirac_algebra_derived"]

def test_cover_families_are_prior_art_arithmetic_only(data):
    cover=data["covers"]
    assert cover["cover_parameters"]==[3,5,7]
    for row in cover["table"]:
        k=row["k"]
        assert row["qk_vertices"]==4*k**3
        assert row["monodromy_order"]==36864*k**6
        assert row["monodromy_kernel_over_k1_order"]==k**6
