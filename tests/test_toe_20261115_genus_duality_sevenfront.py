"""Independent seven-front genesis, topology, and physical-model regressions.

Run: py -3 -m pytest tests/test_toe_20261115_genus_duality_sevenfront.py -q
"""
import importlib.util
import math
from pathlib import Path
from collections import Counter
import pytest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261115_genus_duality_sevenfront_falsifiers.py"

@pytest.fixture(scope="module")
def m():
    spec=importlib.util.spec_from_file_location("genus_sixfront",SRC)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

@pytest.fixture(scope="module")
def top(m):
    return m.two_surface_genus_and_Fano()

@pytest.fixture(scope="module")
def frame(m):
    return m.native_W33_frame_overlap()

def test_all_seven_controls_and_written_json(m):
    all_=m.main()
    assert all_["n_controls"]==7
    assert set(all_["results"])==set(m.FRONTS)
    assert m.OUT.exists()

def test_cs_actual_7_21_14_and_dual_topology(top):
    C=top["Csaszar"]
    assert (C["V"],C["E"],C["F"],C["genus"])==(7,21,14,1)
    assert C["Betti_mod2"]==[1,2,1]
    assert C["dual_graph_bipartite"] and C["dual_graph_girth"]==6
    assert (C["dual_vertices"],C["dual_edges"],C["dual_faces"],C["dual_face_degree"])==(14,21,7,6)

def test_two_Fano_plane_decompositions_are_one_unordered(top):
    assert top["ordered_STS7_partitions"]==2
    assert top["unordered_STS7_partitions"]==1
    faces=top["Cs_partition_two_STS7"]
    for group in faces:
        assert len(group)==7
        pairs=Counter(tuple(sorted(e)) for f in group for e in __import__("itertools").combinations(f,2))
        assert len(pairs)==21 and all(count==1 for count in pairs.values())
    assert len(set(tuple(sorted(f)) for g in faces for f in g))==14

def test_N12_44faces_66edges_and_nonbipartite_dual(top):
    N=top["neighborly_genus6"]
    assert (N["V"],N["E"],N["F"],N["genus"])==(12,66,44,6)
    assert N["Betti_mod2"]==[1,12,1]
    assert (N["dual_vertices"],N["dual_edges"],N["dual_faces"],N["dual_face_degree"])==(44,66,12,11)
    assert not N["dual_graph_bipartite"]
    assert len(N["triangles"])==44
    assert "5.5" in top["genus6_STS12_impossible"]

def test_genus6_geometric_boundary_not_an_inferred_dual_no_go(top):
    assert "not automatically" in top["geometric_status"]
    assert "Schewe" in top["geometric_status"]

def test_Heawood_residues_and_JR_exception(m):
    r=m.genus_ladder_and_prior_claim_audit()
    assert r["admissible_vertex_residues_mod12"]==[0,3,4,7]
    assert r["Jungerman_Ringel_minimal_triangulations"]["2"]=={"min_vertices":10,"min_triangles":24}
    assert r["Jungerman_Ringel_minimal_triangulations"]["6"]=={"min_vertices":12,"min_triangles":44}
    assert all(x["orientable_triangular_embedding_possible"]==(x["n"]%12 in (0,3,4,7))
               for x in r["rows"])

@pytest.mark.parametrize("n,min_genus,triangle",[(4,0,True),(7,1,True),(8,2,False),(9,3,False),(12,6,True),(15,11,True)])
def test_complete_graph_genus_vs_triangular_congruence(m,n,min_genus,triangle):
    r=m.genus_ladder_and_prior_claim_audit()
    row=r["rows"][n-4]
    assert row["minimum_orientable_graph_genus"]==min_genus
    assert row["orientable_triangular_embedding_possible"]==triangle

def test_native_W33_Gram_exact_spectrum(frame):
    assert frame["n_frames"]==1620 and frame["n_rays"]==40
    assert frame["B_gram_identity"]=="B^T B=156 I+21 A_W33+6 J"
    assert frame["B_gram_eigenvalues"]=={"648":1,"198":24,"72":15}
    assert frame["frame_kernel_rank"]==40
    assert frame["frame_kernel_zero_eigenvalue_multiplicity"]==1580

