from scripts.tomotope_toroidal_step_transport_bridge import build_bridge


def test_step_bridge_core_counts():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["toroidal_mode_count"] == 7
    assert summary["oriented_transport_count"] == 42
    assert summary["unoriented_transport_count"] == 21
    assert summary["step_class_count"] == 6
    assert summary["per_step_transport_count"] == 7


def test_slot_channel_and_stabilizer_profile():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["slot_count"] == 6
    assert summary["slot_stabilizer_size"] == 4
    assert summary["weighted_active_transport"] == 168


def test_step_to_slot_and_balanced_channel_loads():
    payload = build_bridge()
    step_to_slot = payload["step_to_slot"]
    slot_counts = payload["slot_transport_counts"]

    assert set(step_to_slot.keys()) == {1, 2, 3, 4, 5, 6}
    assert len(set(step_to_slot.values())) == 6
    assert set(slot_counts.values()) == {7}


def test_bridge_matches_active_dual_toroidal_weight():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["active_packet_weight"] == 168
    assert summary["dual_toroidal_flag_weight"] == 168
    assert summary["all_identities_hold"] is True
