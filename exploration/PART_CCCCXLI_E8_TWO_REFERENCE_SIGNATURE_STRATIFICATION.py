#!/usr/bin/env python3
"""
PART CCCCXLI -- E8 Two-Reference Signature Stratification
=========================================================

Builds directly on CCCCXL.

Goal:
  Classify all unordered two-reference pairs (a,b) over doubled E8 roots by
  their tuple-class count signature for (r·a, r·b), and record exact
  multiplicities plus 24/108/108 feasibility status.

Main certified output:
  - exactly 3 signature families,
  - pair multiplicities 360, 13440, 15120,
  - exactly one feasible family (the 15120 family).

This converts the qualitative "degenerate" statement into a quantitative
stratification theorem for the two-reference ansatz.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXL_E8_TWO_REFERENCE_PARTITION_NOGO import (  # noqa: E402
    _build_e8_roots_doubled,
    _can_partition_24_108_108,
    _pair_class_counts,
)


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _run() -> Dict[str, object]:
    roots = _build_e8_roots_doubled()
    n = len(roots)
    total_pairs = n * (n + 1) // 2

    signature_counts: Dict[Tuple[int, ...], int] = defaultdict(int)
    signature_feasible: Dict[Tuple[int, ...], bool] = {}

    for i in range(n):
        a = roots[i]
        for j in range(i, n):
            b = roots[j]
            sig = tuple(_pair_class_counts(roots, a, b))
            signature_counts[sig] += 1
            if sig not in signature_feasible:
                signature_feasible[sig] = _can_partition_24_108_108(list(sig))

    signatures_sorted = sorted(
        signature_counts.items(), key=lambda kv: (len(kv[0]), kv[0])
    )
    feasible_signatures = [sig for sig, ok in signature_feasible.items() if ok]
    feasible_pair_count = sum(signature_counts[s] for s in feasible_signatures)

    # Exact multiplicities discovered in CCCCXL and re-certified here.
    expected_multiplicities = sorted([360, 13440, 15120])
    observed_multiplicities = sorted(signature_counts.values())

    _ck("E8 root count = 240", n == 240)
    _ck("Total unordered pairs (with diagonal) = 28920", total_pairs == 28920)
    _ck("Exactly three two-reference signature families", len(signature_counts) == 3)
    _ck("Observed multiplicities match 360/13440/15120", observed_multiplicities == expected_multiplicities)
    _ck("Exactly one feasible signature family", len(feasible_signatures) == 1)
    _ck("Feasible pair count = 15120", feasible_pair_count == 15120)
    _ck("Signature counts sum to 28920", sum(signature_counts.values()) == total_pairs)

    verified = all(ok for _, ok in checks)

    signatures_payload = []
    for sig, count in signatures_sorted:
        signatures_payload.append(
            {
                "signature": list(sig),
                "pair_count": count,
                "feasible_24_108_108": bool(signature_feasible[sig]),
            }
        )

    return {
        "part": "CCCCXLI",
        "title": "E8 Two-Reference Signature Stratification",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "search": {
            "roots": n,
            "pairs_including_diagonal": total_pairs,
            "distinct_signatures": len(signature_counts),
            "feasible_signatures": len(feasible_signatures),
            "feasible_pairs": feasible_pair_count,
        },
        "signature_families": signatures_payload,
        "key_observations": [
            "The two-reference ansatz has exactly three signature strata.",
            "Their exact multiplicities are 360, 13440, and 15120.",
            "Only one stratum is 24/108/108-feasible, with size 15120.",
            "Hence degeneracy is structured, not arbitrary.",
        ],
        "honesty_boundary": (
            "This part classifies two-reference strata exactly but does not yet provide "
            "a unique constructive edge↔root operator dictionary."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCXLI_e8_two_reference_signature_stratification_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== E8 TWO-REFERENCE SIGNATURE STRATIFICATION ===")
    print(f"pairs:       {results['search']['pairs_including_diagonal']}")
    print(f"signatures:  {results['search']['distinct_signatures']}")
    print(f"feasible:    {results['search']['feasible_pairs']} pairs in {results['search']['feasible_signatures']} family")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
