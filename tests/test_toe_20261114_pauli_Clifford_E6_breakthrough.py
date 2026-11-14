"""Exact 2026-11-14 Clifford/E6 sixer dictionary, orthogonal Weyl
group, split shear physical positivity no-go, and dense compact
USp8 control with one non-Clifford single-qubit gate.

Run all producers with exact data:
    python -u tests/test_toe_20261114_pauli_Clifford_E6_breakthrough.py
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_pauli_clifford_double_six_bijection as DSC
import toe_20261114_E6_clifford_Weyl_group as W
import toe_20261114_split_shear_quantum_positivity as P
import toe_20261114_dense_USp8_one_nonclifford_gate as C

def test_36_double_sixes_72_sixers_216_closed_pentads():
    x=DSC.main()
    assert x["five_section_count"]==216
    assert x["six_section_count"]==72
    assert x["every_root_packet_exactly_once"]
    assert x["each_index_in_exactly_16_double_sixes"]
    assert len(x["full_pauli_to_compact_root_matching"])==36

def test_36_compact_signed_root_packets_one_to_one_all_36_nonquadric_labels():
    x=DSC.main()
    rows=x["full_pauli_to_compact_root_matching"]
    assert sorted(row["compact_root_packet_index"] for row in rows)==list(range(36))
    assert len({row["nonquadric_label"] for row in rows})==36
    assert all(len(row["six_sections"])==2 for row in rows)
    assert all(len(row["paired_coordinate_edges"])==6 for row in rows)
    assert all(len(row["remaining15_pauli_directions_commuting_with_generator"])==15 for row in rows)

def test_W_E6_order51840_and_original_8mode_clock_is_Clifford():
    x=W.main()
    assert x["group_on_27_pauli_labels_order"]==51840
    assert x["original_eight_mode_clock_is_3qubit_Clifford"]
    assert x["original_27D_label_permutation_in_W_E6"]
    assert x["original_27D_label_permutation_order"]==3
    assert len(x["original_eight_mode_clock_Pauli_images"])==63

def test_split_E6_section_selecting_shear_violates_physical_density_positivity():
    x=P.main()
    assert x["tested_J_twirl_rank2_stabilizer_states"]==180
    assert x["tested_total"]==360
    assert x["new_norm_squared_distribution"]=={"3":120,"4":240}
    assert x["count_new_density_not_positive"]==240
    assert abs(x["explicit_strongest_bad_example"]["min_density_eigenvalue"]+0.125)<1e-12

def test_one_nonClifford_single_qubit_rotation_generates_dense_USp8_but_not_SU8():
    x=C.main()
    assert x["nonquadric_Pauli_orbit_size"]==36
    assert x["Lie_bracket_closure_verified_for_all_ordered_pairs"]==1296
    assert x["initial_extra_gate_not_Clifford"]
    assert x["generated_topological_closure"]=="USp(8), compact and connected, not SU(8)"

if __name__=="__main__":
    tests=[globals()[n] for n in sorted(globals()) if n.startswith("test_")]
    for t in tests:
        t();print("PASS",t.__name__,flush=True)
    print("PASS",len(tests),"/",len(tests),flush=True)
