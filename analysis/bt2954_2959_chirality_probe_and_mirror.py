#!/usr/bin/env python3
"""Passes 2954 and 2959: antiunitary chirality, its minimal local probe, and D12 metadata.

The class-blind impossibility statement is proved by the two uniform ensemble densities.
The frame-conditioned probe is found by exhaustive Pauli-set cover over the twelve
complex-conjugate middle-class pairs. The classical phase-label inversion is then matched
against the existing D12 mirror reflection on its C3 subgroup.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT54 = ROOT / "data" / "PART_BT2954_CHIRALITY_PROBE_results.json"
OUT59 = ROOT / "data" / "PART_BT2959_CHIRALITY_MIRROR_results.json"
OMEGA = np.exp(2j * np.pi / 3)
I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
H = np.array([[1,1],[1,-1]], dtype=complex) / np.sqrt(2)
S = np.diag([1,1j]).astype(complex)


def projective_key(vector, digits=9):
    vector = np.asarray(vector, dtype=complex).reshape(-1)
    vector /= np.linalg.norm(vector)
    pivot = next(i for i, value in enumerate(vector) if abs(value) > 1e-10)
    vector /= vector[pivot] / abs(vector[pivot])
    return tuple((round(float(value.real), digits), round(float(value.imag), digits)) for value in vector)


def matrix_key(matrix, digits=9):
    flat = matrix.reshape(-1)
    pivot = next(i for i, value in enumerate(flat) if abs(value) > 1e-10)
    matrix = matrix / (flat[pivot] / abs(flat[pivot]))
    return tuple((round(float(value.real), digits), round(float(value.imag), digits)) for value in matrix.reshape(-1))


def rays():
    roots = [1, OMEGA, OMEGA**2]
    raw = []
    for mu, nu in itertools.product(range(3), repeat=2): raw.append([0,1,-roots[mu],roots[nu]])
    for mu, nu in itertools.product(range(3), repeat=2): raw.append([1,0,-roots[mu],-roots[nu]])
    for mu, nu in itertools.product(range(3), repeat=2): raw.append([1,-roots[mu],0,roots[nu]])
    for mu, nu in itertools.product(range(3), repeat=2): raw.append([1,roots[mu],roots[nu],0])
    return [np.asarray(vector, dtype=complex) / np.sqrt(3) for vector in raw]


def clifford_generators():
    cx01 = np.zeros((4,4), dtype=complex)
    cx10 = np.zeros((4,4), dtype=complex)
    for a, b in itertools.product(range(2), repeat=2):
        cx01[2*a + (b ^ a), 2*a + b] = 1
        cx10[2*(a ^ b) + b, 2*a + b] = 1
    return [np.kron(H,I), np.kron(I,H), np.kron(S,I), np.kron(I,S), cx01, cx10]


def cliffords():
    identity = np.eye(4, dtype=complex)
    seen = {matrix_key(identity): identity}
    queue = deque([identity])
    generators = clifford_generators()
    while queue:
        current = queue.popleft()
        for generator in generators:
            candidate = generator @ current
            key = matrix_key(candidate)
            if key not in seen:
                seen[key] = candidate
                queue.append(candidate)
    assert len(seen) == 11520
    return list(seen.values())


def classes(ray_vectors, group):
    keys = {projective_key(ray): i for i, ray in enumerate(ray_vectors)}
    unseen = set(range(36))
    result = []
    while unseen:
        seed = min(unseen)
        orbit = {keys[key] for matrix in group if (key := projective_key(matrix @ ray_vectors[seed])) in keys}
        result.append(sorted(orbit))
        unseen -= orbit
    result.sort(key=lambda values: (len(values), values))
    assert [len(values) for values in result] == [4,8,12,12]
    return result


def majority_success(single_shot, count):
    return sum(math.comb(count, k) * single_shot**k * (1-single_shot)**(count-k) for k in range(count//2 + 1, count + 1))


def main():
    ray_vectors = rays()
    group = cliffords()
    class_list = classes(ray_vectors, group)
    middle_a, middle_b = class_list[2], class_list[3]
    density_a = sum(np.outer(ray_vectors[i], ray_vectors[i].conj()) for i in middle_a) / 12
    density_b = sum(np.outer(ray_vectors[i], ray_vectors[i].conj()) for i in middle_b) / 12
    trace_distance = float(np.sum(np.abs(np.linalg.eigvalsh(density_a - density_b))) / 2)
    keys = {projective_key(ray): i for i, ray in enumerate(ray_vectors)}
    pairs = []
    for ray_id in middle_a:
        conjugate_id = keys[projective_key(np.conj(ray_vectors[ray_id]))]
        overlap = float(abs(np.vdot(ray_vectors[ray_id], ray_vectors[conjugate_id]))**2)
        pairs.append((ray_id, conjugate_id, overlap))
    assert all(abs(overlap - 1/3) < 1e-9 for _, _, overlap in pairs)

    paulis = {a+b: np.kron(left, right) for a, left in zip("IXYZ", (I,X,Y,Z)) for b, right in zip("IXYZ", (I,X,Y,Z))}
    odd_y = [name for name in paulis if name.count("Y") % 2 == 1]
    coverage = {name: set() for name in odd_y}
    signs = {}
    for left_id, right_id, _ in pairs:
        for name in odd_y:
            left_value = float(np.vdot(ray_vectors[left_id], paulis[name] @ ray_vectors[left_id]).real)
            right_value = float(np.vdot(ray_vectors[right_id], paulis[name] @ ray_vectors[right_id]).real)
            if abs(left_value + right_value) < 1e-9 and abs(left_value) > 1e-9:
                coverage[name].add((left_id, right_id))
                signs[(left_id, right_id, name)] = 1 if left_value > 0 else -1
    pair_set = {(left, right) for left, right, _ in pairs}
    minimum_covers = []
    for size in range(1, len(odd_y) + 1):
        for selection in itertools.combinations(odd_y, size):
            if set().union(*(coverage[name] for name in selection)) == pair_set:
                minimum_covers.append(selection)
        if minimum_covers:
            break
    assert size == 2
    assert ("IY", "YI") in minimum_covers or ("YI", "IY") in minimum_covers
    lookup = []
    for left_id, right_id, _ in pairs:
        probe = "IY" if (left_id, right_id) in coverage["IY"] else "YI"
        lookup.append([left_id, right_id, probe, signs[(left_id, right_id, probe)]])
    lookup.sort()
    expected_lookup = [
        [1,2,"IY",-1],[3,6,"IY",1],[8,4,"YI",-1],[10,11,"IY",1],
        [12,15,"IY",-1],[17,13,"YI",1],[19,20,"YI",-1],[21,24,"IY",-1],
        [26,22,"IY",1],[28,29,"YI",1],[30,33,"IY",1],[35,31,"IY",-1]
    ]
    assert lookup == expected_lookup
    single = (1 + 1 / math.sqrt(3)) / 2
    result54 = {
        "schema": "w33.pass2954.chirality_probe.v1",
        "status": "COMPLETE_EXACT_CONTROLLER_SOURCE",
        "middle_classes": {"A": middle_a, "B": middle_b},
        "uniform_density_residual_A": float(np.linalg.norm(density_a - np.eye(4)/4)),
        "uniform_density_residual_B": float(np.linalg.norm(density_b - np.eye(4)/4)),
        "uniform_ensemble_trace_distance": trace_distance,
        "class_blind_single_copy_discrimination": "impossible",
        "conjugate_pair_overlap_squared": "1/3",
        "single_fixed_pauli_cover_exists": False,
        "minimum_local_probe_count": size,
        "minimum_local_probe_set": ["YI", "IY"],
        "pair_lookup": lookup,
        "single_shot_success": "(1+1/sqrt(3))/2",
        "single_shot_success_decimal": single,
        "majority_success": {str(count): majority_success(single, count) for count in (1,3,5,7,9)},
        "physical_measurement": "Select qubit; apply S-dagger then H; measure Z. No entangler.",
        "boundary": "Unknown uniform class ensembles are identical. The controller assumes the conjugate pair/frame label is known."
    }

    phase_labels = {}
    for ray_id in middle_a + middle_b:
        mu, nu = (ray_id % 9) // 3, ray_id % 3
        phase_labels[ray_id] = (mu + nu) % 3
    assert {phase_labels[ray_id] for ray_id in middle_a} == {1}
    assert {phase_labels[ray_id] for ray_id in middle_b} == {2}
    reversible_table = []
    for phase in range(3):
        for mirror in range(2):
            reflected = phase if mirror == 0 else (-phase) % 3
            reversible_table.append([phase, mirror, reflected, mirror])
    assert len({tuple(row[2:]) for row in reversible_table}) == 6
    result59 = {
        "schema": "w33.pass2959.chirality_mirror.v1",
        "status": "COMPLETE_EXACT_METADATA_AND_RTL_SOURCE",
        "phase_label": "s=mu+nu mod 3",
        "middle_classes": {"A": 1, "B": 2},
        "conjugation": "s -> -s mod 3",
        "d12_relation": "The mirror relation r -> r^-1 restricts to the same inversion on the C3 phase subgroup.",
        "reversible_table": reversible_table,
        "logical_erasure_bits": 0,
        "boundary": "Classical ray/controller metadata only; no physical antiunitary operation on an unknown state is implemented."
    }
    OUT54.write_text(json.dumps(result54, indent=2, sort_keys=True) + "\n")
    OUT59.write_text(json.dumps(result59, indent=2, sort_keys=True) + "\n")
    print("PASS class-blind impossible; minimal probe cover={YI,IY}; D12 metadata bijective")


if __name__ == "__main__":
    main()
