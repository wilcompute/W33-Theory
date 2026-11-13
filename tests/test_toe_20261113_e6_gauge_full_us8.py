"""Reproducible integration checks for exact signed E6 cubic:
genuine generalized gauge closure, M/IIB parabolic sections, Albert
clock & 6-fold USp8 double cover, non-flat gauge Wilson loops,
three-qutrit shift-code magic and MUB fail-closed search.

Run: python -u tests/test_toe_20261113_e6_gauge_full_us8.py
"""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_E6_cubic_source_semantic_audit as SOURCE
import toe_20261113_E6_exft_generalized_closure_affine as AFFINE
import toe_20261113_E6_exft_quadratic_Jacobiator as QUAD
import toe_20261113_E6_exact_parabolic_stabilizer as PAR
import toe_20261113_Albert_cyclic_clock_sections as CLOCK
import toe_20261113_E6_nonflat_compact_lattice_gauge as GAUGE
import toe_20261113_E6_photonic_magic_repetition as PHOTON
import toe_20261113_USp8_full36_intertwiner_audit as AUDIT
import toe_20261113_USp8_highest_weight_intertwiner as HW
import toe_20261113_USp8_8mode_Albert_clock as COVER
import toe_20261113_USp8_E6_Z2_interferometric_witness as INTERFERENCE
import toe_20261113_E6_Weyl_section_orbits as WEYL
import toe_20261113_fivequbit_size8_CPSAT_lazy_compatibility as MUB
import toe_20261113_pass12654_MUB_size8_complete_crossaudit as MUBA

def test_cubic_sources_semantically_equal_not_byte_equal():
    r=SOURCE.main()
    assert r["parsed_JSON_objects_equal"] and r["signed_45_triads_equal"]
    assert not r["raw_bytes_identical"] and r["seven_coordinate_rephasing_Albert_45_terms_exact"]

def test_affine_E6_generalized_closure_and_bad_derivative_pair():
    r=AFFINE.main()
    assert r["section_cases"]["5"]["exact_affine_closure_trials"]==32
    assert r["section_cases"]["6"]["exact_affine_closure_trials"]==32
    assert r["bad_pair_control"]["closure_residual_max_integer"]>0

def test_quadratic_E6_generalized_closure_and_nonzero_trivial_Jacobiator():
    r=QUAD.main()
    assert r["records"]["5"]["nonzero_Jacobiator_observed_trials"]>0
    assert r["records"]["6"]["nonzero_Jacobiator_observed_trials"]>0
    assert all(z["Jacobiator_generates_zero_gauge_action_on_test_vector"] for z in r["records"].values())

def test_connected_E6_5_and_6_parabolic_Lie_stabilizers():
    r=PAR.main()["sections"]
    assert r["5"]["Lie_stabilizer_dim"]==53 and r["6"]["Lie_stabilizer_dim"]==57
    assert r["5"]["restriction_GL_dim"]==25 and r["6"]["restriction_GL_dim"]==36
    assert r["5"]["kernel_trace_nilradical"]["nilpotent_radical_dim"]==25
    assert r["6"]["kernel_trace_nilradical"]["nilpotent_radical_dim"]==21
    assert r["5"]["kernel_trace_nilradical"]["radical_center_dim"]==5
    assert r["6"]["kernel_trace_nilradical"]["radical_center_dim"]==1

def test_all_51840_Weyl_automorphism_certificate():
    r=json.loads((ROOT/"data/toe_20261113_E6_Weyl_M_IIB_section_stabilizers.json").read_text())
    assert r["complete"] and r["automorphisms_checked"]==51840
    assert [r["maximal_fiver_orbit_seen"],r["maximal_sixer_orbit_seen"]]==[216,72]
    assert [r["maximal_fiver_stabilizer_count_seen"],r["maximal_sixer_stabilizer_count_seen"]]==[240,720]

