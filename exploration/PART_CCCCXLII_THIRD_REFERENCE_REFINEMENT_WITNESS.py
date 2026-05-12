#!/usr/bin/env python3
"""
PART CCCCXLII -- Third-Reference Refinement Witness
===================================================

This part sharpens the two-reference program (CCCCXL/CCCCXLI) with two facts:

1) Refinement monotonicity (structural lemma)
   If a two-reference tuple-class partition realizes 24/108/108, then adding a
   third reference c (refining classes from (r·a,r·b) to (r·a,r·b,r·c)) cannot
   destroy feasibility: each refined class inherits its parent block.

2) Rescue witnesses (computational)
   Third-reference refinement can also create feasibility for some pairs that
   are infeasible at two-reference level.

Certified representative counts:
  - feasible pair (0,13):   240/240 choices of c keep feasibility.
  - infeasible pair (0,1):  234/240 choices of c rescue feasibility.
  - infeasible pair (0,239):126/240 choices of c rescue feasibility.

So third-reference data is strictly stronger than two-reference data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXL_E8_TWO_REFERENCE_PARTITION_NOGO import (  # noqa: E402
    _build_e8_roots_doubled,
    _can_partition_24_108_108,
    _dot,
    _pair_class_counts,
)


def _triple_class_counts(
    roots: List[Tuple[int, ...]],
    a: Tuple[int, ...],
    b: Tuple[int, ...],
    c: Tuple[int, ...],
) -> List[int]:
    counts: Dict[Tuple[int, int, int], int] = {}
    for r in roots:
        key = (_dot(r, a), _dot(r, b), _dot(r, c))
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.values())


def _triple_feasible_c_count(
    roots: List[Tuple[int, ...]], pair: Tuple[int, int]
) -> int:
    i, j = pair
    a = roots[i]
    b = roots[j]
    count = 0
    for c in roots:
        triple_sig = _triple_class_counts(roots, a, b, c)
        if _can_partition_24_108_108(triple_sig):
            count += 1
    return count


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _run() -> Dict[str, object]:
    roots = _build_e8_roots_doubled()

    # Canonical representatives discovered in prior parts/probes.
    pair_feasible = (0, 13)
    pair_infeasible_A = (0, 1)
    pair_infeasible_B = (0, 239)

    sig_feasible = _pair_class_counts(roots, roots[pair_feasible[0]], roots[pair_feasible[1]])
    sig_infeasible_A = _pair_class_counts(roots, roots[pair_infeasible_A[0]], roots[pair_infeasible_A[1]])
    sig_infeasible_B = _pair_class_counts(roots, roots[pair_infeasible_B[0]], roots[pair_infeasible_B[1]])

    two_ref_feasible = _can_partition_24_108_108(sig_feasible)
    two_ref_infeasible_A = _can_partition_24_108_108(sig_infeasible_A)
    two_ref_infeasible_B = _can_partition_24_108_108(sig_infeasible_B)

    c_count_feasible = _triple_feasible_c_count(roots, pair_feasible)
    c_count_infeasible_A = _triple_feasible_c_count(roots, pair_infeasible_A)
    c_count_infeasible_B = _triple_feasible_c_count(roots, pair_infeasible_B)

    _ck("E8 roots count = 240", len(roots) == 240)
    _ck("pair (0,13) is two-reference feasible", two_ref_feasible is True)
    _ck("pair (0,1) is two-reference infeasible", two_ref_infeasible_A is False)
    _ck("pair (0,239) is two-reference infeasible", two_ref_infeasible_B is False)

    _ck("feasible pair keeps feasibility for all 240 choices of c", c_count_feasible == 240)
    _ck("infeasible pair (0,1) rescued for 234 choices of c", c_count_infeasible_A == 234)
    _ck("infeasible pair (0,239) rescued for 126 choices of c", c_count_infeasible_B == 126)

    _ck("rescue counts are strict (0 < count < 240)", 0 < c_count_infeasible_A < 240 and 0 < c_count_infeasible_B < 240)

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCXLII",
        "title": "Third-Reference Refinement Witness",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "representatives": {
            "feasible_pair": {
                "pair": list(pair_feasible),
                "two_reference_feasible": two_ref_feasible,
                "feasible_c_count": c_count_feasible,
            },
            "infeasible_pair_A": {
                "pair": list(pair_infeasible_A),
                "two_reference_feasible": two_ref_infeasible_A,
                "feasible_c_count": c_count_infeasible_A,
            },
            "infeasible_pair_B": {
                "pair": list(pair_infeasible_B),
                "two_reference_feasible": two_ref_infeasible_B,
                "feasible_c_count": c_count_infeasible_B,
            },
        },
        "key_observations": [
            "Third-reference refinement preserves all feasible structure for the canonical feasible pair (0,13).",
            "Third-reference refinement rescues large portions of infeasible pairs: 234 and 126 choices out of 240.",
            "Hence third-reference data strictly refines two-reference classification power.",
        ],
        "honesty_boundary": (
            "This part gives representative certified rescue counts and a structural monotonicity lemma. "
            "A full all-pairs third-reference stratification remains open."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCXLII_third_reference_refinement_witness_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== THIRD-REFERENCE REFINEMENT WITNESS ===")
    print(f"feasible pair (0,13):   {results['representatives']['feasible_pair']['feasible_c_count']}/240")
    print(f"infeasible pair (0,1):  {results['representatives']['infeasible_pair_A']['feasible_c_count']}/240")
    print(f"infeasible pair (0,239):{results['representatives']['infeasible_pair_B']['feasible_c_count']}/240")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
