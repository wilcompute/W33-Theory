from PART_CXL_RG_THRESHOLD_PINNING import (
    PDG_ALPHA_S_MZ,
    delta_gut_for_candidate,
    rg_threshold_pinning_audit,
    solve_k3_for_target,
    threshold_candidates,
)


def test_delta_formula_exact_direction():
    k3_eff, _ = solve_k3_for_target()
    assert delta_gut_for_candidate(24 / 13, k3_eff) < 0
    assert delta_gut_for_candidate(13 / 7, k3_eff) > 0


def test_k3_eff_is_between_structural_candidates():
    k3_eff, alpha = solve_k3_for_target()
    assert (24 / 13) < k3_eff < (13 / 7)
    assert abs(alpha - PDG_ALPHA_S_MZ) < 1e-8


def test_structural_candidates_need_subpercent_thresholds():
    candidates = {c.label: c for c in threshold_candidates()}
    assert abs(candidates["24/13 = 2k/Phi3"].delta_percent) < 0.25
    assert abs(candidates["13/7 = Phi3/Phi6"].delta_percent) < 0.50


def test_37_over_20_needs_tiny_threshold():
    candidates = {c.label: c for c in threshold_candidates()}
    c = candidates["37/20"]
    assert abs(c.delta_percent) < 0.05


def test_natural_loop_units_are_order_one_or_less_for_structural_candidates():
    candidates = {c.label: c for c in threshold_candidates()}
    assert abs(candidates["24/13 = 2k/Phi3"].natural_loop_units) < 0.5
    assert abs(candidates["13/7 = Phi3/Phi6"].natural_loop_units) < 1.0


def test_audit_pinning_window_consistency():
    audit = rg_threshold_pinning_audit()
    window = audit["pinning_window"]
    assert window["k3_eff_lies_between"] is True
    assert window["delta_24_over_13_percent"] < 0
    assert window["delta_13_over_7_percent"] > 0
    assert window["threshold_span_percent"] < 1.0
