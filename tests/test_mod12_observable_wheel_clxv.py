from PART_CLXV_MOD12_OBSERVABLE_WHEEL import (
    Q,
    Q2,
    RANK_SEED,
    K,
    PHI4,
    PHI6,
    J,
    J_INV,
    BINARY_DUALITY,
    HASHIMOTO_NORM,
    Q_AXIS,
    HOLE_GATE,
    DECIMAL_TERMINATING,
    DECIMAL_CYCLIC,
    DECIMAL_MISSING_Q_AXIS,
    J_CYCLE,
    quarter_table,
    mod12_observable_wheel_audit,
)


def test_wheel_threads():
    assert Q_AXIS == {3, 6, 9, 12}
    assert HOLE_GATE == {3, 4, 7, 12}
    assert DECIMAL_TERMINATING == {1, 2, 4, 5, 8}
    assert DECIMAL_CYCLIC == {7}
    assert DECIMAL_MISSING_Q_AXIS == {3, 6, 9}
    assert J_CYCLE == [1, 5, 12, 8]


def test_q_axis_quarter_boundaries():
    assert [row["boundary"] for row in quarter_table()] == [Q, RANK_SEED, Q2, K]


def test_hole_gate_hits_one_per_quarter():
    assert [row["contains_hole_residue"] for row in quarter_table()] == [[3], [4], [7], [12]]


def test_decimal_partition_is_exact_on_1_to_9():
    assert DECIMAL_TERMINATING | DECIMAL_CYCLIC | DECIMAL_MISSING_Q_AXIS == set(range(1, 10))
    assert DECIMAL_TERMINATING.isdisjoint(DECIMAL_CYCLIC)
    assert DECIMAL_TERMINATING.isdisjoint(DECIMAL_MISSING_Q_AXIS)
    assert DECIMAL_CYCLIC.isdisjoint(DECIMAL_MISSING_Q_AXIS)


def test_bridge_identities_on_wheel():
    assert J + BINARY_DUALITY == PHI6 == 7
    assert 2 * J == PHI4 == 10
    assert (J * J) % 13 == K == 12
    assert J_INV == 8
    assert HASHIMOTO_NORM == K - 1 == 11


def test_audit_checks_all_true():
    audit = mod12_observable_wheel_audit()
    assert all(audit["checks"].values())
    assert audit["wheel_rows"][6]["primary_role"] == "Phi6 torus and decimal cyclic denominator"
