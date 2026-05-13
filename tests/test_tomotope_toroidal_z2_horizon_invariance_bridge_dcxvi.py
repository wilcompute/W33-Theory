from scripts.tomotope_toroidal_z2_horizon_invariance_bridge import build_bridge


def test_horizon_invariance_core_values():
    payload = build_bridge()
    s = payload["summary"]

    assert s["forward_half_horizon"] == 8
    assert s["backward_half_horizon"] == 8
    assert s["forward_packet_horizon"] == 14
    assert s["backward_packet_horizon"] == 14
    assert s["energy_half_horizon"] == 4
    assert s["energy_packet_horizon"] == 7


def test_all_horizon_invariance_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
