#!/usr/bin/env python3
"""
PART CCCCXLIII -- Third-Reference Rescue-Profile Stratification (Deterministic Sample)
=======================================================================================

Builds on CCCCXLI (two-reference signature strata) and CCCCXLII (representative
rescue counts) by computing a deterministic first-12 sample per signature family.

For each two-reference signature family:
  - take the first 12 unordered pairs (a,b) in canonical enumeration order,
  - compute the number of third references c (out of 240) that make the
    3-reference tuple-class partition 24/108/108-feasible,
  - record the sampled rescue profile.

Observed deterministic profiles:
  signature [1,1,56,56,126]                          -> 126 (all 12 samples)
  signature [1,1,1,1,1,1,27,27,27,27,27,27,72]      -> 234 (all 12 samples)
  signature [1,1,1,1,12,12,12,12,32,32,32,32,60]    -> 240 (all 12 samples)

This gives a quantitative sampled stratification of third-reference rescue power.
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
    _pair_class_counts,
)


SAMPLE_PER_SIGNATURE = 12


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


def _feasible_c_count(roots: List[Tuple[int, ...]], pair: Tuple[int, int]) -> int:
    i, j = pair
    a, b = roots[i], roots[j]
    count = 0
    for c in roots:
        if _can_partition_24_108_108(_triple_class_counts(roots, a, b, c)):
            count += 1
    return count


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _run() -> Dict[str, object]:
    roots = _build_e8_roots_doubled()
    n = len(roots)

    # Group all unordered pairs by two-reference signature (including diagonal),
    # consistent with CCCCXL / CCCCXLI conventions.
    by_signature: Dict[Tuple[int, ...], List[Tuple[int, int]]] = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            sig = tuple(_pair_class_counts(roots, roots[i], roots[j]))
            by_signature[sig].append((i, j))

    signatures_sorted = sorted(by_signature.keys(), key=lambda s: (len(s), s))
    profile_payload = []

    observed_constant_counts = []
    for sig in signatures_sorted:
        pairs = by_signature[sig]
        sample_pairs = pairs[: min(SAMPLE_PER_SIGNATURE, len(pairs))]
        sample_counts = [_feasible_c_count(roots, pair) for pair in sample_pairs]
        unique_counts = sorted(set(sample_counts))

        if len(unique_counts) == 1:
            observed_constant_counts.append(unique_counts[0])

        profile_payload.append(
            {
                "signature": list(sig),
                "pair_count": len(pairs),
                "sample_size": len(sample_pairs),
                "sample_counts": sample_counts,
                "sample_unique_counts": unique_counts,
            }
        )

    # Expected deterministic witness from probe and CCCCXLII representatives.
    expected_signature_counts = sorted([360, 13440, 15120])
    observed_signature_counts = sorted(len(by_signature[sig]) for sig in signatures_sorted)
    expected_sample_constants = sorted([126, 234, 240])

    _ck("E8 root count = 240", n == 240)
    _ck("Exactly three two-reference signatures", len(signatures_sorted) == 3)
    _ck("Signature multiplicities = 360/13440/15120", observed_signature_counts == expected_signature_counts)
    _ck("Each signature contributes 12 sampled pairs", all(p["sample_size"] == 12 for p in profile_payload))
    _ck("Each sampled profile is constant within signature", all(len(p["sample_unique_counts"]) == 1 for p in profile_payload))
    _ck("Sampled constants are exactly 126/234/240", sorted(observed_constant_counts) == expected_sample_constants)

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCXLIII",
        "title": "Third-Reference Rescue-Profile Stratification (Deterministic Sample)",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "sample_per_signature": SAMPLE_PER_SIGNATURE,
        "profiles": profile_payload,
        "key_observations": [
            "All three two-reference signatures show constant rescue counts on first-12 deterministic samples.",
            "Sample constants are exactly 126, 234, and 240.",
            "The sampled rescue profile increases strictly across the three strata.",
        ],
        "honesty_boundary": (
            "This part certifies deterministic sampled stratification, not full all-pairs third-reference "
            "classification."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCXLIII_third_reference_rescue_profile_stratification_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== THIRD-REFERENCE RESCUE PROFILE STRATIFICATION (SAMPLED) ===")
    for profile in results["profiles"]:
        uniq = profile["sample_unique_counts"]
        print(f"signature size={profile['pair_count']:5d}  sampled unique rescue counts={uniq}")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
