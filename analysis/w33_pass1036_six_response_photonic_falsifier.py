#!/usr/bin/env python3
"""Pass 1036: six-response photonic S3 controller falsifier.

The full controller is tested in its faithful two-mode dihedral representation.
The ternary phase pulse r is a 120-degree rotation; the binary external pulse s
is a reflection.  The defining relation s r s = r^{-1} distinguishes the required
S3 controller from a false scalar C6 implementation, where the two controls commute.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1036_six_response_photonic_falsifier.json"
I2 = np.eye(2)


def close(left: np.ndarray, right: np.ndarray, tol: float = 1e-12) -> bool:
    return float(np.linalg.norm(left - right, ord="fro")) < tol


def key(matrix: np.ndarray) -> tuple[float, ...]:
    return tuple(float(round(value, 12)) for value in matrix.reshape(-1))


def main() -> None:
    angle = 2.0 * math.pi / 3.0
    r = np.array([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)],
    ])
    s = np.array([[1.0, 0.0], [0.0, -1.0]])

    responses: dict[str, np.ndarray] = {}
    for chirality in range(2):
        for phase in range(3):
            responses[f"phase{phase}_chirality{chirality}"] = (
                np.linalg.matrix_power(r, phase)
                @ np.linalg.matrix_power(s, chirality)
            )

    response_values = list(responses.values())
    multiplication_closed = True
    response_keys = {key(matrix) for matrix in response_values}
    for left in response_values:
        for right in response_values:
            multiplication_closed &= key(left @ right) in response_keys

    pairwise_distances = [
        float(np.linalg.norm(response_values[i] - response_values[j], ord="fro"))
        for i in range(6)
        for j in range(i + 1, 6)
    ]
    min_separation = min(pairwise_distances)

    relations = {
        "r_cubed": float(np.linalg.norm(np.linalg.matrix_power(r, 3) - I2, ord="fro")),
        "s_squared": float(np.linalg.norm(s @ s - I2, ord="fro")),
        "sr_squared": float(np.linalg.norm((s @ r) @ (s @ r) - I2, ord="fro")),
        "inversion_echo": float(np.linalg.norm(s @ r @ s - np.linalg.inv(r), ord="fro")),
        "noncommutativity": float(np.linalg.norm(s @ r - r @ s, ord="fro")),
    }

    omega = complex(-0.5, math.sqrt(3.0) / 2.0)
    scalar_r = omega
    scalar_s = -1.0 + 0.0j
    false_inversion_residual = abs(scalar_s * scalar_r * scalar_s - scalar_r.conjugate())
    false_commutator = abs(scalar_s * scalar_r - scalar_r * scalar_s)

    determinant_profile = {
        label: int(round(float(np.linalg.det(matrix))))
        for label, matrix in responses.items()
    }
    phase_orientations = {
        str(phase): [
            float(round(math.cos(phase * angle), 12)),
            float(round(math.sin(phase * angle), 12)),
        ]
        for phase in range(3)
    }

    checks = {
        "six_transfer_matrices_are_distinct": len(response_keys) == 6,
        "six_responses_are_closed_under_composition": multiplication_closed,
        "phase_pulse_has_order_three": relations["r_cubed"] < 1e-12,
        "chirality_pulse_has_order_two": relations["s_squared"] < 1e-12,
        "mixed_pulse_has_order_two": relations["sr_squared"] < 1e-12,
        "chirality_conjugates_phase_to_inverse": relations["inversion_echo"] < 1e-12,
        "controller_is_noncommutative": relations["noncommutativity"] > 1.0,
        "response_separation_is_nonzero": min_separation > 1.0,
        "three_even_responses_have_positive_determinant": sum(value == 1 for value in determinant_profile.values()) == 3,
        "three_odd_responses_have_negative_determinant": sum(value == -1 for value in determinant_profile.values()) == 3,
        "false_scalar_c6_model_commutes": false_commutator < 1e-12,
        "false_scalar_c6_model_fails_inversion_echo": false_inversion_residual > 1.0,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {failed}")

    result = {
        "schema": "w33.pass1036.six_response_photonic_falsifier.python.v1",
        "status": "PASS",
        "headline": (
            "A six-response optical controller must realize S3, not a commuting C6 scalar clock. "
            "In the faithful two-mode representation, the ternary pulse r is a 120-degree "
            "rotation, the binary pulse s is a reflection, and srs=r^{-1}. All six responses "
            "are distinct and closed, while the false scalar C6 model fails the inversion echo."
        ),
        "compiler_labels": [
            {"phase": phase, "chirality": chirality, "label": f"phase{phase}_chirality{chirality}"}
            for chirality in range(2)
            for phase in range(3)
        ],
        "ideal_transfer_matrices": {
            label: [[float(round(value, 12)) for value in row] for row in matrix]
            for label, matrix in responses.items()
        },
        "phase_orientation_readout": phase_orientations,
        "chirality_readout": determinant_profile,
        "falsifier_sequence": [
            "calibrate r and verify r^3=I",
            "calibrate s and verify s^2=I",
            "measure the inversion echo s r s = r^{-1}",
            "verify sr and rs are distinguishable",
            "resolve all six phase/chirality transfer matrices",
        ],
        "ideal_residuals": relations,
        "minimum_pairwise_frobenius_separation": min_separation,
        "false_c6_control": {
            "commutator_residual": false_commutator,
            "inversion_echo_residual": false_inversion_residual,
            "verdict": "fails: scalar sign and phase commute, so the binary pulse cannot invert the ternary phase",
        },
        "acceptance_rule": (
            "A device realizes the full controller only if it resolves six transfer responses, "
            "passes r^3=s^2=(sr)^2=I, passes srs=r^{-1}, and rejects the commuting C6 model. "
            "Observing only a three-cycle certifies the residual C3 carrier, not the full controller."
        ),
        "boundary": (
            "This is a transfer-matrix compiler and falsifier. It does not claim that a particular "
            "optical layout has achieved the required calibration or noise tolerance."
        ),
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Pass1036 status=PASS checks={len(checks)} output={OUT}")


if __name__ == "__main__":
    main()
