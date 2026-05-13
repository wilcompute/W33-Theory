from scripts.tomotope_toroidal_probabilistic_concentration_bridge import build_bridge


def test_concentration_summary_shape():
    payload = build_bridge()
    s = payload["summary"]

    assert s["perturbation_stddev"] == 0.5
    assert s["trials"] >= 1000
    assert 0 <= s["stable_successes"] <= s["trials"]
    assert s["stability_probability"] > 0.95
    assert s["confidence_z"] > 2.0


def test_wilson_bound_is_strong_and_consistent():
    payload = build_bridge()
    s = payload["summary"]

    assert s["wilson_lower_bound"] > 0.95
    assert s["wilson_lower_bound"] <= s["stability_probability"]


def test_all_concentration_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
