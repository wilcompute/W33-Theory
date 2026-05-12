#!/usr/bin/env python3
"""
PART CCCCLI -- E8 Rescue Distribution and Generating-Function Law
=================================================================

Builds on CCCCL (closed-form rescue lookup from d=a·b) and computes the exact
global distribution of rescue counts R(a,b) over all unordered pairs (a,b),
including diagonal.

Exact distribution:
  R=126 : 360 pairs
  R=234 : 13440 pairs
  R=240 : 15120 pairs

So the counting generating function is:
  P(t) = 360 t^126 + 13440 t^234 + 15120 t^240

and the normalized probability generating function is:
  G(t) = P(t) / 28920.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCL_E8_RESCUE_LOOKUP_COMPRESSION_LAW import (  # noqa: E402
    rescue_lookup_from_dot,
)
from PART_CCCCXL_E8_TWO_REFERENCE_PARTITION_NOGO import (  # noqa: E402
    _build_e8_roots_doubled,
    _dot,
)


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _fraction_payload(x: Fraction) -> Dict[str, int | float]:
    return {
        "numerator": x.numerator,
        "denominator": x.denominator,
        "float": float(x),
    }


def _run() -> Dict[str, object]:
    roots = _build_e8_roots_doubled()
    n = len(roots)

    counts_by_rescue = {126: 0, 234: 0, 240: 0}
    counts_by_dot = {-8: 0, -4: 0, 0: 0, 4: 0, 8: 0}

    for i in range(n):
        for j in range(i, n):
            d = _dot(roots[i], roots[j])
            counts_by_dot[d] = counts_by_dot.get(d, 0) + 1
            r = rescue_lookup_from_dot(d)
            counts_by_rescue[r] = counts_by_rescue.get(r, 0) + 1

    total_pairs = sum(counts_by_rescue.values())
    weighted_total = sum(r * c for r, c in counts_by_rescue.items())

    # Exact moment data using rational arithmetic.
    m1 = Fraction(weighted_total, total_pairs)
    m2 = Fraction(sum(c * (r**2) for r, c in counts_by_rescue.items()), total_pairs)
    m3 = Fraction(sum(c * (r**3) for r, c in counts_by_rescue.items()), total_pairs)
    var = m2 - m1 * m1
    mu3 = Fraction(
        sum(c * (r * total_pairs - weighted_total) ** 3 for r, c in counts_by_rescue.items()),
        total_pairs**4,
    )

    expected_dot = {-8: 120, -4: 6720, 0: 15120, 4: 6720, 8: 240}
    expected_rescue = {126: 360, 234: 13440, 240: 15120}

    _ck("E8 roots count = 240", n == 240)
    _ck("Total unordered pairs = 28920", total_pairs == 28920)
    _ck("Dot histogram matches exact classes", counts_by_dot == expected_dot)
    _ck("Rescue distribution is exactly 360/13440/15120", counts_by_rescue == expected_rescue)
    _ck("Weighted rescue total = 6819120", weighted_total == 6819120)
    _ck("Mean rescue is between 234 and 240", Fraction(234, 1) < m1 < Fraction(240, 1))
    _ck("Variance is strictly positive", var > 0)
    _ck("Third central moment is finite", isinstance(mu3, Fraction))

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCLI",
        "title": "E8 Rescue Distribution and Generating-Function Law",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "pair_count": total_pairs,
        "dot_histogram": {str(k): v for k, v in sorted(counts_by_dot.items())},
        "rescue_distribution": {str(k): v for k, v in sorted(counts_by_rescue.items())},
        "counting_generating_polynomial": "P(t)=360 t^126 + 13440 t^234 + 15120 t^240",
        "probability_generating_function": "G(t)=P(t)/28920",
        "weighted_rescue_total": weighted_total,
        "moments": {
            "raw_m1": _fraction_payload(m1),
            "raw_m2": _fraction_payload(m2),
            "raw_m3": _fraction_payload(m3),
            "variance": _fraction_payload(var),
            "central_mu3": _fraction_payload(mu3),
        },
        "theorem_statement": (
            "The all-pairs rescue distribution is exactly triatomic: 126 (360 pairs), "
            "234 (13440 pairs), and 240 (15120 pairs), hence P(t)=360 t^126 + "
            "13440 t^234 + 15120 t^240."
        ),
        "honesty_boundary": (
            "This part is a global distributional corollary of the exact dot-class lookup law (CCCCL), "
            "not an independent structural derivation of that lookup."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCLI_e8_rescue_distribution_mgf_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== E8 RESCUE DISTRIBUTION + MGF LAW ===")
    print(f"distribution: {results['rescue_distribution']}")
    print(f"P(t): {results['counting_generating_polynomial']}")
    print(f"weighted total: {results['weighted_rescue_total']}")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