def test_W33_neighborhood_is_four_K3_not_K12(frame):
    assert frame["induced_12_vertex_neighborhood"]=="4 disjoint K3, NOT K12"
    assert frame["srg_point_graph"]==[40,12,2,4]

def test_frame_overlap_complete_census(frame):
    observed={int(k):v for k,v in frame["projective_frame_overlap_census"].items()}
    assert observed=={0:1081,1:440,2:90,3:8,4:1}
    assert sum(observed.values())==1620
    assert sum(k*v for k,v in observed.items())==648
    assert frame["uniform_mean_overlap"]=="2/5"
    assert frame["sufficient_betaJ_aligned_beats_uniform"]<frame["uniform_local_spinodal_betaJ"]

def test_45_grid_sectors_and_Johnson_products_exact(frame):
    assert frame["frame_one_ray_move_graph_connected_components"]==45
    assert frame["frame_component_size_histogram"]=={"36":45} or frame["frame_component_size_histogram"]=={36:45}
    assert frame["frame_component_ray_union_sizes"]=={"8":45} or frame["frame_component_ray_union_sizes"]=={8:45}
    assert frame["frame_component_ray_membership_histogram"]=={"9":40} or frame["frame_component_ray_membership_histogram"]=={9:40}
    assert frame["frame_component_ray_sets_distinct"]==45
    assert frame["all_45_induced_point_graphs"]=="K4,4"
    assert frame["all_45_frame_transition_graphs"]=="J(4,2) Cartesian J(4,2)"
    assert frame["one_component_transition_spectrum"]=={"-4":4,"-2":12,"0":9,"2":4,"4":6,"8":1}
    assert frame["two_ray_move_graph_degree"]==90
    assert frame["two_ray_moves_within_K44_sector"]==18
    assert frame["two_ray_moves_cross_K44_sectors"]==72
    assert frame["two_ray_only_connected_components"]==1
    assert frame["one_or_two_ray_connected_components"]==1

def test_local_H27_4_cayley_pulse_construction(m):
    r=m.h27_driven_local_clock()
    assert r["Hilbert_dimension"]==27
    assert r["graph_degree_union_Xpm_Ypm"]==4
    assert r["nonzero_directed_hoppings_each_H"]==54
    assert r["recur_after_12_unit_pulses"]
    assert r["max_matrix_unitary_error"]<1e-12
    assert "time-dependent" in r["scope"]

def test_seven_KK_symmetry_vectors_not_full_mixed_tower(m):
    r=m.flux_compensated_Killing_vectors()
    assert r["sphere_Killing_generators"]==["K_x","K_y","K_z"]
    assert r["symmetry_protected_massless_5D_vector_count"]==7
    assert "uncomputed" in r["limits"]

def test_photonic_independent_calibration_shot_requirement(m):
    r=m.optical_calibration_resource_falsifier()
    assert r["n_independent_preparations_per_input_rail_sufficient"]==9580631
    assert r["n_total_16_input_preparations_sufficient"]==153290096
    assert r["calibration_to_signal_shot_ratio"]>2800
    n=r["n_independent_preparations_per_input_rail_sufficient"]
    p=16*2**17*math.exp(-n*.002**2/2)
    assert p<=.01
    assert 16*2**17*math.exp(-(n-1)*.002**2/2)>.01

def test_F8_certificate_correct_scope(m):
    r=m.F8_certified_code_space_gap()
    assert r["pass12673_certified_codespace_lower"]==2.49
    assert r["exact_witness_upper"]==pytest.approx((47-32*math.cos(2*math.pi/9))/9)
    assert r["upper_minus_codespace_lower"]==pytest.approx(.008508646688078)
    assert "no global C64" in r["limitation"]

def test_negative_control_no_nontrivial_polytopal_R3_conclusion(m):
    r=m.two_surface_genus_and_Fano()
    assert r["neighborly_genus6"]["genus"]==6
    assert "does not" not in r["geometric_status"] or "not automatically" in r["geometric_status"]
