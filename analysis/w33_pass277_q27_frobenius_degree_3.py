#!/usr/bin/env python3
"""Pass 277: W(3,27) -- does Frobenius degree matter in ODD characteristic?

Pass 266's mechanism says the odd-q rank is the CHARACTERISTIC-0 rank, with no
2-modular drop, because 2 does not divide q -- and crucially, with NO dependence
on the Frobenius degree t.  In characteristic 2 the degree t is everything (the
rank is Tr(B^t)+1, exponential in t).  So the sharp question is:

    in odd characteristic, is t really irrelevant?

The evidence so far is thin on this exact point: every odd anchor is either a
prime (t=1: q=3,5,7,11,13,17) or the single prime power q=9 (t=2) and q=25 (t=2).
BOTH prime powers tested have t=2.  If the Frobenius degree mattered in odd
characteristic, a t=2 test could easily miss it.

q = 27 = 3^3 is the first odd prime power with t = 3.  The prediction is
parameter-free:
    n       = (q+1)(q^2+1)   = 20440
    rank_2  = (q^2+1)(q+2)/2 = 10585      (char-0 rank; no drop)
    dim C^perp = q(q^2+1)/2  = 9855       (= the SRG multiplicity g)
    k       = q^2+1          = 730

A match confirms that odd characteristic is t-blind, closing the asymmetry
Pass 262 exposed.  A mismatch would mean odd q has its own hidden t-structure --
which would be a major surprise and would reopen the unification question.

GF(27) = F_3[x]/(x^3 - x + 1); x^3 - x + 1 has no root mod 3 (values 1,1,1) and
is cubic, hence irreducible.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass272_q25_second_prime_power import f2_rank_fast, gf_tables

OUT = ROOT / "data" / "w33_pass277_q27_frobenius_degree_3.json"


def build_points(q, MUL, INV):
    pts, seen = [], set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                for d in range(q):
                    if a == b == c == d == 0:
                        continue
                    v = (a, b, c, d)
                    lead = next(x for x in v if x != 0)
                    li = int(INV[lead])
                    nv = (int(MUL[a, li]), int(MUL[b, li]),
                          int(MUL[c, li]), int(MUL[d, li]))
                    if nv not in seen:
                        seen.add(nv)
                        pts.append(nv)
    return pts


def main():
    checks = {}
    q, p, k = 27, 3, 3
    t0 = time.time()

    # GF(27) = F_3[x]/(x^3 - x + 1)  =>  x^3 = x - 1 = -(1 + 2x + 0x^2) mod 3
    MUL, INV, NEG, ADD = gf_tables(p, k, [1, 2, 0])
    checks["gf27_size"] = MUL.shape == (27, 27)
    checks["gf27_all_invertible"] = all(int(MUL[a, INV[a]]) == 1
                                        for a in range(1, 27))
    # field sanity: associativity + distributivity on a sample
    rng = np.random.default_rng(2)
    ok = True
    for _ in range(400):
        a, b, c = (int(x) for x in rng.integers(0, 27, 3))
        if int(MUL[MUL[a, b], c]) != int(MUL[a, MUL[b, c]]):
            ok = False
            break
        if int(MUL[a, ADD[b, c]]) != int(ADD[MUL[a, b], MUL[a, c]]):
            ok = False
            break
    checks["gf27_is_a_field"] = ok

    pts = build_points(q, MUL, INV)
    n = len(pts)
    checks["n_20440"] = n == 20440
    t_pts = round(time.time() - t0, 1)

    P = np.array(pts, dtype=np.int16)
    idx = {tuple(int(x) for x in pts[i]): i for i in range(n)}
    c0, c1, c2, c3 = P[:, 0], P[:, 1], P[:, 2], P[:, 3]

    def norm(v):
        lead = next(x for x in v if x != 0)
        li = int(INV[lead])
        return (int(MUL[v[0], li]), int(MUL[v[1], li]),
                int(MUL[v[2], li]), int(MUL[v[3], li]))

    t1 = time.time()
    lines, covered = [], set()
    for i in range(n):
        a0, a1, a2, a3 = (int(P[i, 0]), int(P[i, 1]), int(P[i, 2]), int(P[i, 3]))
        row = ADD[ADD[MUL[a0, c2], NEG[MUL[a2, c0]]],
                  ADD[MUL[a1, c3], NEG[MUL[a3, c1]]]]
        zeros = np.flatnonzero(row == 0)
        Pi = pts[i]
        for j in zeros:
            j = int(j)
            if j <= i or (i, j) in covered:
                continue
            Qj = pts[j]
            memb = {idx[norm(Qj)]}
            for t in range(q):
                w = tuple(int(ADD[Pi[m], MUL[t, Qj[m]]]) for m in range(4))
                if w != (0, 0, 0, 0):
                    memb.add(idx[norm(w)])
            ml = sorted(memb)
            lines.append(ml)
            for x in range(len(ml)):
                for y in range(x + 1, len(ml)):
                    covered.add((ml[x], ml[y]))
    t_lines = round(time.time() - t1, 1)
    checks["lines_20440"] = len(lines) == 20440
    checks["line_size_28"] = all(len(l) == q + 1 for l in lines[:50])

    t2 = time.time()
    masks = []
    for l in lines:
        v = 0
        for pnt in l:
            v |= 1 << pnt
        masks.append(v)
    rank = f2_rank_fast(masks)
    t_rank = round(time.time() - t2, 1)

    predicted = (q * q + 1) * (q + 2) // 2       # 10585
    g = q * (q * q + 1) // 2                      # 9855
    checks["rank_matches_char0_prediction"] = rank == predicted
    checks["predicted_10585"] = predicted == 10585
    checks["g_9855"] = g == 9855
    checks["dual_dim_equals_g"] = n - rank == g
    checks["k_730"] = n - 2 * g == 730
    checks["odd_characteristic_is_t_blind"] = rank == predicted

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass277.q27_frobenius_degree_3.v1",
        "status": "PASS" if all_pass else "FAIL",
        "q": q, "p": p, "frobenius_degree_t": k,
        "result": {
            "n": n, "lines": len(lines),
            "rank_2_computed": rank, "char0_prediction": predicted,
            "match": bool(rank == predicted),
            "dim_C_perp": n - rank, "g_law": g, "k_css": n - 2 * g,
            "timings_s": {"points": t_pts, "lines": t_lines, "rank": t_rank,
                          "total": round(time.time() - t0, 1)},
        },
        "why_this_matters": (
            "In characteristic 2 the Frobenius degree t is everything: the rank "
            "is Tr(B^t)+1, exponential in t. Pass 266 claims odd characteristic "
            "is t-BLIND -- the rank is just the characteristic-0 value for any t. "
            "But every odd prime power tested so far (q=9, q=25) has t=2, so a "
            "hidden t-structure could have been missed. q = 27 = 3^3 is the "
            "first odd prime power with t=3, and therefore the first genuine "
            "test of t-blindness in odd characteristic."
        ),
        "reading": (
            "W(3,27) was built over GF(27) = F_3[x]/(x^3-x+1) (20440 points and "
            "isotropic lines) and its F2 incidence rank computed directly. The "
            "result decides whether the Frobenius degree has any effect in odd "
            "characteristic. A match at t=3 -- after t=1 (six primes) and t=2 "
            "(q=9, q=25) -- makes the cross-characteristic mechanism of Pass 266 "
            "as well-attested as the char-2 side, and settles the asymmetry that "
            "Pass 262's refuted unification first exposed."
        ),
        "checks": {k2: bool(v) for k2, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
