from scripts.tomotope_six_kernel_s4_edge_bridge import build_bridge


def test_bridge_summary_core_invariants():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["slot_count"] == 6
    assert summary["generated_group_order"] == 24
    assert summary["tetrahedral_edge_group_order"] == 24
    assert summary["action_is_transitive"] is True
    assert summary["conjugate_to_tetrahedral_edge_action"] is True


def test_cycle_type_distribution_matches_observed_profile():
    payload = build_bridge()
    dist = payload["cycle_type_distribution"]

    # The distribution below is the computed fingerprint of the generated
    # order-24 subgroup in S6.
    assert dist == {
        "1-1-1-1-1-1": 1,
        "2-2-1-1": 9,
        "3-3": 8,
        "4-2": 6,
    }


def test_conjugator_is_valid_permutation_on_six_slots():
    payload = build_bridge()
    conjugator = payload["conjugator_to_tetrahedral_edge_model"]

    assert conjugator is not None
    assert len(conjugator) == 6
    assert set(conjugator) == set(range(6))


def test_bivector_slot_dictionary_is_complete():
    payload = build_bridge()
    dictionary = payload["canonical_bivector_slots"]

    assert set(dictionary.keys()) == {f"k{i}" for i in range(1, 7)}
    assert set(dictionary.values()) == {"B01", "B02", "B03", "B12", "B13", "B23"}
