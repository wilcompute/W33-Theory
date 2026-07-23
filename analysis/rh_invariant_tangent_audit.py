#!/usr/bin/env python3
"""Exact audit of the invariant-tangent / phase-torque RH argument.

This module separates three logically different surfaces:

1. the exact Ihara/graph-RH theorem for the W(3,3) collinearity graph;
2. the classical completed-zeta reflection symmetry;
3. the additional compactification, phase-torque, and boundary assumptions used
   in the uploaded topological RH slide decks.

The first surface is exact. The second is standard but only gives symmetry.
The third does not currently imply the classical Riemann Hypothesis.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

Q = 3
V = 40
K = 12
E = 240
BRANCH = K - 1
NONTRIVIAL_EIGENVALUES = (2, -4)


def ihara_poles(adjacency_eigenvalue: int) -> tuple[complex, complex]:
    """Roots of 1 - lambda*u + (k-1)u^2 for W(3,3)."""
    discriminant = adjacency_eigenvalue**2 - 4 * BRANCH
    root_disc = cmath.sqrt(discriminant)
    denominator = 2 * BRANCH
    return (
        (adjacency_eigenvalue + root_disc) / denominator,
        (adjacency_eigenvalue - root_disc) / denominator,
    )


def critical_real_part(radius: float, exponential_base: float) -> float:
    """If u = base^{-s}, return Re(s) corresponding to |u|=radius."""
    if radius <= 0 or exponential_base <= 0 or exponential_base == 1:
        raise ValueError("radius must be positive and base must be positive and != 1")
    return -math.log(radius) / math.log(exponential_base)


def phase_torque_sum(sigma: float, t: float, delta: float, t0: float) -> float:
    """d/dsigma arg[(s-rho_+)(s-rho_-)] for the same-height pair.

    rho_+ = 1/2 + delta + i t0 and rho_- = 1/2 - delta + i t0.
    This is the natural logarithmic phase contribution of the product.
    """
    dt = t - t0
    a_plus = 0.5 + delta
    a_minus = 0.5 - delta
    return (
        -dt / ((sigma - a_plus) ** 2 + dt**2)
        - dt / ((sigma - a_minus) ** 2 + dt**2)
    )


def phase_torque_difference(
    sigma: float, t: float, delta: float, t0: float
) -> float:
    """An antisymmetric difference convention suggested by the slides.

    This vanishes at delta=0, but it is not d/dsigma of the argument of the
    zero-pair product; it inserts an extra relative minus sign.
    """
    dt = t - t0
    a_plus = 0.5 + delta
    a_minus = 0.5 - delta
    return (
        -dt / ((sigma - a_plus) ** 2 + dt**2)
        + dt / ((sigma - a_minus) ** 2 + dt**2)
    )


def symmetric_quartet_polynomial(s: complex, delta: float, t0: float) -> complex:
    """Entire polynomial with RH-like reflection/conjugation symmetry.

    Its zeros are 1/2 +/- delta +/- i t0. For delta > 0 all four zeros are
    off the critical line, while F(1-s)=F(s) and F(conj(s))=conj(F(s)).
    """
    x = s - 0.5
    return ((x - delta) ** 2 + t0**2) * ((x + delta) ** 2 + t0**2)


def symmetric_quartet_roots(delta: float, t0: float) -> tuple[complex, ...]:
    return (
        0.5 + delta + 1j * t0,
        0.5 + delta - 1j * t0,
        0.5 - delta + 1j * t0,
        0.5 - delta - 1j * t0,
    )


def riemann_sphere_map(w: complex | None) -> tuple[float, float, float]:
    """Standard stereographic compactification C union {infinity} -> S^2.

    ``None`` denotes infinity. The map compactifies poles, but by itself places
    no restriction on where zeros of the underlying meromorphic function occur.
    """
    if w is None:
        return (0.0, 0.0, 1.0)
    norm2 = w.real * w.real + w.imag * w.imag
    denominator = norm2 + 1.0
    return (
        2.0 * w.real / denominator,
        2.0 * w.imag / denominator,
        (norm2 - 1.0) / denominator,
    )


def max_abs(values: Iterable[float]) -> float:
    return max(abs(value) for value in values)


def build_audit() -> dict[str, Any]:
    graph_poles = {
        str(eigenvalue): [
            {"real": pole.real, "imag": pole.imag, "modulus": abs(pole)}
            for pole in ihara_poles(eigenvalue)
        ]
        for eigenvalue in NONTRIVIAL_EIGENVALUES
    }
    all_moduli = [
        pole["modulus"] for poles in graph_poles.values() for pole in poles
    ]
    critical_radius = 1.0 / math.sqrt(BRANCH)

    sigma = 1.0
    t = 0.0
    t0 = 14.0
    critical_sum_torque = phase_torque_sum(sigma, t, delta=0.0, t0=t0)
    critical_difference_torque = phase_torque_difference(
        sigma, t, delta=0.0, t0=t0
    )
    off_line_difference_torque = phase_torque_difference(
        sigma, t, delta=0.1, t0=t0
    )

    delta = 0.2
    quartet_t0 = 7.0
    sample_points = (
        0.12 + 0.8j,
        0.41 + 2.3j,
        0.73 - 1.4j,
        1.25 + 0.2j,
    )
    reflection_errors = [
        abs(
            symmetric_quartet_polynomial(s, delta, quartet_t0)
            - symmetric_quartet_polynomial(1 - s, delta, quartet_t0)
        )
        for s in sample_points
    ]
    conjugation_errors = [
        abs(
            symmetric_quartet_polynomial(s.conjugate(), delta, quartet_t0)
            - symmetric_quartet_polynomial(s, delta, quartet_t0).conjugate()
        )
        for s in sample_points
    ]
    quartet_roots = symmetric_quartet_roots(delta, quartet_t0)

    claims = [
        {
            "id": "G1",
            "status": "exact",
            "claim": "W(3,3) is a 12-regular Ramanujan graph.",
            "reason": "Its eigenvalues 2 and -4 satisfy |lambda| < 2*sqrt(11).",
        },
        {
            "id": "G2",
            "status": "exact",
            "claim": "The nontrivial Ihara poles lie on |u|=1/sqrt(11).",
            "reason": "This follows directly from the two quadratic factors.",
        },
        {
            "id": "G3",
            "status": "correction",
            "claim": "The critical circle maps to Re(s)=1/2 under u=11^{-s}.",
            "reason": "Using u=(sqrt(11))^{-s} maps it to Re(s)=1, not 1/2.",
        },
        {
            "id": "Z1",
            "status": "exact_with_domain_caveat",
            "claim": "Completed-zeta symmetry gives phase reflection away from zeros.",
            "reason": "arg(xi) is multivalued and undefined at the zeros.",
        },
        {
            "id": "T1",
            "status": "unsupported",
            "claim": "tan(theta)=Im(z)/Re(z)=tan(phi/2) is an invariant metric.",
            "reason": "It is an angular identity, not a Riemannian metric.",
        },
        {
            "id": "T2",
            "status": "unsupported",
            "claim": "Compactifying s=1 forces a stationary pi/2 boundary.",
            "reason": "Mapping infinity to a point does not force phase derivative zero.",
        },
        {
            "id": "T3",
            "status": "false_for_natural_pair_phase",
            "claim": "A critical-line zero pair has zero boundary phase torque.",
            "reason": "For the natural product phase, both derivatives add.",
        },
        {
            "id": "T4",
            "status": "ad_hoc_if_repaired",
            "claim": "Changing one sign makes torque vanish iff delta=0.",
            "reason": "That difference is not the phase derivative of the product.",
        },
        {
            "id": "T5",
            "status": "fatal_gap",
            "claim": "A local pair contribution cannot be globally cancelled.",
            "reason": "No positivity or no-cancellation theorem is proved.",
        },
        {
            "id": "T6",
            "status": "counterexample",
            "claim": "Reflection symmetry plus compactification forces the line.",
            "reason": "An explicit symmetric quartet polynomial has off-line zeros.",
        },
        {
            "id": "H1",
            "status": "tautological_without_transfer",
            "claim": "lambda -> 1/2+i*sqrt(lambda-1/4) realizes Hilbert-Polya.",
            "reason": "It lands on the line by definition; determinant equality is missing.",
        },
        {
            "id": "C1",
            "status": "not_proved",
            "claim": "The classical Riemann Hypothesis follows.",
            "reason": "The W33 graph-RH is a finite analogue without a transfer theorem.",
        },
    ]

    checks = {
        "w33_ramanujan_bound": all(
            abs(eigenvalue) <= 2 * math.sqrt(BRANCH)
            for eigenvalue in NONTRIVIAL_EIGENVALUES
        ),
        "w33_ihara_nontrivial_poles_on_circle": max_abs(
            modulus - critical_radius for modulus in all_moduli
        )
        < 1e-12,
        "correct_u_equals_11_minus_s_maps_to_half": abs(
            critical_real_part(critical_radius, BRANCH) - 0.5
        )
        < 1e-12,
        "sqrt11_base_maps_to_one_not_half": abs(
            critical_real_part(critical_radius, math.sqrt(BRANCH)) - 1.0
        )
        < 1e-12,
        "natural_pair_torque_nonzero_even_at_delta_zero": abs(
            critical_sum_torque
        )
        > 1e-12,
        "antisymmetric_difference_zero_at_delta_zero": abs(
            critical_difference_torque
        )
        < 1e-12,
        "antisymmetric_difference_nonzero_off_line": abs(
            off_line_difference_torque
        )
        > 1e-12,
        "quartet_reflection_symmetry": max(reflection_errors) < 1e-10,
        "quartet_conjugation_symmetry": max(conjugation_errors) < 1e-10,
        "quartet_has_off_line_zeros": all(
            abs(root.real - 0.5) > 1e-12 for root in quartet_roots
        ),
        "stereographic_infinity_is_north_pole": riemann_sphere_map(None)
        == (0.0, 0.0, 1.0),
        "stereographic_zero_is_south_pole": riemann_sphere_map(0j)
        == (0.0, 0.0, -1.0),
    }

    verdict = {
        "classical_rh_proved": False,
        "w33_graph_rh_proved": True,
        "topological_slide_decks_status": "not a valid proof in current form",
        "salvageable_core": [
            "W(3,3) Ihara determinant",
            "W(3,3) Ramanujan bound",
            "graph-RH critical circle",
            "completed-zeta reflection symmetry away from zeros",
            "phase-gradient language as a heuristic visualization",
        ],
        "minimum_missing_theorem": (
            "A globally defined operator or determinant whose spectrum/zeros are "
            "exactly those of completed zeta, plus a proof that the proposed "
            "boundary functional is coercive or cannot cancel off the line."
        ),
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "invariant tangent regularization and W33 RH bridge audit",
        "constants": {
            "q": Q,
            "v": V,
            "k": K,
            "edges": E,
            "branch": BRANCH,
            "nontrivial_eigenvalues": NONTRIVIAL_EIGENVALUES,
        },
        "graph_rh": {
            "ihara_inverse": (
                "(1-u^2)^200 (1-u)(1-11u) "
                "(1-2u+11u^2)^24 (1+4u+11u^2)^15"
            ),
            "critical_radius": critical_radius,
            "nontrivial_poles": graph_poles,
            "re_s_under_u_equals_11_minus_s": critical_real_part(
                critical_radius, BRANCH
            ),
            "re_s_under_u_equals_sqrt11_minus_s": critical_real_part(
                critical_radius, math.sqrt(BRANCH)
            ),
        },
        "phase_torque_falsifier": {
            "evaluation_point": {"sigma": sigma, "t": t, "t0": t0},
            "natural_sum_at_delta_zero": critical_sum_torque,
            "antisymmetric_difference_at_delta_zero": critical_difference_torque,
            "antisymmetric_difference_at_delta_0_1": off_line_difference_torque,
        },
        "symmetry_counterexample": {
            "definition": (
                "F_delta,t0(s)=(((s-1/2)-delta)^2+t0^2)"
                "*(((s-1/2)+delta)^2+t0^2)"
            ),
            "delta": delta,
            "t0": quartet_t0,
            "roots": [
                {"real": root.real, "imag": root.imag} for root in quartet_roots
            ],
            "max_reflection_error": max(reflection_errors),
            "max_conjugation_error": max(conjugation_errors),
            "conclusion": (
                "Reflection and real conjugation symmetry do not force zeros "
                "onto Re(s)=1/2."
            ),
        },
        "checks": checks,
        "claims": claims,
        "verdict": verdict,
    }


def main() -> None:
    payload = build_audit()
    output = ROOT / "checks" / "rh_invariant_tangent_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
