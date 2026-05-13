from scripts.tomotope_toroidal_z2_orbit_quotient_bridge import build_bridge


def test_orbit_quotient_core_values():
    payload = build_bridge()
    s = payload["summary"]

    assert s["oriented_size"] == 42
    assert s["oriented_fixed_points"] == 0
    assert s["oriented_orbit_count"] == 21
    assert s["weighted_size"] == 168
    assert s["weighted_fixed_points"] == 0
    assert s["weighted_orbit_count"] == 84


def test_all_orbit_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
