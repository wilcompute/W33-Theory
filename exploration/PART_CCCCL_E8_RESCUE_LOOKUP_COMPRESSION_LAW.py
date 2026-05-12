#!/usr/bin/env python3
"""
PART CCCCL -- E8 Rescue Lookup Compression Law
==============================================

After CCCCXLVII established exact class-wise rescue constants by dot-class,
this part compresses the computation to a closed-form lookup.

For doubled E8 roots a,b with d = a·b in {-8,-4,0,4,8}:

  R(a,b) = 240, if d = 0
           234, if |d| = 4
           126, if |d| = 8

where R(a,b) is the number of third references c producing a
24/108/108-feasible triple partition.

This converts rescue evaluation from expensive triple-class counting to a
constant-time invariant lookup on d=a·b.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXL_E8_TWO_REFERENCE_PARTITION_NOGO import (  # noqa: E402
    _build_e8_roots_doubled,
    _can_partition_24_108_108,
    _dot,
)
from PART_CCCCXLII_THIRD_REFERENCE_REFINEMENT_WITNESS import (  # noqa: E402
    _triple_class_counts,
)


def rescue_lookup_from_dot(d: int) -> int:
    if d == 0:
        return 240
    if abs(d) == 4:
        return 234
    if abs(d) == 8:
        return 126
    raise ValueError(f"Unexpected dot class: {d}")


def _triple_feasible_c_count(
    roots: List[Tuple[int, ...]], pair: Tuple[int, int]
) -> int:
    i, j = pair
    a, b = roots[i], roots[j]
    cnt = 0
    for c in roots:
        if _can_partition_24_108_108(_triple_class_counts(roots, a, b, c)):
            cnt += 1
    return cnt


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _run() -> Dict[str, object]:
    roots = _build_e8_roots_doubled()
    n = len(roots)

    pairs_by_dot: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            pairs_by_dot[_dot(roots[i], roots[j])].append((i, j))

    expected_hist = {-8: 120, -4: 6720, 0: 15120, 4: 6720, 8: 240}
    observed_hist = {d: len(pairs_by_dot[d]) for d in sorted(pairs_by_dot)}

    # Canonical representatives (one per dot class).
    canonical_reps = {
        -8: (0, 239),
        -4: (0, 150),
        0: (0, 13),
        4: (0, 1),
        8: (0, 0),
    }

    canonical_direct = {d: _triple_feasible_c_count(roots, p) for d, p in canonical_reps.items()}
    canonical_lookup = {d: rescue_lookup_from_dot(d) for d in canonical_reps}

    # Deterministic direct-check sample: first 20 pairs in each dot class.
    sample_size = 20
    sampled_mismatch = []
    sampled_summary = {}
    for d in sorted(pairs_by_dot):
        sample = pairs_by_dot[d][: min(sample_size, len(pairs_by_dot[d]))]
        vals = []
        for p in sample:
            direct = _triple_feasible_c_count(roots, p)
            vals.append(direct)
            if direct != rescue_lookup_from_dot(d):
                sampled_mismatch.append((d, list(p), direct, rescue_lookup_from_dot(d)))
        sampled_summary[str(d)] = {
            "sample_size": len(sample),
            "direct_min": min(vals),
            "direct_max": max(vals),
            "lookup": rescue_lookup_from_dot(d),
        }

    # Weighted totals from lookup across all pairs.
    weighted_total = sum(observed_hist[d] * rescue_lookup_from_dot(d) for d in observed_hist)

    _ck("E8 roots count = 240", n == 240)
    _ck("Dot histogram exact", observed_hist == expected_hist)
    _ck("Lookup dot classes exactly {±8, ±4, 0}", sorted(observed_hist.keys()) == [-8, -4, 0, 4, 8])
    _ck("Canonical representatives match lookup", canonical_direct == canonical_lookup)
    _ck("Deterministic sampled direct checks match lookup", len(sampled_mismatch) == 0)
    _ck("Lookup constants are 126/234/240", sorted({rescue_lookup_from_dot(d) for d in observed_hist}) == [126, 234, 240])
    _ck("Weighted total rescue count is positive", weighted_total > 0)

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCL",
        "title": "E8 Rescue Lookup Compression Law",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "dot_histogram": {str(k): v for k, v in sorted(observed_hist.items())},
        "canonical_representatives": {str(d): list(p) for d, p in canonical_reps.items()},
        "canonical_direct": {str(d): v for d, v in sorted(canonical_direct.items())},
        "canonical_lookup": {str(d): v for d, v in sorted(canonical_lookup.items())},
        "sampled_summary": sampled_summary,
        "sampled_mismatches": sampled_mismatch,
        "lookup_map": {"abs(d)=8": 126, "abs(d)=4": 234, "d=0": 240},
        "weighted_rescue_total": weighted_total,
        "theorem_statement": (
            "R(a,b), the third-reference rescue count, is a function only of d=a·b: "
            "R=126 for |d|=8, R=234 for |d|=4, and R=240 for d=0."
        ),
        "honesty_boundary": (
            "This part certifies the closed-form lookup with canonical and deterministic "
            "direct checks, not a full brute-force all-pairs direct recomputation."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCL_e8_rescue_lookup_compression_law_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== E8 RESCUE LOOKUP COMPRESSION LAW ===")
    print(f"dot histogram: {results['dot_histogram']}")
    print(f"lookup map: {results['lookup_map']}")
    print(f"weighted rescue total: {results['weighted_rescue_total']}")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
