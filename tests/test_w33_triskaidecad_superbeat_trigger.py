from __future__ import annotations

from analysis.w33_triskaidecad_superbeat_trigger import triskaidecad_superbeat_trigger_packet


def test_mclxxii_obstruction_and_extension_values() -> None:
    packet = triskaidecad_superbeat_trigger_packet()

    assert packet["triskaidecad_obstruction"] == {
        "prime_channel": 13,
        "origin": "k+1 with k=12",
        "J_mod_13": 10,
        "statement": "hendecad superbeat is not divisible by 13, so 13 is the next unsynchronized structural prime",
    }
    assert packet["triskaidecad_extension"] == {
        "K": 3243240,
        "identity": "3243240 = lcm(249480,13) = 13*249480",
        "K_over_A_star": 9009,
        "K_over_cloud": 40040,
        "duality_identity": "3243240 = (13*11*7*9)*360 = (13*11*7*40)*81",
    }


def test_mclxxii_all_checks_pass() -> None:
    packet = triskaidecad_superbeat_trigger_packet()

    assert packet["checks"] == {
        "hendecad_superbeat_is_249480": True,
        "hendecad_not_divisible_by_13": True,
        "hendecad_mod_13_is_10": True,
        "triskaidecad_superbeat_is_minimal_13_closure": True,
        "triskaidecad_closes_action_clock": True,
        "triskaidecad_closes_cloud_packet": True,
        "triskaidecad_preserves_scaled_duality": True,
        "triskaidecad_factorization": True,
        "triskaidecad_over_hendecad_superbeat_is_13": True,
    }
    assert packet["n_verified"] == 9
