from scripts.tomotope_toroidal_commutative_closure_bridge import build_bridge


def test_closure_totals_and_halves():
    payload = build_bridge()
    s = payload["summary"]

    assert s["edge_pair_total"] == 42
    assert s["directional_total"] == 42
    assert s["family_total"] == 42
    assert s["transport_total"] == 42
    assert s["half_split_value"] == 21


def test_closure_weighted_and_duality_values():
    payload = build_bridge()
    s = payload["summary"]

    assert s["weighted_total"] == 168
    assert (s["directional_half_horizon"], s["energy_half_horizon"]) == (8, 4)
    assert (s["directional_packet_horizon"], s["energy_packet_horizon"]) == (14, 7)


def test_all_closure_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
