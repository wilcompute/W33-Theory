from __future__ import annotations

from analysis.w33_meeting_point_c331 import meeting_point_c331_packet


def test_mccii_packets() -> None:
    packet = meeting_point_c331_packet()

    assert packet["packets"] == {
        "aut_tomotope": 96,
        "reye_points": 12,
        "genus": 6,
        "half_wf4": 576,
        "N_M": 36,
        "A2": 36864,
        "E": 32,
    }
    assert packet["meeting_point"] == {
        "k_times_N_M": 432,
        "top_3456_from_8kNM": 3456,
        "top_3456_from_autNM": 3456,
        "top_3456_from_genus_halfWf4": 3456,
        "identity": "3456 = 8*12*36 = 96*36 = 6*576",
    }
    assert packet["mcci_bridge"] == {
        "identity": "(3*A2)/3456 = (3*36864)/3456 = 32 = E",
    }


def test_mccii_all_checks_pass() -> None:
    packet = meeting_point_c331_packet()

    assert packet["checks"] == {
        "c331a_orbit_point_lock": True,
        "c331b_k_nm_is_432": True,
        "c331c_8_k_nm_is_3456": True,
        "c331d_aut_nm_is_3456": True,
        "c331d2_genus_halfwf4_is_3456": True,
        "c331_all_forms_equal": True,
        "bridge_a2_is_36864": True,
        "bridge_q_scaled_a2_over_3456_is_32": True,
        "bridge_matches_shell": True,
        "full_bridge_identity": True,
    }
    assert packet["n_verified"] == 10
