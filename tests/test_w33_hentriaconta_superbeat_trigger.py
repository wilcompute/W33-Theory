from __future__ import annotations

from analysis.w33_hentriaconta_superbeat_trigger import hentriaconta_superbeat_trigger_packet


def test_mclxxvii_obstruction_and_extension_values() -> None:
    packet = hentriaconta_superbeat_trigger_packet()

    assert packet["hentriaconta_obstruction"] == {
        "prime_channel": 31,
        "origin": "k+4*mu+3 with (k,mu)=(12,4)",
        "P_mod_31": 6,
        "statement": "icosiennea superbeat is not divisible by 31, so 31 is the next unsynchronized structural prime",
    }
    assert packet["hentriaconta_extension"] == {
        "Q": 21660532934040,
        "identity": "21660532934040 = lcm(698726868840,31) = 31*698726868840",
        "Q_over_A_star": 60168147039,
        "Q_over_cloud": 267413986840,
        "duality_identity": "21660532934040 = (31*29*23*19*17*13*11*7*9)*360 = (31*29*23*19*17*13*11*7*40)*81",
    }


def test_mclxxvii_all_checks_pass() -> None:
    packet = hentriaconta_superbeat_trigger_packet()

    assert packet["checks"] == {
        "icosiennea_superbeat_is_698726868840": True,
        "icosiennea_not_divisible_by_31": True,
        "icosiennea_mod_31_is_6": True,
        "hentriaconta_superbeat_is_minimal_31_closure": True,
        "hentriaconta_closes_action_clock": True,
        "hentriaconta_closes_cloud_packet": True,
        "hentriaconta_preserves_scaled_duality": True,
        "hentriaconta_factorization": True,
        "hentriaconta_over_icosiennea_superbeat_is_31": True,
    }
    assert packet["n_verified"] == 9
