from PART_CLXVI_FANO_AFFINE_COMPLETION import (
    FANO_LINES,
    FANO_POINTS,
    J_CYCLE,
    Q_AXIS,
    incidence_count,
    pair_count,
    fano_affine_completion_audit,
)


def test_fano_has_seven_points_and_lines():
    assert len(set(FANO_POINTS)) == 7
    assert len(FANO_LINES) == 7


def test_lines_have_three_points_and_points_have_three_lines():
    assert all(len(set(line)) == 3 for line in FANO_LINES)
    counts = incidence_count(FANO_LINES)
    assert all(v == 3 for v in counts.values())


def test_every_pair_on_unique_line():
    counts = pair_count(FANO_LINES)
    assert len(counts) == 21
    assert all(v == 1 for v in counts.values())


def test_affine_cycle_and_infinity_axis():
    assert set(J_CYCLE) == {1, 5, 12, 8}
    assert set(Q_AXIS) == {3, 6, 9}
    assert set(FANO_LINES[-1]) == set(Q_AXIS)


def test_audit_checks_all_true():
    audit = fano_affine_completion_audit()
    assert all(audit["checks"].values())
    assert audit["point_partition"]["affine_J_cycle"] == [1, 5, 12, 8]
    assert audit["point_partition"]["points_at_infinity_q_axis"] == [3, 6, 9]
