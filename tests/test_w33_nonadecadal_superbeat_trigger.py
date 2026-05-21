from __future__ import annotations

from analysis.w33_nonadecadal_superbeat_trigger import nonadecadal_superbeat_trigger_packet


def test_mclxxiv_obstruction_and_extension_values() -> None:
    packet = nonadecadal_superbeat_trigger_packet()

    assert packet["nonadecadal_obstruction"] == {
        "prime_channel": 19,
        "origin": "k+2*mu-1 with (k,mu)=(12,4)",
        "L_mod_19": 6,
        "statement": "heptadecadal superbeat is not divisible by 19, so 19 is the next unsynchronized structural prime",
    }
    assert packet["nonadecadal_extension"] == {
        "N": 1047566520,
        "identity": "1047566520 = lcm(55135080,19) = 19*55135080",
        "N_over_A_star": 2909907,
        "N_over_cloud": 12932920,
        "duality_identity": "1047566520 = (19*17*13*11*7*9)*360 = (19*17*13*11*7*40)*81",
    }


def test_mclxxiv_all_checks_pass() -> None:
    packet = nonadecadal_superbeat_trigger_packet()

    assert packet["checks"] == {
        "heptadecadal_superbeat_is_55135080": True,
        "heptadecadal_not_divisible_by_19": True,
        "heptadecadal_mod_19_is_6": True,
        "nonadecadal_superbeat_is_minimal_19_closure": True,
        "nonadecadal_closes_action_clock": True,
        "nonadecadal_closes_cloud_packet": True,
        "nonadecadal_preserves_scaled_duality": True,
        "nonadecadal_factorization": True,
        "nonadecadal_over_heptadecadal_superbeat_is_19": True,
    }
    assert packet["n_verified"] == 9
