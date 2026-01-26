#!/usr/bin/env python3
"""Search relations between E8 orthogonal-triple blocks that yield SRG(40,12,2,4).

We take one partition of the 120 E8 root lines into 40 triples of mutually
orthogonal lines (from artifacts/e8_rootline_partition.json), then define
relations between triples based on how many orthogonal line-pairs they have.

We test all unions of relation-count classes for regularity and SRG params.

Outputs:
- artifacts/e8_triple_relation_search.json
- artifacts/e8_triple_relation_search.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PARTITION_JSON = ROOT / "artifacts" / "e8_rootline_partition.json"
OUT_JSON = ROOT / "artifacts" / "e8_triple_relation_search.json"
OUT_MD = ROOT / "artifacts" / "e8_triple_relation_search.md"


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


def orthogonal(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(float(np.dot(a, b))) < 1e-9


def main():
    if not PARTITION_JSON.exists():
        raise SystemExit("Missing artifacts/e8_rootline_partition.json; run tools/e8_rootline_partition.py")
    partition = json.loads(PARTITION_JSON.read_text())
    if not partition.get("solution_triples"):
        raise SystemExit("Partition file has no solution_triples")

    triples = partition["solution_triples"]
    if len(triples) != 40:
        raise SystemExit(f"Expected 40 triples, got {len(triples)}")

    roots = build_e8_roots()
    line_reps = build_root_lines(roots)
    if len(line_reps) != 120:
        raise SystemExit(f"Expected 120 root lines, got {len(line_reps)}")

    # compute orthogonality matrix on root lines
    n_lines = len(line_reps)
    ortho = np.zeros((n_lines, n_lines), dtype=bool)
    for i in range(n_lines):
        for j in range(i + 1, n_lines):
            if orthogonal(line_reps[i], line_reps[j]):
                ortho[i, j] = True
                ortho[j, i] = True

    # compute relation counts between triples
    num_triples = len(triples)
    rel_counts = np.zeros((num_triples, num_triples), dtype=int)
    for i in range(num_triples):
        A = triples[i]
        for j in range(i + 1, num_triples):
            B = triples[j]
            count = 0
            for a in A:
                for b in B:
                    if ortho[a, b]:
                        count += 1
            rel_counts[i, j] = count
            rel_counts[j, i] = count

    counts_set = sorted(set(int(rel_counts[i, j]) for i in range(num_triples) for j in range(i + 1, num_triples)))

    # test all unions of count-classes
    candidates = []
    for mask in range(1, 1 << len(counts_set)):
        selected = [counts_set[i] for i in range(len(counts_set)) if (mask >> i) & 1]
        # build adjacency
        adj = np.zeros((num_triples, num_triples), dtype=int)
        for i in range(num_triples):
            for j in range(i + 1, num_triples):
                if rel_counts[i, j] in selected:
                    adj[i, j] = 1
                    adj[j, i] = 1
        degrees = adj.sum(axis=1)
        if len(set(degrees)) != 1:
            continue
        k = int(degrees[0])
        # compute lambda/mu
        lambda_set = set()
        mu_set = set()
        for i in range(num_triples):
            for j in range(i + 1, num_triples):
                common = int(np.dot(adj[i], adj[j]))
                if adj[i, j] == 1:
                    lambda_set.add(common)
                else:
                    mu_set.add(common)
        if len(lambda_set) == 1 and len(mu_set) == 1:
            lam = next(iter(lambda_set))
            mu = next(iter(mu_set))
            candidates.append({
                "counts": selected,
                "k": k,
                "lambda": lam,
                "mu": mu,
            })

    # sort candidates by k
    candidates = sorted(candidates, key=lambda x: (x["k"], x["counts"]))
    target = [c for c in candidates if c["k"] == 12 and c["lambda"] == 2 and c["mu"] == 4]

    summary = {
        "counts_set": counts_set,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "target_srg_40_12_2_4": target,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# E8 Triple-Relation Search (40 blocks)")
    lines.append("")
    lines.append(f"- relation count classes: {counts_set}")
    lines.append(f"- regular SRG candidates found: {len(candidates)}")
    lines.append("")
    lines.append("## Candidates")
    for c in candidates:
        lines.append(f"- counts={c['counts']} -> k={c['k']}, λ={c['lambda']}, μ={c['mu']}")
    lines.append("")
    lines.append("## SRG(40,12,2,4) Matches")
    if target:
        for c in target:
            lines.append(f"- counts={c['counts']} -> k={c['k']}, λ={c['lambda']}, μ={c['mu']}")
    else:
        lines.append("- none")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
