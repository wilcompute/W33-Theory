#!/usr/bin/env python3
"""Localize the W33/Clifford residual C2-extension difference to the swap subgroup.

Both residual order-576 completions map onto the same projective
B_288=(A4 x A4):C2 with central kernel C2.  Globally they are non-isomorphic.
This script proves the difference is already visible on the projective factor-
swap subgroup <sbar> ~= C2:

    W33 pullback       ~= C2 x C2   (split class),
    Clifford pullback  ~= C4        (nontrivial class).

Thus the two restrictions represent the two elements of H^2(C2,C2)=C2.
The statement is finite group cohomology language for an explicitly enumerated
four-element preimage, not a physical phase claim by itself.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_projective_phase_fibre_dichotomy import (  # noqa: E402
    BID, B288, CID, G, GID, W, WID, ZK,
    bmul, gmul, order, pi_g, pi_w, quotient_by_subgroup, wmul,
)

OUT = ROOT / "data" / "w33_swap_extension_class_localization.json"


def quotient_mul(cosets, owner, mul, i, j):
    x = next(iter(cosets[i]))
    y = next(iter(cosets[j]))
    return owner[mul(x, y)]


def element_order_q(cosets, owner, mul, idx):
    e = owner[next(x for x in cosets[owner[next(iter(cosets[0]))]] if False)] if False else None
    # identity is the coset containing the ambient identity, supplied by caller via owner.
    raise RuntimeError("unused")


def build_result():
    # Projective swap subgroup in B288.
    swap_b = (BID[0], BID[1], 1)
    swap_subgroup = {BID, swap_b}
    assert bmul(swap_b, swap_b) == BID

    # W33 split extension pullback: exactly four elements over {1,sbar}.
    Wpull = frozenset(x for x in W if pi_w(x) in swap_subgroup)
    assert len(Wpull) == 4
    Whist = Counter(order(x, wmul, WID) for x in Wpull)
    assert Whist == {1: 1, 2: 3}

    # Complex group G has central C4. Quotient by +/-I to obtain the residual
    # order-576 central C2 extension of B288.
    pm = frozenset(((CID, 0), (ZK, 0)))
    cosets, owner = quotient_by_subgroup(G, pm, gmul)
    assert len(cosets) == 576
    qid = owner[GID]

    # The quotient map to B288 is constant on +/-I cosets.
    qpi = {}
    for i, C in enumerate(cosets):
        images = {pi_g(x) for x in C}
        assert len(images) == 1
        qpi[i] = next(iter(images))
    Cpull = frozenset(i for i in range(len(cosets)) if qpi[i] in swap_subgroup)
    assert len(Cpull) == 4

    def qmul(i, j):
        x = next(iter(cosets[i])); y = next(iter(cosets[j]))
        return owner[gmul(x, y)]

    def qorder(i):
        x = qid
        for n in range(1, 9):
            x = qmul(i, x)
            if x == qid:
                return n
        raise AssertionError("quotient order bound")

    Chist = Counter(qorder(i) for i in Cpull)
    assert Chist == {1: 1, 2: 1, 4: 2}

    # Kernel element and lift-square witness in the residual quotient.
    qker = frozenset(i for i in range(len(cosets)) if qpi[i] == BID)
    assert len(qker) == 2
    zq = next(i for i in qker if i != qid)
    swap_lifts = [i for i in Cpull if qpi[i] == swap_b]
    assert len(swap_lifts) == 2
    assert all(qmul(i, i) == zq for i in swap_lifts)

    checks = {
        "common_projective_swap_is_C2": len(swap_subgroup) == 2,
        "W33_pullback_has_order4": len(Wpull) == 4,
        "W33_pullback_is_V4": Whist == {1: 1, 2: 3},
        "Clifford_residual_quotient_has_order576": len(cosets) == 576,
        "Clifford_pullback_has_order4": len(Cpull) == 4,
        "Clifford_pullback_is_C4": Chist == {1: 1, 2: 1, 4: 2},
        "Clifford_swap_lift_squares_to_kernel": all(qmul(i, i) == zq for i in swap_lifts),
    }

    return {
        "schema": "w33.swap-extension-class-localization.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "base_subgroup": "projective factor swap C2 < B_288",
        "W33_restriction": {
            "preimage_order": 4,
            "structure": "C2 x C2",
            "element_orders": dict(sorted(Whist.items())),
            "extension_class": "split / zero class in H^2(C2,C2)",
        },
        "Clifford_residual_restriction": {
            "preimage_order": 4,
            "structure": "C4",
            "element_orders": dict(sorted(Chist.items())),
            "extension_class": "non-split / nonzero class in H^2(C2,C2)",
            "lift_square": "every lift of the nontrivial projective swap squares to the nontrivial central kernel element",
        },
        "theorem": (
            "The inequivalence of the W33 and residual complex-Clifford C2 phase completions of B_288 is already detected on the factor-swap subgroup: its pullback is V4 for W33 and C4 for the Clifford residual lift."
        ),
        "boundary": (
            "H^2(C2,C2)=C2 is used only to name the two explicitly enumerated central extension classes. No continuum or ontic-randomness conclusion is inferred."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": r["status"], "W33": r["W33_restriction"]["structure"], "Clifford": r["Clifford_residual_restriction"]["structure"]}, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
