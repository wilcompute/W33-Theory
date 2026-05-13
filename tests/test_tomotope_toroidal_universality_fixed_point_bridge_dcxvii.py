from scripts.tomotope_toroidal_universality_fixed_point_bridge import build_bridge


def test_universality_core_values():
    payload = build_bridge()
    s = payload["summary"]

    assert s["base_shell"] == 21
    assert s["oriented_shell"] == 42
    assert s["quotient_shell"] == 84
    assert s["weighted_shell"] == 168


def test_binary_ladder_and_horizon_pairs():
    payload = build_bridge()
    s = payload["summary"]

    assert payload["binary_ladder"] == [21, 42, 84, 168]
    assert (s["linear_half_horizon"], s["linear_packet_horizon"]) == (8, 14)
    assert (s["energy_half_horizon"], s["energy_packet_horizon"]) == (4, 7)


def test_all_universality_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
