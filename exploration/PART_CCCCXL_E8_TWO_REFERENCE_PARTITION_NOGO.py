#!/usr/bin/env python3
"""
PART CCCCXL -- E8 Two-Reference Non-Uniqueness Witness
======================================================

Context:
  CCCCXXXVIII gives the exact count-level bridge 240 = 24+108+108.
  CCCCXXXIX proves no one-threshold E8 root graph matches L(W33).

This part probes the next natural constructive ansatz:

  Choose one or two E8 reference roots (a,b),
  classify each root r by tuple (r·a, r·b),
  then try to partition tuple classes into blocks of sizes 24,108,108.

Result:
    Exhaustive search over all unordered pairs (a,b), including a=b,
    finds MANY such partitions (15120 pairs).

Interpretation:
    Two-reference tuple-class grouping is too permissive: it does not uniquely
    select the W33-side packet bridge. Any future dictionary must add extra
    structure to remove this massive degeneracy.
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def _build_e8_roots_doubled() -> List[Tuple[int, ...]]:
    roots: List[Tuple[int, ...]] = []

    # Type A: (±2, ±2, 0,...,0)  -> 112 roots
    for i, j in combinations(range(8), 2):
        for s1, s2 in product((-2, 2), repeat=2):
            vec = [0] * 8
            vec[i] = s1
            vec[j] = s2
            roots.append(tuple(vec))

    # Type B: (±1,...,±1) with even number of minuses -> 128 roots
    for signs in product((-1, 1), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(tuple(signs))

    roots = sorted(set(roots))
    if len(roots) != 240:
        raise ValueError(f"Expected 240 E8 roots, got {len(roots)}")
    return roots


def _dot(u: Tuple[int, ...], v: Tuple[int, ...]) -> int:
    return int(sum(a * b for a, b in zip(u, v)))


def _can_partition_24_108_108(class_counts: List[int]) -> bool:
    """
    Decide whether class-count bins can be assigned to three groups A/B/C with
    totals (24,108,108), order-fixed for DP as (A,B) and C as remainder.
    """
    if sum(class_counts) != 240:
        return False

    states = {(0, 0)}
    for count in class_counts:
        next_states = set(states)
        for a, b in states:
            if a + count <= 24:
                next_states.add((a + count, b))
            if b + count <= 108:
                next_states.add((a, b + count))
        states = next_states
    return (24, 108) in states


def _pair_class_counts(
    roots: List[Tuple[int, ...]], a: Tuple[int, ...], b: Tuple[int, ...]
) -> List[int]:
    counts: Dict[Tuple[int, int], int] = {}
    for r in roots:
        key = (_dot(r, a), _dot(r, b))
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.values())


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _run() -> Dict[str, object]:
    roots = _build_e8_roots_doubled()
    norms = {_dot(r, r) for r in roots}

    n = len(roots)
    # Unordered pairs including diagonal a=b.
    total_pairs = n * (n + 1) // 2

    signatures_checked: Dict[Tuple[int, ...], bool] = {}
    hits: List[Tuple[int, int]] = []

    for i in range(n):
        a = roots[i]
        for j in range(i, n):
            b = roots[j]
            signature = tuple(_pair_class_counts(roots, a, b))
            if signature not in signatures_checked:
                signatures_checked[signature] = _can_partition_24_108_108(list(signature))
            if signatures_checked[signature]:
                hits.append((i, j))

    _ck("E8 root count = 240", n == 240)
    _ck("All doubled norms are 8", norms == {8})
    _ck("Total unordered pairs with diagonal = 28920", total_pairs == 28920)
    _ck("At least one signature examined", len(signatures_checked) > 0)
    feasible_signatures = sum(1 for ok in signatures_checked.values() if ok)

    _ck("Two-reference family has feasible 24/108/108 partitions", len(hits) > 0)
    _ck("Feasible set is non-unique (strict subset of all pairs)", 0 < len(hits) < total_pairs)
    _ck("Exactly one feasible signature class appears", feasible_signatures == 1)
    _ck("Exhaustive hit count = 15120", len(hits) == 15120)

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCXL",
        "title": "E8 Two-Reference Non-Uniqueness Witness",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "search": {
            "roots": n,
            "pairs_including_diagonal": total_pairs,
            "distinct_signatures": len(signatures_checked),
            "feasible_signatures": feasible_signatures,
            "hits": len(hits),
        },
        "key_observations": [
            "Exhaustive pair search completed over all 28,920 unordered (a,b), including a=b.",
            "A 24/108/108 split exists for 15,120 pairs in this two-reference family.",
            "So two-reference class assignment is too permissive, not uniquely selecting the bridge.",
            "Count-level bridge 240=240 remains intact from earlier parts.",
        ],
        "honesty_boundary": (
            "This part proves non-uniqueness (degeneracy) in two-reference tuple-class "
            "construction. It does not yet construct the unique operator-level dictionary."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCXL_e8_two_reference_partition_nogo_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== E8 TWO-REFERENCE NON-UNIQUENESS WITNESS ===")
    print(f"Pairs searched (including diagonal): {results['search']['pairs_including_diagonal']}")
    print(f"Distinct class-count signatures:     {results['search']['distinct_signatures']}")
    print(f"Feasible signatures:                {results['search']['feasible_signatures']}")
    print(f"Feasible pairs for 24/108/108:      {results['search']['hits']}")
    print("Result: two-reference family is degenerate (non-unique selector).")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
