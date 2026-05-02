from fractions import Fraction

from PART_CLXII_STABILIZER_FIELD_DYNAMICS import (
    Q,
    PHI3,
    PHI4,
    PHI6,
    K,
    HASHIMOTO_NORM,
    J,
    J_INV,
    BINARY_DUALITY,
    mod,
    multiplicative_cycle,
    stabilizer_field_dynamics_audit,
)


def test_stabilizer_residue_is_finite_complex_structure():
    assert J == 5
    assert mod(J * J) == PHI3 - 1 == K == 12
    assert multiplicative_cycle() == [1, 5, 12, 8]


def test_inverse_residue_is_carrier():
    assert J_INV == 8
    assert mod(J * J_INV) == 1
    assert Fraction(J_INV, PHI3) == Fraction(8, 13)


def test_threshold_carrier_imbalance():
    assert Fraction(J, PHI3) == Fraction(5, 13)
    assert Fraction(J_INV - J, PHI3) == Fraction(Q, PHI3) == Fraction(3, 13)


def test_toroidal_and_cyclotomic_atoms_from_residue():
    assert 2 * J == PHI4 == 10
    assert J + BINARY_DUALITY == PHI6 == 7
    assert 3 * J - J_INV == PHI6 == 7


def test_mod12_and_hashimoto_norm():
    assert mod(J * J) == K == 12
    assert K - 1 == HASHIMOTO_NORM == 11


def test_audit_checks_all_true():
    audit = stabilizer_field_dynamics_audit()
    assert all(audit["checks"].values())
    assert audit["toroidal_resonance"]["combined_identity"] == "5+2=7=Phi6"
