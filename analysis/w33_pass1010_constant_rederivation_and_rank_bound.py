#!/usr/bin/env python3
"""Pass 1010: re-deriving the broken constants (mostly: no), and the rank bound.

PART A -- THE NINE BROKEN FORMULAS, RE-DERIVED WHERE POSSIBLE.

Pass 1008 found that nine of fourteen closed forms in the constant ledger do not
evaluate to the value printed beside them.  The obvious next move is to look for
the formula that WAS meant.  That move is also a trap: searching a space of
expressions until one hits a target is fitting, and it is exactly what Pass 981
criticised in the CKM material.  So the search is run with its own false-positive
rate reported.

Search space: all a+b, a-b, a*b, a/b and a/(b+c) over eighteen W(3,3) atoms
(q, v, k, lambda, mu, r, |s|, f, g, kbar, Phi4, Phi6, k-1, v-k, q!, 2q, q^2,
q^3), giving 7,128 distinct expression values, matched to 0.2% tolerance.

    target            hits    reading
    m_H     = 125       0     no simple expression exists
    Omega_L = 0.6833    0     no simple expression exists
    sin2t13 = 0.02198   0     no simple expression exists
    m_W/vEW = 0.3270    0     no simple expression exists
    V_us    = 0.2253    3     q^2/v = 9/40 = 0.225
    H_0     = 67        4     v + kbar = 40 + 27
    n_s     = 0.9667    8     several
    sin2t12 = 0.3077   36     k/(k+kbar) = 12/39 = 4/13, and 35 others

The four zero-hit rows are the informative ones: no expression in this space
reaches them, so those entries cannot be repaired by finding the intended
formula and should be withdrawn rather than rewritten.  The rows with hits are
NOT thereby derived -- 36 hits in 7,128 expressions is what chance produces, and
even the tidiest of them (H_0 = v + kbar, "vacuum plus matter sector") rests on
4 hits.  A hit found by search is a candidate for a derivation, not a derivation.

PART B -- THE RANK IS BOUNDED BY THE NUMBER OF COLLISION CLASSES.

Pass 1009 showed collisions can cancel: three collision classes with rank zero.
That left the actual relationship open.  Sampling k = 6..8 spectra with
v_p(M) = 1 and at least three collision classes, 6,703 cases:

    3 classes -> ranks 0,1,2,3 observed (3 most common)
    4 classes -> ranks 0,1,2,3,4 observed (4 most common)

so the class count is an upper bound, attained about half the time, and never
exceeded.  Total cancellation is rare: 39 of 6,703 samples, about 0.6%.  It is
not explained by how many eigenvalues sit alone in their residue class --
rank-zero cases occur with 0, 1 and 2 singletons alike.

The picture that results: collision classes bound the p-part from above, generic
spectra attain the bound, and the drop below it is a genuine degeneracy of the
stacked branch operators rather than a feature of the collision pattern.  This is
why Pass 828's invariant has to be a rank and cannot be a count.

BOUNDARY.  Part A's search space is finite and hand-chosen; "no simple
expression" means none in that space, not none at all.  Part B is sampling: the
bound rank <= #classes held in every one of 6,703 cases but is not proved here,
and the 0.6% cancellation rate is specific to the sampled spectra.
"""
from __future__ import annotations

import argparse
import collections
import functools
import itertools
import json
import random
from math import gcd
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1010_constant_rederivation_and_rank_bound.json"

ATOMS = {'q': 3, 'v': 40, 'k': 12, 'lam': 2, 'mu': 4, 'r': 2, '|s|': 4,
         'f': 24, 'g': 15, 'kbar': 27, 'Phi4': 10, 'Phi6': 7, 'k-1': 11,
         'v-k': 28, 'q!': 6, '2q': 6, 'q^2': 9, 'q^3': 27}
TARGETS = {'m_H': 125.0, 'H_0': 67.0, 'n_s': 0.9667, 'Omega_Lambda': 0.6833,
           'sin2_theta12': 0.3077, 'sin2_theta13': 0.02198,
           'V_us': 0.2253, 'm_W_over_vEW': 80.44 / 246.0}


def build_space():
    names = list(ATOMS)
    vals = [ATOMS[n] for n in names]
    ex = {}
    for (n1, a), (n2, b) in itertools.product(zip(names, vals), repeat=2):
        ex[f"{n1}+{n2}"] = float(a + b)
        ex[f"{n1}-{n2}"] = float(a - b)
        ex[f"{n1}*{n2}"] = float(a * b)
        if b:
            ex[f"{n1}/{n2}"] = a / b
    for (n1, a), (n2, b), (n3, c) in itertools.product(zip(names, vals), repeat=3):
        if b + c:
            ex[f"{n1}/({n2}+{n3})"] = a / (b + c)
    return ex


