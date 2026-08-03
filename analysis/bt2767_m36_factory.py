#!/usr/bin/env python3
"""Deterministic Pass 2767 M36 preparation ROM.

The numerical stabilizer-overlap calculation remains a verifier, but serialized
values are rounded canonical exact targets so NumPy/LAPACK version changes do not
cause certificate drift.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def hermitian_pauli(v: tuple[int, int, int, int]) -> np.ndarray:
    a, b, c, d = v
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    z = np.diag([1, -1]).astype(complex)
    p1 = (1j ** (a * b)) * np.linalg.matrix_power(x, a) @ np.linalg.matrix_power(z, b)
    p2 = (1j ** (c * d)) * np.linalg.matrix_power(x, c) @ np.linalg.matrix_power(z, d)
    return np.kron(p1, p2)


def symp2(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return (u[0] * v[1] + u[1] * v[0] + u[2] * v[3] + u[3] * v[2]) % 2


def stabilizer_states() -> list[np.ndarray]:
    vectors = [v for v in itertools.product(range(2), repeat=4) if any(v)]
    planes: set[tuple[tuple[int, ...], ...]] = set()
    for u, v in itertools.combinations(vectors, 2):
        if symp2(u, v):
            continue
        w = tuple((u[i] + v[i]) % 2 for i in range(4))
        planes.add(tuple(sorted((u, v, w))))
    assert len(planes) == 15
    states: list[np.ndarray] = []
    ident = np.eye(4, dtype=complex)
    for plane in sorted(planes):
        u = plane[0]
        v = next(x for x in plane[1:] if x != u)
        p = hermitian_pauli(u)
        q = hermitian_pauli(v)
        for s, t in itertools.product((-1, 1), repeat=2):
            rho = ((ident + s * p) @ (ident + t * q)) / 4
            values, vectors_e = np.linalg.eigh(rho)
            psi = vectors_e[:, int(np.argmax(values))]
            psi /= np.linalg.norm(psi)
            if not any(abs(np.vdot(psi, old)) ** 2 > 1 - 1e-9 for old in states):
                states.append(psi)
    assert len(states) == 60
    return states


def ray_controls() -> list[dict]:
    rows: list[dict] = []
    for family in range(4):
        for mu in range(3):
            for nu in range(3):
                phase = [0, 0, 0, 0]
                dark = family
                if family == 0:
                    phase = [0, 0, (3 + 2 * mu) % 6, (2 * nu) % 6]
                elif family == 1:
                    phase = [0, 0, (3 + 2 * mu) % 6, (3 + 2 * nu) % 6]
                elif family == 2:
                    phase = [0, (3 + 2 * mu) % 6, 0, (2 * nu) % 6]
                else:
                    phase = [0, (2 * mu) % 6, (2 * nu) % 6, 0]
                rows.append({"ray_id": family * 9 + 3 * mu + nu, "family": family, "mu": mu, "nu": nu, "dark_mode": dark, "phase6": phase})
    return rows


def controls_to_ray(row: dict) -> np.ndarray:
    zeta6 = np.exp(1j * math.pi / 3)
    ray = np.array([0 if i == row["dark_mode"] else zeta6 ** row["phase6"][i] for i in range(4)], dtype=complex)
    return ray / math.sqrt(3)


def expected_ray(row: dict) -> np.ndarray:
    omega = np.exp(2j * math.pi / 3)
    mu, nu, family = row["mu"], row["nu"], row["family"]
    if family == 0:
        raw = [0, 1, -(omega**mu), omega**nu]
    elif family == 1:
        raw = [1, 0, -(omega**mu), -(omega**nu)]
    elif family == 2:
        raw = [1, -(omega**mu), 0, omega**nu]
    else:
        raw = [1, omega**mu, omega**nu, 0]
    return np.array(raw, dtype=complex) / math.sqrt(3)


def build_rom() -> dict:
    stabilizers = stabilizer_states()
    rows = ray_controls()
    exact_values = [
        ((2 + math.sqrt(3)) / 6, "deep", 0, "(2+sqrt(3))/6"),
        ((5 + 2 * math.sqrt(3)) / 12, "mid", 1, "(5+2*sqrt(3))/12"),
        (3 / 4, "shallow", 2, "3/4"),
    ]
    grades: Counter[str] = Counter()
    for row in rows:
        ray = controls_to_ray(row)
        expected = expected_ray(row)
        assert abs(abs(np.vdot(ray, expected)) ** 2 - 1) < 1e-10
        measured = max(abs(np.vdot(ray, s)) ** 2 for s in stabilizers)
        target, name, grade_code, exact = min(exact_values, key=lambda item: abs(measured - item[0]))
        assert abs(measured - target) < 1e-8
        row["grade"] = name
        row["grade_code"] = grade_code
        row["nearest_stabilizer_fidelity"] = round(target, 15)
        row["nearest_stabilizer_fidelity_exact"] = exact
        grades[name] += 1
    assert grades == Counter({"mid": 24, "deep": 8, "shallow": 4})
    thresholds = {
        "deep": {"depolarizing_magic_witness_p_lt": round((8 - 2 * math.sqrt(3)) / 9, 15), "exact": "(8-2*sqrt(3))/9"},
        "mid": {"depolarizing_magic_witness_p_lt": round((7 - 2 * math.sqrt(3)) / 9, 15), "exact": "(7-2*sqrt(3))/9"},
        "shallow": {"depolarizing_magic_witness_p_lt": round(1 / 3, 15), "exact": "1/3"},
    }
    return {
        "schema": "w33.pass2767.m36_preparation_rom.v2",
        "status": "EXACT_PREPARATION_AND_WITNESS_ONLY",
        "resource_type": "M36_Q4_RAW",
        "hardware_factorization": {"shared_balanced_tritter": 1, "dark_mode_choices": 4, "phase_alphabet": "sixth roots of unity", "states": 36},
        "grade_census": dict(grades),
        "depolarizing_witness_thresholds": thresholds,
        "rows": rows,
        "boundary": "This ROM prepares and types the 36 ququart/two-qubit Witting rays. It does not identify them with qutrit magic states and does not certify a distillation code, injection gadget, or threshold for M36.",
    }


def main() -> None:
    out = build_rom()
    path = ROOT / "data" / "PART_BT2767_M36_PREPARATION_ROM.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"wrote {path}")
    print("grade census", out["grade_census"])


if __name__ == "__main__":
    main()
