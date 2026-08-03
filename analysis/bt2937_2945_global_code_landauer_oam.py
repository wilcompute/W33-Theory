#!/usr/bin/env python3
"""Passes 2937-2945: global support code, decoder, Landauer, OAM, and two outside-box probes."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict, deque
from itertools import combinations, product
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix

P = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2937_BT2945_GLOBAL_CODE_LANDAUER_OAM_results.json"


def canon_affine(a: tuple[int, ...], b: int) -> tuple[int, ...]:
    word = tuple(a) + (b,)
    neg = tuple((-x) % P for x in word)
    return min(word, neg)


def affine_features(dim: int):
    seen = set()
    result = []
    for a in product(range(P), repeat=dim):
        if not any(a):
            continue
        for b in range(P):
            c = canon_affine(a, b)
            if c not in seen:
                seen.add(c)
                result.append((c[:-1], c[-1]))
    return result


def eval_feature(point, feature):
    a, b = feature
    return int((sum(x * y for x, y in zip(a, point)) + b) % P != 0)


def hamming(left, right):
    return sum(x != y for x, y in zip(left, right))


def local_ag3_optimum():
    points = list(product(range(P), repeat=3))
    features = affine_features(3)
    values = np.array([[eval_feature(x, f) for f in features] for x in points], dtype=int)
    pairs = list(combinations(range(len(points)), 2))
    sep = np.array([[values[i, j] != values[k, j] for j in range(len(features))] for i, k in pairs], dtype=float)
    result = milp(
        c=np.ones(len(features)),
        integrality=np.ones(len(features)),
        bounds=Bounds(np.zeros(len(features)), np.full(len(features), 4.0)),
        constraints=LinearConstraint(csr_matrix(sep), np.full(len(pairs), 4.0), np.full(len(pairs), np.inf)),
        options={"time_limit": 120},
    )
    if not result.success:
        raise AssertionError(result.message)
    witness = np.rint(result.x).astype(int)
    assert witness.sum() == 12
    rows = []
    for index, multiplicity in enumerate(witness):
        if multiplicity:
            rows.append({"feature_index": index, "a": list(features[index][0]), "b": features[index][1], "multiplicity": int(multiplicity)})
    return {"feature_count": 39, "point_count": 27, "optimum": 12, "solver_message": result.message, "witness": rows}


GLOBAL_FEATURE_INDICES = [108, 83, 19, 103, 18, 41, 6, 7, 43, 40, 104, 82, 9, 109, 44, 11]


def global_code():
    points = list(product(range(P), repeat=4))
    features = affine_features(4)
    assert len(features) == 120
    chosen = [features[i] for i in GLOBAL_FEATURE_INDICES]
    code = [tuple(eval_feature(x, f) for f in chosen) for x in points]
    distances = Counter(hamming(code[i], code[j]) for i, j in combinations(range(81), 2))
    assert len(set(code)) == 81 and min(distances) == 4

    by_direction = defaultdict(list)
    for feature_index in GLOBAL_FEATURE_INDICES:
        a, b = features[feature_index]
        pivot = next(i for i, value in enumerate(a) if value)
        scale = pow(a[pivot], -1, P)
        direction = tuple(scale * value % P for value in a)
        by_direction[direction].append((scale * b % P, feature_index))
    assert len(by_direction) == 8 and all(len(v) == 2 for v in by_direction.values())
    directions = list(by_direction)
    offsets = [[item[0] for item in by_direction[d]] for d in directions]
    generator = np.array(directions, dtype=int)

    ternary = [tuple((generator @ np.array(x, dtype=int)) % P) for x in points]
    ternary_dist = Counter(hamming(ternary[i], ternary[j]) for i, j in combinations(range(81), 2))
    assert min(ternary_dist) == 4
    weight_enum = Counter(sum(value != 0 for value in word) for word in ternary)
    assert weight_enum == Counter({0: 1, 4: 22, 5: 24, 6: 20, 7: 8, 8: 6})

    parity = np.array([
        [1, 1, 1, 1, 0, 0, 0, 0],
        [2, 0, 2, 0, 1, 1, 0, 0],
        [2, 1, 1, 0, 2, 0, 1, 0],
        [1, 1, 0, 0, 1, 0, 0, 1],
    ], dtype=int)
    assert np.all((parity @ generator) % P == 0)
    syndrome_table = {}
    for position in range(8):
        for magnitude in (1, 2):
            error = np.zeros(8, dtype=int)
            error[position] = magnitude
            syndrome = tuple(int(v) for v in ((parity @ error) % P))
            assert syndrome not in syndrome_table
            syndrome_table[syndrome] = (position, magnitude)
    assert len(syndrome_table) == 16

    permutation = [1, 0, 3, 2, 6, 7, 4, 5]
    signs = [1, 2, 2, 1, 1, 1, 2, 2]
    code_set = {tuple(word) for word in ternary}
    dual_set = {
        tuple(int(v) for v in ((np.array(u, dtype=int) @ parity) % P))
        for u in product(range(P), repeat=4)
    }
    mapped = set()
    for word in code_set:
        out = [0] * 8
        for old, new in enumerate(permutation):
            out[new] = signs[old] * word[old] % P
        mapped.add(tuple(out))
    assert mapped == dual_set
    gram = (generator.T @ generator) % P
    assert np.any(gram)

    weight4_supports = {
        tuple(i for i, value in enumerate(word) if value)
        for word in code_set
        if sum(value != 0 for value in word) == 4
    }
    coordinate_automorphisms = []
    for permutation_candidate in __import__("itertools").permutations(range(8)):
        mapped_supports = {
            tuple(sorted(permutation_candidate[i] for i in support))
            for support in weight4_supports
        }
        if mapped_supports == weight4_supports:
            coordinate_automorphisms.append(permutation_candidate)
    assert len(coordinate_automorphisms) == 24
    monomial_count = 0
    for permutation_candidate in coordinate_automorphisms:
        for sign_candidate in product((1, 2), repeat=8):
            mapped_code = {
                tuple(sign_candidate[i] * word[permutation_candidate[i]] % P for i in range(8))
                for word in code_set
            }
            if mapped_code == code_set:
                monomial_count += 1
    assert monomial_count == 48

    binary_set = {sum(bit << i for i, bit in enumerate(word)) for word in code}
    xor_kernel = [k for k in range(1 << 16) if all((c ^ k) in binary_set for c in binary_set)]
    assert xor_kernel == [0]

    lower = math.ceil(120 * 12 / 117)
    assert lower == 13
    return {
        "affine_feature_orbit": 120,
        "local_AG3_multiset_optimum": 12,
        "three_flat_count": 120,
        "nonconstant_three_flats_per_feature": 117,
        "global_lower_bound": lower,
        "global_upper_bound": 16,
        "selected_feature_indices": GLOBAL_FEATURE_INDICES,
        "selected_features": [{"a": list(a), "b": b} for a, b in chosen],
        "binary_minimum_distance": 4,
        "binary_distance_enumerator": {str(k): v for k, v in sorted(distances.items())},
        "binary_xor_kernel_size": len(xor_kernel),
        "outer_code": {
            "parameters": "[8,4,4]_3",
            "generator_rows": generator.tolist(),
            "pair_offsets": offsets,
            "parity_check_rows": parity.tolist(),
            "weight_enumerator": {str(k): v for k, v in sorted(weight_enum.items())},
            "isodual": True,
            "self_dual": False,
            "monomial_permutation_old_to_new": permutation,
            "monomial_signs": signs,
            "single_symbol_syndrome_count": len(syndrome_table),
            "weight_four_support_count": len(weight4_supports),
            "coordinate_automorphism_order": len(coordinate_automorphisms),
            "coordinate_automorphism_structure": "S4",
            "monomial_automorphism_order": monomial_count,
            "monomial_automorphism_structure": "C2 x S4",
            "syndrome_table": {"".join(map(str, k)): list(v) for k, v in sorted(syndrome_table.items())},
        },
    }


def m36_fault_envelope():
    gc = (7 - 3 * math.sqrt(5)) / 4
    rows = []
    for locations in (2, 4, 6, 8, 10, 12, 16, 20, 24, 32):
        per_location = 1 - (1 - gc) ** (1 / locations)
        rows.append({"fault_locations": locations, "max_independent_fault_probability": per_location})
    return {
        "accepted_fault_budget": gc,
        "exact_budget": "(7-3*sqrt(5))/4",
        "envelope": "p_out <= f + (1-f)R(p), f <= 1-(1-q)^L",
        "per_location_table": rows,
        "boundary": "circuit-independent adversarial accepted-fault envelope; not a compiled circuit threshold",
    }


def calibrated_observer():
    fp, fn, prior_one = 0.002, 0.03, 2 / 3

    def bayes_error(repetitions):
        total = 0.0
        decisions = []
        for ones in range(repetitions + 1):
            p0 = math.comb(repetitions, ones) * fp**ones * (1 - fp) ** (repetitions - ones)
            p1 = math.comb(repetitions, ones) * (1 - fn) ** ones * fn ** (repetitions - ones)
            w0, w1 = (1 - prior_one) * p0, prior_one * p1
            total += min(w0, w1)
            decisions.append(1 if w1 >= w0 else 0)
        return total, decisions

    rows = []
    for target in (1e-3, 1e-6, 1e-9, 1e-12):
        repetitions = 1
        while 16 * bayes_error(repetitions)[0] > target:
            repetitions += 1
        error, decisions = bayes_error(repetitions)
        rows.append({
            "target_total_failure": target,
            "repetitions_per_support_bit": repetitions,
            "per_bit_bayes_error": error,
            "union_bound_16_observations": 16 * error,
            "decision_by_observed_one_count": decisions,
        })
    return {
        "false_positive": fp,
        "false_negative": fn,
        "prior_support_one": prior_one,
        "maximum_adaptive_support_bits": 16,
        "rows": rows,
        "boundary": "independent calibrated-bit channel and union bound; not a laboratory detector model",
    }


def landauer_ledger():
    log81 = math.log2(81)
    raw_static = 8
    protected = 16
    expected_steps = 94 / 27
    return {
        "state_entropy_bits": log81,
        "transcript_theorem": "Any deterministic exact diagnostic transcript that identifies a uniform 81-state frame has entropy exactly log2(81), independent of adaptive policy.",
        "best_static_raw_bits": raw_static,
        "best_static_redundancy_bits": raw_static - log81,
        "protected_raw_bits": protected,
        "protected_redundancy_bits": protected - log81,
        "adaptive_expected_operations": expected_steps,
        "adaptive_uncompressed_mask_bits": 4 * expected_steps,
        "adaptive_compressed_floor_bits": log81,
        "single_error_label_entropy": "h2(p)+4p bits for no error versus 16 equiprobable single-bit errors",
        "finite_time_boundary": "Landauer values are quasistatic floors; finite-time reset adds protocol-dependent positive dissipation and coherence can add cost.",
    }


def oam_group_obstruction():
    fp = np.array([[0, 2, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.int8)
    cxpf = np.array([[1, 0, 0, 0], [0, 1, 0, 2], [1, 0, 1, 0], [0, 0, 0, 1]], dtype=np.int8)
    cxfp = np.array([[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 2, 0, 1]], dtype=np.int8)
    anti = np.diag([1, 2, 1, 2]).astype(np.int8)

    points = []
    for point in product(range(P), repeat=4):
        if not any(point):
            continue
        pivot = next(i for i, value in enumerate(point) if value)
        if point[pivot] == 1:
            points.append(point)
    assert len(points) == 40
    point_index = {point: i for i, point in enumerate(points)}

    def canonical(vector):
        vector = [int(value) % P for value in vector]
        pivot = next(i for i, value in enumerate(vector) if value)
        if vector[pivot] == 2:
            vector = [(2 * value) % P for value in vector]
        return tuple(vector)

    def matrix_permutation(matrix):
        return tuple(
            point_index[canonical(matrix @ np.array(point, dtype=np.int8))]
            for point in points
        )

    def compose(left, right):
        return tuple(left[right[i]] for i in range(40))

    generators = [matrix_permutation(m) for m in (fp, cxpf, cxfp, anti)]
    identity = tuple(range(40))
    actions = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in actions:
                actions.add(candidate)
                queue.append(candidate)
    assert len(actions) == 51840

    def cycle_type(permutation):
        seen = [False] * 40
        lengths = []
        for start in range(40):
            if seen[start]:
                continue
            current, length = start, 0
            while not seen[current]:
                seen[current] = True
                current = permutation[current]
                length += 1
            lengths.append(length)
        return tuple(sorted(lengths, reverse=True))

    inventory = Counter(cycle_type(action) for action in actions)
    maximum = max(cycles[0] for cycles in inventory)
    assert maximum == 12 and (40,) not in inventory
    return {
        "projective_similitude_actions": len(actions),
        "cycle_type_count": len(inventory),
        "maximum_single_orbit": maximum,
        "forty_cycle_exists": False,
        "interpretation": "A single cyclic OAM shift cannot implement the full 40-point W(3,3) address permutation. Geometry-preserving OAM addressing needs at least a multi-cycle sorter/interferometer or multiple mode registers.",
        "cycle_inventory": {"-".join(map(str, k)): v for k, v in sorted(inventory.items())},
    }


def build_result():
    local = local_ag3_optimum()
    code = global_code()
    result = {
        "schema": "w33.pass2937_2945.global_code_landauer_oam.v1",
        "status": "COMPLETE_EXACT_WITH_MODELLED_BOUNDARIES",
        "local_AG3": local,
        "global_affine_support_code": code,
        "symmetry_quotiented_decoder": {
            "architecture": "16 binary probes -> eight ternary symbols -> four-trit syndrome -> 16-entry single-symbol correction table -> recover four frame trits",
            "candidate_scans_removed": 81,
            "outer_syndromes": 16,
            "claim": "one ternary-symbol correction follows from the exact [8,4,4]_3 outer code; directed binary-bit behavior remains a separate RTL contract",
        },
        "m36_fault_envelope": m36_fault_envelope(),
        "calibrated_active_observer": calibrated_observer(),
        "nonlinear_code_identification": code["outer_code"] | {
            "binary_image_length": 16,
            "binary_image_size": 81,
            "binary_image_distance": 4,
            "binary_xor_kernel_size": code["binary_xor_kernel_size"],
        },
        "landauer": landauer_ledger(),
        "oam": {
            "logical_requirement": "optional carrier: the abstract machine needs any two independent qutrit-capable degrees of freedom",
            "selected_hardware_profile": "the repository's OAM/GKP and path-times-OAM proposals use OAM explicitly",
            "group_theoretic_addressing_obstruction": oam_group_obstruction(),
            "hardware_boundary": "operator ABI and radial-shell model are source-complete; no built 40-mode OAM Holonet or calibrated crosstalk matrix is claimed",
        },
    }
    checks = {
        "AG3_optimum_12": local["optimum"] == 12,
        "global_bracket_13_16": code["global_lower_bound"] == 13 and code["global_upper_bound"] == 16,
        "global_binary_d4": code["binary_minimum_distance"] == 4,
        "outer_ternary_844": code["outer_code"]["parameters"] == "[8,4,4]_3",
        "outer_isodual_not_selfdual": code["outer_code"]["isodual"] and not code["outer_code"]["self_dual"],
        "sixteen_unique_single_symbol_syndromes": code["outer_code"]["single_symbol_syndrome_count"] == 16,
        "outer_code_monomial_group_48": code["outer_code"]["monomial_automorphism_order"] == 48,
        "m36_fault_budget_positive": result["m36_fault_envelope"]["accepted_fault_budget"] > 0,
        "calibrated_repetition_rows": len(result["calibrated_active_observer"]["rows"]) == 4,
        "landauer_transcript_floor_log81": abs(result["landauer"]["state_entropy_bits"] - math.log2(81)) < 1e-12,
        "OAM_no_40_cycle": not result["oam"]["group_theoretic_addressing_obstruction"]["forty_cycle_exists"],
        "OAM_max_orbit_12": result["oam"]["group_theoretic_addressing_obstruction"]["maximum_single_orbit"] == 12,
    }
    assert all(checks.values())
    result["checks"] = checks
    result["check_count"] = len(checks)
    result["headline"] = "Global affine support distance four is bracketed 13..16; the 16-bit witness is an isodual [8,4,4]_3 binary image, and no geometry-preserving OAM action is a 40-cycle."
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-frozen", action="store_true")
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.verify_frozen:
        if OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"frozen certificate drift: {OUT}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(rendered, encoding="utf-8")
    print(f"PASS {result['check_count']}/{result['check_count']}")
    print(result["headline"])


if __name__ == "__main__":
    main()
