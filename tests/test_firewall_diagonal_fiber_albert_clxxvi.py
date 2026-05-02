from PART_CLXXVI_FIREWALL_DIAGONAL_FIBER_ALBERT import (
    Q,
    Q2,
    Q3,
    Q4,
    PHI3,
    J,
    J_INV,
    RANK_SEED,
    ALBERT_DIM,
    ALBERT_DIAGONAL,
    ALBERT_OFFDIAGONAL,
    TRIPLE_ALBERT,
    TRIPLE_DIAGONAL,
    TRIPLE_OFFDIAGONAL,
    HEISENBERG_POINTS,
    U_FIBERS,
    Z_LEVELS,
    FIBER_TRIADS,
    AFFINE_U_LINES,
    AFFINE_LINE_TRIADS,
    CUBIC_TRIADS_TOTAL,
    ORIENTED_AFFINE_ROOTS,
    firewall_diagonal_fiber_audit,
)


def test_triple_albert_72_9_split():
    assert ALBERT_DIM == Q3 == 27
    assert ALBERT_DIAGONAL == Q == 3
    assert ALBERT_OFFDIAGONAL == Q * J_INV == 24
    assert TRIPLE_ALBERT == Q4 == 81
    assert TRIPLE_DIAGONAL == Q2 == 9
    assert TRIPLE_OFFDIAGONAL == 72


def test_heisenberg_fibers_are_q2_firewall_triads():
    assert HEISENBERG_POINTS == Q3 == 27
    assert U_FIBERS == FIBER_TRIADS == Q2 == 9
    assert Z_LEVELS == Q == 3
    assert FIBER_TRIADS * Z_LEVELS == HEISENBERG_POINTS


def test_affine_triads_orient_to_e6_roots():
    assert AFFINE_U_LINES == Q2 + Q == 12
    assert AFFINE_LINE_TRIADS == AFFINE_U_LINES * Q == 36
    assert ORIENTED_AFFINE_ROOTS == 2 * AFFINE_LINE_TRIADS == 72
    assert ORIENTED_AFFINE_ROOTS == TRIPLE_OFFDIAGONAL


def test_cubic_firewall_split_and_h1_bridge():
    assert CUBIC_TRIADS_TOTAL == AFFINE_LINE_TRIADS + FIBER_TRIADS == 45
    assert FIBER_TRIADS + ORIENTED_AFFINE_ROOTS == TRIPLE_ALBERT == 81
    assert RANK_SEED + ORIENTED_AFFINE_ROOTS == 78


def test_threshold_carrier_inverse():
    assert (J * J_INV) % PHI3 == 1


def test_audit_checks_all_true():
    audit = firewall_diagonal_fiber_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["identification"] == "9 fiber triads = triple-Albert diagonal sector; 2*36 oriented affine triads = 72 E6 roots"
