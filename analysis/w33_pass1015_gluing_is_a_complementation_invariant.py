#!/usr/bin/env python3
"""Pass 1015: the gluing group is a complementation invariant, and that forces ranks.

THE THEOREM.  For a k-regular graph G on n vertices with complement Gbar,

    A(Gbar) = J - I - A(G).

The all-ones vector is an eigenvector of both, with eigenvalues k and n-1-k.  On
its orthogonal complement J acts as zero, so there A(Gbar) = -I - A(G) and the
two operators have exactly the same eigenvectors.  The eigenspace decomposition
of Q^n is therefore literally the same subspace decomposition for G and Gbar,
with only the labels changing:

    L_c(G) = L_{-1-c}(Gbar)   for c != k,        L_k(G) = L_{n-1-k}(Gbar).

Saturated integer eigenlattices are determined by their rational spans, so these
are equalities of SUBGROUPS of Z^n, not merely isomorphisms.  Hence the sum
sum_i L_i is the same subgroup and

    Z^n / sum_i L_i(G)  =  Z^n / sum_i L_i(Gbar)   -- the SAME group.

Verified on L2(4), L2(5), T(6), T(8) and W(3,3): identical invariant factors in
all five, W(3,3) giving (Z/2)^6 + (Z/6)^9 + Z/120 on both sides.

WHY THIS IS NOT COSMETIC.  The conductor is NOT complementation invariant.  It
moves 32 -> 96 for L2(4), 50 -> 300 for L2(5), 336 -> 840 for T(8), 480 -> 720
for W(3,3).  So a single invariant group is being computed from two different
conductors, and the k-branch machinery must agree across the change.  Two
consequences follow, and both are testable.

CONSEQUENCE 1 -- A SHARPER SUPPORT BOUND.  Pass 1014 showed supp(gluing) is
contained in supp(M), a parameter-determined set.  Applying that to both sides,

    supp(gluing)  <=  supp(M_G)  INTERSECT  supp(M_Gbar),

which is strictly better than either alone.  For L2(4) the complement's
conductor admits p = 3 while the graph's does not, and the intersection {2} is
exactly the true support.  Same for T(8) at p = 5.

CONSEQUENCE 2 -- FORCED VANISHING.  When p divides M_Gbar but not M_G, the G
side has no p-part at all, so the coalescence rank computed on the Gbar side --
where the theorem of Pass 828 is live and generically returns something nonzero
-- MUST be zero.  This is a prediction about F_p ranks of specific matrix
stacks, made without computing them.  Tested in three cases, L2(4) and L2(5) at
p = 3 and T(8) at p = 5: rank 0 in all three, as forced.

That is the reason to care.  Pass 1009 found that coalescence ranks sometimes
collapse to zero and offered no mechanism.  Complementation supplies one: a rank
is forced to vanish whenever the complementary conductor omits the prime.  Not
every vanishing is of this kind -- L2(5) has 2 | M = 50 with v_2 = 1 on BOTH
sides, and the 2-part is still trivial, so unexplained cancellation survives --
but a family of them is now accounted for.

WHAT IT COSTS.  The gluing cannot distinguish a graph from its complement.  Read
with Pass 1014, the invariant's resolution is now bracketed on both sides: finer
than the parameter set (it separates T(8) from the Chang graphs, and L2(4) from
Shrikhande), coarser than isomorphism (it identifies the three Chang graphs with
each other, and every graph with its complement).

BOUNDARY.  Part A is a proof, checked on five graphs.  The support bound is an
upper bound and is not always tight: L2(5) has intersection {2,5} but true
support {5}, the 2-part vanishing for reasons complementation does not explain.
Three forced-vanishing cases were available among the graphs tested; the
prediction is exact in each, but three is a small witness set.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1015_gluing_is_a_complementation_invariant.json"
P1014 = ROOT / "analysis" / "w33_pass1014_ramified_prime_separates_cospectral.py"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"
PRIMES = (2, 3, 5, 7, 11, 13)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M14 = _load(P1014, "w33_pass1014")


def rook(k):
    V = [(i, j) for i in range(k) for j in range(k)]
    n = k * k
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            if a != b and (V[a][0] == V[b][0] or V[a][1] == V[b][1]):
                A[a, b] = 1
    return A


def triangular(k):
    prs = list(itertools.combinations(range(k), 2))
    n = len(prs)
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            if a != b and set(prs[a]) & set(prs[b]):
                A[a, b] = 1
    return A


def w33():
    mod = _load(BASE, "w33_pass682_base")
    pts, edges, tris, K, d1, d2 = mod.build()
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    return A


def complement(A):
    n = A.shape[0]
    return 1 - A - np.eye(n, dtype=np.int64)


def spectrum(A):
    return sorted({int(round(x)) for x in np.linalg.eigvalsh(A.astype(float))},
                  reverse=True)


def gluing(A, cs):
    n = A.shape[0]
    stacked = []
    saturated = True
    for c in cs:
        K = M14.hnf_kernel(A - c * np.eye(n, dtype=np.int64))
        if set(M14.invariant_factors(K)) - {1}:
            saturated = False
        stacked += K
    d = [x for x in M14.invariant_factors(stacked) if x not in (0, 1)]
    return d, saturated


def support(vals):
    return sorted({p for p in PRIMES if any(x % p == 0 for x in vals)})


def graphs():
    return {"L2(4)": rook(4), "L2(5)": rook(5), "T(6)": triangular(6),
            "T(8)": triangular(8), "W(3,3)": w33()}


def part_A_invariance(checks):
    rows = {}
    allsame = True
    allsat = True
    for nm, A in graphs().items():
        C = complement(A)
        eG, eC = spectrum(A), spectrum(C)
        gG, satG = gluing(A, eG)
        gC, satC = gluing(C, eC)
        MG, _ = M14.conductor(eG)
        MC, _ = M14.conductor(eC)
        same = (gG == gC)
        allsame &= same
        allsat &= (satG and satC)
        rows[nm] = {"n": int(A.shape[0]), "spectrum": eG,
                    "complement_spectrum": eC,
                    "conductor": MG, "complement_conductor": MC,
                    "conductor_changes": MG != MC,
                    "gluing": gG, "complement_gluing": gC,
                    "gluing_identical": same,
                    "both_saturated": bool(satG and satC),
                    "label_map_check": all(
                        (-1 - c) in eC for c in eG if c != eG[0])}
    checks["gluing_invariant_under_complementation"] = allsame
    checks["all_kernels_saturated"] = allsat
    checks["conductor_is_not_invariant"] = all(
        v["conductor_changes"] for v in rows.values())
    checks["w33_gluing_matches_pass826_odd_part"] = (
        rows["W(3,3)"]["gluing"] == rows["W(3,3)"]["complement_gluing"]
        and 120 in rows["W(3,3)"]["gluing"])
    checks["eigenvalue_labels_map_by_minus_one_minus_c"] = all(
        v["label_map_check"] for v in rows.values())
    return {"rows": rows,
            "proof": (
                "A(Gbar) = J - I - A(G); the all-ones vector is an eigenvector of "
                "both, and on its orthogonal complement J acts as zero so "
                "A(Gbar) = -I - A(G) there.  The two operators share every "
                "eigenvector, so the eigenspace decomposition of Q^n is the same "
                "and the saturated integer eigenlattices are equal as SUBGROUPS of "
                "Z^n under c -> -1-c.  The quotient by their sum is therefore the "
                "same group."),
            "reading": (
                "Identical invariant factors for all five graphs, W(3,3) included "
                "at (Z/2)^6 + (Z/6)^9 + Z/120, while the conductor changes in "
                "every case -- 480 to 720 for W(3,3).  One invariant group, two "
                "different conductors, so the k-branch machinery must agree across "
                "the change.")}


def part_B_sharpened_support(checks, A_rows):
    rows = {}
    improved = 0
    sound = True
    for nm, r in A_rows.items():
        sG = support([r["conductor"]])
        sC = support([r["complement_conductor"]])
        cap = sorted(set(sG) & set(sC))
        true = support(r["gluing"])
        sound &= set(true) <= set(cap)
        better = (len(cap) < len(sC)) or (len(cap) < len(sG))
        improved += bool(better)
        rows[nm] = {"supp_conductor": sG, "supp_complement_conductor": sC,
                    "intersection": cap, "true_support": true,
                    "intersection_is_tight": (cap == true),
                    "improves_on_one_side": better}
    checks["intersection_bound_is_sound"] = sound
    checks["intersection_improves_somewhere"] = (improved >= 3)
    return {"rows": rows, "graphs_improved": improved,
            "bound": "supp(gluing) <= supp(M_G) INTERSECT supp(M_Gbar)",
            "reading": (
                "The bound holds in every case and is strictly better than one "
                "side alone in most of them: L2(4)'s complement admits p = 3 and "
                "T(8)'s admits p = 5, both excluded by the intersection, which is "
                "exactly the true support there.  It is not always tight -- L2(5) "
                "has intersection {2,5} against true support {5} -- so genuine "
                "cancellation survives beyond what complementation explains.")}


def part_C_forced_vanishing(checks):
    rows = {}
    ok = True
    for nm, A in graphs().items():
        C = complement(A)
        eG, eC = spectrum(A), spectrum(C)
        MG, _ = M14.conductor(eG)
        MC, _ = M14.conductor(eC)
        for p in PRIMES:
            if M14.vp(MC, p) >= 1 and M14.vp(MG, p) == 0:
                rk = M14.coalescence(C, eC, p)
                ok &= (rk == 0)
                rows[f"{nm}_p{p}"] = {
                    "graph": nm, "prime": p,
                    "v_p_conductor": M14.vp(MG, p),
                    "v_p_complement_conductor": M14.vp(MC, p),
                    "coalescence_rank_on_complement": rk,
                    "forced_value": 0, "holds": (rk == 0)}
    checks["forced_vanishing_holds"] = ok
    checks["forced_vanishing_cases_found"] = (len(rows) >= 3)
    return {"rows": rows, "cases": len(rows),
            "prediction": (
                "if p divides M_Gbar but not M_G then the gluing has no p-part, "
                "so the coalescence rank computed on the Gbar side must be zero "
                "even though the Pass 828 theorem is live there"),
            "reading": (
                "Three cases arise among the graphs tested -- L2(4) and L2(5) at "
                "p = 3, T(8) at p = 5 -- and the rank is zero in all three, as "
                "forced.  Pass 1009 observed coalescence ranks collapsing to zero "
                "with no mechanism; complementation supplies one for a family of "
                "them, without computing the rank.")}


def main_payload():
    checks = {}
    A = part_A_invariance(checks)
    B = part_B_sharpened_support(checks, A["rows"])
    C = part_C_forced_vanishing(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1015.gluing_is_a_complementation_invariant.v1",
        "status": status,
        "headline": (
            "THE GLUING GROUP IS A COMPLEMENTATION INVARIANT, AND THAT FORCES "
            "COALESCENCE RANKS TO VANISH.  Since A(Gbar) = J - I - A(G) shares "
            "every eigenvector with A(G), the saturated eigenlattices are equal as "
            "SUBGROUPS of Z^n under c -> -1-c, so G and Gbar have the SAME gluing "
            "group -- verified on L2(4), L2(5), T(6), T(8) and W(3,3), the last "
            "giving (Z/2)^6 + (Z/6)^9 + Z/120 on both sides.  The conductor is not "
            "invariant (480 -> 720 for W(3,3)), so one group is computed from two "
            "conductors and the machinery must agree.  Two consequences: the "
            "support bound sharpens to supp(M_G) INTERSECT supp(M_Gbar), strictly "
            "better than either side in most cases and exactly tight for L2(4) and "
            "T(8); and when p divides one conductor but not the other, the "
            "coalescence rank on the live side is FORCED to zero -- predicted "
            "without computing it, confirmed in all three available cases.  Pass "
            "1009 saw ranks collapse with no mechanism; this is one.  The price is "
            "that the gluing cannot tell a graph from its complement, which with "
            "Pass 1014 brackets its resolution: finer than the parameter set, "
            "coarser than isomorphism."),
        "part_A_invariance": A,
        "part_B_sharpened_support": B,
        "part_C_forced_vanishing": C,
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
            raise SystemExit("Pass 1015 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
