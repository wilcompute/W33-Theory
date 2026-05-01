from PART_CXXXIX_RG_EMBEDDING_INVERSION import (
    ALPHA_UNIFIED,
    M_GUT,
    PDG_ALPHA_S_MZ,
    alpha_s_mz_from_k3,
    beta_qcd_2loop,
    candidate_k3_values,
    one_loop_inverse_k3,
    rg_embedding_inversion_audit,
    solve_k3_for_target,
)


def test_beta_qcd_asymptotic_freedom():
    assert beta_qcd_2loop(0.118, nf=5) < 0
    assert beta_qcd_2loop(0.04, nf=6) < 0


def test_k3_one_is_runaway_under_current_inputs():
    assert alpha_s_mz_from_k3(1.0) is None


def test_inverse_k3_solution_recovers_pdg_alpha_s():
    k3, alpha = solve_k3_for_target()
    assert 1.84 < k3 < 1.86
    assert abs(alpha - PDG_ALPHA_S_MZ) < 1e-8


def test_one_loop_inverse_is_same_window_but_lower():
    k3_1loop = one_loop_inverse_k3()
    assert 1.80 < k3_1loop < 1.82


def test_candidate_24_over_13_is_near_pdg():
    candidates = {c.label: c for c in candidate_k3_values()}
    c = candidates["24/13 = 2(k)/Phi3"]
    assert c.alpha_s_mz is not None
    assert abs(c.sigma) < 2.0


def test_candidate_37_over_20_is_sub_sigma():
    candidates = {c.label: c for c in candidate_k3_values()}
    c = candidates["37/20 = (v-mu+1)/(v/2)"]
    assert c.alpha_s_mz is not None
    assert abs(c.sigma) < 0.5


def test_candidate_13_over_7_is_borderline_window():
    candidates = {c.label: c for c in candidate_k3_values()}
    c = candidates["13/7 = Phi3/Phi6 = M_GUT prefactor"]
    assert c.alpha_s_mz is not None
    assert -4.0 < c.sigma < -2.0


def test_audit_internal_consistency():
    audit = rg_embedding_inversion_audit()
    inv = audit["inverse_solution"]
    assert audit["inputs"]["alpha_unified"] == ALPHA_UNIFIED
    assert audit["inputs"]["M_GUT"] == M_GUT
    assert 1.84 < inv["k3_eff_two_loop"] < 1.86
    assert len(audit["candidate_values"]) >= 7
