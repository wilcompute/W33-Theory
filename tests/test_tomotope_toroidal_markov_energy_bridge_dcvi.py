from scripts.tomotope_toroidal_markov_energy_bridge import build_bridge


def test_energy_bridge_summary_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert 0.0 < summary["spectral_radius"] < 1.0
    assert summary["oriented_transport_count"] == 42
    assert 0.0 < summary["energy_decay_base"] < 1.0
    assert summary["one_channel_horizon_steps"] == 4
    assert summary["packet_energy_horizon_steps"] == 7


def test_energy_threshold_behavior():
    payload = build_bridge()
    derived = payload["derived_values"]

    assert derived["energy_at_one_channel_horizon"] <= 1.0
    assert derived["energy_before_one_channel_horizon"] > 1.0
    assert derived["energy_at_packet_horizon"] <= 1.0 / 24.0
    assert derived["energy_before_packet_horizon"] > 1.0 / 24.0


def test_all_energy_bridge_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
