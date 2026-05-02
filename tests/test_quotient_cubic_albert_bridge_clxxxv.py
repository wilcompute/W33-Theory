from PART_CLXXXV_QUOTIENT_CUBIC_ALBERT_BRIDGE import (
    Q,
    Q2,
    Q3,
    PHI3,
    PHI6,
    J,
    J_INV,
    K,
    RANK_SEED,
    CENTER_QUADS,
    QUOTIENT_POINTS,
    QUOTIENT_LINES,
    POINTS_PER_LINE,
    LINES_PER_POINT,
    INCIDENCES,
    AFFINE_TRIADS,
    FIBER_TRIADS,
    CUBIC_TRIADS,
    ALBERT_DIM,
    ALBERT_INTERNAL_SPLIT_DIAGONAL,
    ALBERT_INTERNAL_SPLIT_OFFDIAGONAL,
    TRANSPORT_EDGES,
    POINT_GRAPH_EDGES,
    LINE_GRAPH_EDGES,
    TRANSPORT_DEGREE,
    POINT_GRAPH_DEGREE,
    LINE_GRAPH_DEGREE,
    LOCAL_S3_ORDER,
    quotient_cubic_albert_audit,
)


def test_quotient_points_are_cubic_triads():
    assert CENTER_QUADS == 2 * QUOTIENT_POINTS == 90
    assert QUOTIENT_POINTS == CUBIC_TRIADS == 45
    assert CUBIC_TRIADS == AFFINE_TRIADS + FIBER_TRIADS
    assert AFFINE_TRIADS == K * Q == 36
    assert FIBER_TRIADS == Q2 == 9
    assert CUBIC_TRIADS == J * Q2


def test_quotient_lines_are_albert_generation():
    assert QUOTIENT_LINES == ALBERT_DIM == Q3 == 27
    assert ALBERT_DIM == ALBERT_INTERNAL_SPLIT_DIAGONAL + ALBERT_INTERNAL_SPLIT_OFFDIAGONAL
    assert (ALBERT_INTERNAL_SPLIT_DIAGONAL, ALBERT_INTERNAL_SPLIT_OFFDIAGONAL) == (3, 24)


def test_dual_gq42_incidence_numbers():
    assert POINTS_PER_LINE == J == 5
    assert LINES_PER_POINT == Q == 3
    assert INCIDENCES == QUOTIENT_LINES * POINTS_PER_LINE == QUOTIENT_POINTS * LINES_PER_POINT == 135
    assert INCIDENCES == J * Q3


def test_graph_and_transport_counts():
    assert POINT_GRAPH_EDGES == QUOTIENT_POINTS * POINT_GRAPH_DEGREE // 2 == 270
    assert LINE_GRAPH_EDGES == QUOTIENT_LINES * LINE_GRAPH_DEGREE // 2 == INCIDENCES == 135
    assert TRANSPORT_EDGES == QUOTIENT_POINTS * TRANSPORT_DEGREE // 2 == 720
    assert POINT_GRAPH_EDGES + TRANSPORT_EDGES == QUOTIENT_POINTS * (QUOTIENT_POINTS - 1) // 2


def test_local_s3_order():
    assert LOCAL_S3_ORDER == RANK_SEED == 2 * Q == 6


def test_threshold_carrier_relations():
    assert PHI6 + 1 == J_INV
    assert (J * J_INV) % PHI3 == 1


def test_audit_checks_all_true():
    audit = quotient_cubic_albert_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["quotient_lines_to_albert"] == "27 quotient lines = q^3 = dim J_3(O)"
