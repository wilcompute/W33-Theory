from scripts.tomotope_toroidal_dual_packet_bridge import build_bridge


def test_bridge_summary_core_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["csaszar_realizations"] == 5
    assert summary["szilassi_realizations"] == 2
    assert summary["toroidal_mode_count"] == 7
    assert summary["packet_size"] == 24
    assert summary["active_toroidal_packets"] == 7
    assert summary["ground_packets"] == 1
    assert summary["total_packets"] == 8


def test_weight_ladder_matches_dual_toroidal_and_tomotope_scales():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["active_packet_weight"] == 168
    assert summary["ground_packet_weight"] == 24
    assert summary["tomotope_weight"] == 192
    assert summary["dual_toroidal_flag_weight"] == 168
    assert summary["all_identities_hold"] is True


def test_mode_assignment_has_five_plus_two_plus_ground_split():
    payload = build_bridge()
    assignment = payload["mode_packet_assignment"]

    assert len(assignment) == 8
    families = [row["family"] for row in assignment]
    assert families.count("csaszar") == 5
    assert families.count("szilassi") == 2
    assert families.count("ground") == 1
    assert all(row["packet_weight"] == 24 for row in assignment)


def test_polyhedra_side_exact_flag_counts():
    payload = build_bridge()
    polyhedra = payload["polyhedra"]

    assert polyhedra["csaszar"]["flags"] == 84
    assert polyhedra["szilassi"]["flags"] == 84
    assert polyhedra["csaszar"]["flags"] + polyhedra["szilassi"]["flags"] == 168
