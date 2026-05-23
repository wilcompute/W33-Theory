from __future__ import annotations

from analysis.w33_poincare_dual_code import poincare_dual_code_packet


def test_mccxii_packet() -> None:
    packet = poincare_dual_code_packet()

    assert packet["surface"] == {
        "primal": {"V": 12, "E": 66, "F": 44, "genus": 6},
        "dual": {"V": 44, "E": 66, "F": 12, "genus": 6},
    }
    assert packet["codes"] == {
        "edge_code": {"n": 72, "k": 66, "rank_H": 6},
        "face_code": {"n": 50, "k": 44, "rank_H": 6},
    }
    assert packet["distance_claim"] == {
        "edge": "d=3=q (conditional from MCCXI)",
        "face": "d=3=q (conditional via Poincare-dual transfer)",
        "identity": "both edge [72,66,3] and face [50,44,3] are conditional closures at q=3",
    }


def test_mccxii_all_checks_pass() -> None:
    packet = poincare_dual_code_packet()

    assert packet["checks"] == {
        "surface_is_12_66_44_g6": True,
        "dual_surface_is_44_66_12": True,
        "dual_genus_is_6": True,
        "edge_code_is_72_66": True,
        "face_code_is_50_44": True,
        "edge_rank_is_6": True,
        "face_rank_is_6": True,
        "both_ranks_equal_genus": True,
        "edge_conditional_d3_from_mccxi": True,
        "face_conditional_d3_via_duality": True,
        "conditional_dq3_for_both_codes": True,
        "assumption_bundle_declared": True,
    }
    assert packet["n_verified"] == 12
