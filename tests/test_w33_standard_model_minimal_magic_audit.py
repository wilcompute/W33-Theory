from __future__ import annotations

from scripts.w33_standard_model_minimal_magic_audit import (
    analyze,
    classify_minimal_magic_frontier,
)


def test_standard_model_minimal_magic_theorem_is_exact_and_atomic() -> None:
    payload = analyze()
    theorem = payload["minimal_magic_theorem"]

    assert theorem["the_exact_generation_memory_layer_stays_inside_the_regular_qutrit_c3_packet"] is True
    assert theorem["the_exact_signed_nonclifford_roots_first_appear_at_algebraic_degree_four"] is True
    assert theorem["the_remaining_signed_magic_packet_has_exact_size_two_and_no_lower_degree_signed_split"] is True
    assert theorem["the_two_quartic_magic_atoms_are_field_theoretically_independent"] is True
    assert theorem["any_canonical_mixing_of_the_two_atoms_raises_degree_to_octic_or_degree_16"] is True


def test_standard_model_minimal_magic_records_show_atomic_quartic_frontier() -> None:
    records = {record["name"]: record for record in classify_minimal_magic_frontier()}

    memory = records["qutrit_memory_packet"]["evidence"]
    atoms = records["quartic_magic_atoms"]["evidence"]
    fields = records["field_independence_of_quartic_atoms"]["evidence"]
    mixing = records["higher_degree_mixing_escalation"]["evidence"]

    assert memory["generation_reduces_to_one_c3_mod3"] is True
    assert memory["generation_module_is_regular_c3_module"] is True
    assert memory["complex_regular_module_splits_as_qutrit_packet"] is True
    assert memory["plus_generator_order_3"] is True
    assert memory["minus_generator_order_3"] is True
    assert memory["minus_equals_plus_squared_mod3"] is True
    assert memory["cycle_conjugacy_is_exact"] is True
    assert memory["line_maps_to_fixed_line"] is True
    assert memory["plane_maps_to_augmentation_plane"] is True

    assert atoms["packet_size"] == 2
    assert atoms["scaled_signed_variable"] == "x = 240 * sigma"
    assert atoms["h2_quartic_polynomial"] == "x**4 - 542*x**2 + 61200"
    assert atoms["hbar2_quartic_polynomial"] == "x**4 - 982*x**2 + 137232"
    assert atoms["h2_galois_group_label"] == "D4"
    assert atoms["hbar2_galois_group_label"] == "D4"

    assert fields["shared_quadratic_subfield_squarefree_parts"] == ()
    assert fields["quartic_root_fields_are_linearly_disjoint_over_q"] is True
    assert fields["quartic_root_field_compositum_degree"] == 16
    assert fields["d4_splitting_fields_are_linearly_disjoint_over_q"] is True
    assert fields["quartic_splitting_field_compositum_degree"] == 64
    assert fields["quartic_splitting_field_galois_group"] == "D4 x D4"

    assert mixing["mixed_product_degree"] == 8
    assert mixing["mixed_ratio_degree"] == 8
    assert mixing["mixed_sum_degree"] == 16
    assert mixing["mixed_product_squared_degree"] == 4
    assert mixing["mixed_ratio_squared_degree"] == 4
    assert mixing["mixed_squared_packets_have_v4_galois_group"] is True
