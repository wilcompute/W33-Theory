#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path

MOD = 3
SP43_ORDER = 51840
I4 = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)


def mm(a, b):
    return tuple(sum(a[4*i+k] * b[4*k+j] for k in range(4)) % MOD for i in range(4) for j in range(4))


def projective_vectors():
    out, seen = [], set()
    for v in product(range(MOD), repeat=4):
        if v == (0,0,0,0):
            continue
        vv = list(v)
        first = next(x for x in vv if x)
        if first == 2:
            vv = [(2*x) % MOD for x in vv]
        key = tuple(vv)
        if key not in seen:
            seen.add(key)
            out.append(key)
    assert len(out) == 40
    return out


def tv(v):
    a,b,c,d = v
    jv = (c % MOD, d % MOD, (-a) % MOD, (-b) % MOD)
    outer = [(vi * wj) % MOD for vi in v for wj in jv]
    return tuple((I4[i] + outer[i]) % MOD for i in range(16))


def closure_order(gens):
    group = {I4}
    q = deque([I4])
    while q:
        x = q.popleft()
        for g in gens:
            y = mm(x, g)
            if y not in group:
                group.add(y)
                q.append(y)
    return len(group)


def build():
    vecs = projective_vectors()
    mats = [tv(v) for v in vecs]
    assert len(set(mats)) == 40
    one = Counter(closure_order([m]) for m in mats)
    two = Counter()
    examples = {}
    for i, j in combinations(range(40), 2):
        o = closure_order([mats[i], mats[j]])
        two[o] += 1
        examples.setdefault(o, [list(vecs[i]), list(vecs[j])])
    return {
        "bt": 1230,
        "title": "Sp43 pair-bound certificate",
        "field": "F3",
        "dimension": 4,
        "projective_transvections": 40,
        "expected_sp43_order": SP43_ORDER,
        "single_order_histogram": {str(k): v for k, v in sorted(one.items())},
        "pair_order_histogram": {str(k): v for k, v in sorted(two.items())},
        "max_single_order": max(one),
        "max_pair_order": max(two),
        "pair_examples": {str(k): v for k, v in sorted(examples.items())},
        "one_or_two_transvections_reach_full_order": max(max(one), max(two)) == SP43_ORDER,
        "lower_bound_transvections_at_least": 3,
        "bt1228_four_transvection_certificate_compatible": True,
        "three_transvection_case_resolved": False,
        "minimality_claim": False,
        "interpretation": "All single closures have order 3, and all pair closures have order 9 or 24. Thus BT1228's four-transvection certificate cannot be improved to one or two transvections; the remaining exact-minimality gap is the three-transvection case."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1230_sp43_pair_bound_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1230, "max_pair_order": result["max_pair_order"], "out": str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
