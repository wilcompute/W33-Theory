#!/usr/bin/env python3
"""Exact audit of the shifted W(3,3) adjacency operator D = A - I.

The graph is reconstructed from symplectic orthogonality on PG(3,3). All
matrix identities are checked with integer arithmetic. The historical cubic
(t+1)((t+1)^2-36) is evaluated on the true spectrum and shown not to
annihilate D.

Scope: finite spectral algebra only. No physical interpretation is inferred
from determinant coefficients.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

Q = 3
N = 40
K = 12
LAMBDA = 2
MU = 4


def canonical_projective_points() -> list[tuple[int, int, int, int]]:
    points: list[tuple[int, int, int, int]] = []
    for vector in np.ndindex((Q, Q, Q, Q)):
        if vector == (0, 0, 0, 0):
            continue
        first = next(x for x in vector if x != 0)
        inv = pow(int(first), -1, Q)
        normalized = tuple((inv * int(x)) % Q for x in vector)
        if normalized == vector:
            points.append(vector)
    assert len(points) == N and len(set(points)) == N
    return points


def symplectic_form(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % Q


def build_adjacency(points: list[tuple[int, int, int, int]]) -> np.ndarray:
    A = np.zeros((len(points), len(points)), dtype=np.int64)
    for i, x in enumerate(points):
        for j in range(i + 1, len(points)):
            A[i, j] = A[j, i] = int(symplectic_form(x, points[j]) == 0)
    return A


def common_neighbor_profile(A: np.ndarray) -> tuple[Counter[int], Counter[int]]:
    A2 = A @ A
    adjacent: Counter[int] = Counter()
    nonadjacent: Counter[int] = Counter()
    for i in range(N):
        for j in range(i + 1, N):
            target = adjacent if A[i, j] else nonadjacent
            target[int(A2[i, j])] += 1
    return adjacent, nonadjacent


def audit() -> dict[str, Any]:
    points = canonical_projective_points()
    A = build_adjacency(points)
    I = np.eye(N, dtype=np.int64)
    J = np.ones((N, N), dtype=np.int64)
    D = A - I

    degrees = A.sum(axis=1)
    adjacent_profile, nonadjacent_profile = common_neighbor_profile(A)

    assert Counter(map(int, degrees)) == Counter({K: N})
    assert adjacent_profile == Counter({LAMBDA: N * K // 2})
    nonedge_count = N * (N - 1) // 2 - N * K // 2
    assert nonadjacent_profile == Counter({MU: nonedge_count})

    # Exact SRG matrix identity.
    srg_residual = A @ A - ((K - MU) * I + (LAMBDA - MU) * A + MU * J)
    assert np.array_equal(srg_residual, np.zeros_like(A))

    # On the all-ones line A has eigenvalue 12. On its orthogonal complement,
    # A satisfies x^2 + 2x - 8 = (x-2)(x+4), giving multiplicities 24 and 15
    # from dimension 39 and trace(A)=0.
    adjacency_spectrum = {12: 1, 2: 24, -4: 15}
    shifted_spectrum = {11: 1, 1: 24, -5: 15}

    corrected_residual = (D - 11 * I) @ (D - I) @ (D + 5 * I)
    assert np.array_equal(corrected_residual, np.zeros_like(D))
    assert np.array_equal(D @ D @ D, 7 * (D @ D) + 49 * D - 55 * I)

    historical_values = {
        eigenvalue: int((eigenvalue + 1) * ((eigenvalue + 1) ** 2 - 36))
        for eigenvalue in shifted_spectrum
    }
    assert historical_values == {11: 1296, 1: -64, -5: 80}
    historical_residual = (D + I) @ ((D + I) @ (D + I) - 36 * I)
    # Numeric rank is a redundant check; exact full rank follows because the
    # residual acts by three nonzero scalars on a complete orthogonal spectral
    # decomposition of dimensions 1+24+15=40.
    assert np.linalg.matrix_rank(historical_residual.astype(float)) == N

    # Rational spectral projectors are verified through scaled integer numerators.
    N11, d11 = (D - I) @ (D + 5 * I), 160
    N1, d1 = -((D - 11 * I) @ (D + 5 * I)), 60
    Nm5, dm5 = (D - 11 * I) @ (D - I), 96
    scaled_projectors = {11: (N11, d11), 1: (N1, d1), -5: (Nm5, dm5)}

    for eigenvalue, (numerator, denominator) in scaled_projectors.items():
        assert np.array_equal(numerator @ numerator, denominator * numerator)
        assert np.array_equal(D @ numerator, eigenvalue * numerator)
    assert np.array_equal(N11 @ N1, np.zeros_like(I))
    assert np.array_equal(N11 @ Nm5, np.zeros_like(I))
    assert np.array_equal(N1 @ Nm5, np.zeros_like(I))
    # lcm(160,60,96)=480: P11+P1+Pm5=I.
    assert np.array_equal(3 * N11 + 8 * N1 + 5 * Nm5, 480 * I)

    projector_ranks = {
        eigenvalue: int(np.trace(numerator) // denominator)
        for eigenvalue, (numerator, denominator) in scaled_projectors.items()
    }
    assert projector_ranks == shifted_spectrum

    moments = {n: int(np.trace(np.linalg.matrix_power(D, n))) for n in range(0, 11)}
    expected_moments = {
        n: int(11**n + 24 + 15 * (-5) ** n) for n in range(0, 11)
    }
    assert moments == expected_moments
    for n in range(8):
        assert moments[n + 3] == 7 * moments[n + 2] + 49 * moments[n + 1] - 55 * moments[n]

    determinant_D = -11 * 5**15

    historical_packets: dict[str, dict[str, Any]] = {
        "packet_A": {"eigenvalues": [-1, 5, -7], "multiplicities": [16, 10, 6]},
        "packet_B": {"eigenvalues": [5, -1, -7], "multiplicities": [10, 16, 6]},
    }
    for packet in historical_packets.values():
        eigs = packet["eigenvalues"]
        mults = packet["multiplicities"]
        packet["dimension"] = int(sum(mults))
        packet["trace"] = int(sum(e * m for e, m in zip(eigs, mults)))
        packet["trace_D2"] = int(sum(e * e * m for e, m in zip(eigs, mults)))

    return {
        "status": "PASS",
        "object": "W(3,3) collinearity graph",
        "construction": "projective points of F_3^4 with symplectic orthogonality",
        "srg": {
            "parameters": [N, K, LAMBDA, MU],
            "degree_histogram": {str(k): v for k, v in sorted(Counter(map(int, degrees)).items())},
            "adjacent_common_neighbors": {str(k): v for k, v in sorted(adjacent_profile.items())},
            "nonadjacent_common_neighbors": {str(k): v for k, v in sorted(nonadjacent_profile.items())},
            "matrix_identity": "A^2=8I-2A+4J",
        },
        "adjacency_spectrum": {str(k): v for k, v in adjacency_spectrum.items()},
        "shifted_operator": "D=A-I",
        "shifted_spectrum": {str(k): v for k, v in shifted_spectrum.items()},
        "corrected_minimal_polynomial": "(t-11)(t-1)(t+5)=t^3-7t^2-49t+55",
        "characteristic_polynomial": "(t-11)(t-1)^24(t+5)^15",
        "determinant_generating_polynomial": "det(I-xD)=(1-11x)(1-x)^24(1+5x)^15",
        "determinant_D": determinant_D,
        "projectors": {
            "11": "(D-I)(D+5I)/160",
            "1": "-(D-11I)(D+5I)/60",
            "-5": "(D-11I)(D-I)/96",
        },
        "projector_ranks": {str(k): v for k, v in projector_ranks.items()},
        "moments_0_to_10": {str(k): v for k, v in moments.items()},
        "moment_closed_form": "Tr(D^n)=11^n+24+15(-5)^n",
        "moment_recurrence": "m_(n+3)=7m_(n+2)+49m_(n+1)-55m_n",
        "historical_claim_audit": {
            "polynomial": "(t+1)((t+1)^2-36)=t^3+3t^2-33t-35",
            "values_on_true_shifted_eigenvalues": {str(k): v for k, v in historical_values.items()},
            "matrix_residual_rank": N,
            "annihilates_D": False,
            "multiplicity_packets": historical_packets,
            "failure_reasons": [
                "the proposed multiplicities sum to 32, not the matrix dimension 40",
                "the proposed roots are not the shifted adjacency eigenvalues",
                "the proposed polynomial is nonzero on all three true eigenspaces",
                "determinant/Taylor/anomaly inferences built from that polynomial do not describe D=A-I",
            ],
        },
        "scope_boundary": (
            "Exact finite spectral identities only; no anomaly, octonion, E8, "
            "particle-content, or dynamical inference is licensed by determinant coefficients."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/PART_2026_07_27_W33_SHIFTED_ADJACENCY_SPECTRAL_AUDIT.json"),
    )
    args = parser.parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
