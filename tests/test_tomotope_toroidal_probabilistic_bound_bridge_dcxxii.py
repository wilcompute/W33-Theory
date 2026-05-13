from scripts.tomotope_toroidal_probabilistic_bound_bridge import build_bridge


def test_probabilistic_stability():
    payload = build_bridge(stddev=0.5, trials=1000, seed=1337)
    s = payload["summary"]

    assert s["linear_half_horizon"] == 8
    assert s["linear_packet_horizon"] == 14
    assert s["energy_half_horizon"] == 4
    assert s["energy_packet_horizon"] == 7
    assert s["perturbation_stddev"] == 0.5
    assert s["random_seed"] == 1337
    assert s["trials"] == 1000
    assert 0 <= s["stable_successes"] <= 1000
    assert s["stability_probability"] > 0.95


def test_all_probabilistic_identities_hold():
    payload = build_bridge(stddev=0.5, trials=1000, seed=1337)
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True


def test_seeded_runs_are_reproducible():
    a = build_bridge(stddev=0.5, trials=1000, seed=2026)
    b = build_bridge(stddev=0.5, trials=1000, seed=2026)
    assert a["summary"]["stable_successes"] == b["summary"]["stable_successes"]