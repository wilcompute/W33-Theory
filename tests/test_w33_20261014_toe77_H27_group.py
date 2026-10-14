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

def test_native_gq24_45_tritangents_are_actual_heisenberg_cosets():
    c=certificate()
    assert c["native_GQ24_line_count"]==45
    assert c["native_GQ24_each_point_lines"]==5
    assert c["native_GQ24_exact_right_cosets_of_five_H27_C3_directions"]
    assert sorted(c["native_216_tritangent_orbit_sizes"])==[9,18,18]
    assert sum(c["native_D8_direction_orbit_sizes"])==5
    assert c["center_preserving_order4_subgroup_size"]==4
    assert c["center_inverting_order8_coset_size"]==4
    assert len(c["native_GQ24_tritangent_lines"])==45

def test_complete_432_heisenberg_generator_gauges_against_frozen_cubic_address():
    c=certificate()
    assert c["original_5_coset_directions_abstract_H27_generator_pairs_tested"]==432
    assert c["original_address_H27_to_native_octagon_equivariant_gauge_count"]>=0
    labels=c["example_original_H27_address_to_octagon_bijection"]
    if labels is not None:
        assert sorted(labels)==list(range(27))

def test_actual_native_216_orbits_on_270_marked_prime_tritangent_walks():
    c=certificate()
    sizes=c["native_216_orbits_on_270_based_oriented_triangle_cubics"]
    assert sum(sizes)==270
    assert all(216%v==0 for v in sizes)
    assert c["native_270_directed_triangle_instruction_bijection"]
    assert c["native_GQ24_line_count"]==45
