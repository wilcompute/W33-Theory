from fractions import Fraction

from PART_CLIII_CYCLOTOMIC_BRIDGE_OPERATOR import (
    Q,
    PHI3,
    PHI4,
    PHI6,
    D,
    bridge_audit,
    bridge_operator,
)


def test_phi4_is_cyclotomic_complement_of_q_in_phi3():
    assert PHI4 == PHI3 - Q


def test_mixer_imbalance_is_q_over_phi3():
    assert D == Fraction(Q, PHI3) == Fraction(3, 13)


def test_bridge_operator_maps_imbalance_to_phi4_projection():
    assert bridge_operator(D) == Fraction(10, 13)
    assert bridge_operator(D) == Fraction(PHI4, PHI3)


def test_phi6_ladder_relations():
    assert PHI6 == PHI3 - 2 * Q
    assert PHI4 - PHI6 == Q


def test_audit_checks_all_true():
    audit = bridge_audit()
    assert all(audit["checks"].values())
    assert audit["operator"]["output"] == "B(D)=10/13"
    assert "inevitable" in audit["theorem_statement"]
