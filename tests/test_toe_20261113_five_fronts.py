"""Five independent mathematical checks and two strict negative controls.

Run: python tests/test_toe_20261113_five_fronts.py
Does not require pytest collection. May also be collected by pytest.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_prime_tower as T
import toe_20261113_chiral_action_compiler_noise as C
import toe_20261113_chiral_e6_cubic_compatibility as E
import toe_20261113_five_qubit_eight_audit as M
import toe_20261113_chiral_null_wigner_magic as W

def test_prime_family_and_arithmetic_controls():
    a=T.verify()
    assert a["status"]=="PASS_EXACT_CUBIC_CONVOLUTION_ALL_FOUR_PRIMES"
    assert [x["active_modes"] for x in a["verified_primes"]]==[8,48,120,360]
    assert [x["frozen_modes"] for x in a["verified_primes"]]==[19,295,1211,6499]
    assert all(x["antisymmetric_full_congruence_orbit_hopping"]=="zero"
               for x in a["opposite_arithmetic_controls"])

def test_action_compiler_and_noise_boundary():
    a=C.verify()
    assert a["dressed_compiler"]["primitive_gates"]=={
        "one_qutrit_rotations":4,"qutrit_SUM":8}
    assert a["dressed_compiler"]["max_absolute_matrix_error"]<1e-12
    scenarios=a["global_depolarizing_channel"]["noise_scenarios"]
    assert scenarios[0]["negative_wigner_mass"]=="16/9"
    assert scenarios[-1]["negative_wigner_mass"]=="0"
    assert a["symmetry_classification"]["parity_odd_nearest_null_direction_unique_up_to_real_scalar"]
    assert a["toy_chirality_selection"]["examples"][2]["minima_at_b_pm"]>0

def test_e6_cubic_counterexample_and_scope():
    a=E.run()
    assert a["canonical_signed_triads"]==45
    assert a["nonzero_output_count"]==27
    assert a["nonzero_examples"][0]["signed_norm_of_9Ue_cubed"]==46
    assert not ("equivariant" in a["validity"] and
                "NOT" not in a["validity"])

def test_five_qubit_search_does_not_false_promote_timeout():
    a=M.verify()
    assert a["eight"]["nodes_explored"]==4310000
    assert a["eight"]["all_orbits_timed_out"]
    assert not a["eight"]["exhaustive_nonexistence_proved"]
    assert a["nine"]["maximal_partial_spread"]
    assert a["nine"]["extendible_candidates"]==0

def test_parent_wigner_negative_control():
    a=W.verify()
    assert a["wigner"]["total_negative_mass"]=="16/9"
    assert a["wigner"]["l1_norm"]=="41/9"

if __name__=="__main__":
    test_prime_family_and_arithmetic_controls()
    test_action_compiler_and_noise_boundary()
    test_e6_cubic_counterexample_and_scope()
    test_five_qubit_search_does_not_false_promote_timeout()
    test_parent_wigner_negative_control()
    print("PASS 5/5 direct-replay fronts, plus q=5/13 and timeout fail-closed controls")
