#!/usr/bin/env python3
"""Pass 1019: the collision condition is the regular two-graph condition (classical).

Pass 1017 found that the Seidel gluing differs from the adjacency gluing exactly
when k - n/2 is an eigenvalue, and Pass 1018 showed W(q,q) never satisfies this
while T(8) and L2(4) both do.  This pass solves that condition in SRG parameters
and identifies what it is.

THE EQUATION.  k - n/2 = s rearranges to

    n = 2(k - s).

Solving it together with the SRG relations mu = k + rs, lambda = mu + r + s and
k(k-lambda-1) = (n-k-1)mu gives, for n <= 96, seventeen admissible parameter
sets, among them (10,3,0,1) Petersen, (16,5,0,2), (16,6,2,2) L2(4) and
Shrikhande, (26,10,3,4), (28,9,0,4), (28,12,6,4) T(8) and the Chang graphs,
(36,14,4,6), (36,15,6,6), (50,21,8,9) and several at n = 64.  Both exceptional
strongly regular families appear, which is the point.

WHAT IT IS -- AND THIS IS NOT NEW.  The Seidel matrix S = J - I - 2A has
eigenvalue n-1-2k on the all-ones vector and -1-2c on the rest.  It therefore
has exactly TWO distinct eigenvalues precisely when n-1-2k = -1-2s, that is when
n = 2(k-s).  A graph whose Seidel matrix has two eigenvalues is, by definition, a
graph in the switching class of a REGULAR TWO-GRAPH -- Seidel's notion, and
entirely classical.  The condition derived here is that condition, rediscovered
from the gluing side.

So the correct statement of the Pass 1016-1018 phenomenon is:

    the Seidel gluing collapses relative to the adjacency gluing exactly on the
    strongly regular graphs in the switching class of a regular two-graph,

and the mechanism is transparent once named: two Seidel eigenvalues means two
eigenlattices instead of three, so the gluing is a quotient by a smaller sum.
That T(8), the Chang graphs, L2(4) and Shrikhande all satisfy it is the standard
fact that they are regular two-graph descendants, not a discovery.

WHAT REMAINS OURS.  The classical side supplies the classification of the
condition.  It does not supply the gluing statement: that Gamma(alpha A + beta J
+ gamma I) = Gamma(A) iff mult(k) = 1 and k + beta n / alpha avoids the spectrum
(Pass 1017), nor the W(q,q) consequence that the substrate family satisfies this
for every q with thresholds -(q^3+1) and -(q-1)^2(q+1)/2 (Pass 1018).  What this
pass adds is the bridge: the parameter locus where the pencil criterion bites is
a named classical object, so the fragile family needs no new name and its
membership can be read off the two-graph literature rather than recomputed.

The repository already carries two-graph material -- exploration/
PART_CCCLVII_TWO_GRAPH_BRIDGE.py, PART_CCCLXI_TWO_GRAPH_INCIDENCE_OPERATOR.py,
PART_CCCLXIV_TWO_GRAPH_PRIMITIVE_RESPONSE_OPERATOR.py and others, all indexed in
RESULTS_INDEX.md -- so this is a connection between two existing tracks and is
recorded as such.  Whether those files already contain the n = 2(k-s) locus is
NOT established here; the grep found the topic, not the identity, and confirming
or citing it is left as the follow-up.

BOUNDARY.  The seventeen parameter sets are those with n <= 96 admitted by the
integrality conditions used here (integral eigenvalues, integral multiplicities,
the standard SRG count).  Admissibility is not existence: a parameter set in the
list need not be realised by a graph.  The identification of n = 2(k-s) with the
two-eigenvalue Seidel condition is exact and proved above; the attribution to
Seidel's regular two-graphs is a citation, not a claim of this pass.
"""
from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1019_fragile_family_is_the_regular_two_graph_condition.json"

NAMED = {(10, 3, 0, 1): "Petersen",
         (16, 5, 0, 2): "Clebsch",
         (16, 6, 2, 2): "L2(4) / Shrikhande",
         (28, 12, 6, 4): "T(8) / Chang",
         (36, 15, 6, 6): "",
         (50, 21, 8, 9): ""}


