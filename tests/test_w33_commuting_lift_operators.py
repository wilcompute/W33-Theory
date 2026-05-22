from __future__ import annotations

from analysis.w33_commuting_lift_operators import commuting_lift_operators_packet


def test_mcxcix_packets() -> None:
    packet = commuting_lift_operators_packet()

    assert packet["base_packet"] == {
        "A0_reye": 576,
        "cell_lift_C": 8,
        "scale_lift_s": 4,
        "A1": 4608,
        "M": 18432,
    }
    assert packet["operator_lock"] == {
        "C_then_s": 18432,
        "s_then_C": 18432,
        "combined_factor": 32,
        "identity": "M = L_s(L_C(A0)) = L_C(L_s(A0)) = 32*A0 = 8*4*576",
    }


def test_mcxcix_all_checks_pass() -> None:
    packet = commuting_lift_operators_packet()

    assert packet["checks"] == {
        "base_reye_symmetry_is_576": True,
        "cell_lift_is_8": True,
        "scale_lift_is_4": True,
        "first_lift_matches_forecast_a1": True,
        "second_lift_matches_monodromy": True,
        "lifts_commute": True,
        "combined_lift_is_32": True,
        "combined_lift_matches_monodromy": True,
        "monodromy_over_base_is_32": True,
        "operator_identity": True,
    }
    assert packet["n_verified"] == 10
