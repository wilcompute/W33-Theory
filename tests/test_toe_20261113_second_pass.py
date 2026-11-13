"""Replay mathematical second-pass results and fail-closed bounded MUB status.
Run directly: python tests/test_toe_20261113_second_pass.py
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_five_fronts_second_pass as F
import toe_20261113_h27_e6_nine_sector_cubic as E
import toe_20261113_e6_nine_sector_trace_hypergraph as T
import toe_20261113_h27_albert_cubic_coordinate_reconstruction as A

def test_single_photon_27_mode_compiler():
    x=F.optical()
    assert (x["mode_count"],x["fourier_3mode_tritters"],
            x["ccz_phase_sites"])==(27,54,8)
    assert (x["phase_site_counts"]["zero"],x["phase_site_counts"]["plus120"],
            x["phase_site_counts"]["minus120"])==(19,4,4)
    assert 0<x["postselected_state_fidelity_for_computational_input"]<1

def test_h27_cubic_invariance_firewall():
    x=F.cubic_e6()
    assert x["signed_cubic_triples"]==45
    assert x["preserve_unsigned_triple_incidence"]==3
    assert x["preserve_signed_cubic_by_pure_permutation"]==1
    assert x["recover_signed_cubic_with_diagonal_pm1"]==3

def test_continuum_degeneracy():
    x=F.continuum()
    assert x["low_k_linear_gradient_choices"]==[(6,6,6),(6,0,6)]
    assert x["no_unique_continuum_cone_from_mod3_directions"]

def test_full_six_leg_choi_entanglement():
    x=F.holographic_choi()
    assert x["num_3_vs_3_cuts"]==20
    assert x["number_maximally_mixed"]==8
    assert x["rank_census"]=={"27":8,"9":4,"6":8}
    assert x["purity_census"]=={"1/27":8,"5/27":12}
    assert not x["AME_6_3_perfect_tensor"]

def test_order_three_signed_e6_center():
    x=E.main()
    assert x["signed_order_three_lift_exists"]
    assert x["b_fibre_patterns"]=={"000":6,"111":6,"222":6,"012":27}
    assert x["integer_random_vector_norm_invariance_tests"]==100

def test_three_det_plus_trace_supports():
    x=T.main()
    assert x["trace_cross_terms"]==27
    assert all(z["is_det_3x3_support"] for z in x["determinant_like_hypergraphs"])
    assert all(z["pairwise_projection_is_3K33"] for z in x["cross_sector_bipartite_projections"])

def test_exact_signed_albert_dictionary():
    x=A.main()
    assert x["tritangent_terms_checked"]==45
    assert x["signed_pm1_rephasing_exists"]
    assert x["all_27_cross_terms_become_trace_ABC_support"]
    assert x["signed_rephasing_negative_E6_indices"]==[6,7,12,16,20,25,26]

def test_mub_eight_is_undecided():
    p=ROOT/"data/toe_20261113_fivequbit_s3_two_class_dlx.json"
    x=json.loads(p.read_text(encoding="utf-8"))
    assert x["s3_symmetry_exact"]["O5_order"]==720
    assert x["s3_symmetry_exact"]["two_classes"]==[[0,1],[2,3,4,5,6,7]]
    assert x["s3_symmetry_exact"]["verified_orbit_elements"]==5760
    assert x["controls"]["n3_size5"]=="exists"
    assert x["controls"]["n3_size7"]=="none"
    assert x["status"]=="undecided"
    assert x["search"]["status"]=="undecided"
    assert any(y["timeout"] for y in x["search"]["per_rep"])

if __name__=="__main__":
    tests=[test_single_photon_27_mode_compiler,
           test_h27_cubic_invariance_firewall,
           test_continuum_degeneracy,
           test_full_six_leg_choi_entanglement,
           test_order_three_signed_e6_center,
           test_three_det_plus_trace_supports,
           test_exact_signed_albert_dictionary,
           test_mub_eight_is_undecided]
    for t in tests:
        t()
        print("PASS",t.__name__,flush=True)
    print("PASS 8/8",flush=True)
