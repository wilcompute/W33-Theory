#!/usr/bin/env python3
"""Pass 2956: complete three-copy CSS [[6,2]] closure for the deep M36 resource.

Corrections to the predecessor search:
  * Pass 2910 instantiated ray 0, which belongs to the shallow four-ray class. The
    engineering target here is deep ray 5.
  * Rejecting every single-error vector is sufficient for quadratic suppression but not
    necessary. An accepted single error may be collinear with the accepted clean logical
    ray. This script evaluates that residual directly.

Scope: every six-qubit CSS rank-four stabilizer subspace and all sixteen syndromes,
43,617 * 16 = 697,872 projectors. This is not the set of all 213,648,435 general
isotropic six-qubit rank-four stabilizer subspaces.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import numpy as np

from bt2954_2959_chirality_probe_and_mirror import cliffords, projective_key, rays

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2956_THREECOPY_CSS_CLOSURE_results.json"

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.diag([1,-1]).astype(complex)
ONE_QUBIT = {(0,0):I, (1,0):X, (0,1):Z, (1,1):Y}


def xor_span(basis):
    values = {0}
    for vector in basis:
        values |= {value ^ vector for value in tuple(values)}
    return frozenset(values)


def binary_rank(vectors, bits=6):
    pivots = [0] * bits
    rank = 0
    for vector in vectors:
        value = vector
        while value:
            pivot = value.bit_length() - 1
            if pivots[pivot]:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                rank += 1
                break
    return rank


def subspace_basis(space):
    basis = []
    for vector in sorted(space):
        if vector and binary_rank(basis + [vector]) > len(basis):
            basis.append(vector)
    assert xor_span(basis) == space
    return basis


def enumerate_subspaces():
    spaces = {0: [frozenset({0})]}
    for dimension in range(1,5):
        seen = set()
        for selection in combinations(range(1,64), dimension):
            if binary_rank(selection) == dimension:
                seen.add(xor_span(selection))
        spaces[dimension] = sorted(seen, key=lambda value: tuple(sorted(value)))
    bases = {dimension: [subspace_basis(space) for space in values] for dimension, values in spaces.items()}
    return spaces, bases


def dot2(left, right):
    return (left & right).bit_count() % 2


def two_qubit_pauli(x_bits, z_bits):
    matrix = np.array([[1]], dtype=complex)
    for qubit in range(2):
        matrix = np.kron(matrix, ONE_QUBIT[((x_bits >> qubit) & 1, (z_bits >> qubit) & 1)])
    return matrix


PAULI2 = {(x,z): two_qubit_pauli(x,z) for x in range(4) for z in range(4)}


def error_basis(magic):
    basis = []
    for vector in [magic] + [np.eye(4, dtype=complex)[:, i] for i in range(4)]:
        residual = vector.copy()
        for accepted in basis:
            residual -= accepted * np.vdot(accepted, residual)
        norm = np.linalg.norm(residual)
        if norm > 1e-10:
            basis.append(residual / norm)
        if len(basis) == 4:
            break
    assert abs(abs(np.vdot(basis[0], magic)) - 1) < 1e-9
    return basis[1:]


def six_qubit_expectation_tables(magic):
    errors = error_basis(magic)
    local_states = [magic] + errors
    local = np.zeros((4,4,4,4), dtype=complex)
    for left_id, left in enumerate(local_states):
        for right_id, right in enumerate(local_states):
            for x_bits in range(4):
                for z_bits in range(4):
                    local[left_id,right_id,x_bits,z_bits] = np.vdot(left, PAULI2[(x_bits,z_bits)] @ right)
    configurations = [(0,0,0)]
    for copy in range(3):
        for error_id in range(1,4):
            configuration = [0,0,0]
            configuration[copy] = error_id
            configurations.append(tuple(configuration))
    diagonal = np.zeros((10,4096), dtype=float)
    clean_to_single = np.zeros((9,4096), dtype=complex)
    for pauli_id in range(4096):
        x_bits, z_bits = pauli_id & 63, pauli_id >> 6
        for state_id, configuration in enumerate(configurations):
            value = 1 + 0j
            for copy in range(3):
                local_x = (x_bits >> (2*copy)) & 3
                local_z = (z_bits >> (2*copy)) & 3
                value *= local[configuration[copy], configuration[copy], local_x, local_z]
            diagonal[state_id, pauli_id] = value.real
        for single_id, configuration in enumerate(configurations[1:]):
            value = 1 + 0j
            for copy in range(3):
                local_x = (x_bits >> (2*copy)) & 3
                local_z = (z_bits >> (2*copy)) & 3
                value *= local[0, configuration[copy], local_x, local_z]
            clean_to_single[single_id, pauli_id] = value
    return diagonal, clean_to_single


H16 = np.array([[1 if ((syndrome & mask).bit_count() % 2) == 0 else -1 for mask in range(16)] for syndrome in range(16)], dtype=float)


def css_codes(spaces, bases):
    for x_rank in range(5):
        for x_index, x_space in enumerate(spaces[x_rank]):
            x_basis = bases[x_rank][x_index]
            orthogonal = {z for z in range(64) if all(dot2(z,x) == 0 for x in x_space)}
            z_rank = 4 - x_rank
            for z_index, z_space in enumerate(spaces[z_rank]):
                if z_space.issubset(orthogonal):
                    yield x_rank, x_index, z_index, x_space, x_basis, z_space, bases[z_rank][z_index]


def generator_expectations(x_basis, z_basis, diagonal, cross):
    generators = [("x", vector) for vector in x_basis] + [("z", vector) for vector in z_basis]
    diagonal_group = np.zeros((10,16), dtype=float)
    cross_group = np.zeros((9,16), dtype=complex)
    for mask in range(16):
        x_value = z_value = 0
        for generator_id, (kind, vector) in enumerate(generators):
            if (mask >> generator_id) & 1:
                if kind == "x": x_value ^= vector
                else: z_value ^= vector
        phase = -1 if (((x_value & z_value).bit_count() // 2) % 2) else 1
        pauli_id = x_value | (z_value << 6)
        diagonal_group[:,mask] = phase * diagonal[:,pauli_id]
        cross_group[:,mask] = phase * cross[:,pauli_id]
    probabilities = diagonal_group @ H16.T / 16
    overlaps = cross_group @ H16.T / 16
    probabilities[np.abs(probabilities) < 1e-10] = 0
    return probabilities, overlaps


def collinearity_search(spaces, bases, diagonal, cross):
    witnesses = []
    rank_split = Counter()
    code_count = 0
    for x_rank, x_index, z_index, _, x_basis, _, z_basis in css_codes(spaces, bases):
        code_count += 1
        probabilities, overlaps = generator_expectations(x_basis, z_basis, diagonal, cross)
        for syndrome in range(16):
            clean_probability = probabilities[0,syndrome]
            if clean_probability <= 1e-10:
                continue
            residuals = probabilities[1:,syndrome] - np.abs(overlaps[:,syndrome])**2 / clean_probability
            residuals[np.abs(residuals) < 2e-9] = 0
            if np.min(residuals) < -1e-7:
                raise AssertionError("projected Gram residual is not positive")
            residuals = np.maximum(residuals, 0)
            if np.max(residuals) < 1e-8:
                witnesses.append((x_rank,x_index,z_index,syndrome,clean_probability,tuple(x_basis),tuple(z_basis)))
                rank_split["all_Z" if x_rank == 0 else "all_X" if x_rank == 4 else f"mixed_{x_rank}"] += 1
    return witnesses, rank_split, code_count


def span_coordinate_map(basis):
    result = {0:0}
    for index, vector in enumerate(basis):
        for value, mask in list(result.items()):
            result[value ^ vector] = mask | (1 << index)
    return result


def bitmask_amplitudes(vector64):
    result = np.zeros(64, dtype=complex)
    for bitmask in range(64):
        bits = tuple((bitmask >> qubit) & 1 for qubit in range(6))
        matrix_index = sum(bits[qubit] << (5-qubit) for qubit in range(6))
        result[bitmask] = vector64[matrix_index]
    return result


def closed_magic_branches(spaces, bases, clean_amplitudes, magic_orbit):
    closed = []
    for x_rank, x_index, z_index, x_space, x_basis, _, z_basis in css_codes(spaces, bases):
        x_coordinates = span_coordinate_map(x_basis)
        x_elements = sorted(x_space)
        z_rank = 4 - x_rank
        for z_syndrome in range(1 << z_rank):
            accepted = [value for value in range(64) if all(dot2(z,value) == ((z_syndrome >> i) & 1) for i,z in enumerate(z_basis))]
            unseen = set(accepted)
            representatives = []
            while unseen:
                representative = min(unseen)
                coset = {representative ^ x for x in x_elements}
                unseen -= coset
                representatives.append(representative)
            assert len(representatives) == 4
            representatives.sort()
            for x_syndrome in range(1 << x_rank):
                syndrome = x_syndrome | (z_syndrome << x_rank)
                coefficients = []
                normalization = math.sqrt(len(x_elements))
                for representative in representatives:
                    amplitude = 0j
                    for x in x_elements:
                        sign = -1 if ((x_coordinates[x] & x_syndrome).bit_count() % 2) else 1
                        amplitude += sign * clean_amplitudes[representative ^ x]
                    coefficients.append(amplitude / normalization)
                clean_probability = sum(abs(value)**2 for value in coefficients)
                if clean_probability < 1e-12:
                    continue
                logical = np.asarray(coefficients) / math.sqrt(clean_probability)
                if projective_key(logical) in magic_orbit:
                    closed.append((x_rank,x_index,z_index,syndrome,clean_probability,tuple(x_basis),tuple(z_basis),tuple(representatives),logical))
    return closed


def closed_slope_search(spaces, bases, diagonal, cross, closed_ids):
    minimum = float("inf")
    best = []
    slope_histogram = Counter()
    success_histogram = Counter()
    count = 0
    for x_rank, x_index, z_index, _, x_basis, _, z_basis in css_codes(spaces, bases):
        relevant = [syndrome for syndrome in range(16) if (x_rank,x_index,z_index,syndrome) in closed_ids]
        if not relevant:
            continue
        probabilities, overlaps = generator_expectations(x_basis, z_basis, diagonal, cross)
        for syndrome in relevant:
            clean_probability = probabilities[0,syndrome]
            residuals = probabilities[1:,syndrome] - np.abs(overlaps[:,syndrome])**2 / clean_probability
            residuals[np.abs(residuals) < 2e-9] = 0
            residuals = np.maximum(residuals, 0)
            slope = float(np.sum(residuals)) / (4 * clean_probability)
            count += 1
            slope_histogram[str(Fraction(slope).limit_denominator(100000))] += 1
            success_histogram[str(Fraction(float(clean_probability)).limit_denominator(100000))] += 1
            row = (x_rank,x_index,z_index,syndrome,clean_probability,tuple(x_basis),tuple(z_basis))
            if slope < minimum - 1e-9:
                minimum = slope
                best = [row]
            elif abs(slope - minimum) < 1e-9:
                best.append(row)
    return minimum, best, slope_histogram, success_histogram, count


def main():
    ray_vectors = rays()
    group = cliffords()
    deep = ray_vectors[5]
    deep_orbit = {projective_key(matrix @ deep) for matrix in group}
    assert len(deep_orbit) == 640
    spaces, bases = enumerate_subspaces()
    diagonal, cross = six_qubit_expectation_tables(deep)
    collinear, rank_split, code_count = collinearity_search(spaces, bases, diagonal, cross)
    assert code_count == 43617
    assert len(collinear) == 54
    assert rank_split == Counter({"all_Z":27,"all_X":27})

    clean_state = np.kron(np.kron(deep, deep), deep)
    clean_amplitudes = bitmask_amplitudes(clean_state)
    closed = closed_magic_branches(spaces, bases, clean_amplitudes, deep_orbit)
    closed_ids = {(row[0],row[1],row[2],row[3]) for row in closed}
    collinear_ids = {(row[0],row[1],row[2],row[3]) for row in collinear}
    assert len(closed) == 67023
    assert not (closed_ids & collinear_ids)
    minimum, best, slope_histogram, success_histogram, closed_count = closed_slope_search(spaces, bases, diagonal, cross, closed_ids)
    assert closed_count == 67023
    assert abs(minimum - 1) < 1e-9
    assert len(best) == 3087
    best_success = max(row[4] for row in best)
    assert abs(best_success - 0.25) < 1e-9

    result = {
        "schema": "w33.pass2956.threecopy_css_closure.v1",
        "status": "COMPLETE_EXACT_CSS_FAMILY",
        "target": "deep M36 representative ray 5",
        "correction": {
            "predecessor_target": "Pass 2910 used shallow ray 0",
            "predecessor_condition": "factor-wise rejection was sufficient but not necessary; collinearity is the correct first-order condition"
        },
        "css_subspaces": code_count,
        "css_rank_split": {str(rank): sum(1 for _ in [None] for row in css_codes(spaces,bases) if row[0] == rank) for rank in range(5)},
        "syndromes_per_subspace": 16,
        "projectors_examined": code_count * 16,
        "single_error_collinear_projectors": len(collinear),
        "collinear_projector_rank_split": dict(rank_split),
        "closed_and_collinear_magic_branches": len(closed_ids & collinear_ids),
        "deep_clean_closed_branches": len(closed),
        "deep_clean_success_histogram": dict(success_histogram),
        "minimum_closed_p_out_slope": str(Fraction(minimum).limit_denominator()),
        "minimum_slope_branch_count": len(best),
        "best_minimum_slope_clean_success": str(Fraction(best_success).limit_denominator()),
        "best_minimum_slope_raw_inputs_per_accepted_output_at_p0": int(round(3 / best_success)),
        "slope_histogram": dict(slope_histogram),
        "explicit_identity_branch": {
            "x_generators": [1,4],
            "z_generators": [2,8],
            "syndrome": 15,
            "success": "(2-p)^2/16",
            "output_fidelity": "1-3p/4",
            "p_out": "p"
        },
        "headline": "No three-copy CSS [[6,2]] branch improves the deep M36 state to first order. The 54 quadratic-collinearity projectors close only on stabilizer logical lines.",
        "boundary": "Complete for all CSS [[6,2]] stabilizer projectors and all syndromes; not all 213,648,435 general isotropic six-qubit stabilizer subspaces."
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS CSS subspaces=43617 closed=67023 min_slope=1 collinear_false_leads=54")


if __name__ == "__main__":
    main()