def admissible(n, k, lam, mu):
    """standard SRG feasibility: integral spectrum and integral multiplicities."""
    if not (0 < k < n - 1 and 0 <= lam < k and 0 < mu <= k):
        return None
    if k * (k - lam - 1) != (n - k - 1) * mu:
        return None
    d = (lam - mu) ** 2 + 4 * (k - mu)
    rt = isqrt(d)
    if rt * rt != d or rt == 0:
        return None
    if (lam - mu + rt) % 2:
        return None
    r = (lam - mu + rt) // 2
    s = (lam - mu - rt) // 2
    num = 2 * k + (n - 1) * (lam - mu)
    if num % rt:
        return None
    f2 = (n - 1) - num // rt
    if f2 % 2:
        return None
    f = f2 // 2
    g = n - 1 - f
    if f <= 0 or g <= 0:
        return None
    return r, s, f, g


def part_A_solve_the_locus(checks, nmax=96):
    rows = {}
    for n in range(5, nmax + 1):
        for k in range(2, n - 1):
            for mu in range(1, k + 1):
                for lam in range(0, k):
                    res = admissible(n, k, lam, mu)
                    if not res:
                        continue
                    r, s, f, g = res
                    if n != 2 * (k - s):
                        continue
                    rows[f"({n},{k},{lam},{mu})"] = {
                        "n": n, "k": k, "lambda": lam, "mu": mu,
                        "r": r, "s": s, "multiplicities": [1, f, g],
                        "seidel_eigenvalues": sorted(
                            {n - 1 - 2 * k, -1 - 2 * r, -1 - 2 * s}),
                        "name": NAMED.get((n, k, lam, mu), "")}
    has_t8 = "(28,12,6,4)" in rows
    has_l24 = "(16,6,2,2)" in rows
    two_eig = all(len(v["seidel_eigenvalues"]) == 2 for v in rows.values())
    checks["locus_is_nonempty"] = (len(rows) > 10)
    checks["contains_T8_chang"] = has_t8
    checks["contains_L24_shrikhande"] = has_l24
    checks["every_member_has_two_seidel_eigenvalues"] = two_eig
    return {"rows": rows, "count": len(rows), "n_max": nmax,
            "equation": "n = 2(k - s), equivalently k - n/2 = s",
            "reading": (
                "Seventeen admissible parameter sets with n <= 96 satisfy the "
                "collision equation, and every one of them has a Seidel matrix "
                "with exactly two distinct eigenvalues.  Both exceptional "
                "strongly regular families are in the list, along with Petersen "
                "and Clebsch.")}


def part_B_identification(checks, rows):
    """S = J-I-2A has two eigenvalues iff n-1-2k = -1-2s iff n = 2(k-s)."""
    ok = True
    for key, v in rows.items():
        n, k, r, s = v["n"], v["k"], v["r"], v["s"]
        lhs = n - 1 - 2 * k
        ok &= (lhs == -1 - 2 * s)
        ok &= (len({lhs, -1 - 2 * r, -1 - 2 * s}) == 2)
    checks["two_eigenvalue_identity_holds"] = ok
    return {"identity": "n - 1 - 2k = -1 - 2s  <=>  n = 2(k - s)",
            "verified_on": len(rows),
            "classical_name": "regular two-graph (Seidel)",
            "attribution": (
                "a graph whose Seidel matrix has exactly two eigenvalues lies in "
                "the switching class of a regular two-graph; this is Seidel's "
                "classical notion and is NOT a result of this pass"),
            "what_is_ours": (
                "the pencil criterion of Pass 1017 and the W(q,q) consequence of "
                "Pass 1018; this pass contributes only the bridge, that the "
                "parameter locus where the criterion bites is that classical "
                "object"),
            "prior_art_in_repo": [
                "exploration/PART_CCCLVII_TWO_GRAPH_BRIDGE.py",
                "exploration/PART_CCCLXI_TWO_GRAPH_INCIDENCE_OPERATOR.py",
                "exploration/PART_CCCLXIV_TWO_GRAPH_PRIMITIVE_RESPONSE_OPERATOR.py"],
            "prior_art_resolution": (
                "RESOLVED in Pass 1020: all three files were read end to end. "
                "None states the n = 2(k-s) locus, the regular two-graph "
                "condition, or the two-eigenvalue Seidel criterion. They build "
                "the W(3,3) two-graph object itself -- the 4480 odd triples, the "
                "40 x 4480 vertex-by-odd-triple incidence operator M, and the "
                "identity M M^T = 320 I + 16 J + 4 A that recovers the adjacency "
                "from the incidence primitive. Their only '2*(k-...)' terms are "
                "the pair-counts 2*(K-1-LAM) and 2*(K-MU), which involve lambda "
                "and mu, not the Seidel eigenvalue s. Moreover W(3,3) is proved "
                "in part C below to be excluded from the locus, so these files "
                "concern a graph that provably does not lie in it. The in-repo "
                "prior art is therefore disjoint from this pass; the classical "
                "attribution to Seidel above stands unchanged."),
            "prior_art_resolved_by": "Pass 1020 (commit 8401f04b5)",
            "reading": (
                "The collision condition is exactly the two-eigenvalue Seidel "
                "condition, verified on every member of the locus.  The mechanism "
                "is then transparent: two Seidel eigenvalues means two "
                "eigenlattices instead of three, so the Seidel gluing is a "
                "quotient by a smaller sum and must be coarser.")}


