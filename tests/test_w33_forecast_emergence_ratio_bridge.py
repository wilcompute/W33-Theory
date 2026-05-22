from __future__ import annotations

from analysis.w33_forecast_emergence_ratio_bridge import (
    forecast_emergence_ratio_bridge_packet,
)


def test_mcxcviii_packets() -> None:
    packet = forecast_emergence_ratio_bridge_packet()

    assert packet["packets"] == {
        "S": 24,
        "P": 12,
        "E": 32,
        "M": 18432,
        "A1": 4608,
    }
    assert packet["bridge"] == {
        "M_over_A1": 4,
        "S_over_P": 2,
        "identity": "M/A1 = (S/P)^2 = 4 and M = 4*A1",
    }


def test_mcxcviii_all_checks_pass() -> None:
    packet = forecast_emergence_ratio_bridge_packet()

    assert packet["checks"] == {
        "emergence_identity": True,
        "forecast_identity": True,
        "divisibility_m_over_a1": True,
        "ratio_m_over_a1_is_4": True,
        "divisibility_s_over_p": True,
        "ratio_s_over_p_is_2": True,
        "ratio_bridge_law": True,
        "equivalent_bridge_m_equals_ratio_times_a1": True,
        "e_cancels_in_bridge": True,
        "numeric_identity": True,
    }
    assert packet["n_verified"] == 10
