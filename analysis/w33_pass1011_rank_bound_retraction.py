#!/usr/bin/env python3
"""Pass 1011: retracting the rank bound of Pass 1010, and the reason it looked true.

Pass 1010 reported that the number of mod-p collision classes bounds the
coalescence rank from above -- "the rank never exceeds the class count", observed
in 6,703 of 6,703 samples.  That is false, and the counterexample is W(3,3)
itself.

THE RETRACTION.  On the adjacency operator of W(3,3) at p = 3 there is exactly
ONE collision class, {2, -4}, and the rank is 10.  Also T(8) at p = 3: one class,
rank 7.  Also T(12) at p = 5: one class, rank 11.  Three of the four canonical
examples in this repository violate the bound, and the first of them is the
object the whole programme is about.

WHY IT LOOKED TRUE.  Pass 1010 sampled spectra with n = k, that is with every
eigenvalue of multiplicity one.  For such an operator N_i = prod_{j != i}(S-c_j)
annihilates every eigenspace except the c_i line, so rank_Q(N_i) = 1, and
reduction mod p can only lower rank.  Within one collision class all the N_i
coincide mod p (their differing factors S-c_i and S-c_{i'} are congruent), so the
class contributes at most one dimension.  Summing, rank <= #classes -- but only
because each multiplicity was 1.  The "theorem" was a restatement of the sampling
design.

The correct general statement is the one Pass 983 already gave: within a class
the N_i coincide mod p, so the stack reduces to one block per class, and the rank
is the F_p rank of that reduced stack -- which for multiplicity m_i can be as
large as the eigenspace dimensions allow.  W(3,3) has multiplicities 1, 24, 15
and rank 10; the bound by class count is simply the m_i = 1 special case.

A SECOND ERROR, CAUGHT BEFORE IT LANDED.  The first attempt to test the bound at
higher multiplicity built upper-triangular integer matrices with repeated
diagonal entries and found the bound violated in 97% of cases.  That test was
invalid: such matrices are DEFECTIVE.  Checking the claimed counterexample,
spectrum [-12,-11,4,10] with multiplicities [2,1,2,2], the product
prod_i (A - c_i I) is nonzero and the geometric multiplicities are 1, 1, 1, 1
against algebraic 2, 1, 2, 2.  The k-branch hypothesis requires a diagonalisable
operator, so those 97% were not counterexamples to anything.  The refutation
above uses symmetric adjacency matrices, which are diagonalisable by
construction.

WHAT SURVIVES OF PASS 1010.  Part A is untouched: the search for the broken
constant formulas, the four targets with no expression in a 7,128-element space,
and the false-positive analysis.  Part B's numbers are also correct as reported
-- the rank never exceeded the class count in that sample -- but the general
claim drawn from them is withdrawn.

BOUNDARY.  This retracts a bound; it does not replace it with another.  Whether
some function of the class structure and the multiplicities bounds the rank is
open, and the m_i = 1 case is the only one where a clean bound is known.
"""
from __future__ import annotations

import argparse
import functools
import importlib.util
import itertools
import json
import random
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1011_rank_bound_retraction.json"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"


def rank_p(M, p):
    M = [[int(x) % p for x in r] for r in M]
    rows = len(M)
    cols = len(M[0]) if rows else 0
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                fq = M[i][c]
                M[i] = [(M[i][j] - fq * M[r][j]) % p for j in range(cols)]
        r += 1
    return r


def triangular(m):
    prs = list(itertools.combinations(range(m), 2))
    n = len(prs)
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            if a != b and set(prs[a]) & set(prs[b]):
                A[a, b] = 1
    return A


