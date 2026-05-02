from PART_CLXXV_TRIPLE_ALBERT_E8_GRADING import (
    Q,
    PHI3,
    PHI6,
    J,
    J_INV,
    OCTONION_DIM,
    ALBERT_DIM,
    ALBERT_DIAGONAL,
    ALBERT_OFFDIAGONAL,
    GENERATION_COUNT,
    TRIPLE_ALBERT_DIM,
    TRIPLE_DIAGONAL,
    TRIPLE_OFFDIAGONAL,
    E6_RANK,
    E6_ROOTS,
    E6_DIM,
    A2_DIM,
    G0_DIM,
    G1_DIM,
    G2_DIM,
    E8_DIM,
    albert_copies,
    triple_albert_e8_audit,
)


def test_single_albert_generation_dimensions():
    assert OCTONION_DIM == 1 + PHI6 == J_INV == 8
    assert ALBERT_DIAGONAL == Q == 3
    assert ALBERT_OFFDIAGONAL == Q * OCTONION_DIM == 24
    assert ALBERT_DIM == ALBERT_DIAGONAL + ALBERT_OFFDIAGONAL == Q ** 3 == 27


def test_triple_albert_is_h1_and_splits_9_plus_72():
    assert GENERATION_COUNT == Q == 3
    assert TRIPLE_ALBERT_DIM == GENERATION_COUNT * ALBERT_DIM == 81
    assert TRIPLE_DIAGONAL == Q ** 2 == 9
    assert TRIPLE_OFFDIAGONAL == 72
    assert TRIPLE_DIAGONAL + TRIPLE_OFFDIAGONAL == TRIPLE_ALBERT_DIM


def test_e6_rank_root_decomposition_from_triple_albert():
    assert E6_RANK == 2 * Q == 6
    assert E6_ROOTS == TRIPLE_OFFDIAGONAL == 72
    assert E6_DIM == E6_RANK + E6_ROOTS == 78


def test_e8_z3_grading_dimensions():
    assert A2_DIM == OCTONION_DIM == 8
    assert G0_DIM == E6_DIM + A2_DIM == 86
    assert G1_DIM == G2_DIM == 81
    assert E8_DIM == G0_DIM + G1_DIM + G2_DIM == 248


def test_one_albert_copy_per_fano_direction():
    rows = albert_copies()
    assert len(rows) == Q
    assert {r.direction_residue for r in rows} == {3, 6, 9}
    assert all(r.total_dim == 27 for r in rows)
    assert all(r.diagonal_dim == 3 and r.offdiagonal_dim == 24 for r in rows)


def test_threshold_carrier_inverse():
    assert (J * J_INV) % PHI3 == 1


def test_audit_checks_all_true():
    audit = triple_albert_e8_audit()
    assert all(audit["checks"].values())
    assert audit["triple_albert_split"]["formula"] == "3*(3+24)=9+72=81"
    assert audit["e8_z3_grading"][-1]["dimension"] == 248
