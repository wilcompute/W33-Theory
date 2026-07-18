#!/usr/bin/env python3
"""Pass 412: multi-slip sandpile decoding and the exact radius-three frontier."""
from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random

import networkx as nx
import numpy as np
import sympy as sp

from w33_pass410_414_common import certificate, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass412_multislip_sandpile_decoder.json"
MODULUS = 216
N = 27


def q3_graph() -> tuple[nx.Graph, np.ndarray, list[tuple[int, int, int]]]:
    vertices = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]
    index = {v: i for i, v in enumerate(vertices)}
    graph = nx.Graph()
    graph.add_nodes_from(range(N))
    lap = np.zeros((N, N), dtype=int)
    np.fill_diagonal(lap, 8)
    for i, (x, y, z) in enumerate(vertices):
        for xp in range(3):
            for yp in range(3):
                if (xp, yp) == (x, y):
                    continue
                zp = (z + y * xp - x * yp) % 3
                j = index[(xp, yp, zp)]
                graph.add_edge(i, j)
                lap[i, j] -= 1
    return graph, lap, vertices


def syndrome_matrix(lap: np.ndarray) -> np.ndarray:
    inverse = sp.Matrix(lap[:-1, :-1].tolist()).inv()
    # d row-vector maps to 216 * d * L^{-T}; L is symmetric.
    return np.array(
        [[int((inverse[row, col] * MODULUS) % MODULUS) for row in range(N - 1)] for col in range(N - 1)],
        dtype=np.int64,
    )


def syndrome(divisor: np.ndarray, matrix: np.ndarray) -> tuple[int, ...]:
    return tuple(int(x) for x in (divisor[:-1].astype(np.int64) @ matrix) % MODULUS)


def net_divisor_count(weight: int, n: int = N) -> int:
    total = 0
    for positive_support in range(1, weight + 1):
        for negative_support in range(1, weight + 1):
            if positive_support + negative_support > n:
                continue
            total += (
                comb(n, positive_support)
                * comb(n - positive_support, negative_support)
                * comb(weight - 1, positive_support - 1)
                * comb(weight - 1, negative_support - 1)
            )
    return total


def positive_compositions(total: int, length: int):
    if length == 1:
        yield (total,)
        return
    for first in range(1, total - length + 2):
        for rest in positive_compositions(total - first, length - 1):
            yield (first,) + rest


def enumerate_net_divisors_on_support(support: tuple[int, ...], max_weight: int):
    yield np.zeros(N, dtype=int)
    support_set = set(support)
    for weight in range(1, max_weight + 1):
        for psize in range(1, min(weight, len(support)) + 1):
            for positive_modes in combinations(support, psize):
                remaining = tuple(sorted(support_set.difference(positive_modes)))
                for nsize in range(1, min(weight, len(remaining)) + 1):
                    for negative_modes in combinations(remaining, nsize):
                        for pparts in positive_compositions(weight, psize):
                            for nparts in positive_compositions(weight, nsize):
                                divisor = np.zeros(N, dtype=int)
                                for mode, value in zip(positive_modes, pparts):
                                    divisor[mode] = value
                                for mode, value in zip(negative_modes, nparts):
                                    divisor[mode] = -value
                                yield divisor


def decode_with_erasure_support(target: tuple[int, ...], support: tuple[int, ...], matrix: np.ndarray, max_weight: int = 3):
    matches = []
    for divisor in enumerate_net_divisors_on_support(tuple(sorted(support)), max_weight):
        if syndrome(divisor, matrix) == target:
            matches.append(divisor)
    return matches


def transport_weight(divisor: np.ndarray) -> int:
    return int(np.maximum(divisor, 0).sum())


