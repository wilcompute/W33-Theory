"""Focused regression tests for the Casey/W33 RH five-frontier release."""

from __future__ import annotations

import math

from analysis.w33_casey_phase_current import (
    cocycle_boundary_energy,
    horizontal_phase_current,
    reflection_cocycle_current,
    zero_product_current,
)
from analysis.w33_ihara_principal_parts import (
    Quad,
    principal_part,
    sector_definition,
)
from analysis.w33_reflection_countermodels import (
    finite_hp_frequencies,
    orbit_defect_energy,
    quartet_q_coefficients,
)
from analysis.w33_rh_phase_operator import (
    classical_xi_log_moments,
    ihara_factor,
    phase_factor,
    principal_phase_moments,
    ratio_invariants,
)
from scripts.rh_claim_linter import lint_text


def test_casey_product_sign_error_and_cocycle_repair():
    assert abs(zero_product_current(1.0, 0.0, 0.5, 14.0)) > 1e-6
    assert abs(reflection_cocycle_current(1.0, 0.0, 0.5, 14.0)) < 1e-12
    assert cocycle_boundary_energy(0.2) > 0
    assert cocycle_boundary_energy(0.0) == 0


def test_casey_boundary_current_is_not_pointwise_zero():
    assert abs(float(horizontal_phase_current(1 + 5j))) > 0.1


def test_w33_self_adjoint_phase_factorization():
    u = 0.07 - 0.03j
    for eigenvalue in (2, -4):
        assert abs(ihara_factor(u, eigenvalue) - phase_factor(u, eigenvalue)) < 1e-12


def test_w33_phase_operator_does_not_match_classical_xi_ratios():
    finite = ratio_invariants(principal_phase_moments())
    classical = ratio_invariants(classical_xi_log_moments())
    assert not math.isclose(
        finite["S4_over_S2_squared"],
        classical["S4_over_S2_squared"],
        rel_tol=1e-3,
    )


def test_exact_ihara_principal_part_and_denominator_ideal():
    sector = sector_definition("positive", 1)
    assert sector["root"] == Quad.rational(1, 10) / sector["denominator_generator"]
    payload = principal_part(sector)
    assert payload["pole_order"] == 24
    assert payload["series_inverse_identity_exact"] is True
    assert payload["coordinate_denominator_ideal"]["norm"] == "11"
    assert len(payload["principal_part_coefficients"]) == 24


def test_reflection_symmetry_needs_self_adjoint_square_axiom():
    assert finite_hp_frequencies(quartet_q_coefficients(0.0, 14.0)) == [14.0, 14.0]
    assert finite_hp_frequencies(quartet_q_coefficients(0.2, 14.0)) is None
    assert orbit_defect_energy(0.2) > 0


def test_claim_linter_distinguishes_scoped_and_unscoped_claims():
    unsafe = "We prove the classical Riemann Hypothesis. Q.E.D."
    safe = (
        "This proves the finite W(3,3) graph-RH analogue, not the classical "
        "Riemann Hypothesis; a transfer theorem remains missing."
    )
    assert any(finding.rule_id == "RH_PROOF" for finding in lint_text(unsafe))
    assert lint_text(safe) == []
