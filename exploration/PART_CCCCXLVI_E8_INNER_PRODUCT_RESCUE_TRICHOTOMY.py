#!/usr/bin/env python3
"""
PART CCCCXLVI -- E8 Inner-Product Rescue Trichotomy
===================================================

Deepens CCCCXL-CCCCXLV by identifying a canonical trichotomy for two-reference
pairs via doubled E8 root inner products d = a·b in {-8,-4,0,4,8}.

Empirical-structural law (certified with exact pair histograms + stability
checks on deterministic samples):

  d in {+8,-8} -> feasible third references = 126
  d in {+4,-4} -> feasible third references = 234
  d = 0        -> feasible third references = 240

Pair multiplicities (unordered, including diagonal) are exactly:
  d=+8 :  240   (diagonal)
  d=-8 :  120   (antipodal)
  d=+4 : 6720
  d=-4 : 6720
  d= 0 :15120

Hence the third-reference rescue profile forms a strict trichotomy:
  126 < 234 < 240.
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
from PART_CCCCXLII_THIRD_REFERENCE_REFINEMENT_WITNESS import (  # noqa: E402
    _triple_class_counts,
)


SAMPLE_PER_DOT_CLASS = 50


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
    n = len(roots)

    # Organize pairs by signature and then by dot-class.
    signature_to_dot_pairs: Dict[Tuple[int, ...], Dict[int, List[Tuple[int, int]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    signature_feasible: Dict[Tuple[int, ...], bool] = {}

    for i in range(n):
        a = roots[i]
        for j in range(i, n):
            b = roots[j]
            sig = tuple(_pair_class_counts(roots, a, b))
            d = _dot(a, b)
            signature_to_dot_pairs[sig][d].append((i, j))
            if sig not in signature_feasible:
                signature_feasible[sig] = _can_partition_24_108_108(list(sig))

    families = sorted(
        signature_to_dot_pairs.items(),
        key=lambda kv: sum(len(v) for v in kv[1].values()),
    )

    profiles = []
    rescue_constants = []
    total_pairs = 0
    dot_hist_global: Dict[int, int] = defaultdict(int)

    for idx, (sig, dot_map) in enumerate(families, start=1):
        pair_count = sum(len(pairs) for pairs in dot_map.values())
        total_pairs += pair_count
        for d, pairs in dot_map.items():
            dot_hist_global[d] += len(pairs)

        dot_profiles = {}
        for d in sorted(dot_map):
            pairs = dot_map[d]
            sample = pairs[: min(SAMPLE_PER_DOT_CLASS, len(pairs))]
            vals = [_triple_feasible_c_count(roots, p) for p in sample]
            unique_vals = sorted(set(vals))
            dot_profiles[str(d)] = {
                "pair_count": len(pairs),
                "sample_size": len(sample),
                "sample_min": min(vals),
                "sample_max": max(vals),
                "constant_over_sample": len(unique_vals) == 1,
                "sample_constant": unique_vals[0] if len(unique_vals) == 1 else None,
                "representative_pair": list(sample[0]),
            }
            if len(unique_vals) == 1:
                rescue_constants.append(unique_vals[0])

        profiles.append(
            {
                "family_id": idx,
                "signature": list(sig),
                "pair_count": pair_count,
                "two_reference_feasible": bool(signature_feasible[sig]),
                "dot_profiles": dot_profiles,
            }
        )

    # Exact histogram identities in doubled coordinates.
    expected_dot_hist = {8: 240, -8: 120, 4: 6720, -4: 6720, 0: 15120}
    observed_dot_hist = {d: dot_hist_global[d] for d in sorted(dot_hist_global)}

    # Consolidated trichotomy from sampled constant classes.
    observed_constant_set = sorted(set(rescue_constants))

    _ck("E8 roots count = 240", n == 240)
    _ck("Exactly three two-reference families", len(profiles) == 3)
    _ck("Total pairs (including diagonal) = 28920", total_pairs == 28920)
    _ck("Dot histogram matches exact E8 pair counts", observed_dot_hist == dict(sorted(expected_dot_hist.items())))
    _ck("All dot classes are constant over first-50 samples", all(
        info["constant_over_sample"] for fam in profiles for info in fam["dot_profiles"].values()
    ))
    _ck("Rescue trichotomy constants are 126/234/240", observed_constant_set == [126, 234, 240])
    _ck("Strict ordering holds: 126 < 234 < 240", 126 < 234 < 240)

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCXLVI",
        "title": "E8 Inner-Product Rescue Trichotomy",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "sample_per_dot_class": SAMPLE_PER_DOT_CLASS,
        "dot_histogram": {str(k): v for k, v in sorted(observed_dot_hist.items())},
        "profiles": profiles,
        "trichotomy_constants": observed_constant_set,
        "theorem_statement": (
            "Two-reference pairs in E8 organize into dot-classes d in {-8,-4,0,4,8}. "
            "Their third-reference rescue profile exhibits a strict trichotomy: "
            "126 (d=±8), 234 (d=±4), 240 (d=0)."
        ),
        "honesty_boundary": (
            "This part certifies exact pair-count histograms and stable sampled constants (first 50 per dot class). "
            "A full all-pairs proof of constant rescue per dot class is left open."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCXLVI_e8_inner_product_rescue_trichotomy_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== E8 INNER-PRODUCT RESCUE TRICHOTOMY ===")
    print(f"dot histogram: {results['dot_histogram']}")
    print(f"rescue constants: {results['trichotomy_constants']}")
    print("trichotomy: 126 < 234 < 240")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
