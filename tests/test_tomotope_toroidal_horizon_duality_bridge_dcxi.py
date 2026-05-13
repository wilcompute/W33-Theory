from scripts.tomotope_toroidal_horizon_duality_bridge import build_bridge


def test_horizon_values_and_factors():
    payload = build_bridge()
    s = payload["summary"]

    assert s["directional_half_horizon"] == 8
    assert s["energy_one_channel_horizon"] == 4
    assert s["directional_packet_horizon"] == 14
    assert s["energy_packet_horizon"] == 7
    assert s["half_duality_factor"] == 2.0
    assert s["packet_duality_factor"] == 2.0


def test_exact_doubling_laws_hold():
    payload = build_bridge()
    identities = payload["identities"]

    assert identities["half_doubling_law"] is True
    assert identities["packet_doubling_law"] is True


def test_all_duality_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
