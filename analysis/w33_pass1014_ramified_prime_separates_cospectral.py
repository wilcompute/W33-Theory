#!/usr/bin/env python3
"""Pass 1014: the conductor is a parameter polynomial; the separating power is ramified.

Two facts about the gluing group meet here, and together they say where its
information actually lives.

PART A -- THE CONDUCTOR IS A POLYNOMIAL IN THE SRG PARAMETERS.

For a strongly regular graph with parameters (n, k, lambda, mu) the eigenvalues
r, s satisfy r + s = lambda - mu and rs = -(k - mu), so every pairwise gap is a
parameter expression:

    (k - r)(k - s) = k^2 - k(lambda - mu) - (k - mu)
    r - s          = sqrt((lambda - mu)^2 + 4(k - mu))

and therefore the k-branch conductor M = lcm(D_k, D_r, D_s), with
D_k = (k-r)(k-s), D_r = (r-k)(r-s), D_s = (s-k)(s-r), is a function of the
parameters alone.  Verified against the direct computation on ten SRGs; W(3,3)
gives D_k = 144 - 24 + 48 - 12 + 4 = 160 and M = 480, matching Pass 826.

The consequence is that the SET OF PRIMES that can carry gluing is determined by
(n, k, lambda, mu).  Nothing about the graph beyond its parameter set is needed
to know where to look.

PART B -- BUT THE GLUING ITSELF IS NOT PARAMETER-DETERMINED.

T(8) and the three Chang graphs all have parameters (28, 12, 6, 4) and spectrum
{12^1, 4^7, (-2)^20}.  They are pairwise non-isomorphic.  Their gluings:

    T(8)      Z^28 / (L_12 + L_4 + L_-2)  =  (Z/6)^6 + Z/84
    Chang 1   Z^28 / (L_12 + L_4 + L_-2)  =  Z/2 + (Z/6)^6 + Z/84
    Chang 2   same as Chang 1
    Chang 3   same as Chang 1

So the gluing is a strictly finer invariant than the parameter set: it separates
T(8) from its switching class.  It is also strictly coarser than isomorphism,
since the three Chang graphs share a gluing -- which is the expected answer, as
they share a 2-rank.

PART C -- THE SEPARATION IS ENTIRELY AT THE RAMIFIED PRIME.

M = 336 = 2^4 * 3 * 7 here, so p = 3 and p = 7 are unramified (v_p(M) = 1) and
p = 2 is ramified (v_2(M) = 4).  At the unramified primes the coalescence
theorem of Pass 828 applies and gives the p-part as a single F_p rank; those
ranks are 7 and 1, IDENTICAL for all four graphs, and they match the 3-part
(Z/3)^7 and 7-part Z/7 read off the Smith form.  The whole difference sits in
the 2-part:

    T(8)     2-part = (Z/2)^6 + Z/4     order 2^8
    Chang    2-part = (Z/2)^7 + Z/4     order 2^9

This is the reading worth keeping.  The unramified part of the gluing is
computed by one rank and agreed across the family; the ramified part -- the part
that needs the kernel-growth filtration rather than a single rank -- is the part
that distinguishes.  Ramification is not a technical complication in this
theory, it is where the invariant's discriminating power is.

A TRAP, RE-ENTERED AND CAUGHT.  The first computation here cleared denominators
from sympy's rational nullspace with one global lcm and read a Smith form off
the result.  That produced four wildly different answers (invariant factors
running to 24 terms) and they were all artefacts: an UNSATURATED lattice has a
basis-dependent Smith form.  This is precisely the error Pass 808 retracted from
Pass 676.  The computation that stands takes the genuine integer kernel by
row-HNF of [B^T | I], which is saturated by construction, and VERIFIES
saturation by checking that each basis matrix has all invariant factors 1.  The
kernel dimensions 1, 7, 20 independently match the SRG multiplicity formula.

BOUNDARY.  Part A is an identity, checked on ten parameter sets.  Parts B and C
are one family, (28, 12, 6, 4); that the separating information is always
ramified is suggested here, not proved.  The gluing does not separate the three
Chang graphs, so it is not a complete invariant.
"""
from __future__ import annotations

import argparse
import functools
import itertools
import json
from math import gcd, isqrt
from pathlib import Path