def build_payload() -> dict:
    graph, lap, vertices = q3_graph()
    smatrix = syndrome_matrix(lap)
    edge_connectivity = nx.edge_connectivity(graph)

    counts = {str(w): net_divisor_count(w) for w in (1, 2, 3)}
    cumulative = 1 + sum(counts.values())

    # Pairing ambiguity: two path decompositions, one net divisor.
    a, b, c, d = 0, 1, 3, 4
    pairing_one = [(a, c), (b, d)]  # target, source
    pairing_two = [(a, d), (b, c)]
    pair_divisor = np.zeros(N, dtype=int)
    for target, source in pairing_one:
        pair_divisor[target] += 1
        pair_divisor[source] -= 1
    pair_divisor_two = np.zeros(N, dtype=int)
    for target, source in pairing_two:
        pair_divisor_two[target] += 1
        pair_divisor_two[source] -= 1

    # Sharp weight-four collision from one Laplacian row.
    root_mode = 0
    neighbors = sorted(graph.neighbors(root_mode))
    left, right = neighbors[:4], neighbors[4:]
    d1 = np.zeros(N, dtype=int)
    d2 = np.zeros(N, dtype=int)
    d1[root_mode] = 4
    for mode in left:
        d1[mode] -= 1
    d2[root_mode] = -4
    for mode in right:
        d2[mode] += 1
    principal = lap[:, root_mode]

    # Erasure-assisted regression over deterministic random low-weight divisors.
    rng = random.Random(412)
    erasure_trials = []
    for _ in range(24):
        support = tuple(sorted(rng.sample(range(N), rng.randint(2, 6))))
        candidates = list(enumerate_net_divisors_on_support(support, 3))
        nonzero = [item for item in candidates if transport_weight(item) > 0]
        chosen = rng.choice(nonzero)
        matches = decode_with_erasure_support(syndrome(chosen, smatrix), support, smatrix, 3)
        erasure_trials.append(len(matches) == 1 and np.array_equal(matches[0], chosen))

    single_syndromes = set()
    for target in range(N):
        for source in range(N):
            if target == source:
                continue
            divisor = np.zeros(N, dtype=int)
            divisor[target] += 1
            divisor[source] -= 1
            single_syndromes.add(syndrome(divisor, smatrix))

    checks = {
        "graph_has_27_vertices": graph.number_of_nodes() == 27,
        "graph_is_8_regular": set(dict(graph.degree()).values()) == {8},
        "edge_connectivity_equals_degree_eight": edge_connectivity == 8,
        "single_slip_count_702": counts["1"] == 702,
        "weight_two_net_count_123552": counts["2"] == 123552,
        "weight_three_net_count_9746802": counts["3"] == 9746802,
        "single_syndromes_unique": len(single_syndromes) == 702,
        "pairing_is_not_encoded": np.array_equal(pair_divisor, pair_divisor_two) and pairing_one != pairing_two,
        "weight_four_witness_is_principal": np.array_equal(d1 - d2, principal),
        "weight_four_witness_has_mass_four_each": transport_weight(d1) == 4 and transport_weight(d2) == 4,
        "weight_four_collision_same_syndrome": syndrome(d1, smatrix) == syndrome(d2, smatrix),
        "all_erasure_trials_decode_uniquely": all(erasure_trials),
    }

    payload = {
        "schema": "w33.pass412.multislip_sandpile_decoder.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": {
            "principal_divisor_minimum_transport_weight": 8,
            "proof": "For any nonconstant integer firing vector, its maximum-level set has outgoing cut at least lambda(Gamma_3)=8, so the positive degree of its Laplacian divisor is at least 8. A single fired vertex attains 8.",
            "unique_net_error_radius": 3,
            "reason": "two net errors of transport weight at most 3 differ by transport weight at most 6, below the minimum nonzero principal weight 8",
            "sharp_failure_weight": 4,
        },
        "net_divisor_class_counts": {
            "formula": "sum_{r,s>=1} C(n,r) C(n-r,s) C(w-1,r-1) C(w-1,s-1)",
            "exact_weight": counts,
            "cumulative_zero_through_weight_three": cumulative,
        },
        "flow_kernel_boundary": {
            "statement": "the sandpile class depends only on net mode imbalance; source-to-target pairing is erased",
            "kernel": "integer directed cycle flows",
            "two_slip_pairing_witness": {
                "pairing_one_target_source": pairing_one,
                "pairing_two_target_source": pairing_two,
                "net_divisor": pair_divisor.tolist(),
            },
            "telemetry_requirement": "time-bin or edge labels are required to reconstruct path pairing; affected-mode erasures are sufficient only for the net divisor",
        },
        "weight_four_collision": {
            "mode": root_mode,
            "neighbors_partition": [left, right],
            "first_net_error": d1.tolist(),
            "second_net_error": d2.tolist(),
            "difference_equals_laplacian_column": principal.tolist(),
            "shared_syndrome": list(syndrome(d1, smatrix)),
        },
        "erasure_aided_decoder": {
            "input": "sandpile syndrome plus detector-supplied affected-mode support of size at most six",
            "method": "enumerate all degree-zero net divisors on that support with transport weight at most three",
            "deterministic_regression_trials": len(erasure_trials),
            "all_trials_unique": all(erasure_trials),
        },
        "claim_boundary": "This corrects net pulse imbalance through weight three. It cannot infer hidden path pairing without time-bin or edge telemetry.",
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 412 certificate drift")
    else:
        write_json(args.output, payload)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
