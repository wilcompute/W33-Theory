from fractions import Fraction

from PART_CLXI_PROJECTIVE_STABILIZER_RESIDUE import (
    Q,
    K,
    PHI3,
    PHI4,
    PHI6,
    HASHIMOTO_NORM,
    STABILIZER,
    T_NUM,
    C_NUM,
    D_NUM,
    mod13,
    projective_stabilizer_residue_audit,
)


def test_stabilizer_residue_and_inverse_recover_mixer_pair():
    assert STABILIZER == 720
    assert T_NUM == STABILIZER % PHI3 == 5
    assert C_NUM == pow(T_NUM, -1, PHI3) == 8
    assert (T_NUM * C_NUM) % PHI3 == 1


def test_residue_pair_generates_mixer_weights():
    assert Fraction(C_NUM, PHI3) == Fraction(8, 13)
    assert Fraction(T_NUM, PHI3) == Fraction(5, 13)
    assert Fraction(C_NUM - T_NUM, PHI3) == Fraction(Q, PHI3) == Fraction(3, 13)


def test_residue_pair_generates_core_atoms():
    assert C_NUM + T_NUM == PHI3 == 13
    assert C_NUM - T_NUM == Q == 3
    assert 2 * T_NUM == PHI4 == 10
    assert 3 * T_NUM - C_NUM == PHI6 == 7


def test_residue_square_generates_degree():
    assert mod13(T_NUM * T_NUM) == K == 12
    assert K - 1 == HASHIMOTO_NORM == 11


def test_audit_checks_all_true():
    audit = projective_stabilizer_residue_audit()
    assert all(audit["checks"].values())
    assert audit["projective_residue"]["carrier_weight"] == "8/13"
    assert audit["projective_residue"]["threshold_weight"] == "5/13"
