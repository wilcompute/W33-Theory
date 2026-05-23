from __future__ import annotations

from analysis.w33_k12_combinatorial_ladder import k12_combinatorial_ladder_packet


def test_mccvii_packets() -> None:
    packet = k12_combinatorial_ladder_packet()

    assert packet["primitives"] == {
        "q": 3,
        "mu": 4,
        "k": 12,
        "Phi_6": 7,
        "Phi_3": 13,
    }
    assert packet["ladder"] == {
        "C(12,1)": 12,
        "C(12,2)": 66,
        "C(12,3)": 220,
        "C(12,4)": 495,
        "C(12,5)": 792,
        "C(12,6)": 924,
    }
    assert packet["central_lock"] == {
        "identity": "C(12,6)=924=mu*q*Phi_6*(k-1)=4*3*7*11",
    }


def test_mccvii_all_checks_pass() -> None:
    packet = k12_combinatorial_ladder_packet()

    assert packet["checks"] == {
        "k_equals_q_mu": True,
        "ladder_r1": True,
        "ladder_r2": True,
        "ladder_r3": True,
        "ladder_r4": True,
        "ladder_r5": True,
        "ladder_r6": True,
        "pascal_symmetry_r1": True,
        "pascal_symmetry_r2": True,
        "pascal_symmetry_r3": True,
        "pascal_symmetry_r4": True,
        "pascal_symmetry_r5": True,
        "central_factor_lock": True,
        "c3_factor_lock": True,
        "c2_matches_horizon_payload": True,
        "phi3_is_13": True,
    }
    assert packet["n_verified"] == 16
