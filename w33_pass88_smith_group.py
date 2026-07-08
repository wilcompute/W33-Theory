#!/usr/bin/env python3
"""
Pass 88 -- Smith group, critical group, and the p-rank: three cokernel invariants that separate
the cospectral GQ(3,3) pair W(3,3) / Q(4,3), and a correction to the Pass 84 hearing hierarchy.

A graph has two Smith-normal-form invariants: the SMITH GROUP coker(A) (cokernel of the adjacency)
and the CRITICAL GROUP coker(L) (cokernel of the Laplacian = sandpile group).  W(3,3) and Q(4,3)
are cospectral, so det(A) and det(L) agree -- yet BOTH cokernels differ, and so does the most
elementary invariant of all, the 2-rank of A (= the dimension of the binary code C_2).

  Smith group coker(A):   S(W) = (Z/2)^8 (+) (Z/8)^15 (+) Z/24
                          S(Q) = (Z/2)^14 (+) (Z/4)^6 (+) (Z/8)^9 (+) Z/24     (both order 3*2^56)
  2-rank of A:            W: 16   Q: 10   ->  binary codes C_2(W)=[40,16,8], C_2(Q)=[40,10,d]
  3-rank of A:            both 39
  critical group coker(L): different (Pass 82; both order 2^81*5^23)

HONEST CORRECTION to Pass 84: the hearing hierarchy listed only the ovoid number and the critical
group as distinguishing the pair.  In fact the 2-rank of the adjacency -- equivalently the DIMENSION
of the binary code -- already separates them (16 vs 10), a much more elementary invariant.  It is
not a spectral invariant (Brouwer-van Eijl: p-ranks of SRGs vary within a cospectral class), so this
is consistent with "the spectrum is deaf."

W(3) and Q(4,3) are graphs #3 and #23 in Brouwer's SRG(40,12,2,4) database (the two GQ(3,3) point
graphs); Haemers-Peeters-van Rijckevorsel studied their binary codes, Brouwer-van Eijl the p-ranks.

Self-contained (reads the GAP Smith-form certificate; computes p-ranks and C_2(Q) directly).
ASCII-only.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from itertools import product as iproduct
from math import prod
from pathlib import Path

import numpy as np

from w33_pass73_prime_geodesics import build_graph
from w33_pass76_cospectral_mates import build_Q43, rank_mod_p

ROOT = Path(__file__).resolve().parent
GAP_OUT = ROOT / "w33_pass88_smith_group_out.txt"


def read_smith():
    txt = GAP_OUT.read_text()

    def grab(key):
        m = re.search(rf"{key}=\[(.*?)\]", txt)
        return [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []

    return {"W": grab("smithA_W"), "Q": grab("smithA_Q")}


def smith_group(diag):
    factors = [d for d in diag if d > 1]
    hist = Counter(factors)
    order = prod(factors)
    a = b = c = 0
    o = order
    while o % 2 == 0:
        o //= 2
        a += 1
    while o % 3 == 0:
        o //= 3
        b += 1
    return {
        "invariant_factors": dict(sorted(hist.items())),
        "order": order,
        "order_factored": f"3*2^{a}" if (b == 1 and o == 1) else f"2^{a}*3^{b}*{o}",
        "structure": " (+) ".join(
            f"(Z/{d})^{m}" if m > 1 else f"Z/{d}" for d, m in sorted(hist.items())
        ),
    }


def v2(n):
    """2-adic valuation."""
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


def two_adic_transfer(diag_w, diag_q):
    """Align the two Smith diagonals (both sorted ascending) and describe how the 2-adic
    valuation is redistributed: the factor of 2 'switches sides' across the central band where
    both diagonals equal 2 -- 6 positions where Q gains a 2 (low side), 6 where W gains one
    (high side), net zero (so the determinants agree)."""
    valW = [v2(d) for d in sorted(diag_w)]
    valQ = [v2(d) for d in sorted(diag_q)]
    diff = [q - w for w, q in zip(valW, valQ)]
    up = [i for i, d in enumerate(diff) if d > 0]  # Q higher valuation (low side)
    down = [i for i, d in enumerate(diff) if d < 0]  # W higher valuation (high side)
    return {
        "aligned_W": sorted(diag_w),
        "aligned_Q": sorted(diag_q),
        "v2_total_W": sum(valW),
        "v2_total_Q": sum(valQ),
        "positions_Q_gains_a_2_low_side": len(up),  # expect 6 (diagonal indices 10..15)
        "positions_W_gains_a_2_high_side": len(
            down
        ),  # expect 6 (diagonal indices 24..29)
        "net_valuation_transfer": sum(diff),  # 0 -> same determinant / order
        "middle_agreeing_two_band": sum(
            1 for w, q in zip(sorted(diag_w), sorted(diag_q)) if w == q == 2
        ),
        "conserved": sum(diff) == 0 and sum(valW) == sum(valQ) == 56,
        "reading": (
            "The Smith forms differ by a symmetric 2-adic transfer: 6 low-side entries go "
            "1->2 (Q gains a 2) and 6 high-side entries go 8->4 (W keeps the 2 Q loses), "
            "reflected across the central band of eight agreeing 2's. Total 2-valuation "
            "56 is conserved, so |S(W)|=|S(Q)|=3*2^56, but the group structures differ."
        ),
    }


def gf2_min_distance(A):
    """Minimum nonzero weight of the binary row-space code of A (enumerate if small)."""
    n = A.shape[0]
    # row-reduce over GF(2) to a basis
    M = (A % 2).astype(np.int8).tolist()
    basis = []
    for row in M:
        r = row[:]
        for b in basis:
            piv = next(i for i, x in enumerate(b) if x)
            if r[piv]:
                r = [(x ^ y) for x, y in zip(r, b)]
        if any(r):
            basis.append(r)
    k = len(basis)
    if k > 20:
        return k, None
    best = n + 1
    B = np.array(basis, dtype=np.int8)
    for bits in iproduct((0, 1), repeat=k):
        if not any(bits):
            continue
        w = int(np.count_nonzero(np.mod(np.array(bits, dtype=np.int8) @ B, 2)))
        if 0 < w < best:
            best = w
    return k, best


def main():
    smith = read_smith()
    _, Aw = build_graph()
    _, Aq = build_Q43()

    SW = smith_group(smith["W"])
    SQ = smith_group(smith["Q"])
    smith_groups_differ = SW["invariant_factors"] != SQ["invariant_factors"]
    same_smith_order = SW["order"] == SQ["order"] == 3 * 2**56
    transfer = two_adic_transfer(smith["W"], smith["Q"])

    rank2_W, rank2_Q = rank_mod_p(Aw, 2), rank_mod_p(Aq, 2)
    rank3_W, rank3_Q = rank_mod_p(Aw, 3), rank_mod_p(Aq, 3)
    kQ, dQ = gf2_min_distance(Aq)

    # critical groups (Pass 82)
    p82 = json.loads((ROOT / "w33_pass82_critical_group.json").read_text())
    KW = p82["critical_group_W33"]["invariant_factors"]
    KQ = p82["critical_group_Q43"]["invariant_factors"]

    checks = {
        "smith_groups_same_order_3x2^56": same_smith_order,
        "smith_groups_differ": smith_groups_differ,
        "2rank_separates_16_vs_10": (rank2_W, rank2_Q) == (16, 10),
        "3ranks_equal_39": rank3_W == rank3_Q == 39,
        "binary_code_dims_differ": rank2_W != rank2_Q == kQ,
        "critical_groups_differ": KW != KQ,
        "two_adic_transfer_symmetric_6_6": (
            transfer["positions_Q_gains_a_2_low_side"] == 6
            and transfer["positions_W_gains_a_2_high_side"] == 6
            and transfer["conserved"]
        ),
    }
    all_ok = all(checks.values())

    hierarchy = [
        ["adjacency / Ihara / Bartholdi / spectral zeta", "DEAF (identical)"],
        ["local neighbourhood + mu-graph (Pass 76)", "DEAF (both 4K3 / 4K1)"],
        ["class number kappa = spanning trees", "DEAF (both 2^81*5^23)"],
        [
            "2-rank of A = binary code dimension (this pass)",
            f"HEARS ({rank2_W} vs {rank2_Q})",
        ],
        ["Smith group coker(A) (this pass)", "HEARS (2-part structure)"],
        ["ovoid number alpha (Pass 77)", "HEARS (7 vs 10)"],
        ["critical group coker(L) (Pass 82)", "HEARS (2-Sylow)"],
    ]

    print("=" * 74)
    print("PASS 88 -- SMITH GROUP, CRITICAL GROUP, AND THE p-RANK SEPARATOR")
    print("=" * 74)
    print(f"Smith group S(W) = coker(A) = {SW['structure']}")
    print(f"            S(Q) = coker(A) = {SQ['structure']}")
    print(
        f"  both order 3*2^56: {same_smith_order}; structures differ: {smith_groups_differ}"
    )
    print()
    print("2-adic transfer (the factor of 2 switches sides across the central 2-band):")
    print(f"   aligned W: {transfer['aligned_W']}")
    print(f"   aligned Q: {transfer['aligned_Q']}")
    print(
        f"   {transfer['positions_Q_gains_a_2_low_side']} low-side entries 1->2 (Q gains a 2); "
        f"{transfer['positions_W_gains_a_2_high_side']} high-side entries 8->4 (W keeps it); "
        f"net transfer {transfer['net_valuation_transfer']} -> total v2=56 conserved"
    )
    print()
    print(
        f"2-rank(A): W={rank2_W}  Q={rank2_Q}   ->  binary codes C_2(W)=[40,16,8], "
        f"C_2(Q)=[40,{kQ},{dQ}]"
    )
    print(f"3-rank(A): W={rank3_W}  Q={rank3_Q}  (equal)")
    print(f"critical group differs (Pass 82): {KW != KQ}")
    print()
    print("REFINED hearing hierarchy for the cospectral pair W(3,3)/Q(4,3):")
    for probe, verdict in hierarchy:
        print(f"   {probe:<48} {verdict}")
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 74)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 74)

    payload = {
        "schema": "w33.pass88.smith_group.v1",
        "status": "PASS" if all_ok else "FAIL",
        "smith_group_W": SW,
        "smith_group_Q": SQ,
        "smith_groups_differ": smith_groups_differ,
        "two_adic_transfer": transfer,
        "p_ranks": {
            "2rank_W": rank2_W,
            "2rank_Q": rank2_Q,
            "3rank_W": rank3_W,
            "3rank_Q": rank3_Q,
        },
        "binary_codes": {"C2_W": [40, rank2_W, 8], "C2_Q": [40, kQ, dQ]},
        "critical_groups": {"K_W": KW, "K_Q": KQ, "differ": KW != KQ},
        "refined_hearing_hierarchy": hierarchy,
        "correction_to_pass84": (
            "The 2-rank of the adjacency (= binary code dimension) separates "
            "the cospectral pair (16 vs 10) -- more elementary than the ovoid "
            "number or the critical group. p-ranks are not spectral (Brouwer-"
            "van Eijl), so this is consistent with the spectrum being deaf."
        ),
        "literature": [
            "Brouwer-van Eijl, p-rank of adjacency of SRGs, JAC 1 (1992) 329-346",
            "Haemers-Peeters-van Rijckevorsel, binary codes of SRGs",
            "W(3),Q(4,3) = Brouwer SRG(40,12,2,4) graphs #3 and #23 (the two GQ(3,3))",
        ],
        "checks": checks,
    }
    (ROOT / "w33_pass88_smith_group.json").write_text(json.dumps(payload, indent=2))
    print("[wrote] w33_pass88_smith_group.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
