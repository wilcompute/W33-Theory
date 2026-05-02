from PART_CLVIII_GLOBAL_E6_WEYL_CLOSURE import (
    Q,
    E,
    V,
    K,
    MU,
    DIRECTED_EDGES,
    TRIANGLES,
    RAMANUJAN_REAL,
    CARTAN_SEED,
    E6_ROOTS,
    ROOT_STABILIZER,
    SP43_ORDER,
    WEYL_E6_ORDER,
    global_e6_weyl_closure_audit,
)


def test_sp43_equals_weyl_e6_order():
    assert SP43_ORDER == WEYL_E6_ORDER == 51840


def test_e6_roots_from_ramanujan_shell_minus_cartan_seed():
    assert RAMANUJAN_REAL == 78
    assert CARTAN_SEED == 2 * Q == 6
    assert E6_ROOTS == RAMANUJAN_REAL - CARTAN_SEED == 72


def test_root_stabilizer_is_q_times_edge_carrier():
    assert ROOT_STABILIZER == Q * E == 720
    assert E6_ROOTS * ROOT_STABILIZER == SP43_ORDER


def test_w33_orbit_stabilizers():
    assert SP43_ORDER // V == (2 * Q) ** 4 == 1296
    assert SP43_ORDER // E == Q**3 * (Q**2 - 1) == 216
    assert SP43_ORDER // DIRECTED_EDGES == MU * Q**3 == 108
    assert SP43_ORDER // TRIANGLES == MU * Q**4 == 324


def test_audit_checks_all_true():
    audit = global_e6_weyl_closure_audit()
    assert all(audit["checks"].values())
    assert audit["e6_shell_closure"]["closure_identity"] == "|Sp(4,3)| = (78-2q)*(qE) = 72*720 = 51840"
