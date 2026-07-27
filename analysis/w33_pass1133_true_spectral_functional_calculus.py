#!/usr/bin/env python3
"""{shifted-adjacency:corrected} Pass 1133: rebuild the W(3,3) point-carrier functional calculus from D=A-I."""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1133_true_spectral_functional_calculus.json"


def projective_points() -> list[tuple[int, int, int, int]]:
    points = []
    for raw in np.ndindex((3, 3, 3, 3)):
        if raw == (0, 0, 0, 0):
            continue
        first = next(x for x in raw if x)
        inv = pow(int(first), -1, 3)
        normalized = tuple((inv * int(x)) % 3 for x in raw)
        if normalized == raw:
            points.append(raw)
    assert len(points) == 40
    return points


def symplectic(x, y) -> int:
    return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3


def adjacency() -> np.ndarray:
    pts = projective_points()
    A = np.zeros((40, 40), dtype=np.int64)
    for i, x in enumerate(pts):
        for j, y in enumerate(pts):
            if i != j and symplectic(x, y) == 0:
                A[i, j] = 1
    assert np.all(A.sum(axis=1) == 12)
    assert np.array_equal(A @ A, 8 * np.eye(40, dtype=np.int64) - 2 * A + 4 * np.ones((40, 40), dtype=np.int64))
    return A


def scaled_projectors(D: np.ndarray) -> dict[str, tuple[np.ndarray, int]]:
    I = np.eye(40, dtype=np.int64)
    return {
        "11": ((D - I) @ (D + 5 * I), 160),
        "1": (-((D - 11 * I) @ (D + 5 * I)), 60),
        "-5": ((D - 11 * I) @ (D - I), 96),
    }


def rational_trace(num: np.ndarray, den: int) -> Fraction:
    return Fraction(int(np.trace(num)), den)


def main() -> None:
    A = adjacency()
    I = np.eye(40, dtype=np.int64)
    D = A - I
    assert np.array_equal(D @ D @ D, 7 * D @ D + 49 * D - 55 * I)

    projectors = scaled_projectors(D)
    ranks = {}
    for name, (num, den) in projectors.items():
        assert np.array_equal(num @ num, den * num)
        ranks[name] = int(rational_trace(num, den))
    names = list(projectors)
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            nx, _ = projectors[x]
            ny, _ = projectors[y]
            assert not np.any(nx @ ny)
    common = np.lcm.reduce([den for _, den in projectors.values()])
    sum_num = sum(num * (common // den) for num, den in projectors.values())
    assert np.array_equal(sum_num, common * I)
    assert ranks == {"11": 1, "1": 24, "-5": 15}

    reductions = []
    coeff = np.array([1, 0, 0], dtype=object)
    for n in range(0, 13):
        reductions.append({"n": n, "constant": int(coeff[0]), "linear": int(coeff[1]), "quadratic": int(coeff[2])})
        c0, c1, c2 = coeff
        coeff = np.array([-55 * c2, c0 + 49 * c2, c1 + 7 * c2], dtype=object)

    moments = [11**n + 24 + 15 * (-5)**n for n in range(13)]
    for n in range(10):
        assert moments[n + 3] == 7 * moments[n + 2] + 49 * moments[n + 1] - 55 * moments[n]

    result = {
        "schema": "w33.pass1133.true_spectral_functional_calculus.v1",
        "audit_tag": "{shifted-adjacency:corrected}",
        "status": "PASS",
        "headline": "The entire W(3,3) point-carrier functional calculus is the three-mode algebra C[D]/((D-11)(D-1)(D+5)).",
        "operator": "D=A-I",
        "spectrum": {"11": 1, "1": 24, "-5": 15},
        "minimal_polynomial": "(t-11)(t-1)(t+5)=t^3-7t^2-49t+55",
        "projectors": {
            "P_11": "(D-I)(D+5I)/160",
            "P_1": "-(D-11I)(D+5I)/60",
            "P_-5": "(D-11I)(D-I)/96"
        },
        "projector_ranks": ranks,
        "functional_calculus": "f(D)=f(11)P_11+f(1)P_1+f(-5)P_-5",
        "spectral_action": "Tr f(D/Lambda)=f(11/Lambda)+24 f(1/Lambda)+15 f(-5/Lambda)",
        "even_spectral_action": "Tr f(D^2/Lambda^2)=f(121/Lambda^2)+24 f(1/Lambda^2)+15 f(25/Lambda^2)",
        "heat_trace": "Tr exp(-t D^2)=exp(-121t)+24 exp(-t)+15 exp(-25t)",
        "unitary_trace": "Tr exp(-itD)=exp(-11it)+24 exp(-it)+15 exp(5it)",
        "resolvent": "(zI-D)^-1=P_11/(z-11)+P_1/(z-1)+P_-5/(z+5)",
        "moment_formula": "Tr(D^n)=11^n+24+15(-5)^n",
        "moment_recurrence": "m_(n+3)=7m_(n+2)+49m_(n+1)-55m_n",
        "moments_n0_to_12": moments,
        "polynomial_reductions_n0_to_12": reductions,
        "consequence": "Every point-carrier heat kernel, propagator, Green function, and polynomial spectral action reduces exactly to the three projectors; no {-7,-1,5} or 32-dimensional packet enters.",
        "checks": {
            "srg_identity": True,
            "minimal_polynomial": True,
            "projector_idempotence": True,
            "projector_orthogonality": True,
            "projector_completeness": True,
            "rank_sum_40": sum(ranks.values()) == 40,
            "moment_recurrence": True
        },
        "scope": "Exact finite spectral algebra. Physical interpretation requires an independently specified spectral triple and cutoff function."
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "ranks": ranks, "moments": moments[:6]}, indent=2))


if __name__ == "__main__":
    main()
