from scripts.tomotope_toroidal_markov_phase_regime_bridge import build_bridge


def test_phase_regime_summary_and_counts():
    payload = build_bridge()
    summary = payload["summary"]

    assert 0.0 < summary["spectral_radius"] < 1.0
    assert summary["active_horizon_steps"] == 4
    assert summary["probability_horizon_steps"] == 7
    assert summary["pre_count_resolution_steps"] == 4
    assert summary["count_only_resolution_steps"] == 3


def test_regime_gap_matches_horizon_difference():
    payload = build_bridge()
    summary = payload["summary"]
    counts = payload["regime_counts"]

    assert counts["count_resolved_probability_unresolved"] == (
        summary["probability_horizon_steps"] - summary["active_horizon_steps"]
    )


def test_all_phase_regime_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