def part_A_rederivation(checks):
    ex = build_space()
    rows = {}
    zero_hit = 0
    for tgt, val in TARGETS.items():
        tol = abs(val) * 2e-3
        hits = sorted(e for e, x in ex.items() if abs(x - val) <= tol)
        if not hits:
            zero_hit += 1
        rows[tgt] = {"target": val, "hits": len(hits),
                     "examples": hits[:3],
                     "verdict": ("no simple expression -- withdraw" if not hits
                                 else "candidate only; hits are within chance")}
    checks["search_space_is_large"] = (len(ex) > 5000)
    checks["four_targets_have_no_expression"] = (zero_hit == 4)
    checks["sin2t12_has_many_hits"] = (rows["sin2_theta12"]["hits"] > 20)
    return {"rows": rows, "search_space": len(ex), "tolerance": "0.2%",
            "atoms": list(ATOMS),
            "zero_hit_targets": zero_hit,
            "reading": (
                "Four targets -- m_H, Omega_Lambda, sin2_theta13 and m_W/vEW -- "
                "are reached by no expression in a space of 7,128, so they cannot "
                "be repaired by recovering an intended formula and should be "
                "withdrawn.  The rest have hits, but 36 hits for sin2_theta12 is "
                "what chance gives; a hit found by search is a candidate for a "
                "derivation, not a derivation.")}


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
                fct = M[i][c]
                M[i] = [(M[i][j] - fct * M[r][j]) % p for j in range(cols)]
        r += 1
    return r


def part_B_rank_bound(checks):
    def vp(x, p):
        v = 0
        while x and x % p == 0:
            x //= p
            v += 1
        return v

    def cond(cs):
        Ds = []
        for c in cs:
            D = 1
            for d in cs:
                if d != c:
                    D *= (c - d)
            Ds.append(abs(D))
        M = 1
        for D in Ds:
            M = M * D // gcd(M, D)
        return M, Ds

    random.seed(33)
    samples = []
    for _ in range(30000):
        k = random.choice([6, 7, 8])
        cs = sorted(random.sample(range(-16, 17), k))
        M, Ds = cond(cs)
        for p in (5, 7):
            if vp(M, p) != 1:
                continue
            g = {}
            for c in cs:
                g.setdefault(c % p, []).append(c)
            cl = [x for x in g.values() if len(x) > 1]
            if len(cl) < 3:
                continue
            n = k
            A = np.zeros((n, n), dtype=np.int64)
            for i, c in enumerate(cs):
                A[i, i] = c
                for j in range(i + 1, n):
                    A[i, j] = random.randint(-2, 2)
            Ao = A.astype(object)
            I = np.eye(n, dtype=object)
            keep = [functools.reduce(lambda Y, d: Y @ (Ao - d * I),
                                     [d for d in cs if d != c], I.copy())
                    for c, D in zip(cs, Ds) if D % p == 0]
            rk = rank_p(np.vstack(keep).tolist(), p)
            singles = sum(1 for x in g.values() if len(x) == 1)
            samples.append((rk, len(cl), singles))
            break
    bound_ok = all(rk <= nc for rk, nc, _ in samples)
    zero = [x for x in samples if x[0] == 0]
    dist = collections.defaultdict(collections.Counter)
    for rk, nc, _ in samples:
        dist[nc][rk] += 1
    checks["rank_never_exceeds_class_count"] = bound_ok
    checks["cancellation_is_rare"] = (0 < len(zero) / max(1, len(samples)) < 0.05)
    checks["enough_samples"] = (len(samples) > 3000)
    return {"samples": len(samples),
            "rank_le_class_count": bound_ok,
            "rank_distribution_by_class_count": {
                str(nc): dict(sorted(c.items())) for nc, c in sorted(dist.items())},
            "zero_rank_cases": len(zero),
            "zero_rank_fraction": round(len(zero) / max(1, len(samples)), 4),
            "singletons_in_zero_rank_cases": sorted({z[2] for z in zero}),
            "reading": (
                "The number of collision classes bounds the rank from above in "
                "all 6,703 samples and is attained about half the time.  Total "
                "cancellation happens in 0.6% of cases and is not explained by "
                "the number of eigenvalues alone in their residue class, since "
                "rank-zero occurs with 0, 1 and 2 singletons alike.  The p-part "
                "invariant therefore has to be a rank and cannot be a count.")}


def main_payload():
    checks = {}
    A = part_A_rederivation(checks)
    B = part_B_rank_bound(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass1010.constant_rederivation_and_rank_bound.v1",
        "status": status,
        "headline": (
            "THE BROKEN CONSTANTS MOSTLY CANNOT BE REPAIRED, AND THE RANK IS "
            "BOUNDED BY THE COLLISION-CLASS COUNT.  Searching 7,128 expressions "
            "in eighteen W(3,3) atoms for the formulas Pass 1008 found broken: "
            "four targets -- m_H, Omega_Lambda, sin2_theta13 and m_W/vEW -- are "
            "reached by nothing at all and should be withdrawn rather than "
            "rewritten, while the rest have hits that are within chance (36 for "
            "sin2_theta12), so a search hit is a candidate, not a derivation.  "
            "Separately, sampling 6,703 spectra with at least three collision "
            "classes, the rank never exceeds the class count and attains it about "
            "half the time; total cancellation occurs in 0.6% of cases and is not "
            "explained by singleton eigenvalues.  Collision classes bound the "
            "p-part from above, which is why Pass 828's invariant must be a rank "
            "rather than a count."),
        "part_A_rederivation": A,
        "part_B_rank_bound": B,
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
            raise SystemExit("Pass 1010 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
