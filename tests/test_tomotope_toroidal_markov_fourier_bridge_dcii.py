from scripts.tomotope_toroidal_markov_fourier_bridge import build_bridge


def test_fourier_bridge_summary_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["active_cycle_size"] == 7
    assert summary["nontrivial_mode_count"] == 6
    assert (summary["affine_offset_num"], summary["affine_offset_den"]) == (1, 8)
    assert (summary["cosine_scale_num"], summary["cosine_scale_den"]) == (3, 4)


def test_nontrivial_moment_values_match_dci_chain():
    payload = build_bridge()
    summary = payload["summary"]

    assert (summary["nontrivial_sum_num"], summary["nontrivial_sum_den"]) == (0, 1)
    assert (
        summary["nontrivial_square_sum_num"],
        summary["nontrivial_square_sum_den"],
    ) == (21, 16)


def test_closed_form_and_identity_checks_all_hold():
    payload = build_bridge()
    identities = payload["identities"]
    assert all(identities.values())
    assert payload["summary"]["all_identities_hold"] is True
    assert len(payload["closed_form"]["nontrivial_modes_numeric"]) == 6
