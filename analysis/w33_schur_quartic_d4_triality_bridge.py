#!/usr/bin/env python3
"""Bridge the W33 order-576 minimum stabilizer to the 2026 Schur-quartic line configuration.

External input (Hohn, arXiv:2607.10090): one 24-line half of the Schur quartic's
48 lines of the second kind is modeled by the 24 roots of D4; its 32 triple
points are the unordered root triples r1+r2+r3=0; the projective stabilizer of
the half is W(D4):C3 with C3 acting by even triality.

Repo computation: reconstruct W(F4) independently, reconstruct W(D4) as even
signed coordinate permutations, and prove that adjoining an order-3 triality
element produces exactly the same root-parity order-576 subgroup already
explicitly identified with the W33 PSp(4,3) minimum-vector stabilizer.

This closes an abstract group/action bridge onto the Schur 24-line carrier. It
does not identify the 45 W33 minimum-vector lines with the 24 Schur lines.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_threeway_576_provenance_closure import (  # noqa: E402
    compose, generated_group, porder, wf4_and_kernels,
)

OUT = ROOT / "data" / "w33_schur_quartic_d4_triality_bridge.json"


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def f4_roots():
    roots = []
    for i in range(4):
        for s in (-1, 1):
            v = [0] * 4; v[i] = 2 * s; roots.append(tuple(v))
    roots.extend(itertools.product((-1, 1), repeat=4))
    for i in range(4):
        for j in range(i + 1, 4):
            for a in (-1, 1):
                for b in (-1, 1):
                    v = [0] * 4; v[i] = 2 * a; v[j] = 2 * b; roots.append(tuple(v))
    roots = tuple(sorted(set(roots)))
    assert len(roots) == 48
    return roots


def signed_perm_action(roots, perm, signs):
    idx = {v: i for i, v in enumerate(roots)}
    return tuple(idx[tuple(signs[i] * v[perm[i]] for i in range(4))] for v in roots)


def wd4_group(roots):
    out = set()
    for perm in itertools.permutations(range(4)):
        for signs in itertools.product((-1, 1), repeat=4):
            prod = 1
            for s in signs: prod *= s
            if prod == 1:
                out.add(signed_perm_action(roots, perm, signs))
    assert len(out) == 192
    return out


def schur_incidence(roots):
    d4 = tuple(r for r in roots if dot(r, r) == 8)
    assert len(d4) == 24
    triples = set()
    for T in itertools.combinations(d4, 3):
        if all(sum(r[k] for r in T) == 0 for k in range(4)):
            triples.add(tuple(sorted(T)))
    triples = tuple(sorted(triples))
    assert len(triples) == 32
    deg = Counter(r for T in triples for r in T)
    assert set(deg.values()) == {4} and len(deg) == 24
    return d4, triples


def restrict_perm(roots, subset, p):
    idx = {r: i for i, r in enumerate(subset)}
    root_index = {r: i for i, r in enumerate(roots)}
    return tuple(idx[roots[p[root_index[r]]]] for r in subset)


def build_result():
    roots = f4_roots()
    _wf4, longk, shortk, rotk, _auto = wf4_and_kernels()
    WD4 = wd4_group(roots)
    d4, triples = schur_incidence(roots)

    candidates = []
    for name, K in (("long-root parity", longk), ("short-root parity", shortk), ("rotation parity", rotk)):
        if WD4 <= K:
            candidates.append((name, K))
    assert len(candidates) == 1
    kernel_name, K576 = candidates[0]

    trialities = [g for g in K576 - WD4 if porder(g) == 3]
    assert trialities
    tau = trialities[0]
    closure = generated_group(tuple(WD4) + (tau,), 48)
    assert closure == K576 and len(closure) == 576

    d4_index = {r: i for i, r in enumerate(d4)}
    triple_sets = {frozenset(d4_index[r] for r in T) for T in triples}
    action24 = {restrict_perm(roots, d4, g) for g in K576}
    assert len(action24) == 576
    assert all(
        {frozenset(p[i] for i in T) for T in triple_sets} == triple_sets
        for p in action24
    )

    order_hist = dict(sorted(Counter(porder(g) for g in K576).items()))
    expected = {1: 1, 2: 43, 3: 80, 4: 84, 6: 272, 12: 96}
    assert order_hist == expected

    checks = {
        "D4_root_shell_has_24_roots": len(d4) == 24,
        "zero_sum_triples_are_32": len(triples) == 32,
        "incidence_is_24_4_32_3": len(d4) == 24 and len(triples) == 32 and all(sum(r in T for T in triples) == 4 for r in d4),
        "WD4_even_signed_permutations_order192": len(WD4) == 192,
        "WD4_lies_in_unique_F4_index2_kernel": len(candidates) == 1,
        "order3_even_triality_closes_to_576": len(closure) == 576,
        "triality_closure_equals_root_parity_kernel": closure == K576,
        "faithful_24_root_action_order576": len(action24) == 576,
        "24_root_action_preserves_all_32_triples": True,
        "spectrum_matches_W33_minimum_stabilizer": order_hist == expected,
    }

    return {
        "schema": "w33.schur-quartic-d4-triality-bridge.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "external_input": {
            "paper": "Gerald Hohn, Automorphisms of a (24_4,32_3)-configuration on the Schur quartic, arXiv:2607.10090 (2026)",
            "claims_used": [
                "24 lines are labeled by the 24 D4 roots",
                "32 triple points are unordered zero-sum root triples",
                "half-stabilizer is W(D4):C3 with even triality",
            ],
        },
        "configuration": {
            "line_roots": len(d4),
            "triple_points": len(triples),
            "line_degree": 4,
            "triple_degree": 3,
        },
        "group_bridge": {
            "WD4_order": len(WD4),
            "triality_order": porder(tau),
            "closure_order": len(closure),
            "F4_kernel_name_in_declared_simple-root_gauge": kernel_name,
            "element_orders": order_hist,
            "W33_identification": "the companion three-way provenance certificate gives an explicit isomorphism from the W33 minimum-vector stabilizer to this root-parity F4 kernel",
        },
        "theorem": (
            "The 2026 Schur-quartic half-stabilizer W(D4):C3 is realized internally as the same F4 root-parity order-576 group already explicitly isomorphic to the W33 PSp(4,3) minimum-vector stabilizer; its faithful 24-root action preserves the exact (24_4,32_3) zero-sum incidence configuration."
        ),
        "boundary": (
            "This is an abstract group plus 24-root-action bridge. It does not supply a canonical W33 45-minimum to Schur 24-line bijection, and it imports the algebro-geometric identification of the root model with actual Schur lines from arXiv:2607.10090."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": r["status"], "group": r["group_bridge"]["closure_order"], "lines": r["configuration"]["line_roots"], "triples": r["configuration"]["triple_points"]}, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
