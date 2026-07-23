"""Finite W33 spectral-coordinate experiment for the RH frontier.

The 9x9 matrix below is a legitimate positive semidefinite self-adjoint
Laplacian.  Mapping an eigenvalue lambda > 1/4 to

    rho(lambda) = 1/2 + i*sqrt(lambda - 1/4)

places its image on the critical line by construction.  This is a useful
coordinate experiment, but it is not yet a Hilbert-Polya realization and does
not prove the classical Riemann Hypothesis.

A genuine Hilbert-Polya bridge must additionally prove that a self-adjoint
operator's spectral determinant is the completed Riemann zeta function (up to
fully controlled factors), and that its spectrum matches every nontrivial zeta
zero ordinate with the correct multiplicities.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# A finite zero-sheet incidence matrix used in the W33 substrate experiments.
H0 = np.array(
    [
        [1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 1, 1, 0, 1],
    ],
    dtype=float,
)

L_YM = H0.T @ H0


def build_spectral_coordinate_audit() -> dict:
    eigenvalues = np.sort(np.linalg.eigvalsh(L_YM))
    is_self_adjoint = bool(np.allclose(L_YM, L_YM.T))
    kernel_dim = int(np.sum(np.abs(eigenvalues) < 1e-10))
    positive_eigenvalues = [
        float(value) for value in eigenvalues if abs(value) >= 1e-10
    ]
    all_positive_above_quarter = all(value > 0.25 for value in positive_eigenvalues)

    coordinate_images = []
    for value in positive_eigenvalues:
        ordinate = float(np.sqrt(value - 0.25)) if value > 0.25 else None
        coordinate_images.append(
            {
                "lambda": value,
                "rho_real": 0.5 if ordinate is not None else None,
                "rho_imag": ordinate,
                "status": (
                    "critical-line coordinate by definition"
                    if ordinate is not None
                    else "not in the chosen coordinate domain"
                ),
            }
        )

    heat_trace = {
        str(t): float(np.sum(np.exp(-t * eigenvalues)))
        for t in (0.1, 0.5, 1.0, 2.0, 5.0)
    }

    transfer_requirements = [
        "Define an infinite-dimensional self-adjoint operator on a rigorous Hilbert space.",
        "Prove its regularized spectral determinant equals completed xi(s), up to controlled factors.",
        "Match the complete zeta-zero ordinate multiset and multiplicities.",
        "Control domains, boundary conditions, trace class/regularization, and continuous spectrum.",
    ]

    return {
        "status": "PASS",
        "classification": "finite toy spectral-coordinate embedding",
        "matrix_shape": list(L_YM.shape),
        "is_self_adjoint": is_self_adjoint,
        "kernel_dim": kernel_dim,
        "eigenvalues": [float(value) for value in eigenvalues],
        "all_nonzero_eigenvalues_above_one_quarter": all_positive_above_quarter,
        "coordinate_images": coordinate_images,
        "heat_trace": heat_trace,
        "logical_result": {
            "images_lie_on_re_one_half": all_positive_above_quarter,
            "reason": "The real part 1/2 is inserted by the coordinate definition.",
            "hilbert_polya_realized": False,
            "classical_rh_proved": False,
        },
        "missing_transfer_requirements": transfer_requirements,
    }


def main() -> None:
    payload = build_spectral_coordinate_audit()
    output = ROOT / "checks" / "w33_riemann_spectral_coordinate_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 finite spectral-coordinate audit")
    print(f"  self-adjoint: {payload['is_self_adjoint']}")
    print(f"  kernel dimension: {payload['kernel_dim']}")
    print(
        "  nonzero eigenvalues > 1/4: "
        f"{payload['all_nonzero_eigenvalues_above_one_quarter']}"
    )
    print("  Hilbert-Polya realized: False")
    print("  Classical RH proved: False")
    print(f"  wrote {output}")


if __name__ == "__main__":
    main()
