from __future__ import annotations

from analysis.w33_monodromy_tower_structure import monodromy_tower_structure_packet


def test_mcciv_packets() -> None:
    packet = monodromy_tower_structure_packet()

    assert packet["levels"] == {
        "L0_q4_faces": 24,
        "L1_tomotope_aut": 96,
        "L2_f4_roots": 96,
        "L3_weyl_f4": 1152,
        "L4_horizon_3456": 3456,
        "L5_code_n": 72,
    }
    assert packet["transitions"] == {
        "L1_over_L0": 4,
        "L3_over_L2": 12,
        "L4_over_L3": 3,
        "identity": "96/24=4, 1152/96=12, 3456/1152=3",
    }
    assert packet["code_link"] == {
        "k": 12,
        "identity": "n = C(k,2) + k/2 = C(12,2) + 6 = 72",
    }


def test_mcciv_all_checks_pass() -> None:
    packet = monodromy_tower_structure_packet()

    assert packet["checks"] == {
        "level0_faces_is_24": True,
        "level1_tomotope_aut_is_96": True,
        "level2_f4_roots_is_96": True,
        "level3_weyl_f4_is_1152": True,
        "level4_horizon_is_3456": True,
        "level5_code_n_is_72": True,
        "l1_over_l0_is_4": True,
        "l3_over_l2_is_k": True,
        "l4_over_l3_is_q": True,
        "code_formula_matches_n": True,
    }
    assert packet["n_verified"] == 10
