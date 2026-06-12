#!/usr/bin/env python3
"""BT778 — PG(3,2)-label stabilizer classification.

BT775 showed that the BT772 mod-2 PG(3,2) label gauge is not equivariant for
all of Sp(4,3).  This verifier classifies the exact stabilizer of that label
partition inside the generated matrix group Sp(4,3).

Result: the full matrix stabilizer is {+I,-I}; projectively this is trivial.
Thus the PG(3,2) gauge is rigid, not a hidden quotient symmetry.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np

from bt766_intrinsic_k44_octet_quotient import build_w33

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT778_PG32_LABEL_STABILIZER_summary.json"
MOD = 3
J = np.array(
    [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]], dtype=int
) % MOD


def key(M):
    return tuple(int(x) % MOD for x in M.flatten())


def norm(v):
    v = tuple(int(x) % MOD for x in v)
    for x in v:
        if x % MOD:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % MOD for y in v)
    raise ValueError("zero vector")


def apply(M, p):
    return norm(tuple((M @ np.array(p, dtype=int)) % MOD))


def transvection(v):
    vv = np.array(v, dtype=int).reshape(4, 1)
    Jv = (J @ vv) % MOD
    return (np.eye(4, dtype=int) + vv @ Jv.T) % MOD


def label(p):
    return tuple(int(x) % 2 for x in p)


def preserves_labels(M, pts, idx):
    induced = {}
    for p in pts:
        source = label(p)
        target = label(apply(M, p))
        if source in induced and induced[source] != target:
            return False, induced
        induced[source] = target
    return len(induced) == 15 and len(set(induced.values())) == 15, induced


def generate_sp43(pts):
    gens = []
    seen_gens = set()
    for p in pts:
        T = transvection(p)
        k = key(T)
        if k not in seen_gens:
            seen_gens.add(k)
            gens.append(T)

    I = np.eye(4, dtype=int) % MOD
    group = {key(I): I}
    q = deque([I])
    while q:
        A = q.popleft()
        for g in gens:
            B = (A @ g) % MOD
            k = key(B)
            if k not in group:
                group[k] = B
                q.append(B)
    return gens, group


def main():
    pts, lines, idx, G, point_lines = build_w33()
    gens, group = generate_sp43(pts)
    stabilizers = []
    induced_maps = []
    for M in group.values():
        ok, induced = preserves_labels(M, pts, idx)
        if ok:
            stabilizers.append(M)
            induced_maps.append(induced)

    plus = np.eye(4, dtype=int) % MOD
    minus = (2 * np.eye(4, dtype=int)) % MOD
    stabilizer_keys = {key(M) for M in stabilizers}
    label_classes = Counter(label(p) for p in pts)
    induced_actions = {tuple(sorted((a, b) for a, b in ind.items())) for ind in induced_maps}

    checks = {
        "transvection_generators_40": len(gens) == 40,
        "generated_group_order_51840": len(group) == 51840,
        "all_generated_matrices_symplectic": all(np.array_equal((M.T @ J @ M) % MOD, J) for M in group.values()),
        "label_partition_has_15_classes": len(label_classes) == 15,
        "matrix_stabilizer_order_2": len(stabilizers) == 2,
        "matrix_stabilizer_is_plus_minus_identity": stabilizer_keys == {key(plus), key(minus)},
        "projective_stabilizer_order_1": len(induced_actions) == 1,
        "induced_label_action_identity_only": all(all(k == v for k, v in ind.items()) for ind in induced_maps),
    }

    result = {
        "theorem": "BT778 PG(3,2)-Label Stabilizer Classification",
        "group": {
            "generated_group": "Sp(4,3)",
            "order": len(group),
            "generator_type": "40 symplectic transvections, one per W33 projective point",
        },
        "label_partition": {
            "method": "coordinatewise normalized F_3^4 representative modulo 2",
            "classes": len(label_classes),
            "class_size_distribution": {str(k): int(v) for k, v in sorted(Counter(label_classes.values()).items())},
        },
        "stabilizer": {
            "matrix_order": len(stabilizers),
            "matrices": [M.astype(int).tolist() for M in stabilizers],
            "projective_order": len(induced_actions),
            "interpretation": "Only ±I preserve the PG(3,2) label partition; projectively this is trivial.",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This classifies the stabilizer of the BT772 coordinate-label partition. It does not classify unrelated 15-dimensional real-frame automorphisms."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
