from __future__ import annotations

from exploration.w33_promoted_neutrino_family_flag_bridge import build_summary


def test_promoted_neutrino_family_flag_bridge() -> None:
    summary = build_summary()
    theorem = summary["promoted_neutrino_family_flag_theorem"]
    operator = summary["promoted_family_flag_operator"]
    selector = summary["pmns_selector_packet"]

    assert theorem["the_upstream_family_carrier_is_exactly_one_plus_two"] is True
    assert theorem["the_raw_democratic_seesaw_is_a_singlet_plus_isotropic_doublet_packet"] is True
    assert theorem["the_promoted_branch_is_exactly_massless_on_the_singlet_line"] is True
    assert theorem["the_promoted_branch_is_exactly_29_times_the_doublet_projector_plus_one_doublet_cartan"] is True
    assert theorem["the_promoted_doublet_trace_is_exactly_58_mev"] is True
    assert theorem["the_promoted_doublet_anisotropy_reproduces_the_exact_33_ratio"] is True
    assert theorem["the_reactor_channel_is_the_only_heptad_suppressed_pmns_channel"] is True
    assert theorem["the_promoted_physical_branch_is_the_exact_anisotropic_doublet_deformation_of_the_old_family_flag_carrier"] is True

    spectrum = operator["spectrum_mev"]
    assert spectrum["m1"]["exact"] == "0"
    assert abs(spectrum["m2"]["float"] - 8.599519796850178) < 1e-12
    assert abs(spectrum["m3"]["float"] - 49.400480203149826) < 1e-12

    assert selector["sin2_theta12"]["exact"] == "4/13"
    assert selector["sin2_theta23"]["exact"] == "7/13"
    assert selector["sin2_theta13"]["exact"] == "2/91"
    assert selector["weighted_identity"]["float"] == 1.0
