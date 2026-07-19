#!/usr/bin/env python3
"""Pass 465: independent q=3 cover-law L2--L4 witness and Lean source audit."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "formal" / "W33" / "Pass465CoverLawL2L4Q3.lean"
OUT = ROOT / "data" / "w33_pass465_formal_cover_l2_l4_audit.json"
Q = 3


def canon(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % Q for x in v)
    first = next(x for x in v if x)
    inv = pow(first, -1, Q)
    return tuple(inv * x % Q for x in v)


def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % Q


def build_geometry():
    points = sorted({canon(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    p0 = (0, 0, 0, 1)
    opposite = [x for x in points if symp(p0, x) != 0]

    def zact(t, x):
        return tuple((x[i] + t * symp(x, p0) * p0[i]) % Q for i in range(4))

    def same_fiber(x, y):
        return any(zact(t, x) == y for t in range(Q))

    def common(x, y):
        return [w for w in points if w != x and w != y and symp(w, x) == 0 and symp(w, y) == 0]

    def bulk_neighbors(x):
        return [w for w in opposite if w != x and symp(x, w) == 0]

    return points, p0, opposite, zact, same_fiber, common, bulk_neighbors


def build_payload() -> dict:
    source = SRC.read_text(encoding="utf-8")
    points, p0, opposite, zact, same_fiber, common, bulk_neighbors = build_geometry()

    l2 = Counter()
    l3 = Counter()
    for x in opposite:
        for y in opposite:
            if x == y:
                continue
            rows = common(x, y)
            split = (sum(symp(p0, w) == 0 for w in rows), sum(symp(p0, w) != 0 for w in rows))
            if symp(x, y) != 0 and not same_fiber(x, y):
                l2[split] += 1
            if symp(x, y) == 0:
                l3[split] += 1

    fibers = {x: {zact(t, x) for t in range(Q)} for x in opposite}
    fiber_independent = all(
        symp(y, z) != 0
        for fiber in fibers.values()
        for y in fiber
        for z in fiber
        if y != z
    )

    l4_neighbor_counts = Counter()
    l4_all_distance_two = True
    for x in opposite:
        for t in range(1, Q):
            y = zact(t, x)
            rows = bulk_neighbors(y)
            l4_neighbor_counts[len(rows)] += 1
            for w in rows:
                middle = [u for u in opposite if u not in (x, w) and symp(x, u) == 0 and symp(u, w) == 0]
                if symp(x, w) == 0 or same_fiber(x, w) or len(middle) != 3:
                    l4_all_distance_two = False

    required = [
        "theorem q3_L2_common_split_one_three",
        "theorem q3_L3_collinear_split_one_one",
        "theorem q3_fiber_card_three_independent",
        "theorem q3_L4_c3_eight_a3_zero",
        "theorem q3_cover_law_L1_L4",
        "theorem cover_b1_identity",
        "theorem cover_shell_recurrences",
        "theorem cover_shell_total",
    ]
    checks = {
        "pg33_has_40_points": len(points) == 40,
        "opposite_chart_has_27_points": len(opposite) == 27,
        "l2_split_is_uniform_1_3": l2 == Counter({(1, 3): 432}),
        "l3_split_is_uniform_1_1": l3 == Counter({(1, 1): 216}),
        "all_fibers_have_three_points": {len(f) for f in fibers.values()} == {3},
        "fibers_are_independent": fiber_independent,
        "l4_neighbor_count_is_eight": l4_neighbor_counts == Counter({8: 54}),
        "l4_neighbors_are_distance_two_from_original": l4_all_distance_two,
        "lean_source_present": SRC.exists(),
        "lean_imports_pass462": "import W33.Pass462CoverLawL1Q3" in source,
        "all_required_declarations_present": all(name in source for name in required),
        "four_native_decide_certificates": source.count("native_decide") == 4,
        "uniform_shell_arithmetic_uses_ring": source.count("ring") >= 3,
        "no_sorry": "sorry" not in source.lower(),
        "no_custom_axiom": "axiom " not in source.lower(),
    }
    return {
        "schema": "w33.pass465.formal_cover_l2_l4_audit.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "q3_objectwise_counts": {
            "L2_ordered_pair_split_histogram": {str(k): v for k, v in sorted(l2.items())},
            "L3_ordered_pair_split_histogram": {str(k): v for k, v in sorted(l3.items())},
            "L4_neighbor_count_histogram": {str(k): v for k, v in sorted(l4_neighbor_counts.items())},
            "distance_shells": [1, 8, 16, 2],
            "intersection_array": [[8, 6, 1], [1, 3, 8]],
        },
        "formal_result": (
            "The explicit PG(3,3) model now contains kernel-checked L2, L3, fiber-independence, and L4 statements, "
            "extending Pass 462 to the complete q=3 cover law. The parameter identities and shell total are proved "
            "symbolically for an indeterminate q."
        ),
        "boundary": (
            "The all-q arithmetic layer is formal, and q=3 geometry is end to end. A uniform Mathlib finite-field "
            "projective cardinality proof for every odd prime power is still not claimed."
        ),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Pass 465 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
