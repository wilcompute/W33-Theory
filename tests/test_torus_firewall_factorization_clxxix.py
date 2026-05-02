from PART_CLXXIX_TORUS_FIREWALL_FACTORIZATION import (
    Q,
    Q2,
    Q4,
    K,
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
    TORUS_EDGES,
    FLAG_ORBITS,
    FLAGS,
    NEXT_H6_EDGES,
    eisenstein_norm,
    torus_firewall_factorization_audit,
)


def test_eisenstein_and_toroidal_projection():
    assert eisenstein_norm(Q - 1, 1) == PHI6 == 7
    assert TORUS_EDGES == Q * PHI6 == 21
    assert FLAG_ORBITS == RANK_SEED * PHI6 == 42
    assert FLAGS == K * PHI6 == 84
    assert FLAGS == 4 * TORUS_EDGES


def test_firewall_projection_factorization():
    assert AFFINE_TRIADS == K * Q == 36
    assert FIREWALL_FIBERS == Q2 == 9
    assert CUBIC_TRIADS == AFFINE_TRIADS + FIREWALL_FIBERS == 45
    assert CUBIC_TRIADS == J * Q2 == 45
    assert K + Q == Q * J == 15


def test_root_projection_and_closures():
    assert ORIENTED_ROOTS == 2 * K * Q == 72
    assert E6_DIM == ORIENTED_ROOTS + RANK_SEED == 78
    assert H1_DIM == ORIENTED_ROOTS + Q2 == Q4 == 81
    assert H1_DIM - E6_DIM == Q


def test_next_h6_edge_identity():
    assert NEXT_H6_EDGES == 66
    assert NEXT_H6_EDGES == PHI3 * J + 1


def test_threshold_carrier_relations():
    assert (J * J_INV) % PHI3 == 1
    assert PHI6 + 1 == J_INV


def test_audit_checks_all_true():
    audit = torus_firewall_factorization_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["closure_equation"] == "k*q+q^2=J*q^2 because k+q=qJ"
