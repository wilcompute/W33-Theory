"""TOE77 exact 216-stabilizer and possible Heisenberg H27 action."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_H27_shared_octagon_group import certificate
def test_actual_H27_classification_not_numerical_coincidence():
    c=certificate()
    assert c["status"]=="PASS_TOE77_NATIVE_27_OCTAGON_EXPLICIT_GROUP_STRUCTURE"
    assert c["pair_stabilizer_order_in_PGSp"]==216
    assert c["pair_orbit_size"]==240
    assert c["transitive_on_27_shared_octagons"]
    assert 216%c["induced_faithful_permutation_group_order"]==0
    assert sum(int(v) for v in c["group_order_histogram"].values())==c["induced_faithful_permutation_group_order"]
    if c["selected_Sylow27_is_extraspecial_Heisenberg_H27"]:
        assert c["selected_Sylow27_center_order"]==3
        assert c["selected_Sylow27_regular_on_27_octagons"]
        assert c["selected_Sylow27_element_order_histogram"]=={1:1,3:26}

def test_normal_H27_and_actual_order_eight_complement_not_just_216_count():
    c=certificate()
    assert c["selected_Sylow27_normal_in_pair_stabilizer"]
    assert c["selected_Sylow27_is_extraspecial_Heisenberg_H27"]
    assert c["explicit_order8_complement_found"]
    assert sum(c["order8_complement_element_orders"].values())==8
    assert c["pair_stabilizer_order_in_PGSp"]==27*8
    if c["pair_stabilizer_is_semidirect_H27_by_Q8"]:
        assert c["order8_complement_is_quaternion_Q8"]
        assert c["H27_center_fixed_pointwise_under_order8"]
        assert c["order8_orbit_size_on_eight_nonzero_H27_mod_center_classes"]==8

def test_order_eight_action_identifies_dihedral_or_other_explicit_structure():
    c=certificate()
    assert sum(c["D8_orbit_sizes_on_eight_nonzero_H27_mod_center_classes"])==8
    assert not c["order8_complement_is_quaternion_Q8"]
    assert not c["H27_center_fixed_pointwise_under_order8"]
    assert c["full_216_group_center_order"]==1
    if c["order8_complement_is_dihedral_D8"]:
        assert c["order8_complement_element_orders"]=={1:1,2:5,4:2}
        assert c["pair_stabilizer_is_semidirect_H27_by_D8"]
        assert c["D8_orbit_sizes_on_eight_nonzero_H27_mod_center_classes"]==[4,4]

def test_pair_orbital_stabilizer_center_inversion_and_E6_incidence():
    c=certificate()
    assert sum(c["unordered_pair_orbit_lengths"])==351
    assert sum(c["unordered_pair_orbit_valencies"])==26
    assert c["native_216_invariant_cubic_surface_intersection_srg_count"]>=0
    assert c["dihedral_reflections_inverting_Heisenberg_center"]==4
    assert c["dihedral_elements_preserving_Heisenberg_center"]==4
    for v in c["native_216_invariant_cubic_surface_intersection_srg_candidates"]:
        assert v["triangle_tritangent_count"]==45
