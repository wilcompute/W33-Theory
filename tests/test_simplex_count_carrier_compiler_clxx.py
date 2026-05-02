from PART_CLXX_SIMPLEX_COUNT_CARRIER_COMPILER import (
    Q,
    K,
    PHI3,
    PHI6,
    J,
    Q4,
    NONZERO_Q4,
    W33_TRIANGLES,
    W33_EDGES,
    W33_DIRECTED_EDGES,
    TORUS_EDGE,
    FLAG_ORBITS,
    FLAG_COUNT,
    NEXT_H,
    NEXT_EDGE,
    NEXT_VERTEX_COMPLETE_FACES,
    NEXT_FACE_COMPLETE_VERTICES,
    simplex_count_carrier_audit,
)


def test_w33_simplex_counts_from_q4_minus_one():
    assert Q4 == 81
    assert NONZERO_Q4 == 80
    assert W33_TRIANGLES == 2 * NONZERO_Q4 == 160
    assert W33_EDGES == Q * NONZERO_Q4 == 240
    assert W33_DIRECTED_EDGES == 2 * Q * NONZERO_Q4 == 480


def test_toroidal_flag_counts_from_phi6():
    assert TORUS_EDGE == 21
    assert FLAG_ORBITS == 2 * Q * PHI6 == 42
    assert FLAG_COUNT == K * PHI6 == 84
    assert FLAG_ORBITS == 2 * TORUS_EDGE
    assert FLAG_COUNT == 4 * TORUS_EDGE


def test_next_h6_edge_closure():
    assert NEXT_H == 2 * Q == 6
    assert NEXT_EDGE == 66
    assert NEXT_EDGE == PHI3 * J + 1
    assert NEXT_VERTEX_COMPLETE_FACES == 44
    assert NEXT_FACE_COMPLETE_VERTICES == 44


def test_audit_checks_all_true():
    audit = simplex_count_carrier_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["next_closure"] == "h=2q, E=C(k,2)=Phi3*J+1=66"
