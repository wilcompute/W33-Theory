#!/usr/bin/env python3
"""Cross-track closures from Holotrade, re-verified inside W33-Theory.

Four ledger items this corpus recorded as open or untested were settled on the
Holotrade track:

  * CSS distance d = q+1 for q >= 5 (ledger row P326, "d <= q+1 only")
      -> Holotrade 7c57f8e, analysis/the_binary_line_code_of_w3q_has_distance_q_plus_one.py
  * the m = 6 Coxeter-Todd rung of the QR tower (ledger row P368/369)
      -> Holotrade a0ed473, analysis/the_coxeter_todd_rung_is_locally_the_cubic_surface.py
  * Pass 7289's recorded-but-untested prediction SRG(126,45,12,18)
      -> same commit
  * Pass 7294's row "LEECH at d=9 gives 40 points -- the same target as E8 at d=3"
      -> Holotrade e680b23, analysis/the_leech_rungs_are_the_suzuki_chain.py

Ownership: those commits own the results. This file does not re-derive the heavy
certificates (group orders, the Leech lattice, the W(3,7) rungs). It re-checks
the fast cores independently, so the ledger here does not rest on a pointer
alone:

  A. The binary line code of W(3,q), q odd. The parity lemma (a line meets the
     neighbourhood of a point in q or 1 points, both odd) and the GQ axiom are
     checked at q = 3, 5. At q = 3 an exhaustive meet-in-the-middle search finds
     that the words of weight <= 4 are exactly the 40 lines. C^perp lies in C
     and is doubly even with k = q^2+1, so a line is a minimum-weight logical:
     CSS distance exactly q+1. The proof for all odd q is in 7c57f8e.
  B. K12 = {x in Z[w]^6 : x mod 2 in the hexacode} (Pass 369's construction):
     theta 1 + 756 + 4032 + 20412; the 126 unit classes of minimal vectors give
     SRG(126,45,12,18) under orthogonality (confirming Pass 7289); K12/2K12
     splits by minimal norm as 378 (norm 4) + 2016 (norm 6) + 1701 (norm 8), so
     the singular classes 1 + 378 + 1701 = 2080 (Pass 369's PLUS count) fall
     into two Aut-invariant pieces, and the K12 shadow is not all of O+(12,2).
  C. The Leech d = 9 row. A Z[zeta_9]-structure needs characteristic
     polynomial Phi_9^4, i.e. trace(g^3) = -12. In the 24-dimensional character
     of Co0 = 2.Co1 (GAP CTblLib, recorded below) every class of order 9 has
     trace(g^3) = -3. Solving for Phi_9/Phi_3/Phi_1 multiplicities gives no
     Phi_9^4. So the row is empty. The rungs that exist are 3a, 5a, 7a, 13a:
     W(11,3), W(5,5), W(3,7), PG(1,13), carrying Feng-Xiang's 2.Suz / 2.J2 /
     2.A7 intriguing sets (e680b23).

Boundary: finite exact checks only; no physics. The classical sources
(Petit-Van de Voorde arXiv:2511.07697, Conway-Sloane 1983, Feng-Xiang
arXiv:2310.09460) are cited in the Holotrade certificates.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "w33_cross_track_holotrade_closures.json"

HOLOTRADE = {
    "css_distance": "7c57f8e",
    "coxeter_todd_rung": "a0ed473",
    "leech_suzuki_chain": "e680b23",
}

# 2.Co1, 24-dimensional faithful character: values chi(g^k) for k | order
CO0_TRACES = {
    "9a": [-3, -3, 24],
    "9b": [0, -3, 24],
    "9c": [3, -3, 24],
    "3a": [-12, 24],
    "5a": [-6, 24],
    "7a": [-4, 24],
    "13a": [-2, 24],
}


def popcount(x: int) -> int:
    return bin(x).count("1")


def w3q(q: int):
    def nm(v):
        i = next(k for k, x in enumerate(v) if x % q)
        z = pow(v[i] % q, -1, q)
        return tuple((z * x) % q for x in v)

    pts = sorted({nm(v) for v in itertools.product(range(q), repeat=4) if any(v)})
    idx = {p: i for i, p in enumerate(pts)}
    n = len(pts)

    def sf(a, b):
        return (a[0] * b[2] - a[2] * b[0] + a[1] * b[3] - a[3] * b[1]) % q

    lines = set()
    for a in range(n):
        for b in range(a + 1, n):
            if sf(pts[a], pts[b]) == 0:
                line = {a} | {
                    idx[nm(tuple((pts[b][k] + x * pts[a][k]) % q for k in range(4)))]
                    for x in range(q)
                }
                lines.add(frozenset(line))
    return n, [sum(1 << i for i in L) for L in sorted(lines, key=sorted)]


def rref(vectors):
    basis = {}
    for v in vectors:
        while v:
            h = v.bit_length() - 1
            if h in basis:
                v ^= basis[h]
            else:
                basis[h] = v
                break
    return basis


def in_span(v, basis):
    while v:
        h = v.bit_length() - 1
        if h not in basis:
            return False
        v ^= basis[h]
    return True


def nullspace(vectors, n):
    piv = {}
    for r in sorted(rref(vectors).values(), key=lambda v: -v.bit_length()):
        h = r.bit_length() - 1
        for ph in list(piv):
            if piv[ph] >> h & 1:
                piv[ph] ^= r
        piv[h] = r
    out = []
    for f in (j for j in range(n) if j not in piv):
        x = 1 << f
        for ph, r in piv.items():
            if r >> f & 1:
                x |= 1 << ph
        out.append(x)
    return out


def css_part():
    res = {}
    for q in (3, 5):
        n, lines = w3q(q)
        adj = [0] * n
        for L in lines:
            for p in range(n):
                if L >> p & 1:
                    adj[p] |= L
        adj = [adj[p] & ~(1 << p) for p in range(n)]
        gq = all(
            popcount(adj[p] & L) == (q if L >> p & 1 else 1)
            for p in range(n)
            for L in lines
        )
        Cb = rref(lines)
        perp = nullspace(list(Cb.values()), n)
        entry = {
            "points": n,
            "lines": len(lines),
            "gqAxiomAndParity": gq and q % 2 == 1,
            "dimC": len(Cb),
            "k": n - 2 * len(perp),
            "CperpInC": all(in_span(v, Cb) for v in perp),
            "CperpDoublyEven": all(popcount(u) % 4 == 0 for u in perp)
            and all(popcount(u & v) % 2 == 0 for u in perp for v in perp),
            "lineIsLogical": not in_span(lines[0], rref(perp)),
        }
        if q == 3:
            col = [0] * n
            for j, h in enumerate(perp):
                for i in range(n):
                    if h >> i & 1:
                        col[i] |= 1 << j
            groups = defaultdict(list)
            for r in range(3):
                for sub in itertools.combinations(range(n), r):
                    syn = mask = 0
                    for i in sub:
                        syn ^= col[i]
                        mask |= 1 << i
                    groups[syn].append(mask)
            words = set()
            for g in groups.values():
                for a, b in itertools.combinations(g, 2):
                    c = a ^ b
                    if c and popcount(c) <= 4:
                        words.add(c)
            entry["wordsOfWeightAtMost4"] = len(words)
            entry["theyAreTheLines"] = words == set(lines)
        res[str(q)] = entry
    return res


def k12_part():
    def mul(x, y):
        a, b = x
        c, d = y
        return (a * c - b * d, a * d + b * c - b * d)

    def conj(x):
        return (x[0] - x[1], -x[1])

    def nrm(x):
        return x[0] * x[0] - x[0] * x[1] + x[1] * x[1]

    f4mul = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    hexgen = [[1, 0, 0, 1, 1, 1], [0, 1, 0, 1, 2, 3], [0, 0, 1, 1, 3, 2]]
    code = set()
    for cf in itertools.product(range(4), repeat=3):
        w = [0] * 6
        for k in range(3):
            for j in range(6):
                w[j] ^= f4mul[cf[k]][hexgen[k][j]]
        code.add(tuple(w))
    elems = sorted(
        ((a, b) for a in range(-4, 5) for b in range(-4, 5) if nrm((a, b)) <= 8), key=nrm
    )
    vecs = []

    def rec(prefix, budget):
        if len(prefix) == 6:
            if budget < 8 and tuple((x[0] % 2) + 2 * (x[1] % 2) for x in prefix) in code:
                vecs.append(tuple(prefix))
            return
        for x in elems:
            if nrm(x) > budget:
                break
            rec(prefix + [x], budget - nrm(x))

    rec([], 8)

    def vnorm(v):
        return sum(nrm(x) for x in v)

    theta = Counter(vnorm(v) for v in vecs)
    mins = [v for v in vecs if vnorm(v) == 4]
    units = [(1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (1, 1)]
    lines, seen = [], set()
    for v in mins:
        if v not in seen:
            cls = {tuple(mul(u, x) for x in v) for u in units}
            seen |= cls
            lines.append(min(cls))

    def h(x, y):
        a = b = 0
        for xi, yi in zip(x, y):
            p = mul(xi, conj(yi))
            a += p[0]
            b += p[1]
        return (a, b)

    adj = {i: {j for j in range(len(lines)) if j != i and h(lines[i], lines[j]) == (0, 0)}
           for i in range(len(lines))}
    k = {len(a) for a in adj.values()}
    lam, mu = set(), set()
    for i, j in itertools.combinations(range(len(lines)), 2):
        (lam if j in adj[i] else mu).add(len(adj[i] & adj[j]))

    # K12/2K12 via an explicit Z-basis (6 hexacode lifts + 2e_i, 2we_i on the last 3 coordinates)
    lift = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (-1, -1)}
    basis = [tuple(mul(s, lift[c]) for c in r) for r in hexgen for s in ((1, 0), (0, 1))]
    basis += [
        tuple(s if j == i else (0, 0) for j in range(6))
        for i in range(3, 6)
        for s in ((2, 0), (0, 2))
    ]
    import sympy

    Bm = sympy.Matrix([[c for x in b for c in x] for b in basis])
    det = int(Bm.det())
    adjm = [[int(x) for x in row] for row in Bm.adjugate().tolist()]

    def key2(v):
        r = [c for x in v for c in x]
        c = [sum(r[i] * adjm[i][j] for i in range(12)) for j in range(12)]
        assert all(x % det == 0 for x in c)
        return tuple((x // det) % 2 for x in c)

    classes = defaultdict(list)
    for v in vecs:
        classes[key2(v)].append(vnorm(v))
    split = Counter(min(ns) for ns in classes.values())
    return {
        "theta": [theta.get(2, 0), theta[4], theta[6], theta[8]],
        "reflectionLines": len(lines),
        "srg": [sorted(k), sorted(lam), sorted(mu)],
        "mod2ClassesByMinNorm": {str(nn): split[nn] for nn in sorted(split)},
        "singular": 1 + split[4] + split[8],
    }


def leech_d9_part():
    def solve(t1, t3):
        out = []
        for a in range(5):
            for b in range(13):
                c = 24 - 6 * a - 2 * b
                if c >= 0 and -b + c == t1 and -3 * a + 2 * b + c == t3:
                    out.append([a, b, c])
        return out

    mult = {c: solve(*CO0_TRACES[c][:2]) for c in ("9a", "9b", "9c")}
    return {
        "order9Multiplicities(Phi9,Phi3,Phi1)": mult,
        "phi9FourthPowerExists": any([4, 0, 0] in m for m in mult.values()),
        "fixedPointFreeTraces": {c: CO0_TRACES[c][0] for c in ("3a", "5a", "7a", "13a")},
        "existingRungs": {"3a": "W(11,3), 2.Suz 90-tight (32760)",
                          "5a": "W(5,5), 2.J2 15/16-ovoids (1890/2016)",
                          "7a": "W(3,7), 2.A7 15/35-tight (120/280)",
                          "13a": "PG(1,13), 6/8"},
    }


def audit():
    css = css_part()
    k12 = k12_part()
    leech = leech_d9_part()
    checks = {
        "css_q3_min_words_are_the_40_lines": css["3"]["wordsOfWeightAtMost4"] == 40 and css["3"]["theyAreTheLines"],
        "css_parity_and_gq_q3_q5": css["3"]["gqAxiomAndParity"] and css["5"]["gqAxiomAndParity"],
        "css_family_q3_q5": all(
            css[str(q)]["k"] == q * q + 1 and css[str(q)]["CperpInC"] and css[str(q)]["CperpDoublyEven"]
            and css[str(q)]["lineIsLogical"] and css[str(q)]["dimC"] == (q * q + 1) * (q + 2) // 2
            for q in (3, 5)
        ),
        "k12_theta": k12["theta"] == [0, 756, 4032, 20412],
        "k12_srg_126_45_12_18": k12["reflectionLines"] == 126 and k12["srg"] == [[45], [12], [18]],
        "k12_mod2_split": k12["mod2ClassesByMinNorm"] == {"4": 378, "6": 2016, "8": 1701} and k12["singular"] == 2080,
        "leech_has_no_zeta9_structure": not leech["phi9FourthPowerExists"],
        "leech_9b_is_phi9_cubed": leech["order9Multiplicities(Phi9,Phi3,Phi1)"]["9b"] == [[3, 2, 2]],
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "owner": {k: "Holotrade " + v for k, v in HOLOTRADE.items()},
        "closes": [
            "ledger P326: CSS distance d=q+1 for all odd q (was open)",
            "ledger P368/369: m=6 Coxeter-Todd rung (was open)",
            "Pass 7289: SRG(126,45,12,18) prediction (was untested) -- confirmed",
            "Pass 7294: Leech d=9 row -- empty (no Z[zeta_9]-structure)",
        ],
        "checks": checks,
        "css": css,
        "k12": k12,
        "leech": leech,
        "boundary": "finite exact re-checks of the fast cores; heavy certificates live in the cited Holotrade commits; no physics",
    }


if __name__ == "__main__":
    result = audit()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for k, v in result["checks"].items():
        print(f"  {k:40s} {v}")
    print("status:", result["status"])
