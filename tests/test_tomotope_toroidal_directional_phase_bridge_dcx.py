from scripts.tomotope_toroidal_directional_phase_bridge import build_bridge


def test_directional_phase_summary_values():
    payload = build_bridge()
    s = payload["summary"]

    assert 0.0 < s["spectral_radius"] < 1.0
    assert s["forward_count"] == 21
    assert s["backward_count"] == 21
    assert s["directional_half_horizon_steps"] == 8
    assert s["directional_packet_horizon_steps"] == 14
    assert s["middle_regime_steps"] == 6


def test_directional_regime_gap_matches_horizon_gap():
    payload = build_bridge()
    s = payload["summary"]
    counts = payload["regime_counts"]

    assert counts["direction_half_resolved_packet_unresolved"] == (
        s["directional_packet_horizon_steps"] - s["directional_half_horizon_steps"]
    )


def test_all_directional_phase_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
