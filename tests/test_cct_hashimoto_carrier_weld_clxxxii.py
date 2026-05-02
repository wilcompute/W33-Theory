from fractions import Fraction

from PART_CLXXXII_CCT_HASHIMOTO_CARRIER_WELD import (
    Q,
    Q2,
    Q4,
    K,
    LAMBDA,
    MU,
    PHI3,
    PHI6,
    J,
    J_INV,
    EDGES_PER_COLOR,
    EDGE_SHELL,
    DIRECTED_SHELL,
    HASHIMOTO_BRANCH,
    EMPIRE_PACKET,
    QUTRIT_SLACK,
    OPEN_TURNS,
    FIRST_LOOP_LOCAL_WORDS,
    FIRST_LOOP_PROBABILITY,
    ORIENTED_TRIANGLE_PRIMITIVES,
    PARRY_STATIONARY_WEIGHT,
    LEGAL_LENGTH3_CYLINDER,
    cct_hashimoto_carrier_weld_audit,
)


def test_completed_boundary_to_hashimoto_shell():
    assert Q4 == 81
    assert EDGES_PER_COLOR == Q4 - 1 == 80
    assert EDGE_SHELL == Q * EDGES_PER_COLOR == 240
    assert DIRECTED_SHELL == 2 * Q * EDGES_PER_COLOR == 480


def test_hashimoto_branch_law_and_split():
    assert HASHIMOTO_BRANCH == K - 1 == 11
    assert EMPIRE_PACKET == K - MU == 8
    assert QUTRIT_SLACK == Q == 3
    assert HASHIMOTO_BRANCH == EMPIRE_PACKET + QUTRIT_SLACK


def test_cct_first_loop_probability():
    assert FIRST_LOOP_LOCAL_WORDS == HASHIMOTO_BRANCH ** Q == 1331
    assert FIRST_LOOP_PROBABILITY == Fraction(LAMBDA, FIRST_LOOP_LOCAL_WORDS) == Fraction(2, 1331)


def test_doob_lensing_exposes_firewall_sector():
    assert OPEN_TURNS == HASHIMOTO_BRANCH - LAMBDA == Q2 == 9
    assert HASHIMOTO_BRANCH == LAMBDA + OPEN_TURNS


def test_primitive_triangle_and_parry_weights():
    assert ORIENTED_TRIANGLE_PRIMITIVES == 320
    assert ORIENTED_TRIANGLE_PRIMITIVES == DIRECTED_SHELL * LAMBDA // Q
    assert PARRY_STATIONARY_WEIGHT == Fraction(1, 480)
    assert LEGAL_LENGTH3_CYLINDER == Fraction(1, 480 * 1331)


def test_threshold_carrier_relations():
    assert PHI6 + 1 == J_INV
    assert (J * J_INV) % PHI3 == 1


def test_audit_checks_all_true():
    audit = cct_hashimoto_carrier_weld_audit()
    assert all(audit["checks"].values())
    assert audit["bridge_identities"]["firewall_match"] == "9 open turns = q^2 firewall/fiber diagonal sector"
