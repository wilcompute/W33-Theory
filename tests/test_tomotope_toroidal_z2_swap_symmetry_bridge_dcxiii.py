from scripts.tomotope_toroidal_z2_swap_symmetry_bridge import build_bridge


def test_z2_core_counts_and_totals():
    payload = build_bridge()
    s = payload["summary"]

    assert s["forward_count"] == 21
    assert s["backward_count"] == 21
    assert s["csaszar_edges"] == 21
    assert s["szilassi_edges"] == 21
    assert s["oriented_total"] == 42
    assert s["weighted_total"] == 168


def test_sigma_is_order_two_on_both_pairs():
    payload = build_bridge()
    actions = payload["sigma_actions"]

    assert actions["directional_twice"] == {"forward": 21, "backward": 21}
    assert actions["family_twice"] == {"csaszar": 21, "szilassi": 21}


def test_all_z2_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
