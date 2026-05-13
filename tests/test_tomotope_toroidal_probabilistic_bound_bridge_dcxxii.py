from scripts.tomotope_toroidal_probabilistic_bound_bridge import build_bridge


def test_probabilistic_stability():
    payload = build_bridge(stddev=0.5, trials=1000)
    s = payload["summary"]

    assert s["linear_half_horizon"] == 8
    assert s["linear_packet_horizon"] == 14
    assert s["energy_half_horizon"] == 4
    assert s["energy_packet_horizon"] == 7
    assert s["perturbation_stddev"] == 0.5
    assert s["stability_probability"] > 0.95


def test_all_probabilistic_identities_hold():
    payload = build_bridge(stddev=0.5, trials=1000)
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True