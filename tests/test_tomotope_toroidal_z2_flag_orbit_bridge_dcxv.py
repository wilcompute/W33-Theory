from scripts.tomotope_toroidal_z2_flag_orbit_bridge import build_bridge


def test_flag_orbit_core_values():
    payload = build_bridge()
    s = payload["summary"]

    assert s["weighted_shell_size"] == 168
    assert s["z2_weighted_orbit_count"] == 84
    assert s["csaszar_flags"] == 84
    assert s["szilassi_flags"] == 84
    assert s["dual_toroidal_flags"] == 168


def test_all_flag_orbit_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
