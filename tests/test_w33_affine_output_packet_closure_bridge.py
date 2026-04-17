from __future__ import annotations

from exploration.w33_affine_output_packet_closure_bridge import build_summary


def test_affine_output_packet_closure_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_output_packet_closure_theorem"]
    rows = summary["affine_output_packet_closure_dictionary"]["output_rows"]

    assert theorem["the_E8_adjoint_packet_248_is_exactly_edge_root_packet_240_plus_bosonic_octet_8"] is True
    assert theorem["the_Heawood_full_shell_336_is_exactly_24_times_14_and_exactly_16_times_21"] is True
    assert theorem["the_full_Dirac_shell_480_is_exactly_20_times_24_and_exactly_40_times_12"] is True
    assert theorem["the_A26_shell_728_is_exactly_248_plus_480"] is True
    assert theorem["the_qE_shell_720_is_exactly_20_times_36"] is True
    assert theorem["the_promoted_affine_output_alphabet_248_336_480_728_720_is_already_closed_inside_the_nonaffine_packet_dictionary"] is True

    assert rows["248"]["closure_forms"]["edge_root_packet_plus_bosonic_octet"] == 248
    assert rows["336"]["closure_forms"]["complement_24_times_G2_dimension_14"] == 336
    assert rows["336"]["closure_forms"]["common_dirac_core_16_times_AG21_21"] == 336
    assert rows["480"]["closure_forms"]["curvature_shell_20_times_complement_24"] == 480
    assert rows["480"]["closure_forms"]["point_carrier_40_times_valency_12"] == 480
    assert rows["728"]["closure_forms"]["E8_adjoint_248_plus_full_Dirac_shell_480"] == 728
    assert rows["720"]["closure_forms"]["curvature_shell_20_times_spread_carrier_36"] == 720
