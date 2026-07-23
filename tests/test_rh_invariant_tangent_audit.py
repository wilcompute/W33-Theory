"""Regression tests for the invariant-tangent RH audit."""

import math

from analysis.rh_invariant_tangent_audit import (
    BRANCH,
    build_audit,
    critical_real_part,
    phase_torque_difference,
    phase_torque_sum,
    symmetric_quartet_polynomial,
    symmetric_quartet_roots,
)


def test_exact_w33_graph_rh_survives_audit():
    payload = build_audit()
    assert payload["checks"]["w33_ramanujan_bound"]
    assert payload["checks"]["w33_ihara_nontrivial_poles_on_circle"]
    assert payload["verdict"]["w33_graph_rh_proved"] is True


def test_graph_circle_normalization_uses_base_11():
    radius = 1 / math.sqrt(BRANCH)
    assert math.isclose(critical_real_part(radius, BRANCH), 0.5)
    assert math.isclose(critical_real_part(radius, math.sqrt(BRANCH)), 1.0)


def test_natural_pair_phase_does_not_cancel_on_critical_line():
    assert not math.isclose(phase_torque_sum(1.0, 0.0, 0.0, 14.0), 0.0)


def test_antisymmetric_repair_is_a_different_convention():
    assert math.isclose(phase_torque_difference(1.0, 0.0, 0.0, 14.0), 0.0)
    assert not math.isclose(phase_torque_difference(1.0, 0.0, 0.1, 14.0), 0.0)


def test_reflection_symmetric_entire_counterexample_has_off_line_zeros():
    delta = 0.2
    t0 = 7.0
    for s in (0.1 + 0.7j, 0.4 + 2.0j, 1.2 - 0.3j):
        assert abs(
            symmetric_quartet_polynomial(s, delta, t0)
            - symmetric_quartet_polynomial(1 - s, delta, t0)
        ) < 1e-10
        assert abs(
            symmetric_quartet_polynomial(s.conjugate(), delta, t0)
            - symmetric_quartet_polynomial(s, delta, t0).conjugate()
        ) < 1e-10
    assert all(
        not math.isclose(root.real, 0.5)
        for root in symmetric_quartet_roots(delta, t0)
    )


def test_classical_rh_is_not_promoted_by_the_audit():
    payload = build_audit()
    assert payload["status"] == "PASS"
    assert payload["verdict"]["classical_rh_proved"] is False
