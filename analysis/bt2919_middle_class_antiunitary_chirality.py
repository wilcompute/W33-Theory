#!/usr/bin/env python3
"""Pass 2919: distinguish the two middle M36 Clifford classes by antiunitary chirality.

The two 12-ray classes have the same stabilizer-fidelity grade and the same complete
probability spectrum against all two-qubit stabilizer states. Complex conjugation swaps
them, fixes the shallow and deep classes setwise, and reverses every Pauli expectation
containing an odd number of Y factors. This supplies a phase-sensitive operational
separator while proving that probability-only stabilizer overlaps cannot separate them.
"""
from __future__ import annotations

import json
from collections import deque
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2919_MIDDLE_CLASS_ANTIUNITARY_CHIRALITY_results.json"
W = np.exp(2j * np.pi / 3)
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j]).astype(complex)


def rays() -> list[np.ndarray]:
    roots = [1, W, W**2]
    raw: list[list[complex]] = []
    for mu, nu in product(range(3), repeat=2): raw.append([0, 1, -roots[mu], roots[nu]])
    for mu, nu in product(range(3), repeat=2): raw.append([1, 0, -roots[mu], -roots[nu]])
    for mu, nu in product(range(3), repeat=2): raw.append([1, -roots[mu], 0, roots[nu]])
    for mu, nu in product(range(3), repeat=2): raw.append([1, roots[mu], roots[nu], 0])
    return [np.asarray(v, dtype=complex) / np.sqrt(3) for v in raw]


def projective_key(v: np.ndarray, digits: int = 9) -> tuple[tuple[float, float], ...]:
    v = np.asarray(v, dtype=complex).reshape(-1)
    v = v / np.linalg.norm(v)
    pivot = next(i for i, value in enumerate(v) if abs(value) > 1e-10)
    v = v / (v[pivot] / abs(v[pivot]))
    return tuple((round(float(z.real), digits), round(float(z.imag), digits)) for z in v)


def matrix_key(m: np.ndarray, digits: int = 9) -> tuple[tuple[float, float], ...]:
    flat = m.reshape(-1)
    pivot = next(i for i, value in enumerate(flat) if abs(value) > 1e-10)
    m = m / (flat[pivot] / abs(flat[pivot]))
    return tuple((round(float(z.real), digits), round(float(z.imag), digits)) for z in m.reshape(-1))


def clifford_generators() -> list[np.ndarray]:
    cx01 = np.zeros((4, 4), dtype=complex)
    cx10 = np.zeros((4, 4), dtype=complex)
    for a, b in product(range(2), repeat=2):
        cx01[2 * a + (b ^ a), 2 * a + b] = 1
        cx10[2 * (a ^ b) + b, 2 * a + b] = 1
    return [np.kron(H, I), np.kron(I, H), np.kron(S, I), np.kron(I, S), cx01, cx10]


def projective_cliffords() -> list[np.ndarray]:
    ident = np.eye(4, dtype=complex)
    seen = {matrix_key(ident): ident}
    queue = deque([ident])
    gens = clifford_generators()
    while queue:
        current = queue.popleft()
        for generator in gens:
            candidate = generator @ current
            key = matrix_key(candidate)
            if key not in seen:
                seen[key] = candidate
                queue.append(candidate)
    assert len(seen) == 11520
    return list(seen.values())


def stabilizer_states() -> list[np.ndarray]:
    start = np.array([1, 0, 0, 0], dtype=complex)
    seen = {projective_key(start): start}
    queue = deque([start])
    gens = clifford_generators()
    while queue:
        current = queue.popleft()
        for generator in gens:
            candidate = generator @ current
            key = projective_key(candidate)
            if key not in seen:
                seen[key] = candidate / np.linalg.norm(candidate)
                queue.append(candidate / np.linalg.norm(candidate))
    assert len(seen) == 60
    return list(seen.values())


def m36_classes(rr: list[np.ndarray], group: list[np.ndarray]) -> list[list[int]]:
    ray_keys = {projective_key(ray): i for i, ray in enumerate(rr)}
    unseen = set(range(36))
    classes: list[list[int]] = []
    while unseen:
        seed = min(unseen)
        ids: set[int] = set()
        for g in group:
            key = projective_key(g @ rr[seed])
            if key in ray_keys: ids.add(ray_keys[key])
        classes.append(sorted(ids)); unseen -= ids
    classes.sort(key=lambda c: (len(c), c))
    assert sorted(map(len, classes)) == [4, 8, 12, 12]
    return classes


