from scripts.tomotope_toroidal_markov_spectral_moment_bridge import build_bridge


def test_spectral_moment_core_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["state_count"] == 8
    assert (summary["trace_p_num"], summary["trace_p_den"]) == (1, 1)
    assert (summary["trace_p2_num"], summary["trace_p2_den"]) == (37, 16)
    assert (
        summary["nontrivial_second_moment_num"],
        summary["nontrivial_second_moment_den"],
    ) == (21, 16)


def test_scaled_transport_recovery_chain():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["scaled_unoriented_transport"] == 21
    assert summary["scaled_oriented_transport"] == 42
    assert summary["stabilizer_weighted_transport"] == 168


def test_all_bridge_identities_hold():
    payload = build_bridge()
    identities = payload["identities"]
    assert all(identities.values())
    assert payload["summary"]["all_identities_hold"] is True
