from __future__ import annotations

from exploration.w33_affine_e8_first_mode_bridge import build_summary


def test_affine_e8_first_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_first_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_affine_e8_vacuum_shift_is_exactly_minus_one_over_q"] is True
    assert theorem["the_first_excited_affine_e8_coefficient_is_exactly_248"] is True
    assert theorem["the_first_excited_affine_e8_coefficient_splits_exactly_as_e8_root_packet_plus_bosonic_octet"] is True
    assert theorem["the_same_coefficient_refines_exactly_as_e6_adjoint_plus_two_triality_chiral_27_times_3_packets_plus_the_bosonic_octet"] is True
    assert theorem["the_bosonic_octet_is_exactly_the_promoted_w33_packet_one_plus_four_plus_three"] is True
    assert theorem["the_recent_affine_e8_modular_layer_and_the_solved_w33_family_spine_therefore_meet_already_at_the_first_excited_mode"] is True

    assert packet["bosonic_octet_8"] == 8
    assert packet["matter_triality_packet_81"] == 81
