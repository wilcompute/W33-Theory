from scripts.tomotope_toroidal_directional_split_bridge import build_bridge


def test_directional_split_counts():
    payload = build_bridge()
    s = payload["summary"]

    assert s["forward_oriented_count"] == 21
    assert s["backward_oriented_count"] == 21
    assert s["total_oriented_count"] == 42


def test_directional_split_matches_dual_family_edges():
    payload = build_bridge()
    s = payload["summary"]

    assert s["csaszar_edges"] == 21
    assert s["szilassi_edges"] == 21
    assert (s["forward_oriented_count"], s["backward_oriented_count"]) == (
        s["csaszar_edges"],
        s["szilassi_edges"],
    )


def test_weighted_directional_closure():
    payload = build_bridge()
    s = payload["summary"]

    assert s["slot_stabilizer_size"] == 4
    assert s["weighted_directional_total"] == 168


def test_all_directional_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
