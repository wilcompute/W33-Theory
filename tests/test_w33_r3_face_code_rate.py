from __future__ import annotations

from analysis.w33_r3_face_code_rate import r3_face_code_rate_packet


def test_mccviii_packets() -> None:
    packet = r3_face_code_rate_packet()

    assert packet["packet"] == {
        "q": 3,
        "k": 12,
        "n_face": 50,
        "k_face": 44,
        "rate": "22/25",
        "u56": 56,
    }
    assert packet["universal_formula"] == {
        "identity": "R_face = (56-k)/(56-k/2) = (C(k,2)-k+2-k)/(C(k,2)-k+2-k/2)",
        "evaluated": "(56-12)/(56-6) = 44/50 = 22/25",
    }


def test_mccviii_all_checks_pass() -> None:
    packet = r3_face_code_rate_packet()

    assert packet["checks"] == {
        "surface_faces_is_44": True,
        "surface_genus_is_6": True,
        "face_code_length_is_50": True,
        "face_code_payload_is_44": True,
        "face_code_rate_is_22_over_25": True,
        "u56_formula_is_exact": True,
        "universal_numerator_is_44": True,
        "universal_denominator_is_50": True,
        "universal_rate_matches_face_rate": True,
        "open_distance_boundary_kept": True,
    }
    assert packet["n_verified"] == 10