import numpy as np
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1014_ramified_prime_separates_cospectral.json"

FAMILIES = [(40, 12, 2, 4), (28, 12, 6, 4), (66, 20, 10, 4), (16, 6, 2, 2),
            (64, 18, 2, 6), (81, 16, 7, 2), (100, 22, 0, 6), (36, 14, 4, 6),
            (45, 12, 3, 3), (50, 21, 8, 9)]


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def conductor(cs):
    """M = lcm_i D_i with D_i = prod_{j != i} (c_i - c_j)."""
    Ds = []
    for c in cs:
        D = 1
        for d in cs:
            if d != c:
                D *= (c - d)
        Ds.append(abs(D))
    M = 1
    for D in Ds:
        M = lcm(M, D)
    return M, Ds


def vp(x, p):
    v = 0
    while x and x % p == 0:
        x //= p
        v += 1
    return v


def part_A_conductor_from_parameters(checks):
    """(k-r)(k-s) = k^2 - k(lam-mu) - (k-mu): the conductor is a parameter polynomial."""
    rows = {}
    allok = True
    for (n, k, lam, mu) in FAMILIES:
        disc = (lam - mu) ** 2 + 4 * (k - mu)
        d = isqrt(disc)
        if d * d != disc:
            continue
        r = ((lam - mu) + d) // 2
        s = ((lam - mu) - d) // 2
        Dk_param = k * k - k * (lam - mu) - (k - mu)      # parameters only
        Dr = abs((r - k) * (r - s))
        Ds = abs((s - k) * (s - r))
        M_param = lcm(lcm(abs(Dk_param), Dr), Ds)
        M_direct, Ds_direct = conductor([k, r, s])
        ok = (M_param == M_direct) and (abs(Dk_param) == Ds_direct[0])
        allok &= ok
        rows[f"SRG({n},{k},{lam},{mu})"] = {
            "r": r, "s": s, "D_k_from_parameters": abs(Dk_param),
            "D_k_direct": Ds_direct[0], "M_from_parameters": M_param,
            "M_direct": M_direct, "agree": ok}
    checks["conductor_is_a_parameter_polynomial"] = allok
    checks["w33_conductor_is_480"] = (rows["SRG(40,12,2,4)"]["M_direct"] == 480)
    return {"rows": rows, "families": len(rows),
            "identity": "(k-r)(k-s) = k^2 - k(lambda-mu) - (k-mu)",
            "reading": (
                "Because r+s = lambda-mu and rs = -(k-mu), every pairwise "
                "eigenvalue gap is a parameter expression, so the conductor M -- "
                "and hence the set of primes that CAN carry gluing -- is "
                "determined by (n, k, lambda, mu) alone.  Checked against direct "
                "computation on ten parameter sets, W(3,3) included at M = 480.")}


def hnf_kernel(B):
    """Z-basis of ker(B) by row-HNF of [B^T | I].  Saturated by construction."""
    n = B.shape[0]
    BT = B.T
    aug = [[int(x) for x in BT[i]] + [1 if j == i else 0 for j in range(n)]
           for i in range(n)]
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if aug[i][c]), None)
        if piv is None:
            continue
        aug[r], aug[piv] = aug[piv], aug[r]
        for i in range(r + 1, n):
            while aug[i][c]:                       # gcd elimination, stays integral
                q = aug[r][c] // aug[i][c]
                aug[r] = [a - q * b for a, b in zip(aug[r], aug[i])]
                aug[r], aug[i] = aug[i], aug[r]
        r += 1
    return [row[n:] for row in aug if not any(row[:n])]


def invariant_factors(rows):
    S = smith_normal_form(Matrix(rows))
    return [int(S[i, i]) for i in range(min(S.shape))]


def triangular(m):
    prs = list(itertools.combinations(range(m), 2))
    n = len(prs)
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            if a != b and set(prs[a]) & set(prs[b]):
                A[a, b] = 1
    return A, prs


def switch(A, S):
    """Seidel switching of A with respect to the vertex subset S."""
    B = A.copy()
    n = A.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and ((i in S) != (j in S)):
                B[i, j] = 1 - A[i, j]
    return B


