from scripts.tomotope_toroidal_markov_relaxation_bridge import build_bridge


def test_relaxation_summary_shape_and_basic_bounds():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["nontrivial_mode_count"] == 6
    assert 0.0 < summary["spectral_radius"] < 1.0
    assert summary["relaxation_gap"] > 0.0
    assert summary["packet_resolution"] == 1.0 / 24.0


def test_packet_resolution_horizon_is_finite_and_small():
    payload = build_bridge()
    t = payload["summary"]["packet_resolution_steps"]

    assert isinstance(t, int)
    assert t >= 1
    assert t <= 7


def test_all_relaxation_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
