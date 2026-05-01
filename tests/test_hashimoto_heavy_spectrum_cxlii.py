import math

from PART_CXLII_HASHIMOTO_HEAVY_SPECTRUM_DERIVATION import (
    HASHIMOTO_NORM,
    MU,
    PHI6,
    Q,
    derived_threshold_branches,
    hashimoto_field_sectors,
    hashimoto_heavy_spectrum_audit,
)


def test_phi6_sector_real_imag_ratio_is_sqrt_mu_over_phi6():
    sectors = {s.label: s for s in hashimoto_field_sectors()}
    phi6 = sectors["negative s=-4 / Phi6 sector"]
    assert phi6.real_square == MU
    assert phi6.imaginary_square == PHI6
    assert abs(phi6.real_imag_ratio - math.sqrt(MU / PHI6)) < 1e-15


def test_ramanujan_modulus_over_q_clock_is_sqrt_kminus1_over_q():
    sectors = hashimoto_field_sectors()
    for s in sectors:
        assert s.norm_square == HASHIMOTO_NORM
        assert abs(s.modulus / math.sqrt(Q) - math.sqrt(HASHIMOTO_NORM / Q)) < 1e-15


def test_derived_branches_are_ppm_close_to_rg_inverse_target():
    branches = {b.branch_label: b for b in derived_threshold_branches()}
    assert abs(branches["24/13 branch from Phi6-sector polar ratio"].relative_k3_error_ppm) < 10
    assert abs(branches["13/7 branch from Ramanujan radial/q-clock ratio"].relative_k3_error_ppm) < 20


def test_24_over_13_branch_uses_negative_phi6_polar_threshold():
    branches = {b.branch_label: b for b in derived_threshold_branches()}
    b = branches["24/13 branch from Phi6-sector polar ratio"]
    assert b.tau < 0
    assert "sqrt(mu/Phi6)" in b.tau_source


def test_13_over_7_branch_uses_positive_radial_q_clock_threshold():
    branches = {b.branch_label: b for b in derived_threshold_branches()}
    b = branches["13/7 branch from Ramanujan radial/q-clock ratio"]
    assert b.tau > 0
    assert "sqrt((k-1)/q)" in b.tau_source


def test_audit_contains_exact_derivations():
    audit = hashimoto_heavy_spectrum_audit()
    deriv = audit["exact_derivations"]
    assert "sqrt(mu/Phi6)" in deriv["phi6_polar_ratio"]
    assert "sqrt((k-1)/q)" in deriv["ramanujan_q_clock_ratio"]
    assert len(audit["hashimoto_field_sectors"]) == 2
    assert len(audit["derived_threshold_branches"]) == 2
