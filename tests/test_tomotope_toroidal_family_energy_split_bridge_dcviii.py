from scripts.tomotope_toroidal_family_energy_split_bridge import build_bridge


def test_family_energy_split_core_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["csaszar_edges"] == 21
    assert summary["szilassi_edges"] == 21
    assert summary["oriented_edges_total"] == 42
    assert summary["family_half_channel_horizon_steps"] == 4
    assert summary["family_packet_horizon_steps"] == 7


def test_family_threshold_values_cross_correctly():
    payload = build_bridge()
    d = payload["derived_values"]

    assert d["family_energy_at_half_horizon"] <= d["family_half_threshold"]
    assert d["family_energy_before_half_horizon"] > d["family_half_threshold"]
    assert d["family_energy_at_packet_horizon"] <= d["family_packet_threshold"]
    assert d["family_energy_before_packet_horizon"] > d["family_packet_threshold"]


def test_all_family_energy_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
