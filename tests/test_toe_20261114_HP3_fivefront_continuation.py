"""Five-front independent reproducers and fail-closed assertions (2026-11-14)."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_HP3_180_quaternionic_3design as D3
import toe_20261114_hidden_qubit_12_pauli_readout as H
import toe_20261114_all288_E6_ExFT_sections_audit as X
import toe_20261114_USp8_constructive_pure_state_compiler as S
import toe_20261114_fivequbit_MUB_independent_rank_audit as M

def test_projected_HP3_3design_but_not4():
    d=D3.main()
    assert d["projective_design_strength"]==3 and d["not_4_design"]
    assert d["independently_compared_Haar_third_moment_entries"]==27**3
    assert d["fourth_counterexample"]["HP3_Haar_E_z0_4"]=="1/33"

def test_optimal_12_hidden_qubit_pauli_menu():
    d=H.main()
    assert d["global_menu_size"]==12
    assert d["ortools_CP_SAT_global_size_le_11"]=="INFEASIBLE"
    assert d["pure_state_reconstruction_tests"]==720
    assert d["max_matrix_entry_reconstruction_error"]<1e-12

def test_all288_linear_maximal_ExFT_sections_and_closure():
    d=X.main()
    assert d["max_coordinate_sections"]=={"5":216,"6":72}
    assert d["all_288_section_self_annihilator_verified_via_rank_mod101"]==288
    assert d["five_section_orbits"]==[216] and d["six_section_orbits"]==[72]
    assert d["explicit_off_section_nonzero_closure_residual"]>0

def test_USp8_pure_state_transitivity_and_45_gate_compiler():
    d=S.main()
    assert d["generator_tangent_rank_at_e0"]==15
    assert d["compiled_gate_count_per_target"]==45
    assert d["minimum_fidelity"]>0.9999999
    assert d["quaternionic_GramSchmidt_residual_max"]<1e-12

def test_MUB_fullrun_audit_with_independent_GF2():
    d=M.main()
    assert d["all_GF2_rank_codes_independently_checked"]
    assert d["negative_fullrun_8_reps_433517130_nodes"]
    assert d["reversed_two_S3_reps_no_witness"]
    assert d["positive_n5_size9_maximality_all_13888_checked"]

if __name__=="__main__":
    funcs=[globals()[n] for n in sorted(globals()) if n.startswith("test_")]
    for fn in funcs:
        fn()
        print("PASS",fn.__name__,flush=True)
    print("PASS",len(funcs),"/",len(funcs),flush=True)
