from __future__ import annotations

from exploration.w33_promoted_neutrino_package_bridge import build_summary


def test_promoted_neutrino_package_bridge() -> None:
    summary = build_summary()
    theorem = summary["promoted_neutrino_package_theorem"]
    promoted = summary["promoted_minimal_normal_package"]

    assert summary["status"] == "ok"
    assert theorem["pmns_audit_matches_mu_phi3_phi6_packet"] is True
    assert theorem["promoted_sum_rule_is_exact"] is True
    assert theorem["promoted_delta31_over_delta21_is_exactly_33"] is True
    assert theorem["minimal_normal_branch_forces_delta32_over_delta21_to_be_32_not_33"] is True
    assert theorem["raw_democratic_seesaw_keeps_the_exact_sum_but_has_zero_solar_split"] is True
    assert theorem["raw_democratic_seesaw_therefore_cannot_be_the_promoted_physical_flavor_package"] is True

    masses = promoted["masses_mev"]
    assert masses["m1"]["exact"] == "0"
    assert abs(masses["m2"]["float"] - 8.599519796850178) < 1e-12
    assert abs(masses["m3"]["float"] - 49.400480203149826) < 1e-12

    effective = promoted["effective_masses_mev"]
    assert abs(effective["m_beta"]["float"] - 8.711464509984326) < 1e-12
    assert abs(effective["m_beta_beta"]["float"] - 2.25079578346403) < 1e-12
