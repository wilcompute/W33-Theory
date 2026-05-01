import math

from PART_CXLIV_TWO_SECTOR_QCD_COUPLING_COMPILER import (
    ALPHA_UNIFIED,
    MU,
    PHI3,
    PHI6,
    compiled_alpha_s_gut,
    compiled_effective_k3,
    negative_sector_threshold_delta,
    negative_sector_threshold_tau,
    positive_sector_bare_k3,
    sector_roles,
    two_sector_qcd_audit,
)


def test_positive_sector_supplies_24_over_13_bare_k3():
    assert positive_sector_bare_k3() == 24 / PHI3


def test_negative_sector_supplies_phi6_polar_threshold():
    assert abs(negative_sector_threshold_tau() - math.log(math.sqrt(MU / PHI6))) < 1e-15
    assert negative_sector_threshold_tau() < 0


def test_threshold_delta_is_one_loop_and_subpercent():
    delta = negative_sector_threshold_delta(ALPHA_UNIFIED)
    assert -0.002 < delta < 0


def test_compiled_effective_k3_matches_phi6_pipeline_value():
    assert abs(compiled_effective_k3() - 1.849448291286928) < 1e-12


def test_compiled_alpha_s_gut_matches_phi6_pipeline_value():
    assert abs(compiled_alpha_s_gut() - 0.021628071565151053) < 1e-15


def test_sector_roles_are_two_distinct_hashimoto_fields():
    roles = sector_roles()
    assert len(roles) == 2
    assert roles[0].field == "Q(√-Phi4) = Q(√-10)"
    assert roles[1].field == "Q(√-Phi6) = Q(√-7)"
    assert "bare" in roles[0].role
    assert "threshold" in roles[1].role


def test_two_sector_audit_recovers_alpha_s_to_subpercent_sigma():
    audit = two_sector_qcd_audit()
    assert audit["rg_output"]["sigma"] < 0.01
    assert audit["compiled_formula"]["k3_bare"] == 24 / PHI3
    assert "two-sector" in audit["theorem_statement"]
