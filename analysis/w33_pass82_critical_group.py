#!/usr/bin/env python3
"""
Pass 82 -- The critical group (sandpile group) separates the cospectral pair W(3,3) / Q(4,3).

Passes 76/77 showed W(3,3) and its dual GQ Q(4,3) are cospectral, LOCALLY IDENTICAL, yet
non-isomorphic SRG(40,12,2,4) graphs, separated geometrically by the ovoid number (alpha 7 vs 10).
This pass adds an ALGEBRAIC separator.

The critical group (sandpile group / graph Jacobian) K(G) = Z^n / im(L), L = kI - A the Laplacian,
is a finite abelian group of order = the number of spanning trees.  Cospectral graphs share |K|
(same Laplacian spectrum => same spanning-tree count) but their critical-group ISOMORPHISM TYPE
can differ.  From the Smith normal form of the two Laplacians (GAP, w33_pass82_critical_group.g):

  K(W(3,3)) = (Z/10)^8  (+) Z/40 (+) (Z/160)^14
  K(Q(4,3)) = (Z/2)^6 (+) (Z/10)^8 (+) Z/40 (+) (Z/80)^6 (+) (Z/160)^8

Both have order 2^81 * 5^23 (matching the Pass 74 spanning-tree count), and identical 5-parts
(Z/5)^23, but DIFFERENT 2-Sylow subgroups -- so the critical group separates the pair, in the
2-primary part.  This is a new, non-spectral, non-geometric (purely algebraic) invariant closing
the same cospectral gap as the ovoid number.

ASCII-only.  critical group / sandpile / Laplacian Smith form: 0 hits in the paper and the Pass
73-81 spine (new).
"""
from __future__ import annotations

import json
import re
from collections import Counter
from math import prod
from pathlib import Path

GAP_OUT = Path("w33_pass82_critical_group_out.txt")


def read_gap():
    if not GAP_OUT.exists():
        return None
    txt = GAP_OUT.read_text()

    def grab_list(key):
        m = re.search(rf"{key}=\[(.*?)\]", txt)
        return [int(x) for x in re.findall(r"-?\d+", m.group(1))] if m else []

    return {"smith_W": grab_list("smith_W"), "smith_Q": grab_list("smith_Q")}


def factor_2_5(n):
    """Return (a, b) with n = 2^a * 5^b (n is a 2,5-number here)."""
    a = b = 0
    while n % 2 == 0:
        n //= 2
        a += 1
    while n % 5 == 0:
        n //= 5
        b += 1
    assert n == 1, f"{n} is not a 2,5-number"
    return a, b


def critical_group(smith):
    """Invariant factors > 1 (drop the 1s and the single 0) -> Z/d summands."""
    factors = [d for d in smith if d > 1]
    order = prod(factors)
    hist = Counter(factors)
    # primary (p-Sylow) decomposition
    p2 = Counter()
    p5 = Counter()
    for d, mult in hist.items():
        a, b = factor_2_5(d)
        if a:
            p2[2**a] += mult
        if b:
            p5[5**b] += mult
    a_tot, b_tot = factor_2_5(order)
    return {
        "invariant_factors": dict(sorted(hist.items())),
        "num_nontrivial_factors": len(factors),
        "order": order,
        "order_factored": f"2^{a_tot} * 5^{b_tot}",
        "sylow_2": {str(k): v for k, v in sorted(p2.items())},
        "sylow_5": {str(k): v for k, v in sorted(p5.items())},
        "structure": " (+) ".join(
            f"(Z/{d})^{m}" if m > 1 else f"Z/{d}" for d, m in sorted(hist.items())
        ),
    }


def main():
    gap = read_gap()
    if gap is None:
        print("[pass82] missing GAP certificate w33_pass82_critical_group_out.txt")
        return 2

    KW = critical_group(gap["smith_W"])
    KQ = critical_group(gap["smith_Q"])

    same_order = KW["order"] == KQ["order"]
    order_is_2811_523 = KW["order"] == (2**81) * (5**23)
    same_5part = KW["sylow_5"] == KQ["sylow_5"]
    different_2part = KW["sylow_2"] != KQ["sylow_2"]
    groups_differ = KW["invariant_factors"] != KQ["invariant_factors"]
    separates = same_order and groups_differ

    checks = {
        "orders_equal_cospectral": same_order,
        "order_is_2^81_5^23_spanning_trees": order_is_2811_523,
        "critical_groups_non_isomorphic": groups_differ,
        "same_5_Sylow": same_5part,
        "different_2_Sylow": different_2part,
        "critical_group_separates_cospectral_pair": separates,
    }
    all_ok = all(checks.values())

    print("=" * 74)
    print("PASS 82 -- CRITICAL GROUP SEPARATES THE COSPECTRAL PAIR W(3,3) / Q(4,3)")
    print("=" * 74)
    print(f"[W(3,3)] K = {KW['structure']}")
    print(
        f"         order = {KW['order_factored']}; 2-Sylow {KW['sylow_2']}; 5-Sylow {KW['sylow_5']}"
    )
    print(f"[Q(4,3)] K = {KQ['structure']}")
    print(
        f"         order = {KQ['order_factored']}; 2-Sylow {KQ['sylow_2']}; 5-Sylow {KQ['sylow_5']}"
    )
    print()
    print(f"same order (cospectral => same spanning trees): {same_order}")
    print(f"order = 2^81 * 5^23 (Pass 74 spanning-tree count): {order_is_2811_523}")
    print(f"5-Sylows identical: {same_5part};  2-Sylows differ: {different_2part}")
    print(
        f"=> critical group SEPARATES the cospectral, locally identical pair: {separates}"
    )
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 74)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 74)

    payload = {
        "schema": "w33.pass82.critical_group.v1",
        "status": "PASS" if all_ok else "FAIL",
        "critical_group_W33": KW,
        "critical_group_Q43": KQ,
        "separation": {
            "same_order": same_order,
            "order_factored": KW["order_factored"],
            "same_5_sylow": same_5part,
            "different_2_sylow": different_2part,
            "separates_cospectral_pair": separates,
            "reading": (
                "Cospectral graphs share |K| (spanning-tree count 2^81*5^23) and here even "
                "the 5-Sylow (Z/5)^23; the 2-Sylow differs, so the sandpile group is a new "
                "algebraic separator of the W(3,3)/Q(4,3) pair -- complementing the "
                "geometric ovoid separator alpha=7 vs 10 (Pass 77)."
            ),
        },
        "cross_checks": {
            "order_matches_pass74_spanning_trees": "2^81 * 5^23",
            "adjacency_smith_pass77": "1^16 2^8 8^15 24 (distinct from the Laplacian critical group)",
        },
        "checks": checks,
    }
    with open("w33_pass82_critical_group.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass82_critical_group.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