def expectation(v: np.ndarray, op: np.ndarray) -> float:
    value = np.vdot(v, op @ v)
    assert abs(value.imag) < 1e-9
    return float(value.real)


def main() -> None:
    rr = rays(); group = projective_cliffords(); classes = m36_classes(rr, group)
    shallow = next(c for c in classes if len(c) == 4)
    deep = next(c for c in classes if len(c) == 8)
    mid_a, mid_b = sorted((c for c in classes if len(c) == 12), key=lambda c: c)
    key_to_id = {projective_key(ray): i for i, ray in enumerate(rr)}
    conjugation = [key_to_id[projective_key(np.conj(ray))] for ray in rr]
    image = lambda ids: sorted(conjugation[i] for i in ids)

    stab = stabilizer_states()
    overlap_spectra = {i: tuple(sorted(round(float(abs(np.vdot(s, rr[i])) ** 2), 12) for s in stab)) for i in range(36)}
    spectra_a = {overlap_spectra[i] for i in mid_a}; spectra_b = {overlap_spectra[i] for i in mid_b}
    paulis = {a + b: np.kron(A, B) for a, A in zip("IXYZ", (I, X, Y, Z)) for b, B in zip("IXYZ", (I, X, Y, Z))}
    representative_a = mid_a[0]; representative_b = conjugation[representative_a]
    signed_expectations = {}; max_conjugation_residual = 0.0
    for name, op in paulis.items():
        ea = expectation(rr[representative_a], op); eb = expectation(rr[representative_b], op)
        odd_y = name.count("Y") % 2 == 1; expected = -ea if odd_y else ea
        max_conjugation_residual = max(max_conjugation_residual, abs(eb - expected))
        if abs(ea) > 1e-9 or abs(eb) > 1e-9:
            signed_expectations[name] = {"middle_a": ea, "middle_b_conjugate": eb, "odd_y": odd_y}

    middle_a_mu_nu = sorted([(i // 9, (i % 9) // 3, i % 3) for i in mid_a])
    middle_b_mu_nu = sorted([(i // 9, (i % 9) // 3, i % 3) for i in mid_b])
    sum_mod_a = sorted({(mu + nu) % 3 for _, mu, nu in middle_a_mu_nu})
    sum_mod_b = sorted({(mu + nu) % 3 for _, mu, nu in middle_b_mu_nu})

    checks = {
        "projective_clifford_order_11520": len(group) == 11520,
        "class_sizes_4_8_12_12": sorted(map(len, classes)) == [4, 8, 12, 12],
        "conjugation_fixes_shallow_setwise": image(shallow) == shallow,
        "conjugation_fixes_deep_setwise": image(deep) == deep,
        "conjugation_swaps_middle_classes": image(mid_a) == mid_b and image(mid_b) == mid_a,
        "stabilizer_probability_spectra_identical": spectra_a == spectra_b and len(spectra_a) == 1,
        "odd_y_expectations_flip_even_y_match": max_conjugation_residual < 1e-9,
        "middle_labels_are_mu_plus_nu_1_vs_2": sum_mod_a == [1] and sum_mod_b == [2],
    }
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]
    result = {
        "schema": "w33.pass2919.middle_class_antiunitary_chirality.v1",
        "status": "COMPLETE_EXACT_NUMERICAL_PHASE_GAUGE", "check_count": len(checks), "checks": checks,
        "classes": {"shallow": shallow, "deep": deep, "middle_a": mid_a, "middle_b": mid_b},
        "conjugation_map": conjugation, "representative_pair": [representative_a, representative_b],
        "representative_signed_pauli_expectations": signed_expectations,
        "maximum_pauli_conjugation_residual": max_conjugation_residual,
        "middle_label_rule": {"middle_a": "mu+nu = 1 mod 3 inside each nine-ray family", "middle_b": "mu+nu = 2 mod 3 inside each nine-ray family"},
        "headline": "The two middle 12-ray Clifford classes are an antiunitary-conjugate pair: probability-only stabilizer overlaps coincide, while every odd-Y Pauli expectation reverses sign in a fixed stabilizer frame.",
        "claim_boundary": "This is an operational phase-sensitive separator relative to a fixed Pauli frame; it is not a new Clifford-invariant scalar and does not make either class intrinsically preferred.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS {len(checks)}/{len(checks)}"); print(result["headline"])


if __name__ == "__main__":
    main()
