#!/usr/bin/env python3
"""Pass 1017: one criterion for the whole pencil, and a scope correction to Pass 1015.

Pass 1015 proved the gluing group is invariant under complementation and Pass
1016 proved the Seidel gluing is a switching-class invariant.  Both are special
cases of a single statement about the pencil

    B  =  alpha A  +  beta J  +  gamma I,     alpha != 0,

and stating it that way both fixes an error in Pass 1015 and explains an
observation Pass 1016 left unexplained.

THE CRITERION.  Let G be k-regular on n vertices with the all-ones vector 1.
Since J1 = n1 and J vanishes on 1-perp, B acts on 1-perp as alpha A + gamma I and
on the line Q1 as the scalar alpha k + beta n + gamma.  So B and A have the same
eigenVECTORS always, and the eigenSPACE DECOMPOSITION is preserved exactly when
the induced relabelling stays injective:

    on 1-perp:  c |-> alpha c + gamma          (c an eigenvalue of A, c != k)
    on Q1:      k |-> alpha k + beta n + gamma

These collide iff alpha k + beta n = alpha c for some eigenvalue c != k, that is
iff k + beta n / alpha is an eigenvalue of A.  Hence:

    THE GLUING OF B EQUALS THE GLUING OF A  <==>  mult(k) = 1  AND
                                                  k + beta n / alpha is not an
                                                  eigenvalue of A other than k.

The multiplicity condition is the same phenomenon at the other end: if mult(k) >
1 then 1 does not span the k-eigenspace, and the eigenspace SPLITS under B
rather than merging.  For a regular graph mult(k) = 1 is equivalent to
connectedness.

THE TWO INSTANCES.

    complement   Abar = -A + J - I     (alpha,beta,gamma) = (-1,1,-1)
                 condition: k - n is not an eigenvalue
    Seidel       S    = -2A + J - I    (alpha,beta,gamma) = (-2,1,-1)
                 condition: k - n/2 is not an eigenvalue

and both are confirmed by the data Pass 1016 already had but did not explain:

    W(3,3)   k - n/2 = 12 - 20 = -8, not an eigenvalue  ->  Seidel gluing EQUALS
             adjacency gluing, and indeed both are (Z/2)^6 + (Z/6)^9 + Z/120
    T(8)     k - n/2 = 12 - 14 = -2, IS an eigenvalue   ->  they must differ, and
             indeed (Z/6)^6 + Z/12 against (Z/6)^6 + Z/84
    L2(4)    k - n/2 =  6 -  8 = -2, IS an eigenvalue   ->  they must differ, and
             indeed Z/2 + (Z/4)^4 + Z/8 against (Z/4)^5 + Z/16

So Pass 1016's finding that the Seidel gluing is coarser is not a fact about
Seidel matrices; it is the collision k = n/2 + s, which happens to hold for both
exceptional SRG families and fails for W(3,3).

THE CORRECTION TO PASS 1015.  That pass stated complementation invariance "for a
k-regular graph G on n vertices" with no further hypothesis.  That is false as
written.  A census of all n = 6 graphs with integral spectrum on both sides, 172
regular cases, finds the gluing invariant in only 120 of them -- 70%.  Adding
the two conditions above splits the census exactly:

    hypothesis holds:   120 graphs, invariant in 120   (100%)
    hypothesis fails:    52 graphs, invariant in   0   (  0%)

a perfect iff, in both directions.  K(3,3) is the witness for the collision
condition: spectrum [3,0,0,0,0,-3], k - n = -3 IS an eigenvalue, so n-1-k = 2
equals -1-(-3) and two eigenspaces MERGE in the complement 2K3.  The 26
disconnected cases are the witnesses for the multiplicity condition.

WHAT SURVIVES.  Every graph Pass 1015 actually tested satisfies the hypothesis
-- W(3,3) has k - n = -28, L2(4) has -10, T(8) has -16, none an eigenvalue -- so
its verifications, the sharpened support bound and the forced-vanishing
prediction are all unaffected.  Only the statement of the proposition was too
broad, in both this file's predecessor and in w33_paper.tex, and both are
corrected.

BOUNDARY.  The criterion is proved above and the iff is verified by complete
census at n = 6 only; that the converse holds in general is not proved here,
though the mechanism (split, or merge) accounts for both directions.  The
census requires integral spectra on both sides, which is why no non-regular
graph appears in it: at n = 6 there are none.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1017_affine_pencil_stability.json"
P1014 = ROOT / "analysis" / "w33_pass1014_ramified_prime_separates_cospectral.py"
BASE = ROOT / "analysis" / "w33_pass682_flatblock_h1_branch_separation.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M14 = _load(P1014, "w33_pass1014")


def spectrum(A):
    return sorted({int(round(x)) for x in np.linalg.eigvalsh(A.astype(float))},
                  reverse=True)


def full_spectrum(A):
    return [int(round(x)) for x in np.linalg.eigvalsh(A.astype(float))]


def gluing(A):
    n = A.shape[0]
    stacked = []
    for c in spectrum(A):
        stacked += M14.hnf_kernel(A - c * np.eye(n, dtype=np.int64))
    return [x for x in M14.invariant_factors(stacked) if x not in (0, 1)]


def pencil(A, alpha, beta, gamma):
    n = A.shape[0]
    return (alpha * A + beta * np.ones((n, n), dtype=np.int64)
            + gamma * np.eye(n, dtype=np.int64))


def criterion(A, alpha, beta):
    """mult(k)=1 and k + beta*n/alpha not an eigenvalue other than k."""
    n = A.shape[0]
    ev = full_spectrum(A)
    k = int(A.sum(1)[0])
    if ev.count(k) != 1:
        return False, None
    t = Fraction(k) + Fraction(beta * n, alpha)
    collide = (t.denominator == 1 and int(t) in set(ev) and int(t) != k)
    return (not collide), (int(t) if t.denominator == 1 else float(t))


def rook(m):
    V = [(i, j) for i in range(m) for j in range(m)]
    n = m * m
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            if a != b and (V[a][0] == V[b][0] or V[a][1] == V[b][1]):
                A[a, b] = 1
    return A


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
    mod = _load(BASE, "w33_pass682_base")
    pts, edges, tris, K, d1, d2 = mod.build()
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    return A


def part_A_pencil_criterion(checks):
    """Both instances, on the three canonical graphs, prediction vs fact."""
    graphs = {"W(3,3)": w33(), "T(8)": triangular(8), "L2(4)": rook(4)}
    instances = {"complement": (-1, 1, -1), "seidel": (-2, 1, -1)}
    rows = {}
    allok = True
    for gname, A in graphs.items():
        gA = gluing(A)
        for iname, (al, be, ga) in instances.items():
            pred, thresh = criterion(A, al, be)
            gB = gluing(pencil(A, al, be, ga))
            fact = (gA == gB)
            ok = (pred == fact)
            allok &= ok
            rows[f"{gname}_{iname}"] = {
                "graph": gname, "instance": iname,
                "pencil": {"alpha": al, "beta": be, "gamma": ga},
                "threshold_k_plus_beta_n_over_alpha": thresh,
                "threshold_is_an_eigenvalue": (thresh in spectrum(A)),
                "predicted_gluing_preserved": pred,
                "actual_gluing_preserved": fact,
                "prediction_correct": ok,
                "gluing_A": gA, "gluing_B": gB}
    checks["pencil_criterion_predicts_every_case"] = allok
    checks["w33_seidel_equals_adjacency"] = rows["W(3,3)_seidel"]["actual_gluing_preserved"]
    checks["t8_seidel_differs"] = not rows["T(8)_seidel"]["actual_gluing_preserved"]
    checks["l24_seidel_differs"] = not rows["L2(4)_seidel"]["actual_gluing_preserved"]
    return {"rows": rows,
            "criterion": (
                "B = alpha A + beta J + gamma I has the same saturated "
                "eigenlattice decomposition as A iff mult(k) = 1 and "
                "k + beta n / alpha is not an eigenvalue of A other than k"),
            "reading": (
                "Six predictions, six correct.  W(3,3) has k - n/2 = -8, not an "
                "eigenvalue, so its Seidel gluing EQUALS its adjacency gluing, "
                "both (Z/2)^6 + (Z/6)^9 + Z/120.  T(8) and L2(4) both have "
                "k - n/2 = -2, which IS an eigenvalue, so theirs must differ, and "
                "they do.  Pass 1016's 'the Seidel gluing is coarser' is therefore "
                "not a fact about Seidel matrices but the collision k = n/2 + s, "
                "which both exceptional SRG families happen to satisfy.")}


def part_B_census_iff(checks):
    """Complete n=6 census: the criterion splits it perfectly, both directions."""
    n = 6
    prs = list(itertools.combinations(range(n), 2))
    E = len(prs)
    tab = {True: [0, 0], False: [0, 0]}
    disconnected = 0
    collided = 0
    for mask in range(1 << E):
        A = np.zeros((n, n), dtype=np.int64)
        for b in range(E):
            if mask >> b & 1:
                i, j = prs[b]
                A[i, j] = 1
                A[j, i] = 1
        w = np.linalg.eigvalsh(A.astype(float))
        if np.max(np.abs(w - np.rint(w))) > 1e-8:
            continue
        if len(set(A.sum(1).tolist())) != 1:
            continue
        C = pencil(A, -1, 1, -1)
        wc = np.linalg.eigvalsh(C.astype(float))
        if np.max(np.abs(wc - np.rint(wc))) > 1e-8:
            continue
        pred, thresh = criterion(A, -1, 1)
        ev = full_spectrum(A)
        k = int(A.sum(1)[0])
        if ev.count(k) != 1:
            disconnected += 1
        elif not pred:
            collided += 1
        t = tab[pred]
        t[0] += 1
        t[1] += (gluing(A) == gluing(C))
    perfect = (tab[True][0] == tab[True][1] and tab[True][0] > 0
               and tab[False][1] == 0 and tab[False][0] > 0)
    checks["census_is_a_perfect_iff"] = perfect
    checks["both_failure_modes_occur"] = (disconnected > 0 and collided > 0)
    return {"vertices": n,
            "hypothesis_holds": {"graphs": tab[True][0], "invariant": tab[True][1]},
            "hypothesis_fails": {"graphs": tab[False][0], "invariant": tab[False][1]},
            "failures_by_multiplicity": disconnected,
            "failures_by_collision": collided,
            "perfect_iff": perfect,
            "reading": (
                "Of 172 regular graphs on six vertices with integral spectrum on "
                "both sides, the gluing is complementation-invariant in exactly "
                "the 120 satisfying the criterion and in none of the other 52.  "
                "Both failure modes are realised: disconnected graphs split the "
                "k-eigenspace, and K(3,3) merges two eigenspaces because "
                "k - n = -3 is an eigenvalue.")}


def part_C_correction(checks):
    """Pass 1015's verifications survive; only the statement was too broad."""
    rows = {}
    for nm, A in (("W(3,3)", w33()), ("L2(4)", rook(4)), ("L2(5)", rook(5)),
                  ("T(6)", triangular(6)), ("T(8)", triangular(8))):
        n = A.shape[0]
        k = int(A.sum(1)[0])
        ev = spectrum(A)
        rows[nm] = {"n": n, "k": k, "spectrum": ev, "k_minus_n": k - n,
                    "k_minus_n_is_an_eigenvalue": (k - n) in ev,
                    "hypothesis_satisfied": criterion(A, -1, 1)[0]}
    allsafe = all(v["hypothesis_satisfied"] for v in rows.values())
    checks["pass1015_examples_all_satisfy_the_hypothesis"] = allsafe
    return {"rows": rows,
            "corrects": (
                "Pass 1015 proposition and w33_paper.tex prop:complementation, "
                "which asserted invariance for any k-regular graph"),
            "survives": (
                "every verification in Pass 1015, its sharpened support bound and "
                "its forced-vanishing prediction, since all five graphs tested "
                "satisfy the corrected hypothesis"),
            "reading": (
                "W(3,3) has k - n = -28, L2(4) -10, L2(5) -16, T(6) -7, T(8) -16, "
                "and none of these is an eigenvalue of its graph, so the results "
                "stand exactly as computed.  The proposition was stated more "
                "broadly than it holds, and that is what is corrected.")}