def part_C_wqq_is_excluded(checks):
    """W(q,q): n = 2(k-s) would force (q+1)(q^2+1) = 2(q^2+2q+1); never for q>=2."""
    rows = {}
    clean = True
    for q in range(2, 13):
        n = (q + 1) * (q ** 2 + 1)
        k = q * (q + 1)
        s = -q - 1
        hit = (n == 2 * (k - s))
        if hit:
            clean = False
        rows[str(q)] = {"q": q, "n": n, "k": k, "s": s,
                        "two_k_minus_s": 2 * (k - s),
                        "is_regular_two_graph_locus": hit}
    checks["wqq_never_in_the_locus"] = clean
    return {"rows": rows,
            "reading": (
                "For W(q,q), n = (q+1)(q^2+1) while 2(k-s) = 2(q+1)^2, and these "
                "agree only if q^2+1 = 2q+2, which has no integer root at all.  "
                "So no W(q,q) is a regular two-graph descendant, at any q, and "
                "the substrate is permanently outside the fragile family.")}


def main_payload():
    checks = {}
    A = part_A_solve_the_locus(checks)
    B = part_B_identification(checks, A["rows"])
    C = part_C_wqq_is_excluded(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1019.fragile_family_is_the_regular_two_graph_condition.v1",
        "status": status,
        "headline": (
            "THE COLLISION CONDITION IS THE REGULAR TWO-GRAPH CONDITION, WHICH IS "
            "CLASSICAL.  Pass 1017's Seidel threshold k - n/2 lands on the "
            "spectrum exactly when n = 2(k-s); solving that with the SRG relations "
            "gives seventeen admissible parameter sets for n <= 96, including "
            "Petersen, Clebsch, L2(4)/Shrikhande and T(8)/Chang.  Every one of "
            "them has a Seidel matrix with exactly TWO eigenvalues, because "
            "n-1-2k = -1-2s is literally the same equation -- and a graph whose "
            "Seidel matrix has two eigenvalues is a graph in the switching class "
            "of a regular two-graph, Seidel's classical notion.  So the 'fragile "
            "family' needs no new name: the Seidel gluing collapses precisely on "
            "regular two-graph descendants, and the mechanism is that two Seidel "
            "eigenvalues give two eigenlattices instead of three.  That T(8), the "
            "Chang graphs, L2(4) and Shrikhande all qualify is standard, not a "
            "discovery.  What remains ours is the pencil criterion (Pass 1017) "
            "and the W(q,q) consequence (Pass 1018); this pass contributes the "
            "bridge, plus the exclusion: (q+1)(q^2+1) = 2(q+1)^2 has no integer "
            "root, so no W(q,q) is a regular two-graph descendant at any q."),
        "part_A_solve_the_locus": A,
        "part_B_identification": B,
        "part_C_wqq_is_excluded": C,
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
            raise SystemExit("Pass 1019 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
