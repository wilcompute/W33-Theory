from scripts.tomotope_toroidal_edge_pair_bridge import build_bridge


def test_edge_pair_core_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["csaszar_edges"] == 21
    assert summary["szilassi_edges"] == 21
    assert summary["combined_dual_edges"] == 42
    assert summary["unoriented_transport_count"] == 21
    assert summary["oriented_transport_count"] == 42


def test_oriented_transport_equals_combined_dual_edges():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["oriented_transport_count"] == (
        summary["csaszar_edges"] + summary["szilassi_edges"]
    )


def test_weighted_closure_to_active_packet():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["slot_stabilizer_size"] == 4
    assert summary["stabilizer_weighted_oriented"] == 168
    assert summary["active_packet_weight"] == 168


def test_all_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
