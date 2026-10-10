#!/usr/bin/env python3
"""Passes 2953 and 2958: close the diameter-19 shell objectwise.

The script rebuilds ASp(4,3), performs the forward four-generator BFS, closes actual
full-group conjugacy classes using the generators and their inverses, and Fourier-analyzes
the terminal shell's fixed-point incidence on F_3^4.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT53 = ROOT / "data" / "PART_BT2953_DIAMETER19_CONJUGACY_results.json"
OUT58 = ROOT / "data" / "PART_BT2958_HARD_SHELL_FOURIER_results.json"

LIN = {
    "F_p": ((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)),
    "CX_pf": ((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1)),
    "CX_fp": ((1,0,1,0),(0,1,0,0),(0,0,1,0),(0,2,0,1)),
    "Z_p": ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)),
}
TRANS = {"F_p":(0,0,0,0),"CX_pf":(0,0,0,0),"CX_fp":(0,0,0,0),"Z_p":(0,1,0,0)}
NAMES = ("F_p", "CX_pf", "CX_fp", "Z_p")
IDENT = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
ZERO = (0,0,0,0)
STATES = list(product(range(3), repeat=4))
STATE_INDEX = {value: i for i, value in enumerate(STATES)}
WEIGHTS = np.array([27,9,3,1], dtype=np.int32)


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))


def matvec(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def add(a, b):
    return tuple((x + y) % 3 for x, y in zip(a, b))


def neg(a):
    return tuple((-x) % 3 for x in a)


def matrix_order(matrix, bound=200):
    power = IDENT
    for order in range(1, bound + 1):
        power = mul(matrix, power)
        if power == IDENT:
            return order
    raise AssertionError("matrix order bound exceeded")


def inverse_matrix(matrix):
    order = matrix_order(matrix)
    power = IDENT
    for _ in range(order - 1):
        power = mul(matrix, power)
    assert mul(matrix, power) == IDENT
    return power


def affine_order(matrix, translation, bound=500):
    linear, shift = IDENT, ZERO
    for order in range(1, bound + 1):
        linear, shift = mul(matrix, linear), add(matvec(matrix, shift), translation)
        if linear == IDENT and shift == ZERO:
            return order
    raise AssertionError("affine order bound exceeded")


def build_sp43():
    matrices = [IDENT]
    index = {IDENT: 0}
    queue = deque([IDENT])
    for_current = (LIN["F_p"], LIN["CX_pf"], LIN["CX_fp"])
    while queue:
        current = queue.popleft()
        for generator in for_current:
            candidate = mul(generator, current)
            if candidate not in index:
                index[candidate] = len(matrices)
                matrices.append(candidate)
                queue.append(candidate)
    assert len(matrices) == 51840
    return matrices, index


def forward_bfs(matrices, matrix_index):
    count = len(matrices) * 81
    matrix_permutation = {}
    translation_map = {}
    for name in NAMES:
        linear, shift = LIN[name], TRANS[name]
        matrix_permutation[name] = np.array([matrix_index[mul(linear, matrix)] for matrix in matrices], dtype=np.int32)
        translation_map[name] = np.array([STATE_INDEX[add(matvec(linear, value), shift)] for value in STATES], dtype=np.int16)
    depth = np.full(count, 255, dtype=np.uint8)
    start = matrix_index[IDENT] * 81 + STATE_INDEX[ZERO]
    depth[start] = 0
    frontier = np.array([start], dtype=np.int64)
    new_counts = [1]
    distance = 0
    while frontier.size:
        distance += 1
        matrix_ids, state_ids = frontier // 81, frontier % 81
        candidates = []
        for name in NAMES:
            next_matrix = matrix_permutation[name][matrix_ids]
            next_state = translation_map[name][state_ids]
            candidates.append(next_matrix.astype(np.int64) * 81 + next_state)
        candidate = np.unique(np.concatenate(candidates))
        candidate = candidate[depth[candidate] == 255]
        if candidate.size == 0:
            distance -= 1
            break
        depth[candidate] = distance
        new_counts.append(int(candidate.size))
        frontier = candidate
    assert distance == 19
    assert int((depth != 255).sum()) == count
    assert int((depth == 19).sum()) == 188
    return depth, np.flatnonzero(depth == 19), new_counts


def conjugation_tables(matrices, matrix_index):
    generators = []
    for name in NAMES:
        linear, shift = LIN[name], TRANS[name]
        inverse = inverse_matrix(linear)
        generators.append((name, linear, shift))
        generators.append((name + "^-1", inverse, neg(matvec(inverse, shift))))
    state_array = np.asarray(STATES, dtype=np.int8)
    tables = []
    for name, linear, shift in generators:
        inverse = inverse_matrix(linear)
        matrix_permutation = np.empty(len(matrices), dtype=np.int32)
        correction = np.empty((len(matrices), 4), dtype=np.int8)
        for i, matrix in enumerate(matrices):
            conjugate_matrix = mul(mul(linear, matrix), inverse)
            matrix_permutation[i] = matrix_index[conjugate_matrix]
            correction[i] = (np.asarray(shift, dtype=np.int8) - np.asarray(matvec(conjugate_matrix, shift), dtype=np.int8)) % 3
        transformed_states = (state_array @ np.asarray(linear, dtype=np.int8).T) % 3
        tables.append((name, matrix_permutation, correction, transformed_states))
    return tables


def conjugate_ids(ids, table):
    _, matrix_permutation, correction, transformed_states = table
    ids = np.asarray(ids, dtype=np.int64)
    matrix_ids, state_ids = ids // 81, ids % 81
    vectors = (transformed_states[state_ids] + correction[matrix_ids]) % 3
    next_state_ids = vectors.astype(np.int32) @ WEIGHTS
    return matrix_permutation[matrix_ids].astype(np.int64) * 81 + next_state_ids


def element_data(element_id, matrices):
    matrix_id, state_id = divmod(int(element_id), 81)
    matrix, shift = matrices[matrix_id], STATES[state_id]
    fixed = sum(add(matvec(matrix, value), shift) == value for value in STATES)
    charpoly = tuple(int(value) % 3 for value in sp.Matrix(matrix).charpoly(sp.Symbol("x")).all_coeffs())
    return {
        "representative_element_index": int(element_id),
        "translation": list(shift),
        "translation_weight": sum(value != 0 for value in shift),
        "matrix_order": matrix_order(matrix),
        "affine_order": affine_order(matrix, shift),
        "fixed_frames": fixed,
        "trace_mod3": sum(matrix[i][i] for i in range(4)) % 3,
        "charpoly_mod3": list(charpoly),
    }


def inverse_element(element_id, matrices, matrix_index):
    matrix_id, state_id = divmod(int(element_id), 81)
    matrix, shift = matrices[matrix_id], STATES[state_id]
    inverse = inverse_matrix(matrix)
    return matrix_index[inverse] * 81 + STATE_INDEX[neg(matvec(inverse, shift))]


def conjugacy_closure(shell, matrices, matrix_index):
    total_elements = len(matrices) * 81
    tables = conjugation_tables(matrices, matrix_index)
    class_id = np.full(total_elements, -1, dtype=np.int16)
    classes = []
    for representative in shell:
        if class_id[representative] >= 0:
            continue
        cid = len(classes)
        class_id[representative] = cid
        frontier = np.array([representative], dtype=np.int64)
        class_size = 1
        radius = 0
        while frontier.size:
            candidate = np.unique(np.concatenate([conjugate_ids(frontier, table) for table in tables]))
            candidate = candidate[class_id[candidate] < 0]
            if candidate.size == 0:
                break
            class_id[candidate] = cid
            class_size += int(candidate.size)
            frontier = candidate
            radius += 1
        shell_members = shell[class_id[shell] == cid]
        row = element_data(representative, matrices)
        row.update({
            "class_id": cid,
            "full_class_size": class_size,
            "centralizer_size": total_elements // class_size,
            "shell_intersection": int(shell_members.size),
            "conjugacy_radius_from_representative": radius,
        })
        classes.append(row)
    for row in classes:
        inverse = inverse_element(row["representative_element_index"], matrices, matrix_index)
        inverse_id = int(class_id[inverse])
        row["inverse_class_if_shell_intersecting"] = None if inverse_id < 0 else inverse_id
    return classes


def hard_shell_fourier(shell, matrices):
    fixed_counts = np.zeros(81, dtype=np.int32)
    for element_id in shell:
        matrix_id, state_id = divmod(int(element_id), 81)
        matrix, shift = matrices[matrix_id], STATES[state_id]
        for i, value in enumerate(STATES):
            fixed_counts[i] += int(add(matvec(matrix, value), shift) == value)
    omega = np.exp(2j * np.pi / 3)
    transform = {}
    for character in STATES:
        total = 0j
        for i, value in enumerate(STATES):
            pairing = sum(a * b for a, b in zip(character, value)) % 3
            total += int(fixed_counts[i]) * omega ** (-pairing)
        transform[character] = total
    zeros = [list(character) for character, value in transform.items() if abs(value) < 1e-8]
    slices = {}
    for coordinate, name in enumerate(("xp", "zp", "xf", "zf")):
        slices[name] = {str(level): sum(int(fixed_counts[i]) for i, state in enumerate(STATES) if state[coordinate] == level) for level in range(3)}
    result = {
        "schema": "w33.pass2958.hard_shell_fourier.v1",
        "status": "COMPLETE_EXACT",
        "hard_shell_fixed_incidence_total": int(fixed_counts.sum()),
        "per_frame_count_histogram": {str(k): v for k, v in sorted(Counter(map(int, fixed_counts)).items())},
        "ternary_fourier_nonzero": sum(abs(value) >= 1e-8 for value in transform.values()),
        "ternary_fourier_zero_count": len(zeros),
        "zero_characters": zeros,
        "coordinate_slice_incidence": slices,
        "headline": "Exactly the two nontrivial pure-zp characters vanish; terminal-shell fixed incidences split 60/60/60 across zp.",
        "boundary": "This refutes a sparse 15/24/40/81 Hodge or code-module identification; it is an exact finite Fourier statement only."
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    matrices, matrix_index = build_sp43()
    depth, shell, new_counts = forward_bfs(matrices, matrix_index)
    classes = conjugacy_closure(shell, matrices, matrix_index)
    result53 = {
        "schema": "w33.pass2953.diameter19_conjugacy.v1",
        "status": "COMPLETE_EXACT",
        "group_order": len(matrices) * 81,
        "directed_diameter": int(depth.max()),
        "shell_size": int(shell.size),
        "conjugacy_classes_intersecting_shell": len(classes),
        "sum_full_class_sizes": sum(row["full_class_size"] for row in classes),
        "ball_new_counts": new_counts,
        "classes": classes,
        "headline": "The 188 hardest elements meet 12 full ASp(4,3) conjugacy classes; the prior 25 algebraic profiles strictly over-refined conjugacy."
    }
    result58 = hard_shell_fourier(shell, matrices)
    assert len(classes) == 12
    assert [row["shell_intersection"] for row in classes] == [2,22,6,6,4,6,6,4,2,8,12,110]
    assert result58["zero_characters"] == [[0,1,0,0],[0,2,0,0]]
    assert result58["coordinate_slice_incidence"]["zp"] == {"0":60,"1":60,"2":60}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / OUT53.name).write_text(json.dumps(result53, indent=2, sort_keys=True) + "\n")
    (args.output_dir / OUT58.name).write_text(json.dumps(result58, indent=2, sort_keys=True) + "\n")
    print("PASS conjugacy classes=12 shell=188 Fourier support=79/81")


if __name__ == "__main__":
    main()
