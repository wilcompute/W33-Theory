#!/usr/bin/env python3
"""Pass 2773: physical four-setting trace sensor for the 34-class decoder."""
from __future__ import annotations

import json
import math
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
Q = 3
Mat = tuple[tuple[int, ...], ...]
I4: Mat = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
FP: Mat = ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
FF: Mat = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0))
SP: Mat = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
SF: Mat = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1))
CX: Mat = ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1))


def mm(a: Mat, b: Mat) -> Mat:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % Q for j in range(4)) for i in range(4))


def inv(a: Mat) -> Mat:
    aug = [list(a[i]) + [int(i == j) for j in range(4)] for i in range(4)]
    r = 0
    for c in range(4):
        p = next(i for i in range(r, 4) if aug[i][c] % Q)
        aug[r], aug[p] = aug[p], aug[r]
        scale = 1 if aug[r][c] % Q == 1 else 2
        aug[r] = [(scale * x) % Q for x in aug[r]]
        for i in range(4):
            if i != r and aug[i][c] % Q:
                f = aug[i][c] % Q
                aug[i] = [(aug[i][j] - f * aug[r][j]) % Q for j in range(8)]
        r += 1
    return tuple(tuple(row[4:]) for row in aug)


def generators() -> list[tuple[str, Mat]]:
    out = []
    for name, g in (("Fp", FP), ("Ff", FF), ("Sp", SP), ("Sf", SF), ("CX", CX)):
        out.append((name, g))
        gi = inv(g)
        if gi != g:
            out.append((name + "^-1", gi))
    return out


def generate_group() -> dict[Mat, tuple[Mat | None, str | None]]:
    parent = {I4: (None, None)}
    q = deque([I4])
    gens = generators()
    while q:
        x = q.popleft()
        for name, g in gens:
            y = mm(x, g)
            if y not in parent:
                parent[y] = (x, name)
                q.append(y)
    assert len(parent) == 51840
    return parent


def unique(values: list[complex], tol: float = 1e-8) -> list[tuple[complex, int]]:
    reps: list[complex] = []
    counts: list[int] = []
    for z in values:
        for i, r in enumerate(reps):
            if abs(z - r) < tol:
                counts[i] += 1
                break
        else:
            reps.append(z)
            counts.append(1)
    return sorted(zip(reps, counts), key=lambda x: (round(abs(x[0]), 8), round(np.angle(x[0]), 8)))


def code(z: complex) -> dict[str, float]:
    return {"real": round(float(z.real), 12), "imag": round(float(z.imag), 12), "magnitude": round(float(abs(z)), 12)}


def build() -> dict:
    parent = generate_group()
    omega = np.exp(2j * np.pi / 3)
    f3 = np.array([[omega ** (j * k) for k in range(3)] for j in range(3)], dtype=complex) / math.sqrt(3)
    p3 = np.diag([omega ** ((2 * j * j) % 3) for j in range(3)]).astype(complex)
    i3 = np.eye(3, dtype=complex)
    summation = np.zeros((9, 9), dtype=complex)
    for p in range(3):
        for f in range(3):
            summation[3 * p + ((f + p) % 3), 3 * p + f] = 1
    ug = {"Fp": np.kron(f3, i3), "Ff": np.kron(i3, f3), "Sp": np.kron(p3, i3), "Sf": np.kron(i3, p3), "CX": summation}
    for name in list(ug):
        ug[name + "^-1"] = ug[name].conj().T

    unitary: dict[Mat, np.ndarray] = {I4: np.eye(9, dtype=complex)}
    for g, (prev, name) in parent.items():
        if g == I4:
            continue
        assert prev is not None and name is not None
        unitary[g] = unitary[prev] @ ug[name]

    a1 = [np.trace(u) / 9 for u in unitary.values()]
    a2 = [np.trace(u @ u) / 9 for u in unitary.values()]
    alphabet1 = unique(a1)
    alphabet2 = unique(a2)
    assert len(alphabet1) == 16 and len(alphabet2) == 10

    def min_sep(alphabet: list[tuple[complex, int]]) -> float:
        values = [z for z, _ in alphabet]
        return min(abs(values[i] - values[j]) for i in range(len(values)) for j in range(i + 1, len(values)))

    delta1, delta2 = min_sep(alphabet1), min_sep(alphabet2)
    assert abs(delta1 - (math.sqrt(3) - 1) / 9) < 1e-10
    delta = min(delta1, delta2)
    epsilon = delta / (2 * math.sqrt(2))

    shots = {}
    for failure in (0.05, 0.01, 0.001, 0.000001):
        per_quadrature = math.ceil(math.log(8 / failure) / (2 * epsilon * epsilon))
        shots[str(failure)] = {
            "detected_shots_per_quadrature": per_quadrature,
            "four_setting_detected_shots": 4 * per_quadrature,
        }

    return {
        "schema": "w33.pass2773.physical_metaplectic_sensor.v1",
        "status": "EXACT_ALPHABET_AND_CONSERVATIVE_SHOT_BOUND",
        "group_order": len(parent),
        "measurement_identity": "A_k=Tr(U^k)/9",
        "physical_protocol": {
            "ancilla": "path qubit prepared in |+>",
            "internal_register": "nine time-frequency modes",
            "arm_zero": "identity",
            "arm_one": "compiled U^k",
            "settings": ["k=1,X", "k=1,Y", "k=2,X", "k=2,Y"],
            "parallel_mode": "multiplex all nine computational inputs and average detector-resolved path contrast",
            "sequential_fallback_settings": 36,
            "determinant": "tracked digitally from the Clifford instruction stream",
            "class_function": "Theta_k=(9*A_k)^9/det(U^k)",
        },
        "trace_alphabet": {
            "k1_size": len(alphabet1),
            "k2_size": len(alphabet2),
            "k1": [{**code(z), "multiplicity": n} for z, n in alphabet1],
            "k2": [{**code(z), "multiplicity": n} for z, n in alphabet2],
            "minimum_complex_plane_separation": delta,
            "minimum_separation_exact": "(sqrt(3)-1)/9",
        },
        "nearest_alphabet_shot_bound": {
            "quadrature_tolerance": epsilon,
            "union_bound": "P_fail <= 8 exp(-2 N epsilon^2)",
            "shots": shots,
            "loss_scaling": "launched shots = detected shots / eta_detection",
            "phase_noise_scaling": "replace delta by exp(-sigma_phi^2/2)*delta for Gaussian path-phase noise",
        },
        "boundary": (
            "The shot count is a conservative Hoeffding/union bound for the exact finite trace alphabet. "
            "It is not an experimental calibration result; mode-dependent loss and coherent drift must be measured."
        ),
    }


def main() -> None:
    out = build()
    path = ROOT / "data" / "PART_BT2773_PHYSICAL_METAPLECTIC_SENSOR.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"alphabet": out["trace_alphabet"], "shots": out["nearest_alphabet_shot_bound"]["shots"]}, indent=2))


if __name__ == "__main__":
    main()
