#!/usr/bin/env python3
"""Pass 3194: coarsest curvature-aware quotient of the frozen D4 policy tree."""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3194_CURVATURE_CAUSAL_QUOTIENT_results.json"
D4 = [(a, b) for a in range(4) for b in range(2)]
DI = {g: i for i, g in enumerate(D4)}
IDENTITY = (0, 0)
FAULTS = [g for g in D4 if g != IDENTITY]
EDGES = list(itertools.combinations(range(10), 2))
TRIANGLES = list(itertools.combinations(range(10), 3))
FROZEN23 = [
    (5, 6, 9), (2, 5, 9), (4, 5, 8), (2, 4, 7), (0, 3, 6),
    (0, 1, 8), (1, 2, 4), (1, 3, 5), (3, 4, 8), (0, 4, 9),
    (2, 3, 8), (4, 8, 9), (1, 7, 8), (1, 4, 6), (0, 2, 3),
    (3, 7, 9), (1, 3, 9), (2, 6, 9), (3, 5, 7), (0, 1, 7),
    (3, 6, 8), (0, 4, 5), (4, 6, 7),
]
SELECTED = [TRIANGLES.index(t) for t in FROZEN23]
REMAINING = [i for i in range(120) if i not in set(SELECTED)]


def mul(g, h):
    a, b = g
    c, d = h
    return ((a + (-1 if b else 1) * c) % 4, (b + d) % 2)


def inv(g):
    a, b = g
    return ((-((-1 if b else 1) * a)) % 4, b)


def directed(edge, g, u, v):
    if (u, v) == edge:
        return g
    if (v, u) == edge:
        return inv(g)
    return IDENTITY


def syndrome(hypothesis):
    values = []
    for i, j, k in TRIANGLES:
        product = IDENTITY
        for u, v in ((i, j), (j, k), (k, i)):
            factor = IDENTITY
            for edge, group_element in hypothesis:
                factor = mul(directed(edge, group_element, u, v), factor)
            product = mul(factor, product)
        values.append(DI[product])
    return tuple(values)


def hypotheses():
    rows = [tuple()]
    rows.extend(((edge, g),) for edge in EDGES for g in FAULTS)
    rows.extend(
        ((edge, g), (other, h))
        for edge, other in itertools.combinations(EDGES, 2)
        for g in FAULTS
        for h in FAULTS
    )
    assert len(rows) == 48_826
    return rows


def curvature_labels(rows):
    measured_pairs = set()
    for triangle in FROZEN23:
        triangle_edges = [tuple(sorted(e)) for e in itertools.combinations(triangle, 2)]
        for a, b in itertools.combinations(triangle_edges, 2):
            measured_pairs.add(tuple(sorted((a, b))))
    assert len(measured_pairs) == 69

    def commutator(a, b):
        return mul(mul(mul(a, b), inv(a)), inv(b))

    labels = []
    for row in rows:
        if len(row) != 2:
            labels.append(0)
            continue
        (edge, a), (other, b) = row
        if tuple(sorted((edge, other))) not in measured_pairs:
            labels.append(0)
        else:
            labels.append(2 if commutator(a, b) == (2, 0) else 1)
    assert Counter(labels) == Counter({0: 45_445, 1: 1_725, 2: 1_656})
    return labels


def choose_action(indices, full):
    best = None
    for triangle in REMAINING:
        parts = defaultdict(list)
        for index in indices:
            parts[int(full[index, triangle])].append(index)
        key = (-len(parts), max(map(len, parts.values())), triangle)
        if best is None or key < best[0]:
            best = (key, triangle, parts)
    assert best is not None
    return best[1], best[2]


def raw_signature(indices, full):
    if len(indices) <= 1:
        return ("STOP",)
    action, parts = choose_action(indices, full)
    return (
        "TEST", action,
        tuple(sorted((outcome, raw_signature(tuple(child), full)) for outcome, child in parts.items())),
    )


def curvature_signature(indices, full, labels):
    histogram = Counter(labels[index] for index in indices)
    typed = (histogram[0], histogram[1], histogram[2])
    if len(indices) <= 1:
        return ("STOP", typed)
    action, parts = choose_action(indices, full)
    return (
        "TEST", action, typed,
        tuple(sorted((outcome, curvature_signature(tuple(child), full, labels)) for outcome, child in parts.items())),
    )


def collect_nodes(signature, output):
    output.add(repr(signature))
    if signature[0] == "TEST":
        children = signature[2] if len(signature) == 3 else signature[3]
        for _, child in children:
            collect_nodes(child, output)


def main() -> None:
    rows = hypotheses()
    full = np.array([syndrome(row) for row in rows], dtype=np.uint8)
    grouped = defaultdict(list)
    for index, key in enumerate(map(tuple, full[:, SELECTED])):
        grouped[key].append(index)
    collisions = [tuple(values) for values in grouped.values() if len(values) > 1]
    assert len(grouped) == 46_284
    assert len(collisions) == 1_436
    assert max(map(len, collisions)) == 3

    labels = curvature_labels(rows)
    raw = [raw_signature(c, full) for c in collisions]
    typed = [curvature_signature(c, full, labels) for c in collisions]
    raw_nodes: set[str] = set()
    typed_nodes: set[str] = set()
    for signature in raw:
        collect_nodes(signature, raw_nodes)
    for signature in typed:
        collect_nodes(signature, typed_nodes)

    raw_initial = len(set(map(repr, raw)))
    typed_initial = len(set(map(repr, typed)))
    assert (raw_initial, len(raw_nodes)) == (457, 470)
    assert (typed_initial, len(typed_nodes)) == (770, 876)

    initial_histograms = Counter()
    for collision in collisions:
        h = Counter(labels[index] for index in collision)
        initial_histograms[f"{h[0]},{h[1]},{h[2]}"] += 1

    result = {
        "schema": "w33.pass3194.curvature_causal_quotient.v1",
        "hypotheses": len(rows),
        "base_signatures": len(grouped),
        "raw_collision_classes": len(collisions),
        "curvature_partition": {"none": 45_445, "flat": 1_725, "curved": 1_656},
        "untyped_quotient": {"initial_states": raw_initial, "all_recursive_states": len(raw_nodes), "fixed_bits": math.ceil(math.log2(len(raw_nodes)))},
        "curvature_aware_quotient": {"initial_states": typed_initial, "all_recursive_states": len(typed_nodes), "fixed_bits": math.ceil(math.log2(len(typed_nodes)))},
        "additional_recursive_states": len(typed_nodes) - len(raw_nodes),
        "additional_fixed_bits": math.ceil(math.log2(len(typed_nodes))) - math.ceil(math.log2(len(raw_nodes))),
        "initial_curvature_histogram_types": dict(sorted(initial_histograms.items())),
        "minimality": "The decision tree is acyclic. Recursive signatures containing output label, chosen action and outcome-indexed child classes are the canonical Moore/bisimulation quotient, hence coarsest for the frozen contracts.",
        "headline": "Exact curvature typing refines the 470-state controller to 876 states and costs one fixed state bit, not a dense 48,826-hypothesis register.",
        "boundary": "Exact for the frozen noiseless future-action policy and the none/flat/curved output contract. Continuous noisy beliefs, changed utility coefficients and laboratory channels may require a different quotient."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"raw": len(raw_nodes), "curvature": len(typed_nodes)}, sort_keys=True))


if __name__ == "__main__":
    main()
