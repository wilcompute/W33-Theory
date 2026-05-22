from __future__ import annotations

from analysis.w33_post_monodromy_octet_lift import post_monodromy_octet_lift_packet


def test_mcci_packets() -> None:
    packet = post_monodromy_octet_lift_packet()

    assert packet["packets"] == {
        "A0": 576,
        "A1": 4608,
        "M": 18432,
        "A2": 36864,
        "C": 8,
        "E": 32,
        "S": 24,
    }
    assert packet["forecast_lock"] == {
        "identity": "A2=8*A1=64*A0=36864=2*M=2*E*S^2",
    }


def test_mcci_all_checks_pass() -> None:
    packet = post_monodromy_octet_lift_packet()

    assert packet["checks"] == {
        "base_packet_is_consistent": True,
        "a2_is_octet_lift_of_a1": True,
        "a2_is_36864": True,
        "a2_over_a0_is_64": True,
        "a2_over_a1_is_8": True,
        "a2_over_m_is_2": True,
        "a2_equals_2m": True,
        "a2_equals_2e_s_square": True,
        "m_equals_e_s_square": True,
        "power_chain_identity": True,
    }
    assert packet["n_verified"] == 10
