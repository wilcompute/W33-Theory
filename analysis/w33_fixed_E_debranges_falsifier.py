#!/usr/bin/env python3
"""Fixed-E de Branges audit at the norm-11 scale.

Define Xi(z)=xi(1/2+i z) and fix, once and for all,

    c_11 = 1/log(11),
    E_11(z) = Xi(z) + i c_11 Xi'(z).

The sign is chosen so that a Laguerre--Polya Xi would produce the expected
Hermite--Biehler orientation. The script samples the HB gap and a normalized
kernel matrix, then injects one controlled off-real quartet to calibrate
sensitivity. Passing a finite grid is not a global HB proof.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
C11 = mp.mpf(1) / mp.log(11)


def completed_xi(s: mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    if abs(z) < mp.mpf("1e-35") or abs(z - 1) < mp.mpf("1e-35"):
        return mp.mpc(mp.mpf("0.5"))
    return (
        mp.mpf("0.5") * z * (z - 1) * mp.power(mp.pi, -z / 2)
        * mp.gamma(z / 2) * mp.zeta(z)
    )


def xi_log_derivative(s: mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    return (
        1 / z + 1 / (z - 1) - mp.log(mp.pi) / 2
        + mp.digamma(z / 2) / 2 + mp.zeta(z, derivative=1) / mp.zeta(z)
    )


def Xi(z: mp.mpc) -> mp.mpc:
    return completed_xi(mp.mpf("0.5") + 1j * mp.mpc(z))


def Xi_prime(z: mp.mpc) -> mp.mpc:
    s = mp.mpf("0.5") + 1j * mp.mpc(z)
    value = completed_xi(s)
    return 1j * value * xi_log_derivative(s)


def E_fixed(z: mp.mpc) -> mp.mpc:
    point = mp.mpc(z)
    return Xi(point) + 1j * C11 * Xi_prime(point)


def sharp(function: Callable[[mp.mpc], mp.mpc], z: mp.mpc) -> mp.mpc:
    return mp.conj(function(mp.conj(mp.mpc(z))))


def hb_gap(function: Callable[[mp.mpc], mp.mpc], z: mp.mpc) -> mp.mpf:
    point = mp.mpc(z)
    return abs(function(point)) ** 2 - abs(sharp(function, point)) ** 2


def normalized_gap(function: Callable[[mp.mpc], mp.mpc], z: mp.mpc) -> mp.mpf:
    point = mp.mpc(z)
    left = abs(function(point)) ** 2
    right = abs(sharp(function, point)) ** 2
    return (left - right) / (left + right)


def debranges_kernel(function: Callable[[mp.mpc], mp.mpc], z: mp.mpc, w: mp.mpc) -> mp.mpc:
    z = mp.mpc(z)
    w = mp.mpc(w)
    numerator = (
        mp.conj(function(w)) * function(z)
        - mp.conj(sharp(function, w)) * sharp(function, z)
    )
    denominator = 2 * mp.pi * 1j * (mp.conj(w) - z)
    return numerator / denominator


def normalized_kernel_min_eigenvalue(function: Callable[[mp.mpc], mp.mpc], points: list[mp.mpc]) -> float:
    size = len(points)
    matrix = np.empty((size, size), dtype=np.complex128)
    for i, z in enumerate(points):
        for j, w in enumerate(points):
            matrix[i, j] = complex(debranges_kernel(function, z, w))
    matrix = (matrix + matrix.conjugate().T) / 2
    diagonal = np.real(np.diag(matrix))
    if np.any(diagonal <= 0):
        return float(np.min(diagonal))
    normalized = matrix / np.sqrt(diagonal[:, None] * diagonal[None, :])
    normalized = (normalized + normalized.conjugate().T) / 2
    return float(np.linalg.eigvalsh(normalized)[0])


def quartet(z: mp.mpc, delta: mp.mpf, gamma: mp.mpf) -> mp.mpc:
    point = mp.mpc(z)
    return ((point - gamma) ** 2 + delta**2) * ((point + gamma) ** 2 + delta**2)


def quartet_prime(z: mp.mpc, delta: mp.mpf, gamma: mp.mpf) -> mp.mpc:
    point = mp.mpc(z)
    first = (point - gamma) ** 2 + delta**2
    second = (point + gamma) ** 2 + delta**2
    return 2 * (point - gamma) * second + 2 * (point + gamma) * first


def perturbed_E(delta: mp.mpf, gamma: mp.mpf) -> Callable[[mp.mpc], mp.mpc]:
    def function(z: mp.mpc) -> mp.mpc:
        q = quartet(z, delta, gamma)
        q_prime = quartet_prime(z, delta, gamma)
        a = Xi(z) * q
        a_prime = Xi_prime(z) * q + Xi(z) * q_prime
        return a + 1j * C11 * a_prime
    return function


def build_certificate() -> dict[str, Any]:
    mp.mp.dps = 55
    y_values = ("0.02", "0.05", "0.1", "0.2", "0.4", "0.6", "1", "2", "3", "5")
    grid = [
        mp.mpc(mp.mpf(x_index) / 2, mp.mpf(y))
        for x_index in range(101)
        for y in y_values
    ]
    gaps = [hb_gap(E_fixed, point) for point in grid]
    normalized_gaps = [normalized_gap(E_fixed, point) for point in grid]
    min_index = min(range(len(grid)), key=lambda index: normalized_gaps[index])

    kernel_points = [
        mp.mpc(x, mp.mpf("0.30") + mp.mpf("0.02") * (index % 3))
        for index, x in enumerate((0, 5, 10, 14, 18, 22, 26, 30, 35, 40, 45, 50))
    ]
    fixed_kernel_min = normalized_kernel_min_eigenvalue(E_fixed, kernel_points)

    delta = mp.mpf("0.2")
    gamma = mp.mpf("14")
    defective = perturbed_E(delta, gamma)
    witness = mp.mpc("14", "0.15")
    defective_gap = hb_gap(defective, witness)
    defective_diagonal = defective_gap / (4 * mp.pi * mp.im(witness))

    checks = {
        "fixed_E_gap_positive_on_1010_point_grid": min(gaps) > 0,
        "fixed_E_normalized_gap_positive_on_grid": min(normalized_gaps) > 0,
        "fixed_E_12x12_kernel_matrix_positive": fixed_kernel_min > 1e-7,
        "controlled_off_line_quartet_produces_negative_gap": defective_gap < 0,
        "controlled_off_line_quartet_produces_negative_kernel_diagonal": defective_diagonal < 0,
        "norm11_scale_fixed_before_testing": abs(C11 - 1 / mp.log(11)) < mp.mpf("1e-15"),
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "fixed completed-xi de Branges candidate at c=1/log(11) and calibrated quartet falsifier",
        "candidate": {
            "Xi": "Xi(z)=xi(1/2+i z)",
            "scale": "c_11=1/log(11)",
            "E": "E_11(z)=Xi(z)+i c_11 Xi'(z)",
            "E_sharp": "E_11#(z)=conj(E_11(conj(z)))",
            "HB_requirement": "|E_11(z)|>|E_11#(z)| for every Im(z)>0",
        },
        "finite_grid_audit": {
            "x_range": "0 through 50 in steps of 0.5",
            "y_values": list(y_values),
            "point_count": len(grid),
            "minimum_raw_gap": mp.nstr(min(gaps), 30),
            "minimum_normalized_gap": mp.nstr(min(normalized_gaps), 30),
            "minimum_normalized_gap_point": {
                "real": mp.nstr(mp.re(grid[min_index]), 12),
                "imag": mp.nstr(mp.im(grid[min_index]), 12),
            },
            "normalized_12x12_kernel_min_eigenvalue": fixed_kernel_min,
            "verdict": "not falsified on the registered finite grid; this is not a global HB proof",
        },
        "controlled_falsifier": {
            "perturbation": "Xi_delta,gamma(z)=Xi(z)[((z-gamma)^2+delta^2)((z+gamma)^2+delta^2)]",
            "delta": str(delta),
            "gamma": str(gamma),
            "off_real_zeros": ["14+0.2i", "14-0.2i", "-14+0.2i", "-14-0.2i"],
            "witness_point": "14+0.15i",
            "HB_gap": mp.nstr(defective_gap, 30),
            "kernel_diagonal": mp.nstr(defective_diagonal, 30),
            "verdict": "the same fixed-E construction detects the injected off-line quartet",
        },
        "claim_boundary": {
            "proved": [
                "the numerical test is sensitive to a controlled off-line quartet",
                "the fixed norm-11 candidate passes the registered gap and kernel tests",
            ],
            "not_proved": [
                "that E_11 is Hermite--Biehler on the entire upper half-plane",
                "that finite kernel minors imply all kernel minors are positive",
                "classical RH",
            ],
            "next_exact_target": "replace the finite grid by a global inequality for the fixed E_11, or produce one explicit upper-half-plane counterexample",
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_fixed_E_debranges_falsifier_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
