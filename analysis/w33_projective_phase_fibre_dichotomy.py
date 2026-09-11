#!/usr/bin/env python3
"""Projective phase-fibre dichotomy over the common B_288 observable group.

Both the W33 minimum-vector stabilizer and the standard non-entangling complex
Clifford group project to

    B_288 = (A4 x A4) : C2 = SmallGroup(288,1025).

The common local interior is K_288=(2T x 2T)/diag(C2), 2T=SL(2,3).
This script constructs two completions of that interior exactly:

  W33 / real completion:
      W = K : <s>, s^2=1, s(a,b)s^{-1}=(b,a), |W|=576.

  determinant-one complex Clifford completion:
      G = <K,t>, tKt^{-1}=swap(K), t^4=z, |G|=1152,
      where z is the nontrivial center of K.  Thus t has order 8 and t^2
      generates the scalar C4 center.  This is the abstract lift relation of
      the special-SWAP SU(4) representative used for C1' bowtie C1'.

The two maps to B_288 are built explicitly using the projective action
SL(2,3)/{+-I} = A4 on P^1(F3).  Their kernels are C2 and C4 respectively.
For a uniform hidden group element conditioned only on its projective image,
Shannon entropy and min-entropy are therefore exactly 1 and 2 bits.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_oriented288_binary_tetrahedral_bridge import (  # noqa: E402
    CP,
    CID,
    SL23,
    canon_pair,
    cinv,
    cmul,
    minv3,
    mmul,
)

OUT = ROOT / "data" / "w33_projective_phase_fibre_dichotomy.json"
I2 = (1, 0, 0, 1)
NEG_I2 = (2, 0, 0, 2)
ZK = canon_pair(NEG_I2, I2)


def cpswap(x):
    return canon_pair(x[1], x[0])


# W33 split swap completion, abstractly on K x C2.
WID = (CID, 0)
W = frozenset((x, e) for x in CP for e in (0, 1))


def wmul(A, B):
    x, e = A
    y, f = B
    if e:
        y = cpswap(y)
    return cmul(x, y), e ^ f


def winv(A):
    x, e = A
    xi = cinv(x)
    if e:
        xi = cpswap(xi)
    return xi, e


# Complex SU(4) completion in normal forms K t^k, 0<=k<4, with t^4=z.
GID = (CID, 0)
G = frozenset((x, k) for x in CP for k in range(4))


def gmul(A, B):
    x, k = A
    y, ell = B
    if k & 1:
        y = cpswap(y)
    x = cmul(x, y)
    total = k + ell
    if total >= 4:
        x = cmul(x, ZK)
        total -= 4
    return x, total


def ginv(A):
    x, k = A
    ell = (-k) % 4
    carry = 1 if k and k + ell >= 4 else 0
    target = cinv(x)
    if carry:
        target = cmul(target, ZK)
    if k & 1:
        target = cpswap(target)
    return target, ell


def order(x, mul, identity, bound=48):
    y = identity
    for n in range(1, bound + 1):
        y = mul(x, y)
        if y == identity:
            return n
    raise AssertionError("order bound exceeded")


def center(group, mul):
    return frozenset(x for x in group if all(mul(x, y) == mul(y, x) for y in group))


def closure(gens, mul, identity):
    group = {identity}
    queue = deque([identity])
    gens = tuple(gens)
    while queue:
        x = queue.popleft()
        for g in gens:
            y = mul(g, x)
            if y not in group:
                group.add(y)
                queue.append(y)
    return frozenset(group)


def derived(group, mul, inv, identity):
    comms = set()
    for x in group:
        xi = inv(x)
        for y in group:
            yi = inv(y)
            comms.add(mul(mul(mul(xi, yi), x), y))
    return closure(comms, mul, identity)


# Projective action of SL(2,3) on P^1(F3), giving A4.
P1 = ((1, 0), (0, 1), (1, 1), (1, 2))
P1_INDEX = {p: i for i, p in enumerate(P1)}


def canon_p1(v):
    a, b = v[0] % 3, v[1] % 3
    if a:
        s = 1 if a == 1 else 2
        return (1, (s * b) % 3)
    assert b
    return (0, 1)


def rho(m):
    return tuple(
        P1_INDEX[canon_p1(((m[0] * x + m[1] * y) % 3, (m[2] * x + m[3] * y) % 3))]
        for x, y in P1
    )


A4 = frozenset(rho(m) for m in SL23)
assert len(A4) == 12


def pcompose(p, q):
    return tuple(p[q[i]] for i in range(4))


def bmul(A, B):
    a, b, e = A
    c, d, f = B
    if e:
        c, d = d, c
    return pcompose(a, c), pcompose(b, d), e ^ f


BID = (tuple(range(4)), tuple(range(4)), 0)
B288 = frozenset((a, b, e) for a in A4 for b in A4 for e in (0, 1))
assert len(B288) == 288


def projective_pair(x):
    return rho(x[0]), rho(x[1])


def pi_w(A):
    x, e = A
    a, b = projective_pair(x)
    return a, b, e


def pi_g(A):
    x, k = A
    a, b = projective_pair(x)
    return a, b, k & 1


def quotient_by_subgroup(group, subgroup, mul):
    cosets = []
    owner = {}
    for x in group:
        if x in owner:
            continue
        C = frozenset(mul(x, h) for h in subgroup)
        j = len(cosets)
        cosets.append(C)
        for y in C:
            owner[y] = j
    return cosets, owner


def build_result():
    assert len(CP) == 288
    assert len(W) == 576 and len(G) == 1152
    assert all(wmul(x, winv(x)) == WID == wmul(winv(x), x) for x in W)
    assert all(gmul(x, ginv(x)) == GID == gmul(ginv(x), x) for x in G)

    wc = center(W, wmul)
    gc = center(G, gmul)
    wd = derived(W, wmul, winv, WID)
    gd = derived(G, gmul, ginv, GID)
    whist = dict(sorted(Counter(order(x, wmul, WID) for x in W).items()))
    ghist = dict(sorted(Counter(order(x, gmul, GID) for x in G).items()))

    assert len(wc) == 2 and len(gc) == 4
    assert len(wd) == len(gd) == 96
    assert whist == {1: 1, 2: 43, 3: 80, 4: 84, 6: 272, 12: 96}
    assert ghist == {1: 1, 2: 31, 3: 80, 4: 32, 6: 176, 8: 192, 12: 256, 24: 384}

    s = (CID, 1)
    t = (CID, 1)
    assert order(s, wmul, WID) == 2
    assert order(t, gmul, GID) == 8
    t2 = gmul(t, t)
    t4 = gmul(t2, t2)
    assert t2 in gc and order(t2, gmul, GID) == 4
    assert t4 == (ZK, 0)

    # Both completions act by the same factor exchange on K.
    assert all(wmul(wmul(s, (x, 0)), winv(s)) == (cpswap(x), 0) for x in CP)
    assert all(gmul(gmul(t, (x, 0)), ginv(t)) == (cpswap(x), 0) for x in CP)

    # Explicit common projective quotient.
    assert {pi_w(x) for x in W} == B288
    assert {pi_g(x) for x in G} == B288
    assert all(pi_w(wmul(x, y)) == bmul(pi_w(x), pi_w(y)) for x in W for y in W)
    assert all(pi_g(gmul(x, y)) == bmul(pi_g(x), pi_g(y)) for x in G for y in G)
    wker = frozenset(x for x in W if pi_w(x) == BID)
    gker = frozenset(x for x in G if pi_g(x) == BID)
    assert wker == wc and gker == gc

    # Quotienting only the conventional +/-I subgroup reproduces the separate
    # residual-C2 576-group used by the phase-completion no-go.
    pm = frozenset(((CID, 0), (ZK, 0)))
    residual_cosets, _ = quotient_by_subgroup(G, pm, gmul)
    assert len(residual_cosets) == 576

    checks = {
        "common_local_interior_K288": len(CP) == 288,
        "W33_split_completion_order576": len(W) == 576,
        "complex_special_swap_completion_order1152": len(G) == 1152,
        "W33_center_C2": len(wc) == 2,
        "complex_center_C4": len(gc) == 4 and max(order(x, gmul, GID) for x in gc) == 4,
        "both_derived_subgroups_order96": len(wd) == len(gd) == 96,
        "W33_swap_has_order2": order(s, wmul, WID) == 2,
        "complex_special_swap_has_order8": order(t, gmul, GID) == 8,
        "complex_swap_square_is_central_order4": t2 in gc and order(t2, gmul, GID) == 4,
        "complex_swap_fourth_power_is_minus_identity": t4 == (ZK, 0),
        "same_factor_exchange_action_on_K": True,
        "both_project_exactly_to_B288": {pi_w(x) for x in W} == {pi_g(x) for x in G} == B288,
        "W33_projective_kernel_equals_center": wker == wc,
        "complex_projective_kernel_equals_center": gker == gc,
        "complex_mod_plusminusI_has_order576": len(residual_cosets) == 576,
    }

    return {
        "schema": "w33.projective-phase-fibre-dichotomy.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "observable_group": {
            "name": "B_288 = (A4 x A4) : C2",
            "order": 288,
            "GAP_id": "SmallGroup(288,1025)",
            "construction": "project SL(2,3) factors onto A4 via P^1(F3), retain factor-swap parity",
        },
        "common_local_interior": {
            "name": "K_288 = (2T x 2T)/diag(C2)",
            "order": 288,
            "center_order": 2,
            "projective_local_group": "A4 x A4, order 144",
        },
        "W33_completion": {
            "order": len(W),
            "center_order": len(wc),
            "derived_order": len(wd),
            "swap_order": order(s, wmul, WID),
            "swap_square": "1",
            "element_orders": whist,
            "projective_fibre_bits_uniform": 1.0,
        },
        "complex_Clifford_completion": {
            "order": len(G),
            "center_order": len(gc),
            "derived_order": len(gd),
            "special_swap_order": order(t, gmul, GID),
            "special_swap_square": "central generator of C4",
            "special_swap_fourth_power": "-I = nontrivial center of K_288",
            "element_orders": ghist,
            "projective_fibre_bits_uniform": 2.0,
            "literature_identification": "C1' bowtie C1', SmallGroup(1152,155473), projective SmallGroup(288,1025)",
        },
        "observer_information": {
            "uniform_W33_H_shannon_given_projective": "log2(2) = 1 bit",
            "uniform_W33_H_min_entropy_given_projective": "1 bit",
            "uniform_complex_G_shannon_given_projective": "log2(4) = 2 bits",
            "uniform_complex_G_min_entropy_given_projective": "2 bits",
            "reading": (
                "The same projective observable state has different hidden phase-fibre capacity in the two completions. "
                "This is quotient information loss, not encryption and not a claim about ontic quantum randomness."
            ),
        },
        "theorem": (
            "W33 and the conventional complex non-entangling Clifford group have the same B_288 projective quotient "
            "and the same binary-tetrahedral local interior, but inequivalent factor-exchange lifts. W33 uses an honest "
            "order-two swap; the SU(4) Clifford lift uses an order-eight special swap whose square generates the C4 scalar center."
        ),
        "external_boundary": (
            "The identification of the order-1152 model with C1' bowtie C1' and its projective GAP ID is imported from "
            "Kubischta--Teixeira, arXiv:2409.14624. All finite multiplication, center, derived, quotient, order-spectrum, "
            "and entropy statements in this certificate are recomputed exactly."
        ),
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "observable": result["observable_group"]["GAP_id"],
        "W33_hidden_bits": result["W33_completion"]["projective_fibre_bits_uniform"],
        "complex_hidden_bits": result["complex_Clifford_completion"]["projective_fibre_bits_uniform"],
        "swap_orders": [result["W33_completion"]["swap_order"], result["complex_Clifford_completion"]["special_swap_order"]],
    }, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
