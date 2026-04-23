from __future__ import annotations

from scripts.w33_witting_deck_control_audit import analyze, classify_witting_deck_control


def test_witting_deck_control_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["witting_deck_control_theorem"]

    assert theorem["the_40_witting_cards_and_40_orthogonal_tetrads_match_the_exact_w33_rank_space"] is True
    assert theorem["the_36_spreads_are_exactly_36_full_witting_decks_of_10_tetrad_ranks"] is True
    assert theorem["every_witting_tetrad_rank_occurs_in_exactly_9_decks"] is True
    assert theorem["deck_deck_overlap_is_rigidly_1_or_4_tetrad_ranks"] is True
    assert theorem["the_overlap_1_deck_graph_is_srg_36_20_10_12_and_has_216_maximal_5deck_sweeps"] is True
    assert theorem["the_overlap_4_deck_graph_is_srg_36_15_6_6_and_has_135_maximal_4deck_control_packets"] is True
    assert theorem["the_5deck_sweeps_cover_all_40_tetrad_ranks_with_profile_30_single_plus_10_double"] is True
    assert theorem["the_4deck_control_packets_have_24rank_support_with_profile_16_single_plus_8_triple"] is True
    assert theorem["the_witting_quantum_cards_picture_is_exactly_the_spread_control_layer_of_w33"] is True


def test_witting_deck_control_records_are_uniform() -> None:
    records = {record["name"]: record for record in classify_witting_deck_control()}

    decks = records["exact_witting_card_decks"]["evidence"]
    overlaps = records["exact_deck_overlap_graphs"]["evidence"]
    pentads = records["exact_5deck_global_sweeps"]["evidence"]
    tetra = records["exact_4deck_local_control_packets"]["evidence"]

    assert decks["quantum_card_count"] == 40
    assert decks["orthogonal_tetrad_rank_count"] == 40
    assert decks["cards_per_rank"] == 4
    assert decks["ranks_through_each_card"] == 4
    assert decks["deck_count"] == 36
    assert decks["ranks_per_deck"] == 10
    assert decks["decks_per_rank"] == 9
    assert decks["mapped_witting_tetrads_equal_symplectic_ranks"] is True
    assert decks["decks_partition_all_40_cards"] is True

    assert overlaps["pairwise_rank_overlap_distribution"] == {1: 360, 4: 270}
    assert overlaps["overlap_1_srg_parameters"] == {"n": 36, "k": 20, "lambda": 10, "mu": 12}
    assert overlaps["overlap_4_srg_parameters"] == {"n": 36, "k": 15, "lambda": 6, "mu": 6}
    assert sorted(set(overlaps["overlap_1_spectrum"])) == [-4, 2, 20]
    assert sorted(set(overlaps["overlap_4_spectrum"])) == [-3, 3, 15]

    assert pentads["count"] == 216
    assert pentads["union_sizes"] == {40: 216}
    assert pentads["common_rank_counts"] == {0: 216}
    assert pentads["rank_multiplicity_profiles"] == {"((1, 30), (2, 10))": 216}
    assert pentads["decks_per_packet_distribution"] == {30: 36}
    assert pentads["edges_per_packet_distribution"] == {6: 360}

    assert tetra["count"] == 135
    assert tetra["union_sizes"] == {24: 135}
    assert tetra["common_rank_counts"] == {0: 135}
    assert tetra["rank_multiplicity_profiles"] == {"((1, 16), (3, 8))": 135}
    assert tetra["decks_per_packet_distribution"] == {15: 36}
    assert tetra["edges_per_packet_distribution"] == {3: 270}