def w33():
    spec = importlib.util.spec_from_file_location("w33_pass682_base", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pts, edges, tris, K, d1, d2 = mod.build()
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    return A


def coalescence(A, cs, p):
    n = A.shape[0]
    Ao = A.astype(object)
    I = np.eye(n, dtype=object)
    Ds = []
    for c in cs:
        D = 1
        for d in cs:
            if d != c:
                D *= (c - d)
        Ds.append(abs(D))
    keep = [functools.reduce(lambda Y, d: Y @ (Ao - d * I),
                             [d for d in cs if d != c], I.copy())
            for c, D in zip(cs, Ds) if D % p == 0]
    return rank_p(np.vstack(keep).tolist(), p) if keep else 0


def classes(cs, p):
    g = {}
    for c in cs:
        g.setdefault(c % p, []).append(c)
    return [x for x in g.values() if len(x) > 1]


def part_A_refutation(checks):
    rows = {}
    violations = 0
    cases = [("W(3,3)", w33(), [12, 2, -4], 3, [1, 24, 15]),
             ("W(3,3)", w33(), [12, 2, -4], 5, [1, 24, 15]),
             ("T(8)", triangular(8), [12, 4, -2], 3, [1, 7, 20]),
             ("T(12)", triangular(12), [20, 8, -2], 5, [1, 11, 54])]
    for nm, A, cs, p, mult in cases:
        cl = classes(cs, p)
        rk = coalescence(A, cs, p)
        bad = rk > len(cl)
        if bad:
            violations += 1
        rows[f"{nm}_p{p}"] = {"graph": nm, "prime": p, "spectrum": cs,
                              "multiplicities": mult,
                              "num_collision_classes": len(cl),
                              "rank": rk, "bound_violated": bad}
    checks["w33_violates_the_bound"] = rows["W(3,3)_p3"]["bound_violated"]
    checks["multiple_canonical_violations"] = (violations >= 3)
    return {"rows": rows, "violations": violations,
            "retracts": "Pass 1010 part B, 'rank never exceeds the class count'",
            "reading": (
                "W(3,3) at p = 3 has one collision class and rank 10; T(8) has "
                "one and rank 7; T(12) has one and rank 11.  Three of the four "
                "canonical examples in this repository break the bound, and the "
                "first is the object the programme is about.")}


def part_B_why_it_looked_true(checks):
    """With all multiplicities 1, rank_Q(N_i) = 1 and the bound is automatic."""
    random.seed(1011)
    ok = True
    checked = 0
    for _ in range(400):
        k = random.choice([5, 6])
        cs = sorted(random.sample(range(-12, 13), k))
        n = k                                   # multiplicity 1 everywhere
        A = np.zeros((n, n), dtype=np.int64)
        for i, c in enumerate(cs):
            A[i, i] = c
            for j in range(i + 1, n):
                A[i, j] = random.randint(-2, 2)
        Ao = A.astype(object)
        I = np.eye(n, dtype=object)
        for c in cs:
            N = functools.reduce(lambda Y, d: Y @ (Ao - d * I),
                                 [d for d in cs if d != c], I.copy())
            rq = np.linalg.matrix_rank(np.array(N, dtype=float), tol=1e-6)
            if rq > 1:
                ok = False
            checked += 1
    checks["multiplicity_one_gives_rank_one_N"] = ok
    return {"branch_operators_checked": checked,
            "all_rank_one_over_Q": ok,
            "explanation": (
                "with every multiplicity 1, N_i annihilates all eigenspaces but "
                "the c_i line, so rank_Q(N_i) = 1; reduction mod p only lowers "
                "rank, and within a class the N_i coincide mod p, so each class "
                "contributes at most one dimension.  rank <= #classes is then "
                "automatic -- a restatement of the sampling design, not a "
                "theorem."),
            "reading": (
                "Every branch operator in a multiplicity-one spectrum has "
                "rational rank exactly 1, which is why Pass 1010's sample could "
                "not have produced a counterexample.")}


def part_C_invalid_first_attempt(checks):
    cs = [-12, -11, 4, 10]
    mult = [2, 1, 2, 2]
    diag = []
    for c, m in zip(cs, mult):
        diag += [c] * m
    n = len(diag)
    random.seed(11)
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        A[i, i] = diag[i]
        for j in range(i + 1, n):
            A[i, j] = random.randint(-2, 2)
    Ao = A.astype(object)
    I = np.eye(n, dtype=object)
    P = functools.reduce(lambda Y, c: Y @ (Ao - c * I), cs, I.copy())
    diagonalisable = int(np.max(np.abs(P))) == 0
    geo = {str(c): int(n - np.linalg.matrix_rank((A - c * np.eye(n)).astype(float),
                                                 tol=1e-8)) for c in cs}
    checks["first_attempt_was_defective"] = (not diagonalisable)
    return {"spectrum": cs, "algebraic_multiplicities": mult,
            "geometric_multiplicities": geo,
            "minimal_polynomial_vanishes": diagonalisable,
            "verdict": ("upper-triangular matrices with repeated diagonal entries "
                        "are defective, so the k-branch hypothesis fails and the "
                        "97% 'violations' found that way were not counterexamples"),
            "reading": (
                "The first attempt to break the bound used non-diagonalisable "
                "matrices and had to be discarded.  The refutation that stands "
                "uses symmetric adjacency matrices, diagonalisable by "
                "construction.")}


def main_payload():
    checks = {}
    A = part_A_refutation(checks)
    B = part_B_why_it_looked_true(checks)
    C = part_C_invalid_first_attempt(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1011.rank_bound_retraction.v1",
        "status": status,
        "headline": (
            "RETRACTING PASS 1010'S RANK BOUND: W(3,3) IS THE COUNTEREXAMPLE.  "
            "Pass 1010 reported that the mod-p collision-class count bounds the "
            "coalescence rank, on 6,703 of 6,703 samples.  It is false: W(3,3) at "
            "p = 3 has ONE collision class and rank 10, T(8) has one and rank 7, "
            "T(12) has one and rank 11.  The bound held in that sample only "
            "for multiplicity-one spectra, where each branch operator has "
            "rational rank 1 and the bound follows trivially -- a restatement of the "
            "sampling design.  A first attempt to break it at higher multiplicity "
            "was itself invalid, using upper-triangular matrices with repeated "
            "eigenvalues, which are defective and violate the k-branch "
            "diagonalisability hypothesis; the standing refutation uses symmetric "
            "adjacency matrices.  Pass 1010's Part A -- the constant "
            "re-derivation search and its false-positive analysis -- is "
            "untouched."),
        "part_A_refutation": A,
        "part_B_why_it_looked_true": B,
        "part_C_invalid_first_attempt": C,
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
            raise SystemExit("Pass 1011 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
