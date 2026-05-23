from __future__ import annotations

from analysis.w33_c220_holographic_ladder import c220_holographic_ladder_packet


def test_mccvi_packets() -> None:
    packet = c220_holographic_ladder_packet()

    assert packet["packets"] == {
        "q": 3,
        "d_z": 4,
        "k": 12,
        "C_k_3": 220,
        "Sym2_dim": 66,
        "q_pow_dz": 81,
    }
    assert packet["enhancement"] == {
        "ratio": "220/81",
        "identity": "220/81 = C(12,3)/3^4",
    }
    assert packet["ladder"] == {
        "C(12,1)": 12,
        "C(12,2)": 66,
        "C(12,3)": 220,
        "C(12,4)": 495,
        "C(12,5)": 792,
        "C(12,6)": 924,
    }


def test_mccvi_all_checks_pass() -> None:
    packet = c220_holographic_ladder_packet()

    assert packet["checks"] == {
        "c220_identity": True,
        "sym2_is_66_not_220": True,
        "enhancement_is_220_over_81": True,
        "enhancement_matches_mccv": True,
        "ladder_r1": True,
        "ladder_r2": True,
        "ladder_r3": True,
        "ladder_r4": True,
        "ladder_r5": True,
        "ladder_r6": True,
    }
    assert packet["n_verified"] == 10
