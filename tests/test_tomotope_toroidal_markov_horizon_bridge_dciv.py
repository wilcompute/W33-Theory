from scripts.tomotope_toroidal_markov_horizon_bridge import build_bridge


def test_horizon_summary_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert 0.0 < summary["spectral_radius"] < 1.0
    assert summary["probability_threshold"] == 1.0 / 24.0
    assert summary["active_packet_threshold"] == 1.0 / 7.0
    assert summary["probability_horizon_steps"] == 7
    assert summary["active_packet_horizon_steps"] == 4


def test_horizon_ordering_and_minimality_related_values():
    payload = build_bridge()
    summary = payload["summary"]
    derived = payload["derived_values"]

    assert summary["active_packet_horizon_steps"] <= summary["probability_horizon_steps"]
    assert derived["active_packet_bound_at_horizon"] <= 1.0
    assert derived["active_packet_bound_before_horizon"] > 1.0


def test_all_horizon_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
