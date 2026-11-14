"""Nov 14 exact Gaussian USp8, ExFT tensor hierarchy, Wilson
section falsifier, calibrated optical clock, independent five-qubit
MUB rank-code audit, and quaternionic CP7->HP3 charge tangent.

Run: python -u tests/test_toe_20261114_six_fronts_exact.py
Every producer is re-executed; the 433M/108M node parallel
MUB negative searches are NOT replayed (certificates are audited).
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as EX
import toe_20261114_e6_tensor_hierarchy as HI
import toe_20261114_e6_Wilson_section_census as WI
import toe_20261114_35mode_loss_photonic_witness as OP
import toe_20261114_independent_fivequbit_rankcode_audit as MU
import toe_20261114_CP7_HP3_charge_differential as HP

def test_exact_Gaussian_integer_full_USp8_and_eight_mode_four_couplers():
    r=EX.main()
    assert r["B_nonzeros"]==108
    assert r["source_36_root_packets_in_compact_us8_span"]
    assert r["compact_Pauli_Gram_diagonal"]==48
    assert r["clock_lift_g8_cubed"]=="H^3=-(2den)^3 I8"
    assert r["reduced_clock_8_denominator"]==2
    assert r["four_2mode_balanced_coupler_pairs"]==[[0,4],[1,5],[2,6],[3,7]]

def test_E6_two_section_tensor_hierarchy_and_explicit_Jacobiator_potential():
    r=HI.main()
    assert all(s["exact_polynomial_trials"]==16 for s in r["regions"].values())
    assert all(s["E_bracket_jacobiators_nonzero"]==16 for s in r["regions"].values())
    assert all(all(q==[3] for q in s["Jacobiator_explicit_potential_numerator_ratio_observations"])
               for s in r["regions"].values())

def test_all_630_Wilson_link_pairs_disprove_one_plaquette_section_selection():
    r=WI.main()
    assert r["unordered_link_pairs"]==630
    assert r["nonflat_count"]==360 and r["flat_count"]==270
    assert r["nonflat_only_five"]==r["nonflat_only_six"]==0
    assert r["nonflat_neither"]==0
    assert r["smallest_nonflat_wilson_action"]==18

def test_loss_calibrated_two_representation_optical_clock_and_erasure_no_go():
    r=OP.main()
    assert r["mode_count"]==35
    assert r["photonic_trials"]["3"]["return_detector_click_probability_pred"]<.005
    assert r["photonic_trials"]["3"]["return_detector_click_probability_null"]>.70
    assert r["three_pulse_classical_two_hypothesis_Bhattacharyya_bound"]["shots_for_Bhattacharyya_upper_bound_error"]==23
    assert not r["full_loss_no_go"]["full_photon_loss_exactly_correctable"]

def test_independent_GF2_orbits_and_size_nine_Pauli_MUB_witnesses():
    r=MU.main()
    assert r["all_nonsingular"]==13888
    assert r["orthogonal_group_O5_order"]==720
    assert r["eight_orbit_sizes"]==[720]*8
    assert r["two_S3_classes"]==[[0,1],[2,3,4,5,6,7]]
    assert sum(v["witnesses_independently_verified"]
               for v in r["all_forward_reverse_size9_witnesses_independently_checked"].values())==10
    assert r["both_reported_complete_no_timeout"]

def test_quaternionic_charge_map_rank_twelve_and_all_coordinate_section_projections():
    r=HP.main()
    assert r["exact_basepoint_real_Jacobian_shape"]==[27,14]
    assert r["basepoint_nonzero_singular_values_squared"]==[8]*12
    assert len(r["two_CP1_vertical_kernel_directions"])==2
    assert r["generic_state_section_restricted_tangent_rank_counts"]["5"]=={"5":216}
    assert r["generic_state_section_restricted_tangent_rank_counts"]["6"]=={"6":72}

if __name__=="__main__":
    tests=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
        print("PASS",test.__name__,flush=True)
    print("PASS",len(tests),"/",len(tests),flush=True)
