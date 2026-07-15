#!/usr/bin/env python3
"""Pass 272: the second odd prime power -- W(3,25).

Pass 267 declared q = 25 (n = 16276) out of reach.  The obstruction was the
rank routine, not the mathematics: the committed f2_rank re-sorts its basis on
every insertion, which costs O(r^2 log r) big-integer comparisons and is hopeless
at r ~ 8451.  This witness replaces it with a pivot-indexed elimination (a dict
keyed by the leading bit, no sorting, O(1) pivot lookup) and attempts the build.

The cross-characteristic claim of Pass 266 predicts, with NO free parameters:
    n            = (q+1)(q^2+1)   = 16276
    rank_2        = (q^2+1)(q+2)/2 = 8451      (= the characteristic-0 rank; odd
                                                 q has no 2-modular drop)
    dim C^perp    = q(q^2+1)/2     = 7825      (= the SRG multiplicity g)
    k_CSS         = q^2+1          = 626

q = 25 is only the SECOND odd prime power ever reached here (after q = 9), so it
is the sharpest available test that the odd-q tower is about CHARACTERISTIC and
not about primality.  Whatever the machine returns is reported.
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

OUT = ROOT / "data" / "w33_pass272_q25_second_prime_power.json"


# ---------------- GF(p^k) with full multiplication / inverse tables
def gf_tables(p, k, irred):
    q = p ** k

    def to_poly(a):
        out = []
        for _ in range(k):
            out.append(a % p)
            a //= p
        return out

    def from_poly(c):
        v = 0
        for i in reversed(range(k)):
            v = v * p + (c[i] % p)
        return v

    def mul(a, b):
        pa, pb = to_poly(a), to_poly(b)
        prod = [0] * (2 * k - 1)
        for i, x in enumerate(pa):
            if x:
                for j, y in enumerate(pb):
                    prod[i + j] = (prod[i + j] + x * y) % p
        for d in range(len(prod) - 1, k - 1, -1):
            c = prod[d]
            if c:
                prod[d] = 0
                for i in range(k):
                    prod[d - k + i] = (prod[d - k + i] - c * irred[i]) % p
        return from_poly(prod[:k])

    MUL = np.zeros((q, q), dtype=np.int16)
    for a in range(q):
        for b in range(q):
            MUL[a, b] = mul(a, b)
    INV = np.zeros(q, dtype=np.int16)
    for a in range(1, q):
        for b in range(1, q):
            if MUL[a, b] == 1:
                INV[a] = b
                break
    NEG = np.zeros(q, dtype=np.int16)
    for a in range(q):
        NEG[a] = from_poly([(-c) % p for c in to_poly(a)])
    ADD = np.zeros((q, q), dtype=np.int16)
    for a in range(q):
        pa = to_poly(a)
        for b in range(q):
            pb = to_poly(b)
            ADD[a, b] = from_poly([(x + y) % p for x, y in zip(pa, pb)])
    return MUL, INV, NEG, ADD


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


def f2_rank_fast(masks):
    """pivot-indexed F2 elimination: dict keyed by leading bit, no sorting."""
    pivots = {}
    rank = 0
    for v in masks:
        cur = v
        while cur:
            hb = cur.bit_length() - 1
            p = pivots.get(hb)
            if p is None:
                pivots[hb] = cur
                rank += 1
                break
            cur ^= p
    return rank


def main():
    checks = {}
    q, p, k = 25, 5, 2
    t0 = time.time()

    # GF(25) = F_5[x]/(x^2 - 2)  (2 is a non-residue mod 5: squares are 1,4)
    MUL, INV, NEG, ADD = gf_tables(p, k, [NEG_C := 3, 0])  # x^2 = -(3) = 2
    checks["gf25_size"] = MUL.shape == (25, 25)
    checks["gf25_all_invertible"] = all(int(MUL[a, INV[a]]) == 1
                                        for a in range(1, 25))

    pts = build_points(q, MUL, INV)
    n = len(pts)
    checks["n_16276"] = n == 16276
    t_pts = round(time.time() - t0, 1)

    P = np.array(pts, dtype=np.int16)
    idx = {tuple(int(x) for x in pts[i]): i for i in range(n)}

    def norm(v):
        lead = next(x for x in v if x != 0)
        li = int(INV[lead])
        return (int(MUL[v[0], li]), int(MUL[v[1], li]),
                int(MUL[v[2], li]), int(MUL[v[3], li]))

    # symplectic Gram row: B(P_i, .) = p0 q2 - p2 q0 + p1 q3 - p3 q1
    c0, c1, c2, c3 = P[:, 0], P[:, 1], P[:, 2], P[:, 3]
    lines, covered = [], set()
    t1 = time.time()
    for i in range(n):
        a0, a1, a2, a3 = (int(P[i, 0]), int(P[i, 1]), int(P[i, 2]), int(P[i, 3]))
        t_a = MUL[a0, c2]
        t_b = NEG[MUL[a2, c0]]
        t_c = MUL[a1, c3]
        t_d = NEG[MUL[a3, c1]]
        row = ADD[ADD[t_a, t_b], ADD[t_c, t_d]]
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
    checks["lines_16276"] = len(lines) == 16276
    checks["line_size_q_plus_1"] = all(len(l) == q + 1 for l in lines[:50])

    # F2 rank via pivot-indexed elimination
    t2 = time.time()
    masks = []
    for l in lines:
        v = 0
        for pnt in l:
            v |= 1 << pnt
        masks.append(v)
    rank = f2_rank_fast(masks)
    t_rank = round(time.time() - t2, 1)

    predicted = (q * q + 1) * (q + 2) // 2      # 8451
    g = q * (q * q + 1) // 2                     # 7825
    checks["rank_matches_char0_prediction"] = rank == predicted
    checks["no_2_modular_drop"] = rank == predicted
    checks["predicted_8451"] = predicted == 8451
    checks["g_7825"] = g == 7825
    checks["k_626"] = n - 2 * g == 626
    checks["dual_dim_equals_g"] = n - rank == g

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass272.q25_second_prime_power.v1",
        "status": "PASS" if all_pass else "FAIL",
        "q": q,
        "result": {
            "n": n, "lines": len(lines),
            "rank_2_computed": rank,
            "char0_prediction": predicted,
            "match": bool(rank == predicted),
            "dim_C_perp": n - rank, "g_law": g,
            "k_css": n - 2 * g,
            "timings_s": {"points": t_pts, "lines": t_lines, "rank": t_rank,
                          "total": round(time.time() - t0, 1)},
        },
        "what_this_tests": (
            "q = 25 is only the SECOND odd prime power ever reached in this "
            "program (after q = 9). Pass 266 predicts, with no free parameters, "
            "that odd q is CROSS characteristic and therefore suffers NO "
            "2-modular rank drop, so rank_2 must equal the characteristic-0 rank "
            "(q^2+1)(q+2)/2 = 8451. A match is a genuine out-of-sample "
            "confirmation that the odd-q tower is about characteristic, not "
            "primality."
        ),
        "method_note": (
            "Pass 267 called q=25 unreachable; the obstruction was the rank "
            "routine, not the mathematics. The committed f2_rank re-sorts its "
            "basis on every insertion (O(r^2 log r) big-integer comparisons). "
            "Replacing it with a pivot-indexed dict elimination (leading-bit key, "
            "no sorting) makes n = 16276 tractable."
        ),
        "checks": {k2: bool(v) for k2, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
