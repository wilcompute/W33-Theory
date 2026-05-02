from PART_CLXXVIII_E6_H1_FIREWALL_CLOSURE_SQUARE import (
    Q,
    Q2,
    Q4,
    PHI3,
    PHI6,
    J,
    J_INV,
    RANK_SEED,
    AFFINE_TRIADS,
    FIREWALL_FIBERS,
    CUBIC_TRIADS,
    ORIENTED_ROOTS,
    E6_DIM,
    H1_DIM,
    A2_DIM,
    G0_DIM,
    E8_DIM,
    closure_square_audit,
)


def test_lower_cubic_closure():
    assert FIREWALL_FIBERS == Q2 == 9
    assert CUBIC_TRIADS == AFFINE_TRIADS + FIREWALL_FIBERS == 45


def test_orientation_root_sector():
    assert ORIENTED_ROOTS == 2 * AFFINE_TRIADS == 72


def test_two_closures_of_root_sector():
    assert E6_DIM == ORIENTED_ROOTS + RANK_SEED == 78
    assert H1_DIM == ORIENTED_ROOTS + FIREWALL_FIBERS == Q4 == 81
    assert H1_DIM - E6_DIM == Q == 3


def test_subtraction_diagnostics():
    assert H1_DIM - ORIENTED_ROOTS == FIREWALL_FIBERS
    assert E6_DIM - ORIENTED_ROOTS == RANK_SEED
    assert CUBIC_TRIADS - AFFINE_TRIADS == FIREWALL_FIBERS


def test_e8_z3_closure():
    assert A2_DIM == J_INV == 8
    assert G0_DIM == E6_DIM + A2_DIM == 86
    assert E8_DIM == G0_DIM + H1_DIM + H1_DIM == 248


def test_threshold_carrier_relations():
    assert (J * J_INV) % PHI3 == 1
    assert PHI6 + 1 == J_INV


def test_audit_checks_all_true():
    audit = closure_square_audit()
    assert all(audit["checks"].values())
    assert audit["commuting_square"]["top"] == "36 --orient x2--> 72"
    assert audit["commuting_square"]["right_H1"] == "72 --+9 firewall--> 81"
