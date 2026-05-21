from __future__ import annotations

from analysis.w33_heptadecadal_superbeat_trigger import heptadecadal_superbeat_trigger_packet


def test_mclxxiii_obstruction_and_extension_values() -> None:
    packet = heptadecadal_superbeat_trigger_packet()

    assert packet["heptadecadal_obstruction"] == {
        "prime_channel": 17,
        "origin": "k+mu+1 with (k,mu)=(12,4)",
        "K_mod_17": 14,
        "statement": "triskaidecad superbeat is not divisible by 17, so 17 is the next unsynchronized structural prime",
    }
    assert packet["heptadecadal_extension"] == {
        "L": 55135080,
        "identity": "55135080 = lcm(3243240,17) = 17*3243240",
        "L_over_A_star": 153153,
        "L_over_cloud": 680680,
        "duality_identity": "55135080 = (17*13*11*7*9)*360 = (17*13*11*7*40)*81",
    }


def test_mclxxiii_all_checks_pass() -> None:
    packet = heptadecadal_superbeat_trigger_packet()

    assert packet["checks"] == {
        "triskaidecad_superbeat_is_3243240": True,
        "triskaidecad_not_divisible_by_17": True,
        "triskaidecad_mod_17_is_14": True,
        "heptadecadal_superbeat_is_minimal_17_closure": True,
        "heptadecadal_closes_action_clock": True,
        "heptadecadal_closes_cloud_packet": True,
        "heptadecadal_preserves_scaled_duality": True,
        "heptadecadal_factorization": True,
        "heptadecadal_over_triskaidecad_superbeat_is_17": True,
    }
    assert packet["n_verified"] == 9
