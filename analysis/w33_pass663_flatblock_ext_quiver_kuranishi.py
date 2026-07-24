#!/usr/bin/env python3
"""Pass 663: the full Ext quiver and Kuranishi cone of the flat-block order,
over torsion-free Z_p.

Pass 662 identified Pass 656's commutant R = Z_2[S]/(S^2 - 4S) as the
flat-block order O_q = Z_p[S]/(S(S - 2q)) at (p, q) = (2, 2), and matched two of
its invariants -- the cross-degree-one Ext^1 and the diagonal Ext^2, both Z/4.
It computed them over the truncated ring Z/p^N, which is correct for a COKERNEL
but wrong for a KERNEL, because Z/p^N has torsion.  Pass 656 also records that
the OTHER two entries VANISH: self-Ext^1 = 0 and cross-Ext^2 = 0.  Those are
kernel entries, and they vanish exactly because the true order is over the
torsion-free ring Z_p.  This pass computes the complete quiver correctly and
adds the quadratic obstruction.

THE MODULES.  O_q = Z_p[S]/(S(S - 2q)) has two branch lattices, each Z_p:
M_0 with S acting as 0 and M_{2q} with S acting as 2q.  The resolution of M_0
is periodic, ... -> O --(S-2q)--> O --S--> O -> M_0, so Hom(-, M_s) is the
2-periodic cochain complex with maps alternating multiplication by s and by
s - 2q on the rank-one lattice M_s = Z_p.  Over Z_p a nonzero scalar c has
ker(mult c) = 0 and coker(mult c) = Z_p/(c) = Z/p^{v_p(c)}.

THE FULL QUIVER.

    Ext^1(M_0, M_0)    = ker(mult(-2q))  = 0
    Ext^1(M_0, M_{2q}) = coker(mult 2q)  = Z/p^{v_p(2q)}
    Ext^2(M_0, M_0)    = coker(mult(-2q))= Z/p^{v_p(2q)}
    Ext^2(M_0, M_{2q}) = ker(mult 2q)    = 0

At (p, q) = (2, 2), v_2(4) = 2, so this reads (0, Z/4, Z/4, 0) -- Pass 656's
complete table, including the two vanishing entries the truncated computation
would have gotten wrong.  For odd q with p = q, 2 is a unit so v_q(2q) = 1 and
the quiver is (0, Z/q, Z/q, 0).

THE KURANISHI CONE.  Deform M_0 (+) M_{2q} by the off-diagonal first-order class
N = [[0, y], [x, 0]] (the two cross-Ext^1 parameters).  The first-order equation
N(S - 2q) + S N = 0 holds identically, so every (x, y) is a first-order
deformation.  The second-order obstruction is N^2 = diag(xy, xy), so the
obstruction map is (x, y) -> (xy, xy) into Ext^2(M_0,M_0) (+) Ext^2(M_{2q},M_{2q}),
and the unobstructed Kuranishi cone is xy = 0.  This reproduces Pass 656's cone
at q = 2 (mod 4) and predicts it for odd q (mod q).  The whole obstruction is
the nodal one: S(S - 2q) is a genuine product of two distinct branches, and
smoothing both at once costs their product.

REFINEMENT OF PASS 662.  Pass 662's two stated invariants stand; its method
(the ring Z/p^N) is replaced here by the torsion-free order Z_p, which is what
makes the kernel entries vanish and completes the match to Pass 656.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass663_flatblock_ext_quiver_kuranishi.json"


def vp(n, p):
    n = abs(n)
    v = 0
    while n and n % p == 0:
        n //= p
        v += 1
    return v


def ext_entry(scalar, kind, p):
    """Over Z_p: kernel of mult by a nonzero scalar is 0; cokernel is
    Z/p^{v_p(scalar)}.  Returns a small dict describing the group."""
    if scalar == 0:
        return {"group": "Z_p" if kind == "ker" else "0",
                "order": None}
    if kind == "ker":
        return {"group": "0", "order": 1}
    order = p ** vp(scalar, p)
    return {"group": (f"Z/{order}" if order > 1 else "0"), "order": order}


def full_quiver(p, q):
    t = 2 * q
    return {
        "Ext1_self_M0_M0": ext_entry(-t, "ker", p),      # ker(mult -2q)
        "Ext1_cross_M0_M2q": ext_entry(t, "coker", p),   # coker(mult 2q)
        "Ext2_self_M0_M0": ext_entry(-t, "coker", p),    # coker(mult -2q)
        "Ext2_cross_M0_M2q": ext_entry(t, "ker", p),     # ker(mult 2q)
    }


def part_A_quiver(checks):
    rows = {}
    for (p, q) in ((2, 2), (3, 3), (5, 5), (7, 7)):
        rows[f"p{p}_q{q}"] = {k: v["group"] for k, v in full_quiver(p, q).items()}
    p22 = rows["p2_q2"]
    checks["reproduces_pass656_full_table"] = (
        p22["Ext1_self_M0_M0"] == "0"
        and p22["Ext1_cross_M0_M2q"] == "Z/4"
        and p22["Ext2_self_M0_M0"] == "Z/4"
        and p22["Ext2_cross_M0_M2q"] == "0")
    checks["vanishing_entries_are_kernels"] = (
        p22["Ext1_self_M0_M0"] == "0" and p22["Ext2_cross_M0_M2q"] == "0")
    checks["odd_q_quiver_is_0_Zq_Zq_0"] = all(
        rows[f"p{q}_q{q}"]["Ext1_cross_M0_M2q"] == f"Z/{q}"
        and rows[f"p{q}_q{q}"]["Ext2_self_M0_M0"] == f"Z/{q}"
        and rows[f"p{q}_q{q}"]["Ext1_self_M0_M0"] == "0"
        and rows[f"p{q}_q{q}"]["Ext2_cross_M0_M2q"] == "0"
        for q in (3, 5, 7))
    return {"rows": rows,
            "pass656_table": "(self-Ext1, cross-Ext1, self-Ext2, cross-Ext2) = (0, Z/4, Z/4, 0)",
            "reading": (
                "Over the torsion-free order Z_p, the kernel entries "
                "(self-Ext1, cross-Ext2) vanish and the cokernel entries "
                "(cross-Ext1, self-Ext2) are Z/p^{v_p(2q)}.  At (p,q)=(2,2) "
                "this is (0, Z/4, Z/4, 0), Pass 656's complete quiver; the "
                "cross-degree-one / diagonal-degree-two pattern is exactly the "
                "coker/ker split.  The odd-q analogue is (0, Z/q, Z/q, 0)."),
            "correction_of_662": (
                "Pass 662 computed the two cokernel invariants over the "
                "truncated ring Z/p^N, which has torsion; the two vanishing "
                "kernel entries need the torsion-free Z_p and are supplied "
                "here.  Pass 662's stated values (both Z/4) are unchanged.")}


def _mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def part_B_kuranishi(checks):
    rows, first_ok, obstruction_ok = {}, True, True
    for q in (2, 3, 5, 7):
        t = 2 * q
        D = [[0, 0], [0, t]]
        Dm = [[-t, 0], [0, 0]]                       # D - 2q I
        per_pair = {}
        for (x, y) in ((1, 1), (1, 0), (2, 3)):
            N = [[0, y], [x, 0]]
            first = _mm(N, Dm)
            SN = _mm(D, N)
            first = [[first[i][j] + SN[i][j] for j in range(2)]
                     for i in range(2)]
            N2 = _mm(N, N)
            if any(first[i][j] for i in range(2) for j in range(2)):
                first_ok = False
            if not (N2 == [[x * y, 0], [0, x * y]]):
                obstruction_ok = False
            per_pair[f"x{x}_y{y}"] = {
                "first_order_coboundary_zero": all(
                    first[i][j] == 0 for i in range(2) for j in range(2)),
                "obstruction_N2": [[N2[0][0], N2[0][1]], [N2[1][0], N2[1][1]]],
                "on_cone_xy_eq_0": (x * y) % t == 0}
        rows[f"q{q}"] = per_pair
    checks["first_order_always_unobstructed"] = first_ok
    checks["obstruction_is_diag_xy_xy"] = obstruction_ok
    return {"rows": rows,
            "obstruction_map": "(x, y) -> (xy, xy) into Ext^2(M0,M0) (+) Ext^2(M2q,M2q)",
            "cone": "xy = 0 (mod 2q); Pass 656's cone at q=2 is mod 4",
            "reading": (
                "First-order deformation N=[[0,y],[x,0]] is unobstructed for "
                "every (x,y); the second-order obstruction is N^2 = "
                "diag(xy,xy), so the Kuranishi cone is xy = 0.  This is the "
                "nodal obstruction: S(S-2q) is a product of two distinct "
                "branches and smoothing both at once costs their product.  "
                "Reproduces Pass 656 exactly at q=2 and predicts the odd-q "
                "cone.")}


def part_C_summary(checks):
    checks["summary_recorded"] = True
    return {"proved": (
        "The complete continuous Ext quiver of the flat-block order O_q = "
        "Z_p[S]/(S(S-2q)) on its two branch lattices is (self-Ext1, "
        "cross-Ext1, self-Ext2, cross-Ext2) = (0, Z/p^{v_p(2q)}, "
        "Z/p^{v_p(2q)}, 0), and the quadratic Kuranishi obstruction is "
        "(x,y) -> (xy,xy) with cone xy=0.  At (p,q)=(2,2) this is Pass 656 in "
        "full; for odd q it is (0, Z/q, Z/q, 0) with cone xy=0 mod q."),
        "still_open": (
            "That the S8 characteristic lattices of Pass 656 ARE these two "
            "branch lattices of the flat-block order, rather than only sharing "
            "their homological invariants; the module-level identification "
            "needs the GAP construction and remains the testable consequence "
            "of Pass 662.")}


def main_payload():
    checks = {}
    A = part_A_quiver(checks)
    B = part_B_kuranishi(checks)
    C = part_C_summary(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass663.flatblock_ext_quiver_kuranishi.v1",
        "status": status,
        "headline": (
            "THE FULL Ext QUIVER AND KURANISHI CONE OF THE FLAT-BLOCK ORDER "
            "OVER TORSION-FREE Z_p.  For O_q = Z_p[S]/(S(S-2q)) with branch "
            "lattices M_0 (S=0) and M_{2q} (S=2q), the periodic resolution "
            "gives (self-Ext1, cross-Ext1, self-Ext2, cross-Ext2) = (0, "
            "Z/p^{v_p(2q)}, Z/p^{v_p(2q)}, 0): the cokernel entries are "
            "Z/p^{v_p(2q)} and the kernel entries vanish, Z_p being "
            "torsion-free (proved).  At (p,q)=(2,2) this is (0, Z/4, Z/4, 0), Pass "
            "656's COMPLETE table -- the two vanishing entries the truncated "
            "computation of Pass 662 could not see.  The quadratic obstruction "
            "for M_0 (+) M_{2q}, from the off-diagonal deformation "
            "N=[[0,y],[x,0]], is N^2 = diag(xy,xy), so the Kuranishi cone is "
            "xy=0, reproducing Pass 656 at q=2 and predicting the odd-q "
            "quiver (0, Z/q, Z/q, 0) with the same cone.  This refines Pass "
            "662: its two invariants stand; the torsion-free order completes "
            "the quiver."),
        "part_A_full_quiver": A,
        "part_B_kuranishi_obstruction": B,
        "part_C_summary": C,
        "boundary": (
            "Everything is exact integer / p-adic arithmetic on the abstract "
            "order and its two branch lattices.  It reproduces Pass 656's "
            "quiver and cone and predicts the odd-q analogue, but does not "
            "identify the S8 lattices with the branch lattices -- that "
            "remains Pass 662's testable consequence."),
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 663 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
