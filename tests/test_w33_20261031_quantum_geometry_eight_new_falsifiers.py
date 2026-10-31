"""Regression for eight additional W33 quantum geometry and physics audits."""
import math
import numpy as np
import pytest
from analysis import w33_20261031_quantum_geometry_eight_new_falsifiers as E
from analysis import w33_20261031_same_subgroup_ambient_lift_audit as L
from analysis import w33_20261031_full_subgroup_GF5_representation as R
from analysis.w33_20261031_torsion_order5_probe import rk,ker

@pytest.fixture(scope="module")
def packet():
    return {"lifts":L.build(),"group":R.build(),"other":E.build()}

def test_all_projective_GF9_lifts(packet):
    d=packet["lifts"]["lifts"]
    for k in ("2","3","5"):
        assert d[k]["status"]=="LIFT_FOUND"
        x=d[k]["lift"]
        assert x["certified_all_820_points"]and x["certified_all_820_lines"]
        assert x["frobenius_exponent"]==1
    assert d["generated_graph_group_order"]==120

def test_group_is_A5_times_C2_not_S5_or_binary(packet):
    d=packet["group"]
    assert d["projective_group_order"]==120
    assert d["derived_subgroup_order"]==d["perfect_derived_subgroup_order"]==60
    assert d["group_center_order"]==2 and d["derived_subgroup_center_order"]==1
    assert d["all_group_products_verified"]==360

def test_faithful_seven_dim_Gf5_module(packet):
    d=packet["group"]
    assert d["GF5_representation_image_order"]==120
    assert d["GF5_commutant_dimension"]==3
    assert d["GF5_invariant_vector_dimension"]==1
    assert d["central_even_module_dimension"]==4
    assert d["central_odd_module_dimension"]==3
    assert d["order5_nilpotent_ranks"]==[7,4,2,0,0,0]
    assert d["GF5_trivial_one_dim_summand_splits"]
    assert d["even3_irreducible_over_GF5"] and d["odd3_irreducible_over_GF5"]
    assert d["even3_odd3_derived_A5_hom_dimension"]==1

def test_reconstructed_mod5_group_relations(packet):
    acts={int(k):np.array(v,dtype=np.int64)for k,v in packet["group"]["GF5_generator_actions"].items()}
    for k,M in acts.items():
        assert np.array_equal(np.linalg.matrix_power(M,k)%5,np.eye(7,dtype=np.int64))
    Z=np.array(packet["group"]["central_element_GF5_action"],dtype=np.int64)
    assert np.array_equal(Z@Z%5,np.eye(7,dtype=np.int64))
    assert all(np.array_equal(M@Z%5,Z@M%5)for M in acts.values())

def test_prime_specific_saturated_kernel_equivalence(packet):
    d=packet["group"]
    assert d["canonical_5torsion_identification_verified"]
    assert "saturated rank-6" in d["canonical_5torsion_proof"]

def test_wilson_loop_U1_gauge_invariance(packet):
    d=packet["other"]["parts"]["optical_U1_Wilson_gauge"]
    assert d["signed_triangle_Wilson_products"]==[6.,-6.]
    assert d["random_U1_local_rephasings_verified"]==200
    assert d["maximum_invariance_error"]<1e-13

def test_clock_finite_size_gap_and_positive_finite_spectrum(packet):
    d=packet["other"]["parts"]["finite_quantum_clock"]
    assert len(d["models"])==3
    assert all(s["gap"]>1e-9 for x in d["models"]for s in x["spectral_samples"] if s["transverse_field"]>0)
    assert all(s["ground_degeneracy"]==1 for x in d["models"]for s in x["spectral_samples"] if s["transverse_field"]>0)

def test_globally_trivial_chern_bloch_bundle(packet):
    d=packet["other"]["parts"]["native_Chern_trivial_frame"]
    assert d["rank"]==3
    assert [x["grid"]for x in d["grid_tests"]]==[7,11,17]
    assert all(abs(x["chern_number"])<1e-10 for x in d["grid_tests"])

def test_frame_connection_Ward_identity(packet):
    d=packet["other"]["parts"]["local_connection_Ward"]
    assert d["gauge_invariance_error"]<1e-11
    assert d["infinitesimal_Ward_residual"]<1e-8

def test_real_S3_category_obstruction(packet):
    d=packet["other"]["parts"]["quantum_double_S3_vs_Jones"]
    assert d["S3_rank"]==8 and d["SU2_level4_rank"]==5
    assert d["S3_total_quantum_dimension_squared"]==36
    assert d["SU2_level4_total_quantum_dimension_squared"]==12

def test_MUB_complete_ten_contexts(packet):
    d=packet["other"]["parts"]["ten_W33_MUB_contexts"]
    assert d["number_bases"]==10 and d["Hilbert_dimension"]==9
    assert d["max_unbiased_probability_error"]<1e-12
    used=[v for line in d["40_direction_spread"]for v in line]
    assert sorted(used)==list(range(40))

def test_heat_trace_cartesian_artifact(packet):
    d=packet["other"]["parts"]["spectral_dimension_artifact"]
    assert d["laplacian_spectrum"]=={"0":1,"10":24,"16":15}
    assert abs(d["Cartesian_square_peak_dimension"]-2*d["sampled_peak"]["dimension"])<1e-12

def test_frozen_certificates_match_reproduction(packet):
    for d,p in ((packet["lifts"],L.OUT),(packet["group"],R.OUT),(packet["other"],E.OUT)):
        import json
        assert json.loads(p.read_text())["status"]==d["status"]
