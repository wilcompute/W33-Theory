from scripts.tomotope_toroidal_binary_lattice_bridge import build_bridge


def test_binary_lattice_core_exponents():
    payload = build_bridge()
    s = payload["summary"]

    assert s["base_shell"] == 21
    assert (s["exponent_base"], s["exponent_oriented"], s["exponent_quotient"], s["exponent_weighted"]) == (
        0,
        1,
        2,
        3,
    )


def test_horizon_pair_and_gap_duality():
    payload = build_bridge()
    s = payload["summary"]

    assert (s["linear_half_horizon"], s["linear_packet_horizon"]) == (8, 14)
    assert (s["energy_half_horizon"], s["energy_packet_horizon"]) == (4, 7)
    assert (s["linear_packet_horizon"] - s["linear_half_horizon"]) == 6
    assert (s["energy_packet_horizon"] - s["energy_half_horizon"]) == 3


def test_all_binary_lattice_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
