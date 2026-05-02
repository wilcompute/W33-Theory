from PART_CLXIII_DECIMAL_REPTEND_COMPILER import (
    Q,
    PHI4,
    PHI6,
    RANK_SEED,
    decimal_reptend_compiler_audit,
    multiplicative_order,
    reptend,
    terminating_denominators_1_to_9,
    q_axis_denominators_1_to_9,
    reptend_multiples,
)


def test_reptend_core_is_phi4_phi6_period_2q():
    assert PHI4 == 10
    assert PHI6 == 7
    assert multiplicative_order(PHI4, PHI6) == RANK_SEED == 2 * Q == 6
    assert reptend(1, PHI6, PHI4) == "142857"


def test_reptend_formula_and_all_nines_identity():
    block = int(reptend(1, PHI6, PHI4))
    assert block == (PHI4 ** RANK_SEED - 1) // PHI6 == 142857
    assert PHI6 * block == PHI4 ** RANK_SEED - 1 == 999999


def test_digit_partition_of_denominators_1_to_9():
    assert set(terminating_denominators_1_to_9()) == {1, 2, 4, 5, 8}
    assert set(q_axis_denominators_1_to_9()) == {3, 6, 9}
    assert set(terminating_denominators_1_to_9()) | set(q_axis_denominators_1_to_9()) | {PHI6} == set(range(1, 10))


def test_all_multiples_of_one_seventh_are_rotations():
    multiples = reptend_multiples()
    assert len(multiples) == 6
    assert all(m.is_rotation for m in multiples)
    assert [m.block for m in multiples] == ["142857", "285714", "428571", "571428", "714285", "857142"]


def test_mod12_quarter_axis():
    assert {Q, RANK_SEED, Q * Q, 12} == {3, 6, 9, 12}


def test_audit_checks_all_true():
    audit = decimal_reptend_compiler_audit()
    assert all(audit["checks"].values())
    assert audit["reptend_core"]["reptend"] == "142857"
