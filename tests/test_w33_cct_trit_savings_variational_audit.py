from __future__ import annotations

from scripts.w33_cct_trit_savings_variational_audit import (
    cct_trit_savings_variational_summary,
)


def test_variational_packet_matches_least_change_equivalence() -> None:
    summary = cct_trit_savings_variational_summary()
    packet = summary["variational_packet"]

    assert packet["neighbor_packet"] == 8
    assert packet["equivalence_identity"] == (
        "d_H(E0,Ei) = |E0| + |Ei| - 2|E0 intersection Ei|"
    )
    assert packet["argmax_overlap_indices"] == packet["argmin_change_indices"]


def test_softargmax_packet_has_hot_uniform_and_cold_concentration() -> None:
    summary = cct_trit_savings_variational_summary()
    packet = summary["softargmax_packet"]

    assert packet["beta_hot"] == 0.0
    assert packet["uniform_hot_probability"] == 0.125
    assert packet["cold_mass_on_argmax_set"] > 0.999
    assert packet["tie_probabilities_equal"] is True


def test_finite_improvement_packet_certifies_hamming_step_bound() -> None:
    summary = cct_trit_savings_variational_summary()
    packet = summary["finite_improvement_packet"]

    assert packet["path_length"] == packet["hamming_initial"]
    assert packet["path_length"] <= packet["fip_bound"]

    potential = packet["potential_values"]
    assert potential == tuple(sorted(potential))


def test_theorem_bundle_is_all_true_and_boundary_explicit() -> None:
    summary = cct_trit_savings_variational_summary()

    assert all(summary["theorem"].values())
    assert summary["w33_alignment_packet"]["count_identity"] == "K-1 = (K-MU)+Q = 11"
    assert "does not claim full global selector closure" in summary["w33_alignment_packet"]["boundary"]