def test_Albert_clock_preserves_signed_cubic_and_18_12_sections():
    r=CLOCK.main()
    assert r["clock_exactly_preserves_all_45_signed_cubic_terms"]
    assert r["fixed_sections"]["5"]["fixed_setwise"]==18
    assert r["fixed_sections"]["6"]["fixed_setwise"]==12
    assert r["skew_matrix_A_equal_UminusUT_has_infinitesimal_cubic_invariance"]

def test_nonflat_compact_E6_gauge_Wilson_energy_invariance():
    r=GAUGE.main()
    assert r["Wilson_loop_is_not_identity"]
    assert r["Wilson_loop_matrix_order"]==3 and r["Wilson_loop_trace"]==9
    assert r["sitewise_cubic_invariance"]
    assert r["entire_729_laplacian_gauge_covariance_exact_integer"]
    assert r["fixed_maximal_sections_by_Wilson_loop"]=={"5":18,"6":12}

def test_photonic_Clifford_encoded_magic_shift_syndromes():
    r=PHOTON.main()
    k=r["Knill_Laflamme_shift_subcode"]
    assert k["all_49_overlap_matrices_are_delta_ab_I3"]
    assert not k["single_Z_error_correctable"]
    assert abs(k["probability_guaranteed_correctable_weight_le1"]-.998816)<1e-12

def test_Cartan_only_intertwiner_requires_phases():
    r=AUDIT.main()
    assert not r["full_36_lie_intertwiner_already_present"]
    assert r["number_generators_fit_below_1e_minus_9"]==4
    assert r["maximum_nonCartan_relative_residual"]>.1

def test_highest_weight_reconstructs_all_36_USp8_generators():
    r=HW.main()
    assert r["status"]=="FULL_36_INTERTWINER_VERIFIED"
    assert r["construction"]["rank_generated"]==27
    assert r["max_relative_residual"]<1e-9
    assert r["construction"]["isometry_residual"]<1e-9

def test_order_six_USp8_center_reduces_to_order_three_on_27():
    r=COVER.main()
    assert r["status"]=="PASS_FULL36_USP8_INTERTWINER_AND_ALBERT_CLOCK_ORDER6_LIFT_ORDER3_WEDGE"
    assert r["Albert_clock_defining_8mode_order6"]
    assert r["Albert_clock_defining_8mode_cubed_is_center_minus_I"]
    assert r["Albert_clock_27mode_induced_order3"]
    assert r["Albert_clock_8mode_group_eigen_mult"]==[4,4]
    assert r["induced_27mode_group_intertwiner_residual"]<1e-9

def test_central_Z2_clock_two_irrep_interferometric_witness():
    r=INTERFERENCE.main()
    assert r["clock_eight_order"]==6 and r["clock_twentyseven_order"]==3
    assert r["balanced_two_irrep_input_revival_probability_after_three"]<1e-20
    assert abs(r["balanced_two_irrep_input_revival_probability_after_six"]-1)<1e-9

def test_parallel_433m_node_size8_completed_certificate_crossaudit():
    r=MUBA.main()
    assert r["total_exact_cover_DFS_nodes"]==433517130
    assert r["all_eight_orbits_completed_no_witness"]
    assert not r["all_eight_orbits_timed_out"]
    assert r["fresh_control_n5_size9_found"]

def test_MUB_five_qubit_size8_fail_closed_on_solver_timeout():
    r=json.loads((ROOT/"data/toe_20261113_fivequbit_size8_lazy_cpsat_full_compatibility.json").read_text())
    assert r["status"]=="UNDECIDED_SIZE8"
    assert len(r["results"])==2
    assert [z["class_rep"] for z in r["results"]]==[692,694]
    assert all(z["status"]=="UNKNOWN" for z in r["results"])
    assert all(z["pairwise_nogood_cuts_added"]>=1 for z in r["results"])
    assert all(z["valid_full_witness"] is None for z in r["results"])

if __name__=="__main__":
    tests=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print("PASS",t.__name__,flush=True)
    print("PASS",len(tests),"/",len(tests),flush=True)
