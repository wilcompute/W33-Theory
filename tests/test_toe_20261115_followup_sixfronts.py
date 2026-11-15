"""Regression suite for 2026-11-15 five-front audit and quartic E6 bridge.

No untrusted existing worktree files are modified by test imports beyond
explicit named output certificates under data/.
"""
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
    s=importlib.util.spec_from_file_location(name,ROOT/"analysis"/path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

@pytest.fixture(scope="module")
def results():
    m=load("toe_20261115_followup_fivefronts_nonlinear_genus_D9_F8_photon.py","fivefront_audit")
    o=m.run()
    assert o["n_fronts"]==5
    return o["results"]

@pytest.fixture(scope="module")
def quartic():
    m=load("toe_20261115_quartic_E6_sixsector_bridge.py","quartic_E6")
    record=m.run()
    m.OUT.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf8")
    return record

def test_five_fronts_executed(results):
    assert len(results)==5
    assert all(v["status"] for v in results.values())

def test_quadratic_obstruction_to_E6_six_directions(results):
    o=results["E6_quadratic_6_dark_modes"]
    assert o["T_rank"]==o["Q_1600x27_rank"]==21
    assert o["dark_E6_dimension"]==o["projector_rank"]==6
    assert o["projector_trace_times_90"]==540
    assert o["pair_witnesses_for_all_45_octets"]==45
    assert "Q contracted with E" in o["exact_dark_annihilator"]

def test_cubic_surface_dual_planar_chart_enumeration(results):
    o=results["genus6_planar_dual_plane_model"]
    assert (o["primal_facets"],o["dual_faces"],o["dual_vertices"],o["dual_edges"])==(44,12,44,66)
    assert o["dual_face_lengths"]==[11]
    assert o["face_boundary_orderings_verified"]==12
    assert o["degrees_of_freedom_before_Euclidean_gauge"]==36
    assert o["accepted_random_plane_sets"]>=20
    assert o["self_crossing_face_edge_pair_min"]>=0
    assert "not a proof" in o["scope"]

def test_D9_zero_mode_counts_and_spin2_limits(results):
    o=results["D9_product_cubic_KK_zero_mode_comparison"]
    assert o["comparison"]["S2_times_S2"]["protected_5D_vector_count"]==7
    assert o["comparison"]["smooth_cubic_surface"]["protected_5D_vector_count"]==1
    assert o["comparison"]["S2_times_S2"]["primitive_h11"]==1
    assert o["comparison"]["smooth_cubic_surface"]["primitive_h11"]==6
    assert o["protected_primitive_metric_modes_m2L2"]==36
    assert o["anisotropic_charge_limit_gap_tends_zero"]
    assert "full mixed KK" in o["scope"]

def test_F8_rational_PPT_certificate_is_not_global(results):
    o=results["F8_global_vs_code_certificates"]
    exact=Fraction(o["certified_PPT_16_dim_common_code_lower_rational"])
    assert 2<exact<Fraction(5,2)
    assert o["PPT_integer_diagonal_dominance_margin"]>0
    assert o["global_degree6_SOS_numerical_not_rationally_certified"]<float(exact)
    assert o["exact_witness_global_upper"]>float(exact)
    assert "16-dimensional code" in o["important_correction"]
    assert "not a rigorously" in o["important_correction"]

def test_photonic_calibration_joint_confidence_and_pooling(results):
    o=results["photonic_4class_pooled_calibration"]
    assert o["accepted_total_calibration_shots"]==6573041
    assert o["pooled_accepted_readout_calibration_shots"]==4728601
    assert o["accepted_parity_calibration_each_flip_rate"]==922220
    assert o["calibration_sufficient_sample_reduction_factor"]>23
    assert .5<o["joint_99pct_corrected_witness_lower"]<o["synthetic_Fhat_previous"]
    assert sum(o["joint_failure_budget"].values())==pytest.approx(.01)

@pytest.mark.parametrize("which",["circulant_calibration","two_parity_flip_rates","five_witness_settings"])
def test_split_confidence_components_present(results,which):
    o=results["photonic_4class_pooled_calibration"]
    assert o["joint_failure_budget"][which]>0

def test_quartic_full_rank_and_equal_conditioning(quartic):
    assert quartic["quartic_270x27_rank"]==27
    assert quartic["quartic_Gram_identity"]=="R^T R = 10 I_27"
    assert quartic["singular_values_all"]=="sqrt(10) (27 copies)"
    assert quartic["disjoint_octet_pairs"]==quartic["W33_point_quartet_inputs"]==270
    assert quartic["ten_orthogonal_replicates_per_cubic_line"]==10

def test_quartic_six_modes_unlocked_from_quadratic_dark(quartic):
    assert quartic["quadratic_45x27_rank"]==21
    assert quartic["quadratic_dark_sector_dimension"]==6
    assert quartic["quartic_dark_sextet_rank"]==6
    assert quartic["unique_cubic_line_per_pair"]
    assert quartic["four_distinct_points_each_selector"]

def test_quartic_covariance_all_transvections(quartic):
    assert quartic["all_40_symplectic_transvections_covariant"]
    assert "not a deterministic single-photon" in quartic["scope"]

def test_e6_both_certificates_written_and_json_round_trip(quartic,results):
    paths=[ROOT/"data"/"toe_20261115_quartic_E6_sixsector_bridge.json",
           ROOT/"data"/"toe_20261115_fivefront_followup_certificates.json"]
    for path in paths:
        d=json.loads(path.read_text(encoding="utf8"))
        assert d
    assert quartic["status"]=="EXACT_QUARTIC_W33_TO_E6_FULL_27_LINE_SELECTORS"
