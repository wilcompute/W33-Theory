#!/usr/bin/env python3
"""BT1219 -- exact SL(2,3) closure simulator.

Upgrades BT1216 from synthetic 2T metadata to exact finite matrix closure.
We enumerate SL(2,3) as 2x2 matrices over F3 with determinant 1.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import Counter

MOD = 3

Matrix = tuple[tuple[int, int], tuple[int, int]]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return (
        ((a[0][0]*b[0][0] + a[0][1]*b[1][0]) % MOD,
         (a[0][0]*b[0][1] + a[0][1]*b[1][1]) % MOD),
        ((a[1][0]*b[0][0] + a[1][1]*b[1][0]) % MOD,
         (a[1][0]*b[0][1] + a[1][1]*b[1][1]) % MOD),
    )


def det(a: Matrix) -> int:
    return (a[0][0]*a[1][1] - a[0][1]*a[1][0]) % MOD


def eye() -> Matrix:
    return ((1,0),(0,1))


def enumerate_sl23() -> list[Matrix]:
    out = []
    for a in range(MOD):
        for b in range(MOD):
            for c in range(MOD):
                for d in range(MOD):
                    m = ((a,b),(c,d))
                    if det(m) == 1:
                        out.append(m)
    return out


def order(m: Matrix) -> int:
    x = eye()
    for n in range(1, 100):
        x = matmul(x, m)
        if x == eye():
            return n
    raise RuntimeError("order search failed")


def trace_mod3(m: Matrix) -> int:
    return (m[0][0] + m[1][1]) % MOD


def closure_ok(group: list[Matrix]) -> bool:
    s = set(group)
    return all(matmul(a,b) in s for a in group for b in group)


def build_result() -> dict:
    group = enumerate_sl23()
    orders = Counter(order(m) for m in group)
    traces = Counter(trace_mod3(m) for m in group)
    result = {
        "bt": 1219,
        "title": "Exact SL(2,3) closure simulator",
        "field": "F3",
        "definition": "2x2 matrices over F3 with determinant 1",
        "order": len(group),
        "expected_order": 24,
        "order_ok": len(group) == 24,
        "closure_ok": closure_ok(group),
        "identity_count": sum(1 for m in group if m == eye()),
        "element_order_spectrum": {str(k): orders[k] for k in sorted(orders)},
        "expected_element_order_spectrum": {"1":1,"2":1,"3":8,"4":6,"6":8},
        "trace_mod3_counts": {str(k): traces[k] for k in sorted(traces)},
        "generators_candidate": {
            "S": [[0, 2], [1, 0]],
            "T": [[1, 1], [0, 1]],
            "generated_by_ST_not_checked_here": True
        },
        "recovers_bt1216_single_qutrit_target": len(group) == 24 and closure_ok(group) and {str(k): orders[k] for k in sorted(orders)} == {"1":1,"2":1,"3":8,"4":6,"6":8},
    }
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/bt1219_exact_sl23_closure.json"))
    args = p.parse_args()
    result = build_result()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1219, "order": result["order"], "closure_ok": result["closure_ok"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
