from PART_CXLIII_BRANCH_SELECTION_PHI6_POLAR import (
    PHI3,
    PHI6,
    branch_selection_audit,
    score_branches,
    selected_branch,
)


def test_selected_branch_is_phi6_polar():
    selected = selected_branch()
    assert selected.branch_label == "24/13 branch from Phi6-sector polar ratio"
    assert selected.decision == "SELECTED"


def test_selected_branch_has_correct_bare_k3():
    selected = selected_branch()
    assert selected.bare_k3 == 24 / PHI3


def test_rejected_branch_is_global_radial_clock():
    scores = {s.branch_label: s for s in score_branches()}
    radial = scores["13/7 branch from Ramanujan radial/q-clock ratio"]
    assert radial.bare_k3 == PHI3 / PHI6
    assert radial.uses_global_radial_clock == 1
    assert radial.decision == "REJECTED_FOR_QCD_THRESHOLD"


def test_phi6_branch_scores_above_radial_branch():
    scores = score_branches()
    selected = selected_branch()
    assert all(selected.branch_score > s.branch_score for s in scores if s.branch_label != selected.branch_label)


def test_selected_branch_is_ppm_close():
    selected = selected_branch()
    assert abs(selected.relative_k3_error_ppm) < 10


def test_audit_records_qcd_beta0_locality_principle():
    audit = branch_selection_audit()
    assert audit["qcd_beta_atom"]["beta0"] == PHI6
    assert "Phi6" in audit["selection_principle"]
    assert audit["selected_effective_model"]["k3_bare"] == "24/13"
    assert "13/7 branch" in audit["rejected_branch_note"]
