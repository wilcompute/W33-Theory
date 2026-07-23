#!/usr/bin/env python3
"""Classification of reflection-symmetric finite RH countermodels.

Put z=s-1/2. A real polynomial satisfying F(1-s)=F(s) is an even real
polynomial in z, hence F(s)=Q(z^2) with Q in R[y]. Its zeros lie on the
critical line exactly when every zero of Q is real and non-positive.

This gives the finite Hilbert-Polya criterion:

    F(s)=C det((s-1/2)^2 I + H^2), H=H*,

if and only if the finite zero set is on Re(s)=1/2 (up to zero multiplicities
and a real constant C). Symmetry alone only gives quartet closure and is far
weaker than this determinant identity.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]


def quartet_polynomial(s: complex, delta: float, gamma: float) -> complex:
    z = s - 0.5
    return ((z - delta) ** 2 + gamma**2) * ((z + delta) ** 2 + gamma**2)


def quartet_roots(delta: float, gamma: float) -> tuple[complex, ...]:
    return (
        0.5 + delta + 1j * gamma,
        0.5 + delta - 1j * gamma,
        0.5 - delta + 1j * gamma,
        0.5 - delta - 1j * gamma,
    )


def quartet_q_coefficients(delta: float, gamma: float) -> tuple[float, float, float]:
    """Q(y)=y^2+b*y+c for F(s)=Q((s-1/2)^2)."""
    return (1.0, 2 * (gamma**2 - delta**2), (gamma**2 + delta**2) ** 2)


def quadratic_roots(a: float, b: float, c: float) -> tuple[complex, complex]:
    disc = cmath.sqrt(b * b - 4 * a * c)
    return ((-b + disc) / (2 * a), (-b - disc) / (2 * a))


def q_roots_are_real_nonpositive(coefficients: tuple[float, float, float]) -> bool:
    roots = quadratic_roots(*coefficients)
    return all(abs(root.imag) < 1e-12 and root.real <= 1e-12 for root in roots)


def finite_hp_frequencies(coefficients: tuple[float, float, float]) -> list[float] | None:
    """Return H frequencies if Q(y)=prod(y+omega_j^2), else None."""
    roots = quadratic_roots(*coefficients)
    if not q_roots_are_real_nonpositive(coefficients):
        return None
    return sorted(math.sqrt(max(0.0, -root.real)) for root in roots)


def evaluate_hp_determinant(s: complex, frequencies: Iterable[float]) -> complex:
    z = s - 0.5
    value = 1 + 0j
    for omega in frequencies:
        value *= z * z + omega * omega
    return value


def orbit_defect_energy(delta: float, boundary_sigma: float = 1.0) -> float:
    """Squared reflection-cocycle energy from the constructive Casey repair."""
    a = boundary_sigma - 0.5
    d = abs(delta)
    if a <= 0 or d >= a:
        raise ValueError("require boundary_sigma>1/2 and |delta|<boundary_sigma-1/2")
    return math.pi * d * d / (a * (a * a - d * d))


def total_orbit_defect_energy(deltas: Iterable[float]) -> float:
    return sum(orbit_defect_energy(delta) for delta in deltas)


def build_certificate() -> dict[str, Any]:
    gamma = 14.0
    sample_points = (0.17 + 0.8j, 0.63 + 3.2j, 1.2 - 0.4j)
    examples = []
    for delta in (0.0, 0.05, 0.2, 0.4):
        coeffs = quartet_q_coefficients(delta, gamma)
        q_roots = quadratic_roots(*coeffs)
        frequencies = finite_hp_frequencies(coeffs)
        reflection_error = max(
            abs(
                quartet_polynomial(s, delta, gamma)
                - quartet_polynomial(1 - s, delta, gamma)
            )
            for s in sample_points
        )
        conjugation_error = max(
            abs(
                quartet_polynomial(s.conjugate(), delta, gamma)
                - quartet_polynomial(s, delta, gamma).conjugate()
            )
            for s in sample_points
        )
        hp_error = None
        if frequencies is not None:
            hp_error = max(
                abs(
                    quartet_polynomial(s, delta, gamma)
                    - evaluate_hp_determinant(s, frequencies)
                )
                for s in sample_points
            )
        examples.append(
            {
                "delta": delta,
                "gamma": gamma,
                "zeros": [
                    {"real": root.real, "imag": root.imag}
                    for root in quartet_roots(delta, gamma)
                ],
                "Q_coefficients": coeffs,
                "Q_discriminant": -16 * gamma**2 * delta**2,
                "Q_roots": [
                    {"real": root.real, "imag": root.imag} for root in q_roots
                ],
                "reflection_error": reflection_error,
                "conjugation_error": conjugation_error,
                "critical_line": delta == 0,
                "finite_self_adjoint_square_determinant_exists": frequencies
                is not None,
                "frequencies": frequencies,
                "hp_reconstruction_error": hp_error,
                "orbit_defect_energy": orbit_defect_energy(delta),
            }
        )

    mixed_deltas = [0.0, 0.05, 0.2]
    mixed_energy = total_orbit_defect_energy(mixed_deltas)

    checks = {
        "all_examples_have_reflection_symmetry": all(
            example["reflection_error"] < 1e-10 for example in examples
        ),
        "all_examples_have_conjugation_symmetry": all(
            example["conjugation_error"] < 1e-10 for example in examples
        ),
        "symmetry_allows_off_line_quartets": any(
            not example["critical_line"] for example in examples
        ),
        "casey_quartic_discriminant_negative_off_line": all(
            example["Q_discriminant"] < 0
            for example in examples
            if example["delta"] > 0
        ),
        "self_adjoint_square_factorization_exact_on_line": all(
            example["hp_reconstruction_error"] is None
            or example["hp_reconstruction_error"] < 1e-8
            for example in examples
        ),
        "self_adjoint_square_factorization_fails_off_line": all(
            not example["finite_self_adjoint_square_determinant_exists"]
            for example in examples
            if example["delta"] > 0
        ),
        "defect_energy_positive_if_any_orbit_off_line": mixed_energy > 0,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "classification_theorem": {
            "normal_coordinate": "z=s-1/2",
            "symmetry_form": "F(1-s)=F(s) and real symmetry imply F(s)=Q(z^2)",
            "critical_line_criterion": (
                "all zeros of F lie on Re(s)=1/2 iff all zeros of Q are real and non-positive"
            ),
            "finite_hilbert_polya_criterion": (
                "F(s)=C det(z^2 I+H^2) for a finite self-adjoint H iff the finite zero "
                "set lies on the critical line"
            ),
        },
        "casey_quartet_reduction": {
            "F": "((z-delta)^2+gamma^2)((z+delta)^2+gamma^2)",
            "Q": "y^2+2(gamma^2-delta^2)y+(gamma^2+delta^2)^2",
            "discriminant": "-16 gamma^2 delta^2",
            "conclusion": (
                "for gamma nonzero, the self-adjoint determinant condition holds exactly "
                "when delta=0"
            ),
        },
        "minimal_extra_axiom": {
            "insufficient": [
                "functional-equation symmetry",
                "complex conjugation symmetry",
                "compactification of infinity",
                "pairing zeros into reflected quartets",
            ],
            "sufficient_finite_version": (
                "an exact determinant identity with a self-adjoint square, not merely a "
                "self-adjoint matrix followed by a map that inserts 1/2"
            ),
            "classical_analogue": (
                "a de Branges/Weil/Li-type positive Hermitian form or an exact "
                "infinite-dimensional self-adjoint determinant identity"
            ),
        },
        "examples": examples,
        "mixed_orbit_energy": {
            "deltas": mixed_deltas,
            "energy": mixed_energy,
            "zero_iff_all_deltas_zero": True,
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_reflection_countermodel_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