def main_payload():
    checks = {}
    A = part_A_pencil_criterion(checks)
    B = part_B_census_iff(checks)
    C = part_C_correction(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1017.affine_pencil_stability.v1",
        "status": status,
        "headline": (
            "ONE CRITERION GOVERNS THE WHOLE PENCIL alpha A + beta J + gamma I, "
            "AND IT CORRECTS PASS 1015.  Since J acts as n on the all-ones vector "
            "and as zero on its complement, B = alpha A + beta J + gamma I always "
            "shares A's eigenvectors, and the eigenLATTICE decomposition -- hence "
            "the gluing -- is preserved exactly when mult(k) = 1 and "
            "k + beta n / alpha is not an eigenvalue of A.  Complementation is "
            "(alpha,beta) = (-1,1) giving the threshold k - n; Seidel is (-2,1) "
            "giving k - n/2.  Six predictions on three canonical graphs, six "
            "correct: W(3,3) has k - n/2 = -8, not an eigenvalue, so its SEIDEL "
            "gluing EQUALS its adjacency gluing, both (Z/2)^6 + (Z/6)^9 + Z/120; "
            "T(8) and L2(4) both have k - n/2 = -2, an eigenvalue, so theirs "
            "differ.  Pass 1016's 'the Seidel gluing is coarser' is thus not a "
            "fact about Seidel matrices but a collision those two families happen "
            "to have.  The criterion also CORRECTS Pass 1015, which claimed "
            "complementation invariance for every k-regular graph: a complete n=6 "
            "census finds it holds in only 120 of 172 cases, and the criterion "
            "splits them perfectly -- 120 of 120 where it holds, 0 of 52 where it "
            "fails, with K(3,3) merging and disconnected graphs splitting.  Every "
            "graph Pass 1015 actually tested satisfies the hypothesis, so its "
            "verifications, support bound and forced-vanishing prediction all "
            "stand; only the statement was too broad."),
        "part_A_pencil_criterion": A,
        "part_B_census_iff": B,
        "part_C_correction": C,
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
            raise SystemExit("Pass 1017 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
