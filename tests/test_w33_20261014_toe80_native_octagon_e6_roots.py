"""TOE80: exact E6 Cartan and 72 Weyl roots FROM native W33 octagons."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe80_native_octagon_e6_roots import certificate,determinant_integer

def test_native_w33_shared_octagon_projector_e6_roots():
    c=certificate()
    assert c["status"]=="PASS_TOE80_NATIVE_W33_OCTAGON_EXACT_E6_72_ROOTS"
    assert c["rational_projection_rank"]==6
    assert c["nonadjacent_line_pairs"]==216
    assert c["positive_and_negative_E6_root_vectors"]==72
    assert c["distinct_unoriented_E6_root_lines"]==36
    assert c["each_root_line_repeated_in_nonadjacent_pairs"]==6
    assert c["closure_under_all_root_reflections_exact"]
    assert c["root_system_integral_inner_product_histogram"]=={
      "-2":72,"-1":1440,"0":2160,"1":1440,"2":72}
    assert c["positive_root_count"]==36
    assert c["number_of_distinct_root_reflections_on_27_weights"]==36
    assert c["Weyl_group_on_27_native_weights_order"]==51840
    assert c["Weyl_group_transitive_on_27_weights"]
    assert c["Weyl_minuscule_weight_stabilizer_order"]==1920
    assert c["Weyl_E6_to_native_216_subgroup_index"]==240
    assert len(c["six_generating_simple_root_reflections_27_permutations"])==6

def test_integer_Cartan_e6_and_central_triplet_split():
    c=certificate()
    A=c["E6_Cartan_matrix_from_native_octagons"]
    assert len(A)==6 and all(len(x)==6 for x in A)
    assert determinant_integer(A)==3
    assert c["E6_Dynkin_branch_arm_lengths"]==[1,2,2]
    assert len(c["six_simple_roots_as_directed_octagon_index_pairs"])==6
    h=c["native_H27_center_action_on_E6_root_module"]
    assert h["C3_projector_fixed_dimension"]==0
    assert h["trace_Z_on_six_dimensional_real_module"]==-3
    assert h["complex_irrep_eigenspaces"]=={"omega":3,"omega_conjugate":3}
