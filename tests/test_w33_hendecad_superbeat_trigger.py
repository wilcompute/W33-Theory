from __future__ import annotations

from analysis.w33_hendecad_superbeat_trigger import hendecad_superbeat_trigger_packet


def test_mclxxi_obstruction_and_extension_values() -> None:
    packet = hendecad_superbeat_trigger_packet()

    assert packet["hendecad_obstruction"] == {
        "prime_channel": 11,
        "origin": "k-1 with k=12",
        "H_mod_11": 9,
        "statement": "heptad superbeat is not divisible by 11, so 11 is the next unsynchronized structural prime",
    }
    assert packet["hendecad_extension"] == {
        "J": 249480,
        "identity": "249480 = lcm(22680,11) = 11*22680",
        "J_over_A_star": 693,
        "J_over_cloud": 3080,
        "duality_identity": "249480 = (11*7*9)*360 = (11*7*40)*81",
    }


def test_mclxxi_all_checks_pass() -> None:
    packet = hendecad_superbeat_trigger_packet()

    assert packet["checks"] == {
        "heptad_superbeat_is_22680": True,
        "superbeat_not_divisible_by_11": True,
        "superbeat_mod_11_is_9": True,
        "hendecad_superbeat_is_minimal_11_closure": True,
        "hendecad_closes_action_clock": True,
        "hendecad_closes_cloud_packet": True,
        "hendecad_preserves_scaled_duality": True,
        "hendecad_factorization": True,
        "hendecad_over_heptad_superbeat_is_11": True,
    }
    assert packet["n_verified"] == 9
