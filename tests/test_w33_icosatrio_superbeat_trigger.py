from __future__ import annotations

from analysis.w33_icosatrio_superbeat_trigger import icosatrio_superbeat_trigger_packet


def test_mclxxv_obstruction_and_extension_values() -> None:
    packet = icosatrio_superbeat_trigger_packet()

    assert packet["icosatrio_obstruction"] == {
        "prime_channel": 23,
        "origin": "k+2*mu+3 with (k,mu)=(12,4)",
        "N_mod_23": 10,
        "statement": "nonadecadal superbeat is not divisible by 23, so 23 is the next unsynchronized structural prime",
    }
    assert packet["icosatrio_extension"] == {
        "O": 24094029960,
        "identity": "24094029960 = lcm(1047566520,23) = 23*1047566520",
        "O_over_A_star": 66927861,
        "O_over_cloud": 297457160,
        "duality_identity": "24094029960 = (23*19*17*13*11*7*9)*360 = (23*19*17*13*11*7*40)*81",
    }


def test_mclxxv_all_checks_pass() -> None:
    packet = icosatrio_superbeat_trigger_packet()

    assert packet["checks"] == {
        "nonadecadal_superbeat_is_1047566520": True,
        "nonadecadal_not_divisible_by_23": True,
        "nonadecadal_mod_23_is_10": True,
        "icosatrio_superbeat_is_minimal_23_closure": True,
        "icosatrio_closes_action_clock": True,
        "icosatrio_closes_cloud_packet": True,
        "icosatrio_preserves_scaled_duality": True,
        "icosatrio_factorization": True,
        "icosatrio_over_nonadecadal_superbeat_is_23": True,
    }
    assert packet["n_verified"] == 9
