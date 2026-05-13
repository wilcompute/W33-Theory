from scripts.tomotope_toroidal_biscale_automaton_bridge import build_bridge


def test_biscale_horizons_and_full_times():
    payload = build_bridge()
    s = payload["summary"]

    assert (s["linear_half_horizon"], s["linear_packet_horizon"]) == (8, 14)
    assert (s["energy_half_horizon"], s["energy_packet_horizon"]) == (4, 7)
    assert (s["first_energy_full_t"], s["first_linear_full_t"]) == (7, 14)


def test_joint_state_structure():
    payload = build_bridge()
    s = payload["summary"]
    joint = payload["joint_state_order"]

    assert s["distinct_joint_states"] == 5
    assert joint == [
        "L_pre|E_pre",
        "L_pre|E_mid",
        "L_pre|E_full",
        "L_mid|E_full",
        "L_full|E_full",
    ]


def test_all_biscale_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
