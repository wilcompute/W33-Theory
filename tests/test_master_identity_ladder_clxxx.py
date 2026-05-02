from PART_CLXXX_MASTER_IDENTITY_LADDER import (
    Q,
    Q2,
    Q3,
    Q4,
    K,
    PHI3,
    PHI4,
    PHI6,
    RANK_SEED,
    J,
    J_INV,
    NORM,
    OCTONION_DIM,
    ALBERT_DIM,
    TRIPLE_ALBERT,
    TRIPLE_DIAGONAL,
    TRIPLE_OFFDIAGONAL,
    E6_DIM,
    A2_DIM,
    G0_DIM,
    E8_DIM,
    TORUS_EDGES,
    FLAG_ORBITS,
    FLAGS,
    NEXT_H6_EDGES,
    AFFINE_TRIADS,
    FIREWALL_FIBERS,
    CUBIC_TRIADS,
    ORIENTED_ROOTS,
    master_identity_ladder_audit,
)


def test_master_ladder_core():
    assert NORM == PHI6 == 7
    assert OCTONION_DIM == 1 + PHI6 == J_INV == 8
    assert ALBERT_DIM == 3 + 3 * OCTONION_DIM == Q3 == 27
    assert TRIPLE_ALBERT == Q * ALBERT_DIM == Q4 == 81


def test_firewall_e6_h1_split():
    assert TRIPLE_DIAGONAL == Q2 == 9
    assert TRIPLE_OFFDIAGONAL == ORIENTED_ROOTS == 72
    assert TRIPLE_DIAGONAL + TRIPLE_OFFDIAGONAL == TRIPLE_ALBERT
    assert E6_DIM == ORIENTED_ROOTS + RANK_SEED == 78
    assert TRIPLE_ALBERT - E6_DIM == Q


def test_e8_z3_closure():
    assert A2_DIM == OCTONION_DIM == 8
    assert G0_DIM == E6_DIM + A2_DIM == 86
    assert E8_DIM == G0_DIM + TRIPLE_ALBERT + TRIPLE_ALBERT == 248


def test_toroidal_projection():
    assert TORUS_EDGES == Q * PHI6 == 21
    assert FLAG_ORBITS == RANK_SEED * PHI6 == 42
    assert FLAGS == K * PHI6 == 84
    assert NEXT_H6_EDGES == PHI3 * J + 1 == 66


def test_firewall_square_projection():
    assert AFFINE_TRIADS == K * Q == 36
    assert FIREWALL_FIBERS == Q2 == 9
    assert CUBIC_TRIADS == AFFINE_TRIADS + FIREWALL_FIBERS == J * Q2 == 45
    assert ORIENTED_ROOTS == 2 * AFFINE_TRIADS == 72
    assert K + Q == Q * J == 15


def test_threshold_carrier_inverse_and_atoms():
    assert (J * J_INV) % PHI3 == 1
    assert (Q, Q2, Q3, Q4) == (3, 9, 27, 81)
    assert (K, PHI3, PHI4, PHI6) == (12, 13, 10, 7)


def test_audit_checks_all_true():
    audit = master_identity_ladder_audit()
    assert all(audit["checks"].values())
    assert audit["compact_formulae"]["E8_closure"] == "248=(78+8)+81+81"
