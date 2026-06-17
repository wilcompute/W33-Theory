#!/usr/bin/env python3
"""BT1228 -- compressed Sp(4,3) generator certificate.

BT1221 generated Sp(4,3) using all 40 unique transvections.  BT1228 shows that
a concrete 4-transvection set already generates the full order-51840 group.
This is a compressed generator certificate, not a proof that four is minimal.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import deque

MOD = 3
I = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
J = (0,0,1,0, 0,0,0,1, 2,0,0,0, 0,2,0,0)
GENERATOR_VECTORS = [(0,0,0,2), (0,2,0,0), (0,0,2,2), (1,0,0,0)]
EXPECTED_ORDER = 51840


def mm(a, b):
    a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15 = a
    b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15 = b
    return (
        (a0*b0+a1*b4+a2*b8+a3*b12)%3,(a0*b1+a1*b5+a2*b9+a3*b13)%3,(a0*b2+a1*b6+a2*b10+a3*b14)%3,(a0*b3+a1*b7+a2*b11+a3*b15)%3,
        (a4*b0+a5*b4+a6*b8+a7*b12)%3,(a4*b1+a5*b5+a6*b9+a7*b13)%3,(a4*b2+a5*b6+a6*b10+a7*b14)%3,(a4*b3+a5*b7+a6*b11+a7*b15)%3,
        (a8*b0+a9*b4+a10*b8+a11*b12)%3,(a8*b1+a9*b5+a10*b9+a11*b13)%3,(a8*b2+a9*b6+a10*b10+a11*b14)%3,(a8*b3+a9*b7+a10*b11+a11*b15)%3,
        (a12*b0+a13*b4+a14*b8+a15*b12)%3,(a12*b1+a13*b5+a14*b9+a15*b13)%3,(a12*b2+a13*b6+a14*b10+a15*b14)%3,(a12*b3+a13*b7+a14*b11+a15*b15)%3)


def transvection(v):
    a,b,c,d = v
    w = (c % 3, d % 3, (2*a) % 3, (2*b) % 3)
    vals = []
    for vi in v:
        for wj in w:
            vals.append((vi * wj) % 3)
    return tuple((I[i] + vals[i]) % 3 for i in range(16))


def generate(gens):
    group = {I}
    q = deque([I])
    while q:
        x = q.popleft()
        for g in gens:
            y = mm(x, g)
            if y not in group:
                group.add(y)
                q.append(y)
    return group


def build_result() -> dict:
    gens = [transvection(v) for v in GENERATOR_VECTORS]
    group = generate(gens)
    return {
        "bt": 1228,
        "title": "Compressed Sp43 generator certificate",
        "field": "F3",
        "dimension": 4,
        "generator_vectors": [list(v) for v in GENERATOR_VECTORS],
        "generator_count": len(gens),
        "previous_transvection_count": 40,
        "generated_order": len(group),
        "expected_order": EXPECTED_ORDER,
        "order_ok": len(group) == EXPECTED_ORDER,
        "compression_ratio": "4/40",
        "minimality_claim": false,
        "interpretation": "A concrete four-transvection set generates the full Sp43 target. This makes the two-qutrit finite gate target more implementable without claiming four is minimal.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/bt1228_sp43_compressed_generators.json"))
    args = parser.parse_args()
    result = build_result()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1228, "order_ok": result["order_ok"], "generated_order": result["generated_order"]}, indent=2))


if __name__ == "__main__":
    main()
