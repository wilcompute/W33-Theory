from scripts.tomotope_toroidal_markov_ground_bridge import build_bridge


def test_markov_bridge_core_summary():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["state_count"] == 8
    assert summary["active_state_count"] == 7
    assert summary["packet_total_weight"] == 192
    assert summary["stationary_active_weight"] == 168
    assert summary["stationary_ground_weight"] == 24


def test_stationary_masses_are_7_over_8_and_1_over_8():
    payload = build_bridge()
    summary = payload["summary"]

    assert (summary["stationary_active_mass_num"], summary["stationary_active_mass_den"]) == (7, 8)
    assert (summary["stationary_ground_mass_num"], summary["stationary_ground_mass_den"]) == (1, 8)


def test_transition_matrix_rows_are_stochastic():
    payload = build_bridge()
    row_sums = payload["row_sums"]
    assert all(value == "1/1" for value in row_sums)


def test_all_markov_identities_hold():
    payload = build_bridge()
    identities = payload["identities"]
    assert all(identities.values())
    assert payload["summary"]["all_identities_hold"] is True
