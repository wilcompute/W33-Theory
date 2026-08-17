#!/usr/bin/env python3
"""Passes 6541--6544: full Veldkamp-space reconstruction from the doily code.

This verifier starts from the Pass6533--6540 quadratic-evaluation code C and
checks that the 31 nonzero codewords, with binary 2-dimensional subspaces as
lines, recover the full Veldkamp space of W(3,2) ~= W(2): PG(4,2) with 31
points and 155 lines. It then recovers the exact five Veldkamp line types from
code weights plus the doily incidence geometry reconstructed by C^perp.

Scope: finite binary geometry/coding only.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "data" / "PART_W33_PASS6541_6544_DOILY_VELDKAMP_CODE_LINES.json"
BASE_PATH = HERE / "w33_pass6533_6540_doily_quadratic_evaluation_code.py"

spec = importlib.util.spec_from_file_location("doily_code_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)


def xor(u, v):
    return tuple(a ^ b for a, b in zip(u, v))


def main():
    all_a = [base.ZERO] + base.V
    C = {base.codeword(a, t) for a in all_a for t in (0, 1)}
    zero = (0,) * 15
    nonzero = sorted(C - {zero})
    assert len(nonzero) == 31

    doily_lines = set()
    for i, x in enumerate(base.V):
        for y in base.V[i + 1:]:
            if base.B(x, y) == 0:
                z = base.add(x, y)
                doily_lines.add(frozenset((base.VIDX[x], base.VIDX[y], base.VIDX[z])))
    assert len(doily_lines) == 15

    veldkamp_lines = set()
    for u, v in itertools.combinations(nonzero, 2):
        w = xor(u, v)
        assert w != zero and w in C
        veldkamp_lines.add(frozenset((u, v, w)))
    assert len(veldkamp_lines) == 155

    type_counts = Counter()
    weight_type_counts = Counter()

    for triple in veldkamp_lines:
        words = list(triple)
        weights = tuple(sorted(sum(w) for w in words))
        core = set(range(15))
        for w in words:
            core &= set(base.zeros(w))
        core = frozenset(core)

        if len(core) == 1:
            vtype = "single_point"
            assert weights == (8, 10, 10)
        elif len(core) == 5:
            vtype = "pentad"
            assert weights == (6, 6, 8)
        elif len(core) == 3 and core in doily_lines:
            vtype = "collinear_triple"
            assert weights == (8, 8, 8)
        elif len(core) == 3:
            centers = [
                p for p in range(15)
                if all(p == q or base.B(base.V[p], base.V[q]) == 0 for q in core)
            ]
            if len(centers) == 1:
                vtype = "unicentric_triad"
                assert weights == (6, 8, 10)
            elif len(centers) == 3:
                vtype = "tricentric_triad"
                assert weights == (8, 8, 8)
            else:
                raise AssertionError(("unexpected triad center count", len(centers), core))
        else:
            raise AssertionError(("unexpected Veldkamp core", len(core), weights, core))

        type_counts[vtype] += 1
        weight_type_counts[weights] += 1

    assert type_counts == Counter({
        "single_point": 15,
        "collinear_triple": 15,
        "unicentric_triad": 60,
        "tricentric_triad": 20,
        "pentad": 45,
    })
    assert weight_type_counts == Counter({
        (8, 10, 10): 15,
        (8, 8, 8): 35,
        (6, 8, 10): 60,
        (6, 6, 8): 45,
    })

    w6 = [w for w in nonzero if sum(w) == 6]
    w8 = [w for w in nonzero if sum(w) == 8]
    w10 = [w for w in nonzero if sum(w) == 10]
    pair_fusion = Counter()
    for A, B, label in ((w6, w6, "6+6"), (w10, w10, "10+10"), (w6, w10, "6+10"), (w8, w8, "8+8")):
        if A is B:
            pairs = itertools.combinations(A, 2)
        else:
            pairs = itertools.product(A, B)
        for u, v in pairs:
            pair_fusion[(label, sum(xor(u, v)))] += 1

    assert pair_fusion == Counter({
        ("6+6", 8): 45,
        ("10+10", 8): 15,
        ("6+10", 8): 60,
        ("8+8", 8): 105,
    })

    result = {
        "passes": "6541-6544",
        "object": "doily Veldkamp space reconstructed from quadratic-evaluation code",
        "projective_code_geometry": {
            "nonzero_codewords": 31,
            "vector_dimension": 5,
            "projective_space": "PG(4,2)",
            "veldkamp_lines": len(veldkamp_lines),
        },
        "veldkamp_line_types": {
            "single_point": type_counts["single_point"],
            "collinear_triple": type_counts["collinear_triple"],
            "unicentric_triad": type_counts["unicentric_triad"],
            "tricentric_triad": type_counts["tricentric_triad"],
            "pentad": type_counts["pentad"],
        },
        "weight_composition_counts": {
            "8,10,10": weight_type_counts[(8, 10, 10)],
            "8,8,8": weight_type_counts[(8, 8, 8)],
            "6,8,10": weight_type_counts[(6, 8, 10)],
            "6,6,8": weight_type_counts[(6, 6, 8)],
        },
        "all_perp_line_split": {
            "total_8,8,8": 35,
            "collinear_triple": 15,
            "tricentric_triad": 20,
            "separator": "minimum dual supports / doily-line incidence",
        },
        "fusion_laws": {
            "6+6": "8 (45 unordered pairs)",
            "10+10": "8 (15 unordered pairs)",
            "6+10": "8 (60 mixed pairs)",
            "8+8": "8 (105 unordered pairs)",
        },
        "scope": "finite binary geometry/coding only",
        "checks": "PASS",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
