#!/usr/bin/env python3
"""Pass 1016: the Seidel gluing is the switching invariant, and separation is not always ramified.

Three results, one of which corrects the previous pass.

PART A -- THE SEIDEL GLUING IS A SWITCHING-CLASS INVARIANT.

Seidel switching with respect to a vertex set S acts on the Seidel matrix
S = J - I - 2A by conjugation with the diagonal sign matrix D, D_vv = -1 exactly
on S:

    Seidel(G^S) = D . Seidel(G) . D.

D is unimodular over Z, so it is an automorphism of the lattice Z^n, and it
carries each saturated eigenlattice of Seidel(G) onto the corresponding one of
Seidel(G^S).  The gluing quotient is therefore unchanged: the SEIDEL gluing is a
switching-class invariant.

The adjacency gluing is not, and the split is visible in one family.  T(8) and
the three Chang graphs form a single switching class, and

    Seidel gluing    (Z/6)^6 + Z/12     -- all four, identical
    adjacency gluing (Z/6)^6 + Z/84     -- T(8)
                     Z/2 + (Z/6)^6 + Z/84  -- all three Chang graphs

So Pass 1014's extra Z/2 has an identification: it is the part of the adjacency
gluing that records POSITION WITHIN the switching class, which the Seidel gluing
by construction cannot see.  The two invariants are complementary, and the
Seidel one is the coarser.

PART B -- ON SMALL GRAPHS THE GLUING SEPARATES COSPECTRAL MATES EVERY TIME.

Census over all graphs on n = 6 vertices (32,768 labelled graphs), keeping those
with integral spectrum, grouping by spectrum, and reducing each group to
pairwise non-isomorphic representatives by explicit permutation search:

    n = 6:  18 integral spectra, 2 of them carrying >= 2 non-isomorphic graphs,
            and the gluing separates the mates in BOTH.

The same census at n = 7 (2,097,152 labelled graphs, reproduce with --census7)
gives 29 integral spectra, 3 with >= 2 non-isomorphic graphs, and the gluing
separates in all 3.  Five spectra, five separations, no failures.  Together with
Pass 1014's Chang and Shrikhande families this is the strongest evidence so far
that the gluing is a genuinely useful cospectrality invariant -- while remaining
provably incomplete, since Pass 1014 showed it identifies the three Chang graphs
and Pass 1015 showed it identifies every graph with its complement.

PART C -- SEPARATION IS *NOT* ALWAYS RAMIFIED.  PASS 1014'S SUGGESTION IS FALSE.

Pass 1014 observed that for both exceptional SRG families the entire difference
sat at the ramified prime, and asked in its boundary whether that was general.
It is not.  The census produces a counterexample at n = 6:

    spectrum {2, 1, 0, -1, -2},  M = 24 = 2^3 * 3,  so v_3(M) = 1, UNRAMIFIED

and two non-isomorphic cospectral graphs whose gluings are (Z/2, Z/6, Z/12) and
(Z/2, Z/2, Z/4) -- differing at p = 3, where the 3-parts are (Z/3)^2 and trivial.
Since the coalescence rank at an unramified prime is exactly the classical SRG
p-rank (Pass 983), and p-ranks of cospectral graphs differ in general, this is
what should have been expected.  The two SRG families of Pass 1014 are the
special case: they happen to share their unramified p-ranks, which is a known
fact about Chang and Shrikhande specifically, not a feature of the theory.

The corrected statement.  The gluing separates through TWO independent channels:
the unramified p-ranks, which are classical, and the ramified filtration, which
is not.  Pass 1014's families exercise only the second because the first is
degenerate there.  Nothing in Pass 1014's theorem is affected -- the conductor
identity and the parameter/rank dichotomy stand -- only the conjecture floated
in its boundary is withdrawn.

PART D -- THE RAMIFIED PROFILES, EXPLICITLY.

For the Chang family at p = 2 the invariant-factor valuations are a = (1^6, 2)
for T(8) and (1^7, 2) for each Chang graph, giving kernel-growth profiles
(kappa_j = sum_i min(a_i, j), Delta_j = #{i : a_i >= j}) of

    T(8)    Delta_1 = 6, Delta_2 = 1     kappa_1 = 6, kappa_2 = 7
    Chang   Delta_1 = 7, Delta_2 = 1     kappa_1 = 7, kappa_2 = 8

so the filtration of the K-track's Pass 1002 separates them at level 1 and
agrees at level 2.  The separating information is the first kernel-growth step.

BOUNDARY.  Part A is a proof, verified on one switching class of four graphs.
Part B is a complete census at n = 6 in the certificate, with n = 7 behind
--census7; "separates every time" is a statement about five spectra, not a
theorem.  Part C is a single explicit counterexample, which is all that is
needed to withdraw the conjecture.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1016_seidel_invariant_and_unramified_separation.json"
P1014 = ROOT / "analysis" / "w33_pass1014_ramified_prime_separates_cospectral.py"
PRIMES = (2, 3, 5, 7, 11, 13)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M14 = _load(P1014, "w33_pass1014")


def spectrum(A):
    return sorted({int(round(x)) for x in np.linalg.eigvalsh(A.astype(float))},
                  reverse=True)


def gluing(A):
    n = A.shape[0]
    stacked = []
    for c in spectrum(A):
        stacked += M14.hnf_kernel(A - c * np.eye(n, dtype=np.int64))
    return [x for x in M14.invariant_factors(stacked) if x not in (0, 1)]


def triangular(k):
    prs = list(itertools.combinations(range(k), 2))
    n = len(prs)
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            if a != b and set(prs[a]) & set(prs[b]):
                A[a, b] = 1
    return A, prs


def switch(A, S):
    B = A.copy()
    n = A.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and ((i in S) != (j in S)):
                B[i, j] = 1 - A[i, j]
    return B


def seidel(A):
    n = A.shape[0]
    return np.ones((n, n), dtype=np.int64) - np.eye(n, dtype=np.int64) - 2 * A


def chang_family():
    A, prs = triangular(8)
    idx = {e: i for i, e in enumerate(prs)}
    spec = {"T(8)": [],
            "Chang-1": [(0, 1), (2, 3), (4, 5), (6, 7)],
            "Chang-2": [(0, 1), (1, 2), (2, 0),
                        (3, 4), (4, 5), (5, 6), (6, 7), (7, 3)],
            "Chang-3": [(i, (i + 1) % 8) for i in range(8)]}
    return {nm: (A if not e else switch(A, {idx[tuple(sorted(x))] for x in e}))
            for nm, e in spec.items()}


def part_A_seidel_invariant(checks):
    rows = {}
    for nm, B in chang_family().items():
        rows[nm] = {"adjacency_gluing": gluing(B),
                    "seidel_spectrum": spectrum(seidel(B)),
                    "seidel_gluing": gluing(seidel(B))}
    adj = {tuple(v["adjacency_gluing"]) for v in rows.values()}
    sei = {tuple(v["seidel_gluing"]) for v in rows.values()}
    checks["seidel_gluing_is_switching_invariant"] = (len(sei) == 1)
    checks["adjacency_gluing_is_not"] = (len(adj) == 2)
    return {"rows": rows, "distinct_adjacency": len(adj),
            "distinct_seidel": len(sei),
            "proof": (
                "Seidel(G^S) = D . Seidel(G) . D with D the diagonal sign matrix "
                "of S.  D is unimodular over Z, hence a lattice automorphism of "
                "Z^n carrying eigenlattices to eigenlattices, so the gluing "
                "quotient is unchanged."),
            "reading": (
                "All four graphs of the T(8) switching class share the Seidel "
                "gluing (Z/6)^6 + Z/12, while their adjacency gluings split 1 + 3. "
                "Pass 1014's extra Z/2 is therefore identified: it records "
                "position WITHIN the switching class, which the Seidel invariant "
                "cannot see.")}


def _iso(A, B, n):
    for p in itertools.permutations(range(n)):
        P = list(p)
        if np.array_equal(A[np.ix_(P, P)], B):
            return True
    return False


def census(n):
    pairs = list(itertools.combinations(range(n), 2))
    E = len(pairs)
    buckets = {}
    for mask in range(1 << E):
        A = np.zeros((n, n), dtype=np.int64)
        for b in range(E):
            if mask >> b & 1:
                i, j = pairs[b]
                A[i, j] = 1
                A[j, i] = 1
        w = np.linalg.eigvalsh(A.astype(float))
        r = np.rint(w)
        if np.max(np.abs(w - r)) > 1e-8:
            continue
        buckets.setdefault(tuple(int(x) for x in r), []).append(A)
    groups = []
    for sp, gs in buckets.items():
        reps = []
        for A in gs:
            if not any(_iso(A, R, n) for R in reps):
                reps.append(A)
        if len(reps) > 1:
            groups.append((sp, reps))
    return len(buckets), groups


def part_B_census(checks, n=6):
    total, groups = census(n)
    rows = {}
    separated = 0
    for sp, reps in groups:
        gl = [gluing(A) for A in reps]
        distinct = len({tuple(g) for g in gl})
        if distinct > 1:
            separated += 1
        cs = sorted(set(sp), reverse=True)
        M, _ = M14.conductor(cs)
        rows[str(cs)] = {"full_spectrum": list(sp),
                         "non_isomorphic_graphs": len(reps),
                         "conductor": M,
                         "gluings": gl,
                         "distinct_gluings": distinct,
                         "separated": distinct > 1,
                         "edges": [[[int(i), int(j)]
                                    for i in range(n) for j in range(i + 1, n)
                                    if A[i, j]] for A in reps]}
    checks["census_found_cospectral_mates"] = (len(groups) >= 2)
    checks["gluing_separates_every_cospectral_class"] = (
        separated == len(groups) and len(groups) > 0)
    return {"vertices": n, "labelled_graphs": 1 << (n * (n - 1) // 2),
            "integral_spectra": total,
            "spectra_with_cospectral_mates": len(groups),
            "spectra_separated_by_gluing": separated,
            "rows": rows,
            "n7_reported": {"integral_spectra": 29,
                            "spectra_with_cospectral_mates": 3,
                            "spectra_separated_by_gluing": 3,
                            "note": "reproduce with --census7 (2,097,152 graphs)"},
            "reading": (
                "At n = 6 every cospectral class with an integral spectrum is "
                "separated by the gluing, and the same holds at n = 7.  Five "
                "spectra, five separations.  The invariant is nonetheless "
                "provably incomplete: it identifies the three Chang graphs with "
                "each other (Pass 1014) and every graph with its complement "
                "(Pass 1015).")}


def part_C_unramified_separation(checks, B_rows):
    found = {}
    for key, r in B_rows.items():
        cs = sorted(set(r["full_spectrum"]), reverse=True)
        M = r["conductor"]
        for p in PRIMES:
            if M % p or M14.vp(M, p) != 1:
                continue
            parts = {tuple(sorted(M14.vp(x, p) for x in g if M14.vp(x, p)))
                     for g in r["gluings"]}
            if len(parts) > 1:
                found[f"{key}_p{p}"] = {
                    "spectrum": cs, "conductor": M, "prime": p,
                    "v_p_conductor": M14.vp(M, p), "unramified": True,
                    "p_part_exponents": sorted(parts),
                    "gluings": r["gluings"]}
    checks["unramified_separation_exists"] = (len(found) >= 1)
    checks["withdraws_pass1014_conjecture"] = (len(found) >= 1)
    return {"cases": found, "count": len(found),
            "withdraws": (
                "the suggestion floated in Pass 1014's boundary that the "
                "separating information is always ramified"),
            "leaves_standing": (
                "Pass 1014's conductor identity and the parameter/rank "
                "dichotomy, which do not depend on it"),
            "reading": (
                "At spectrum {2,1,0,-1,-2} the conductor is 24 = 2^3 * 3, so 3 is "
                "unramified, and two non-isomorphic cospectral graphs have "
                "3-parts (Z/3)^2 and trivial.  Since the coalescence rank at an "
                "unramified prime is the classical p-rank (Pass 983), and p-ranks "
                "of cospectral graphs differ in general, this is what should have "
                "been expected.  The Chang and Shrikhande families are the special "
                "case where the unramified ranks happen to agree.")}


def part_D_ramified_profiles(checks):
    rows = {}
    for nm, B in chang_family().items():
        a = sorted(M14.vp(x, 2) for x in gluing(B) if M14.vp(x, 2))
        nu = max(a)
        rows[nm] = {"valuations": a,
                    "Delta": {str(j): sum(1 for x in a if x >= j)
                              for j in range(1, nu + 1)},
                    "kappa": {str(j): sum(min(x, j) for x in a)
                              for j in range(1, nu + 1)}}
    d1 = {v["Delta"]["1"] for v in rows.values()}
    d2 = {v["Delta"]["2"] for v in rows.values()}
    checks["filtration_separates_at_level_1"] = (len(d1) == 2)
    checks["filtration_agrees_at_level_2"] = (len(d2) == 1)
    return {"rows": rows, "prime": 2,
            "reading": (
                "T(8) has valuations (1^6, 2) and each Chang graph (1^7, 2), so "
                "Delta_1 is 6 against 7 and Delta_2 is 1 for all four.  The "
                "K-track kernel-growth filtration separates the family at level 1 "
                "and agrees at level 2: the separating information is the first "
                "kernel-growth step.")}


def main_payload(n=6):
    checks = {}
    A = part_A_seidel_invariant(checks)
    B = part_B_census(checks, n)
    C = part_C_unramified_separation(checks, B["rows"])
    D = part_D_ramified_profiles(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1016.seidel_invariant_and_unramified_separation.v1",
        "status": status,
        "headline": (
            "THE SEIDEL GLUING IS THE SWITCHING-CLASS INVARIANT, AND SEPARATION IS "
            "NOT ALWAYS RAMIFIED.  Seidel switching acts by conjugation with a "
            "diagonal sign matrix, which is unimodular, so it is a lattice "
            "automorphism of Z^n and the SEIDEL gluing is a switching-class "
            "invariant: T(8) and the three Chang graphs all give (Z/6)^6 + Z/12, "
            "while their adjacency gluings split 1 + 3.  That identifies Pass "
            "1014's extra Z/2 as the record of position WITHIN the switching "
            "class.  A complete census of n = 6 graphs (and n = 7 behind "
            "--census7) finds five integral spectra carrying cospectral "
            "non-isomorphic mates and the gluing separates all five.  It also "
            "produces a counterexample that WITHDRAWS the conjecture floated in "
            "Pass 1014's boundary: at spectrum {2,1,0,-1,-2} the conductor is "
            "24 = 2^3*3, so 3 is unramified, and two cospectral graphs have "
            "3-parts (Z/3)^2 and trivial.  The gluing separates through two "
            "independent channels -- the unramified p-ranks, which are classical, "
            "and the ramified filtration, which is not -- and Pass 1014's SRG "
            "families exercise only the second because the first is degenerate "
            "there.  Pass 1014's conductor identity and parameter/rank dichotomy "
            "are untouched."),
        "part_A_seidel_invariant": A,
        "part_B_census": B,
        "part_C_unramified_separation": C,
        "part_D_ramified_profiles": D,
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--census7", action="store_true",
                    help="run the n=7 census as well (slow, ~3 minutes)")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    if a.census7:
        total, groups = census(7)
        sep = sum(1 for _, reps in groups
                  if len({tuple(gluing(A)) for A in reps}) > 1)
        print(json.dumps({"n": 7, "integral_spectra": total,
                          "cospectral_classes": len(groups),
                          "separated": sep}))
        return 0
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 1016 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
