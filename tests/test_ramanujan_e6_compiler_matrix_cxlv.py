from PART_CXLV_RAMANUJAN_E6_COMPILER_MATRIX import (
    NEGATIVE_MULT,
    NEGATIVE_REAL_DIM,
    PHI3,
    POSITIVE_MULT,
    POSITIVE_REAL_DIM,
    RAMANUJAN_COMPLEX_DIM,
    RAMANUJAN_REAL_DIM,
    compiler_sectors,
    ramanujan_e6_audit,
    so_n_adjoint_dim,
    su_n_adjoint_dim,
)


def test_positive_multiplicity_is_su5_adjoint():
    assert POSITIVE_MULT == su_n_adjoint_dim(5) == 24


def test_negative_multiplicity_is_so6_and_su4_adjoint():
    assert NEGATIVE_MULT == so_n_adjoint_dim(6) == 15
    assert NEGATIVE_MULT == su_n_adjoint_dim(4) == 15


def test_real_shell_is_e6_dimension():
    assert POSITIVE_REAL_DIM + NEGATIVE_REAL_DIM == RAMANUJAN_REAL_DIM == 78


def test_complex_shell_is_three_phi3():
    assert RAMANUJAN_COMPLEX_DIM == POSITIVE_MULT + NEGATIVE_MULT == 3 * PHI3


def test_real_shell_is_six_phi3():
    assert RAMANUJAN_REAL_DIM == 6 * PHI3


def test_compiler_roles_are_carrier_and_threshold():
    sectors = compiler_sectors()
    assert len(sectors) == 2
    assert "carrier" in sectors[0].compiler_role
    assert "threshold" in sectors[1].compiler_role
    assert sectors[0].qcd_formula_piece == "k3_bare = 24/Phi3"
    assert sectors[1].qcd_formula_piece == "tau = log sqrt(mu/Phi6)"


def test_audit_records_e6_two_adjoint_compiler():
    audit = ramanujan_e6_audit()
    assert audit["checks"]["real_shell_is_E6_dim"] is True
    assert audit["checks"]["positive_mult_is_su5_adjoint"] is True
    assert audit["checks"]["negative_mult_is_so6_adjoint"] is True
    assert "two-adjoint" in audit["theorem_statement"]
