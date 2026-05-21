from __future__ import annotations

from analysis.w33_icosiennea_superbeat_trigger import icosiennea_superbeat_trigger_packet


def test_mclxxvi_obstruction_and_extension_values() -> None:
    packet = icosiennea_superbeat_trigger_packet()

    assert packet["icosiennea_obstruction"] == {
        "prime_channel": 29,
        "origin": "k+4*mu+1 with (k,mu)=(12,4)",
        "O_mod_29": 9,
        "statement": "icosatrio superbeat is not divisible by 29, so 29 is the next unsynchronized structural prime",
    }
    assert packet["icosiennea_extension"] == {
        "P": 698726868840,
        "identity": "698726868840 = lcm(24094029960,29) = 29*24094029960",
        "P_over_A_star": 1940907969,
        "P_over_cloud": 8626257640,
        "duality_identity": "698726868840 = (29*23*19*17*13*11*7*9)*360 = (29*23*19*17*13*11*7*40)*81",
    }


def test_mclxxvi_all_checks_pass() -> None:
    packet = icosiennea_superbeat_trigger_packet()

    assert packet["checks"] == {
        "icosatrio_superbeat_is_24094029960": True,
        "icosatrio_not_divisible_by_29": True,
        "icosatrio_mod_29_is_9": True,
        "icosiennea_superbeat_is_minimal_29_closure": True,
        "icosiennea_closes_action_clock": True,
        "icosiennea_closes_cloud_packet": True,
        "icosiennea_preserves_scaled_duality": True,
        "icosiennea_factorization": True,
        "icosiennea_over_icosatrio_superbeat_is_29": True,
    }
    assert packet["n_verified"] == 9
