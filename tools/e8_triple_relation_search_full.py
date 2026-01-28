#!/usr/bin/env python3
"""Search stronger relations between E8 orthogonal-triple blocks.

We take one partition of the 120 E8 root lines into 40 triples of mutually
orthogonal lines and compute full 6x6 inner-product counts between triples
(using both ± roots per line).

We then search unions of relation classes for SRG(40,12,2,4).

Outputs:
- artifacts/e8_triple_relation_search_full.json
- artifacts/e8_triple_relation_search_full.md
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PARTITION_JSON = ROOT / "artifacts" / "e8_rootline_partition.json"
OUT_JSON = ROOT / "artifacts" / "e8_triple_relation_search_full.json"
OUT_MD = ROOT / "artifacts" / "e8_triple_relation_search_full.md"

MAX_CLASS_UNIONS = 1 << 12  # guard for class explosion


def build_e8_roots() -> np.ndarray:
    roots = []
    # type 1: (±1, ±1, 0,...)
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    v = np.zeros(8)
                    v[i] = s1
                    v[j] = s2
                    roots.append(v)
    # type 2: (±1/2)^8 with even number of minus signs
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(np.array(signs) / 2.0)
    return np.array(roots, dtype=float)


def canonical_line(root: np.ndarray) -> tuple[float, ...]:
    idx = None
    for i, x in enumerate(root):
        if abs(x) > 1e-9:
            idx = i
            break
    if idx is None:
        raise ValueError("Zero root")
    if root[idx] < 0:
        root = -root
    return tuple(root.tolist())


def build_root_lines(roots: np.ndarray) -> list[np.ndarray]:
    line_map = {}
    reps = []
    used = set()
    for i, r in enumerate(roots):
        if i in used:
            continue
        key = canonical_line(r)
        if key in line_map:
            continue
        # find -r
        neg = -r
        j = None
        for k, s in enumerate(roots):
            if np.allclose(s, neg):
                j = k
                break
        if j is None:
            raise RuntimeError("Missing neg root")
        used.add(i)
        used.add(j)
        line_map[key] = len(reps)
        reps.append(r)
    return reps


def root_type(root: np.ndarray) -> str:
    # type1: two ±1, rest 0; type2: eight ±1/2
    vals = sorted(set(np.abs(root)))
    if vals == [0.0, 1.0]:
        return "type1"
    return "type2"


def main():
    if not PARTITION_JSON.exists():
        raise SystemExit(
            "Missing artifacts/e8_rootline_partition.json; run tools/e8_rootline_partition.py"
        )
    partition = json.loads(PARTITION_JSON.read_text())
    triples = partition.get("solution_triples", [])
    if len(triples) != 40:
        raise SystemExit(f"Expected 40 triples, got {len(triples)}")

    roots = build_e8_roots()
    line_reps = build_root_lines(roots)
    if len(line_reps) != 120:
        raise SystemExit(f"Expected 120 root lines, got {len(line_reps)}")

    # classify line types
    line_types = [root_type(r) for r in line_reps]
    triple_type_counts = []
    for t in triples:
        counts = {"type1": 0, "type2": 0}
        for idx in t:
            counts[line_types[idx]] += 1
        triple_type_counts.append(counts)
    type_pattern_counts = {}
    for counts in triple_type_counts:
        key = (counts["type1"], counts["type2"])
        type_pattern_counts[key] = type_pattern_counts.get(key, 0) + 1

    # build 6-root sets for each triple
    triple_roots = []
    for t in triples:
        roots6 = []
        for idx in t:
            r = line_reps[idx]
            roots6.append(r)
            roots6.append(-r)
        triple_roots.append(np.array(roots6))

    # classify relation classes by full 6x6 inner-product counts
    relation_classes = {}
    rel_matrix = [[None] * 40 for _ in range(40)]
    for i in range(40):
        for j in range(i + 1, 40):
            A = triple_roots[i]
            B = triple_roots[j]
            # 6x6 inner products
            prod = A @ B.T
            # count values (exclude exact 2/-2 since different lines)
            counts = {
                -1: int(np.sum(np.isclose(prod, -1.0))),
                0: int(np.sum(np.isclose(prod, 0.0))),
                1: int(np.sum(np.isclose(prod, 1.0))),
            }
            key = (counts[-1], counts[0], counts[1])
            relation_classes.setdefault(key, 0)
            relation_classes[key] += 1
            rel_matrix[i][j] = key
            rel_matrix[j][i] = key

    class_keys = sorted(relation_classes.keys())

    # search unions of relation classes for SRG(40,12,2,4)
    candidates = []
    target = []
    total_subsets = 1 << len(class_keys)
    # guard: if too many classes, only test single classes and complements
    if total_subsets > MAX_CLASS_UNIONS:
        subsets = []
        for i in range(len(class_keys)):
            subsets.append({class_keys[i]})
            subsets.append(set(class_keys) - {class_keys[i]})
    else:
        subsets = []
        for mask in range(1, total_subsets):
            subset = {class_keys[i] for i in range(len(class_keys)) if (mask >> i) & 1}
            subsets.append(subset)

    for subset in subsets:
        # build adjacency
        adj = np.zeros((40, 40), dtype=int)
        for i in range(40):
            for j in range(i + 1, 40):
                if rel_matrix[i][j] in subset:
                    adj[i, j] = 1
                    adj[j, i] = 1
        degrees = adj.sum(axis=1)
        if len(set(degrees)) != 1:
            continue
        k = int(degrees[0])
        # compute lambda/mu
        lambda_set = set()
        mu_set = set()
        for i in range(40):
            for j in range(i + 1, 40):
                common = int(np.dot(adj[i], adj[j]))
                if adj[i, j] == 1:
                    lambda_set.add(common)
                else:
                    mu_set.add(common)
        if len(lambda_set) == 1 and len(mu_set) == 1:
            lam = next(iter(lambda_set))
            mu = next(iter(mu_set))
            item = {"classes": sorted(list(subset)), "k": k, "lambda": lam, "mu": mu}
            candidates.append(item)
            if k == 12 and lam == 2 and mu == 4:
                target.append(item)

    summary = {
        "relation_class_count": len(class_keys),
        "relation_classes": {str(k): relation_classes[k] for k in class_keys},
        "triple_type_distribution": {
            "type1_count_set": sorted({c["type1"] for c in triple_type_counts}),
            "type2_count_set": sorted({c["type2"] for c in triple_type_counts}),
            "pattern_counts": {
                str(k): v for k, v in sorted(type_pattern_counts.items())
            },
        },
        "candidate_count": len(candidates),
        "candidates": candidates,
        "target_srg_40_12_2_4": target,
        "subset_search_mode": (
            "full" if total_subsets <= MAX_CLASS_UNIONS else "single+complements"
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# E8 Triple-Relation Search (Full 6x6 inner products)")
    lines.append("")
    lines.append(f"- relation classes: {len(class_keys)}")
    lines.append(f"- subset search: {summary['subset_search_mode']}")
    lines.append(f"- SRG candidates: {summary['candidate_count']}")
    lines.append(f"- SRG(40,12,2,4) matches: {len(target)}")
    lines.append("")
    lines.append("## Triple type distribution (line types per triple)")
    lines.append(
        f"- type1 count set: {summary['triple_type_distribution']['type1_count_set']}"
    )
    lines.append(
        f"- type2 count set: {summary['triple_type_distribution']['type2_count_set']}"
    )
    lines.append("- pattern counts:")
    for k, v in summary["triple_type_distribution"]["pattern_counts"].items():
        lines.append(f"  - {k}: {v}")
    lines.append("")
    lines.append("## Relation classes (counts of pair occurrences)")
    for k in class_keys:
        lines.append(f"- {k}: {relation_classes[k]}")
    lines.append("")
    lines.append("## SRG(40,12,2,4) matches")
    if target:
        for item in target:
            lines.append(
                f"- classes={item['classes']} -> k={item['k']}, λ={item['lambda']}, μ={item['mu']}"
            )
    else:
        lines.append("- none")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
