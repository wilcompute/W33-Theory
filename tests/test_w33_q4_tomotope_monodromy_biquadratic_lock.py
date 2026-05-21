from __future__ import annotations

from analysis.w33_q4_tomotope_monodromy_biquadratic_lock import (
    q4_tomotope_monodromy_biquadratic_lock_packet,
)


def test_mclxxxiii_packet_values() -> None:
    packet = q4_tomotope_monodromy_biquadratic_lock_packet()

    assert packet["q4_packet"] == {
        "face_nodes": 24,
        "edge_nodes": 32,
        "incidences": 96,
        "quotient_incidences": 48,
    }
    assert packet["tomotope_packet"] == {
        "automorphism_order": 96,
        "flags": 192,
        "monodromy_order": 18432,
        "medial_incidences": 48,
    }
    assert packet["locks"] == {
        "A_times_F": 18432,
        "2_times_I_squared": 18432,
        "face_edge_face": 18432,
        "quotient_times_flag_doubler": 18432,
        "identity": "18432 = 96*192 = 2*96^2 = 24*32*24 = 48*384",
    }


def test_mclxxxiii_all_checks_pass() -> None:
    packet = q4_tomotope_monodromy_biquadratic_lock_packet()

    assert packet["checks"] == {
        "mclxxxii_invariants_present": True,
        "automorphism_equals_q4_incidences": True,
        "flags_are_double_incidences": True,
        "monodromy_equals_automorphism_times_flags": True,
        "monodromy_equals_two_times_incidence_square": True,
        "monodromy_equals_face_edge_face_packet": True,
        "quotient_incidences_equal_medial": True,
        "monodromy_equals_quotient_times_flag_doubler": True,
        "monodromy_over_automorphism_equals_flags": True,
        "monodromy_over_flags_equals_automorphism": True,
    }
    assert packet["n_verified"] == 10
