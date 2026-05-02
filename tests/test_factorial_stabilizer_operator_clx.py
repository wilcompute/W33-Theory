from PART_CLX_FACTORIAL_STABILIZER_OPERATOR import (
    Q,
    E,
    DIRECTED_EDGES,
    A0,
    PHI4,
    LOCAL_SEED,
    GLOBAL_LIFT,
    CARTAN_RANK,
    ROOT_STABILIZER,
    E6_ROOTS,
    WEYL_E6_ORDER,
    factorial_stabilizer_audit,
)


def test_local_seed_is_cartan_rank():
    assert LOCAL_SEED == 2 * Q == CARTAN_RANK == 6


def test_global_lift_is_root_stabilizer():
    assert GLOBAL_LIFT == 720
    assert ROOT_STABILIZER == GLOBAL_LIFT == Q * E


def test_edge_and_directed_edge_from_global_lift():
    assert E == GLOBAL_LIFT // Q == 240
    assert DIRECTED_EDGES == 2 * GLOBAL_LIFT // Q == 480
    assert A0 == DIRECTED_EDGES


def test_e6_roots_and_weyl_order_from_factorial_lift():
    assert E6_ROOTS == GLOBAL_LIFT // PHI4 == 72
    assert WEYL_E6_ORDER == GLOBAL_LIFT * GLOBAL_LIFT // PHI4 == 51840
    assert WEYL_E6_ORDER == E6_ROOTS * ROOT_STABILIZER


def test_audit_checks_all_true():
    audit = factorial_stabilizer_audit()
    assert all(audit["checks"].values())
    assert audit["derived_closure"]["W_E6"] == "|W(E6)|=(2q)!^2/Phi4=51840"
