from exploration.PART_CCCXXII_EMPIRICAL_DATA_V1_CURRENT_RESIDUALS import (
    KOIDE_TARGET,
    SIN2_THETA_W_GUT_TARGET,
    KOIDE_DATA,
    KOIDE_RESIDUAL,
    KOIDE_SIGMA,
    KOIDE_Z,
    SIN2_EFF_LEPT,
    SIGMA_SIN2_EFF_LEPT,
    SIN2_RAW_RESIDUAL,
    SIN2_RAW_Z,
    residual_records,
    empirical_data_current_audit,
)


def test_koide_current_residual():
    assert str(KOIDE_TARGET) == "2/3"
    assert 0.66666 < KOIDE_DATA < 0.66667
    assert abs(KOIDE_RESIDUAL) < 3e-6
    assert KOIDE_SIGMA > 0
    assert abs(KOIDE_Z) < 1


def test_weak_mixing_marked_rg_required():
    assert str(SIN2_THETA_W_GUT_TARGET) == "3/8"
    assert SIN2_EFF_LEPT == 0.23148
    assert SIGMA_SIN2_EFF_LEPT == 0.00012
    assert SIN2_RAW_RESIDUAL < 0
    assert abs(SIN2_RAW_Z) > 100


def test_residual_records_statuses():
    records = residual_records()
    assert len(records) == 2
    assert records[0].status == "PASS_WITHIN_1_SIGMA_UNDER_THIS_SCHEME"
    assert records[1].status == "RG_REQUIRED_NOT_A_DIRECT_PASS_FAIL_TEST"


def test_audit_checks_all_true():
    audit = empirical_data_current_audit()
    assert all(audit["checks"].values())
    assert audit["residuals"][0]["z_score"] == KOIDE_Z
