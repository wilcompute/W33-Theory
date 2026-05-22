from __future__ import annotations

from analysis.w33_octet_lift_forecast import octet_lift_forecast_packet


def test_mcxcvii_packets() -> None:
    packet = octet_lift_forecast_packet()

    assert packet["base_packet"] == {
        "C": 8,
        "N0": 72,
        "A0": 576,
        "identity": "A0=C*N0=8*72=576",
    }
    assert packet["forecast_packet"] == {
        "N1": 576,
        "A1": 4608,
        "identity": "N1=8*72=576 and A1=8*576=4608",
    }
    assert packet["cross_bridge"] == {
        "E": 32,
        "P": 12,
        "identity": "A1=E*P^2=32*12^2=4608",
    }


def test_mcxcvii_all_checks_pass() -> None:
    packet = octet_lift_forecast_packet()

    assert packet["checks"] == {
        "base_identity": True,
        "forecast_horizon_total": True,
        "forecast_symmetry_volume": True,
        "forecast_chain_is_octet_iterate": True,
        "forecast_symmetry_equals_edge_point_square": True,
        "forecast_ratio_a1_over_a0_is_8": True,
        "forecast_ratio_n1_over_n0_is_8": True,
        "forecast_density_a1_over_n1_is_8": True,
        "forecast_integrality": True,
    }
    assert packet["n_verified"] == 9
