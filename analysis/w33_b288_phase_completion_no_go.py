#!/usr/bin/env python3
"""Exact phase-completion comparison over the common projective group B_288.

Repo input:
  H_W33 has order 576, center C2, derived order 96, and
  H_W33/Z(H_W33) ~= A4 wr C2 = SmallGroup(288,1025).

External classification input (Kubischta--Teixeira, arXiv:2409.14624):
  the primitive non-entangling group C1' bowtie C1' has total order 1152,
  projective group SmallGroup(288,1025), and sigma lift notation, i.e. the
  displayed SU(4) lift has scalar center C4.

Quotienting that C4 lift by its unique order-two scalar subgroup gives an
abstract order-576 central extension of B_288. The quotient can be constructed
without matrix numerics as

    G_Cliff,576 = (A4 x A4) : C4,

where the generator of C4 acts by swapping the two A4 factors. Its square is
the residual central phase. This script enumerates that group exactly and
proves it is NOT isomorphic to the W33 lift by derived order and element-order
spectrum.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_b288_phase_completion_no_go.json"
W33_CERT = ROOT / "data" / "PART_W33_20260828_MINIMUM_STABILIZER_576_STRUCTURE.json"


def compose(p, q):
    return tuple(p[q[i]] for i in range(4))


def inverse(p):
    out = [0] * 4
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def parity(p):
    return sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2


S4 = tuple(itertools.permutations(range(4)))
A4 = tuple(p for p in S4 if parity(p) == 0)
E4 = tuple(range(4))
ID = (E4, E4, 0)


def mul(x, y):
    a, b, k = x
    c, d, ell = y
    if k % 2:
        c, d = d, c
    return (compose(a, c), compose(b, d), (k + ell) % 4)


def invg(x):
    a, b, k = x
    ai, bi = inverse(a), inverse(b)
    if k % 2:
        ai, bi = bi, ai
    return (ai, bi, (-k) % 4)


def order(x):
    y = ID
    for n in range(1, 49):
        y = mul(x, y)
        if y == ID:
            return n
    raise AssertionError("order bound exceeded")


def closure(gens):
    gens = tuple(gens)
    group = {ID}
    queue = deque([ID])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = mul(g, x)
            if y not in group:
                group.add(y)
                queue.append(y)
    return group


def derived(group):
    comms = set()
    for x in group:
        xi = invg(x)
        for y in group:
            yi = invg(y)
            comms.add(mul(mul(mul(xi, yi), x), y))
    return closure(comms)


def build():
    group = {(a, b, k) for a in A4 for b in A4 for k in range(4)}
    assert len(group) == 576
    assert all(mul(x, invg(x)) == ID == mul(invg(x), x) for x in group)

    center = [x for x in group if all(mul(x, y) == mul(y, x) for y in group)]
    dg = derived(group)
    hist = dict(sorted(Counter(order(x) for x in group).items()))
    assert len(center) == 2
    assert len(dg) == 48
    assert hist == {1: 1, 2: 31, 3: 80, 4: 96, 6: 176, 12: 192}

    w33 = json.loads(W33_CERT.read_text(encoding="utf-8"))["unsignedStabilizer"]
    w33_hist = {int(k): int(v) for k, v in w33["elementOrderCensus"].items()}
    assert w33["order"] == 576
    assert w33["centerOrder"] == 2
    assert w33["derivedOrder"] == 96
    assert w33_hist == {1: 1, 2: 43, 3: 80, 4: 84, 6: 272, 12: 96}

    z = next(x for x in center if x != ID)
    assert z == (E4, E4, 2)
    quotient = {(a, b, k % 2) for a, b, k in group}
    assert len(quotient) == 288

    checks = {
        "complex_intermediate_order_576": len(group) == 576,
        "complex_intermediate_center_C2": len(center) == 2,
        "complex_intermediate_derived_order_48": len(dg) == 48,
        "complex_intermediate_spectrum_exact": hist == {1: 1, 2: 31, 3: 80, 4: 96, 6: 176, 12: 192},
        "residual_central_square_is_k_equals_2": z == (E4, E4, 2),
        "common_projective_quotient_order_288": len(quotient) == 288,
        "w33_lift_center_C2": w33["centerOrder"] == 2,
        "w33_lift_derived_order_96": w33["derivedOrder"] == 96,
        "w33_and_complex_C2_lifts_are_nonisomorphic": len(dg) != w33["derivedOrder"] and hist != w33_hist,
    }

    return {
        "schema": "w33.b288-phase-completion-no-go.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "common_projective_group": {
            "name": "A4 wr C2 = (A4 x A4) : C2",
            "order": 288,
            "GAP_id": "SmallGroup(288,1025)",
        },
        "w33_C2_lift": {
            "order": 576,
            "center_order": w33["centerOrder"],
            "derived_order": w33["derivedOrder"],
            "element_orders": w33_hist,
            "structure": w33["structure"],
        },
        "complex_Clifford_C4_lift_literature_input": {
            "group": "C1' bowtie C1'",
            "total_order": 1152,
            "projective_order": 288,
            "projective_GAP_id": "SmallGroup(288,1025)",
            "full_GAP_id": "SmallGroup(1152,155473)",
            "lift_symbol": "sigma",
            "scalar_center_order": 4,
            "source": "Kubischta--Teixeira, Classification of the Subgroups of the Two-Qubit Clifford Group, arXiv:2409.14624, Table II / Appendix E",
        },
        "complex_residual_C2_quotient": {
            "construction": "(A4 x A4) : C4 with C4 acting through factor swap",
            "order": len(group),
            "center_order": len(center),
            "derived_order": len(dg),
            "element_orders": hist,
            "quotient_by_center_order": len(quotient),
        },
        "theorem": (
            "The W33 order-576 central C2 lift and the residual C2 quotient of the standard "
            "complex Clifford C4 lift have the same projective quotient B_288 but are nonisomorphic. "
            "Therefore the W33 phase bit is not obtained by simply discarding half of the conventional "
            "Clifford C4 scalar phase."
        ),
        "boundary": (
            "The C4 Clifford-lift identification is imported from the cited classification. The order-576 "
            "intermediate quotient is reconstructed abstractly and checked exactly here. This is a finite "
            "group-extension theorem, not evidence that global quantum phase is observable."
        ),
        "checks": checks,
    }


def main():
    result = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "common_projective": result["common_projective_group"]["GAP_id"],
        "w33_derived": result["w33_C2_lift"]["derived_order"],
        "clifford_residual_derived": result["complex_residual_C2_quotient"]["derived_order"],
    }, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