def chang_family():
    A, prs = triangular(8)
    idx = {e: i for i, e in enumerate(prs)}
    spec = {
        "T(8)": [],
        "Chang-1": [(0, 1), (2, 3), (4, 5), (6, 7)],                 # perfect matching
        "Chang-2": [(0, 1), (1, 2), (2, 0),
                    (3, 4), (4, 5), (5, 6), (6, 7), (7, 3)],         # C3 + C5
        "Chang-3": [(i, (i + 1) % 8) for i in range(8)],             # C8
    }
    out = {}
    for nm, edges in spec.items():
        S = {idx[tuple(sorted(e))] for e in edges}
        out[nm] = A if not edges else switch(A, S)
    return out


def part_B_gluing_separates(checks):
    cs = [12, 4, -2]
    graphs = chang_family()
    rows = {}
    for nm, B in graphs.items():
        ev = sorted({int(round(x)) for x in np.linalg.eigvalsh(B.astype(float))},
                    reverse=True)
        stacked = []
        dims = []
        saturated = True
        for c in cs:
            K = hnf_kernel(B - c * np.eye(B.shape[0], dtype=np.int64))
            dims.append(len(K))
            if set(invariant_factors(K)) - {1}:
                saturated = False
            stacked += K
        d = [x for x in invariant_factors(stacked) if x not in (0, 1)]
        order = 1
        for x in d:
            order *= x
        rows[nm] = {"spectrum": ev, "kernel_dims": dims,
                    "kernels_saturated": saturated,
                    "gluing_invariant_factors": d, "gluing_order": order}
    distinct = {tuple(v["gluing_invariant_factors"]) for v in rows.values()}
    chang = {tuple(rows[k]["gluing_invariant_factors"])
             for k in ("Chang-1", "Chang-2", "Chang-3")}
    checks["all_kernels_saturated"] = all(v["kernels_saturated"]
                                          for v in rows.values())
    checks["multiplicities_are_1_7_20"] = all(v["kernel_dims"] == [1, 7, 20]
                                              for v in rows.values())
    checks["cospectral"] = len({tuple(v["spectrum"]) for v in rows.values()}) == 1
    checks["gluing_separates_T8_from_chang"] = (
        rows["T(8)"]["gluing_invariant_factors"]
        != rows["Chang-1"]["gluing_invariant_factors"])
    checks["chang_graphs_share_a_gluing"] = (len(chang) == 1)
    checks["exactly_two_gluings"] = (len(distinct) == 2)
    return {"rows": rows, "distinct_gluings": len(distinct),
            "reading": (
                "T(8) and the three Chang graphs share parameters (28,12,6,4) and "
                "the full spectrum, and are pairwise non-isomorphic.  T(8) glues "
                "to (Z/6)^6 + Z/84; all three Chang graphs glue to Z/2 + (Z/6)^6 "
                "+ Z/84.  The gluing is therefore strictly finer than the "
                "parameter set and strictly coarser than isomorphism.  Kernel "
                "dimensions 1, 7, 20 match the SRG multiplicity formula and every "
                "kernel is verified saturated.")}


