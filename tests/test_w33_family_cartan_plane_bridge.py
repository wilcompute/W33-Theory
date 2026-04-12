from __future__ import annotations

from exploration.w33_family_cartan_plane_bridge import build_summary


def test_family_cartan_plane_bridge() -> None:
    summary = build_summary()
    theorem = summary["family_cartan_plane_theorem"]
    packet = summary["promoted_neutrino_doublet_packet"]

    assert theorem["the_ckm_family_axis_and_the_neutrino_cartan_axis_are_exactly_orthogonal"] is True
    assert theorem["they_have_exactly_the_same_norm"] is True
    assert theorem["the_neutrino_axis_is_exactly_minus_J_times_the_ckm_axis_on_the_family_doublet"] is True
    assert theorem["they_form_a_complete_orthogonal_basis_of_the_common_family_doublet_plane"] is True
    assert theorem["the_promoted_neutrino_branch_is_exactly_29_times_the_doublet_identity_plus_one_cartan_on_the_neutrino_axis"] is True
    assert theorem["quark_family_asymmetry_and_neutrino_family_splitting_are_therefore_one_common_exact_family_cartan_plane"] is True

    assert packet["doublet_mean"]["exact"] == "29"
    assert abs(packet["doublet_eigenvalues_mev"]["m2"] - 8.599519796850178) < 1e-12
    assert abs(packet["doublet_eigenvalues_mev"]["m3"] - 49.400480203149826) < 1e-12