def rank_p(M, p):
    M = [[int(x) % p for x in r] for r in M]
    R = len(M)
    C = len(M[0]) if R else 0
    r = 0
    for c in range(C):
        piv = next((i for i in range(r, R) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(R):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(C)]
        r += 1
    return r


def coalescence(A, cs, p):
    n = A.shape[0]
    Ao = A.astype(object)
    I = np.eye(n, dtype=object)
    keep = []
    for c in cs:
        D = 1
        for d in cs:
            if d != c:
                D *= (c - d)
        if D % p == 0:
            keep.append(functools.reduce(lambda Y, d: Y @ (Ao - d * I),
                                         [d for d in cs if d != c], I.copy()))
    return rank_p(np.vstack(keep).tolist(), p) if keep else 0


def p_part(factors, p):
    return sorted(vp(x, p) for x in factors if vp(x, p))


def part_C_separation_is_ramified(checks, B_rows):
    cs = [12, 4, -2]
    M, _ = conductor(cs)
    ram = {p: vp(M, p) for p in (2, 3, 7)}
    graphs = chang_family()
    rows = {}
    for nm, B in graphs.items():
        fac = B_rows[nm]["gluing_invariant_factors"]
        rows[nm] = {
            "coalescence_rank_p3": coalescence(B, cs, 3),
            "coalescence_rank_p7": coalescence(B, cs, 7),
            "gluing_2_part_exponents": p_part(fac, 2),
            "gluing_3_part_exponents": p_part(fac, 3),
            "gluing_7_part_exponents": p_part(fac, 7)}
    unram_same = (len({(v["coalescence_rank_p3"], v["coalescence_rank_p7"])
                       for v in rows.values()}) == 1)
    three_same = len({tuple(v["gluing_3_part_exponents"]) for v in rows.values()}) == 1
    seven_same = len({tuple(v["gluing_7_part_exponents"]) for v in rows.values()}) == 1
    two_differs = (rows["T(8)"]["gluing_2_part_exponents"]
                   != rows["Chang-1"]["gluing_2_part_exponents"])
    rank3_matches = all(len(v["gluing_3_part_exponents"]) == v["coalescence_rank_p3"]
                        for v in rows.values())
    rank7_matches = all(len(v["gluing_7_part_exponents"]) == v["coalescence_rank_p7"]
                        for v in rows.values())
    checks["conductor_336_ramified_only_at_2"] = (
        M == 336 and ram[2] == 4 and ram[3] == 1 and ram[7] == 1)
    checks["unramified_ranks_agree_across_family"] = unram_same
    checks["unramified_parts_agree"] = (three_same and seven_same)
    checks["coalescence_rank_matches_gluing_p_part"] = (rank3_matches and rank7_matches)
    checks["ramified_part_is_what_differs"] = two_differs
    return {"conductor": M, "valuations": ram, "rows": rows,
            "reading": (
                "M = 336 = 2^4 * 3 * 7, so 3 and 7 are unramified and 2 is "
                "ramified with v_2 = 4.  At the unramified primes the Pass 828 "
                "coalescence theorem gives the p-part as a single F_p rank; those "
                "ranks are 7 and 1 and are IDENTICAL for all four graphs, matching "
                "the (Z/3)^7 and Z/7 read off the Smith form.  The entire "
                "difference is in the 2-part: (Z/2)^6 + Z/4 for T(8) against "
                "(Z/2)^7 + Z/4 for the Chang graphs.  The unramified part is one "
                "rank and is shared; the ramified part -- the part that needs the "
                "kernel-growth filtration rather than a rank -- is the part that "
                "distinguishes.")}


def main_payload():
    checks = {}
    A = part_A_conductor_from_parameters(checks)
    B = part_B_gluing_separates(checks)
    C = part_C_separation_is_ramified(checks, B["rows"])
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1014.ramified_prime_separates_cospectral.v1",
        "status": status,
        "headline": (
            "THE CONDUCTOR IS A PARAMETER POLYNOMIAL, BUT THE GLUING'S "
            "DISCRIMINATING POWER LIVES ENTIRELY AT THE RAMIFIED PRIME.  Since "
            "r+s = lambda-mu and rs = -(k-mu), the conductor M = lcm(D_k,D_r,D_s) "
            "with D_k = k^2 - k(lambda-mu) - (k-mu) is a function of the SRG "
            "parameters alone -- verified on ten families, W(3,3) at M = 480 -- so "
            "the primes that CAN carry gluing are parameter-determined.  The "
            "gluing itself is not: T(8) and the three Chang graphs share "
            "(28,12,6,4) and the full spectrum {12,4^7,(-2)^20} yet T(8) glues to "
            "(Z/6)^6 + Z/84 while all three Chang graphs glue to Z/2 + (Z/6)^6 + "
            "Z/84.  And the difference is exactly at the ramified prime: "
            "M = 336 = 2^4*3*7, the unramified coalescence ranks are 7 and 1 for "
            "all four graphs and match the 3- and 7-parts exactly, while the "
            "2-parts are (Z/2)^6 + Z/4 against (Z/2)^7 + Z/4.  Ramification is not "
            "a technical complication in this theory; it is where the information "
            "is.  The gluing is strictly finer than the parameter set and strictly "
            "coarser than isomorphism, since the three Chang graphs share it."),
        "part_A_conductor_from_parameters": A,
        "part_B_gluing_separates": B,
        "part_C_separation_is_ramified": C,
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
            raise SystemExit("Pass 1014 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
