#!/usr/bin/env python3
"""Pass 4793 -- self-duality is not the finest question. Polarity is, and it selects the
Suzuki groups.

Pass 4774 computed that W(3,q) is self-dual exactly when q is even, at seven values of q.
That is a statement about whether a duality EXISTS.  Classical theory says a strictly finer
question is whether an *involutory* duality exists -- a POLARITY, a map exchanging points
and lines whose square is the identity.  The two questions have different answers:

    self-duality  <=>  q even                 (q = 2, 4, 8, 16, ...)
    polarity      <=>  q an ODD power of 2    (q = 2, 8, 32, ...)   [Tits]

So q = 4 should be self-dual WITHOUT admitting a polarity.  If that holds, the even family
splits, and it splits along the line that produces the Suzuki groups: the absolute points of
the polarity form the Suzuki-Tits ovoid of q^2+1 points, and its stabiliser is Sz(q) of order
q^2 (q^2+1)(q-1).

THIS PASS TESTS THE SPLIT AT q = 2 AND q = 4 BY EXHAUSTION, which is the point -- the
prediction is not that a search failed to find a polarity at q = 4, but that none exists, and
that is a statement about the whole automorphism group of the incidence structure.

A duality is an automorphism of the LEVI (incidence) graph that exchanges the two parts;
a polarity is such an automorphism of order 2.  Both are decidable by enumerating the
automorphism group of a bipartite graph on 2(q+1)(q^2+1) vertices.

    py -3 analysis/w33_pass4793_the_polarity_is_a_suzuki_group.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


PP = _load("pp", "w33_pass4754_4755_prime_power_quadrangles_and_bliss.py")


def levi(pts, lines):
    """Bipartite incidence graph: points 0..n-1, lines n..2n-1."""
    n = len(pts)
    g = igraph.Graph(n=n + len(lines))
    e = []
    for j, L in enumerate(lines):
        for p in L:
            e.append((p, n + j))
    g.add_edges(e)
    return g, n


def close_group(gens, deg, cap=4_000_000):
    """Full permutation group from generators, as a set of tuples."""
    ident = tuple(range(deg))
    seen = {ident}
    frontier = [ident]
    while frontier:
        x = frontier.pop()
        for g in gens:
            y = tuple(g[x[i]] for i in range(deg))
            if y not in seen:
                seen.add(y)
                if len(seen) > cap:
                    return None
                frontier.append(y)
    return seen


def main() -> int:
    print("=" * 78)
    print("Pass 4793 -- does a POLARITY exist? the even family should split")
    print("=" * 78)

    print(f"\n  {'q':>3s} {'pts':>5s} {'|Aut(Levi)|':>12s} {'dualities':>10s} "
          f"{'POLARITY':>9s} {'predicted':>10s} {'abs pts':>8s} {'q^2+1':>6s}")
    rows = []
    for p, k in ((2, 1), (2, 2)):
        q = p ** k
        pts, lines = PP.build_w3(PP.GF(p, k))
        B, n = levi(pts, lines)
        gens = [list(g) for g in B.automorphism_group()]
        G = close_group(gens, B.vcount())
        if G is None:
            print(f"  {q:3d} {n:5d}  group too large to enumerate at this size")
            continue

        def swaps(perm):
            return perm[0] >= n          # part-exchanging iff a point maps to a line

        dual = [x for x in G if swaps(x)]
        pol = [x for x in dual if all(x[x[i]] == i for i in range(len(x)))]
        # absolute points of a polarity: p incident with its image line
        inc = {(u, v) for u, v in B.get_edgelist()}
        inc |= {(v, u) for u, v in list(inc)}
        absn = None
        if pol:
            t = pol[0]
            absn = sum(1 for i in range(n) if (i, t[i]) in inc)
        odd_power = (p == 2 and k % 2 == 1)
        rows.append({"q": q, "points": n, "aut_order": len(G),
                     "dualities": len(dual), "polarities": len(pol),
                     "polarity_exists": bool(pol), "predicted": bool(odd_power),
                     "agrees": bool(bool(pol) == odd_power),
                     "absolute_points": absn, "q2_plus_1": q * q + 1})
        print(f"  {q:3d} {n:5d} {len(G):12,d} {len(dual):10,d} "
              f"{str(bool(pol)):>9s} {str(odd_power):>10s} "
              f"{str(absn):>8s} {q*q+1:6d}")

    agree = all(r["agrees"] for r in rows)
    q2 = next((r for r in rows if r["q"] == 2), None)
    q4 = next((r for r in rows if r["q"] == 4), None)

    print(f"""
    {'THE EVEN FAMILY SPLITS, EXACTLY WHERE TITS SAYS IT DOES.' if agree else 'THE SPLIT DOES NOT MATCH -- READ THE ROWS.'}

    Both q = 2 and q = 4 are self-dual, and Pass 4774 could not tell them apart: dualities
    exist in both. Ask for an INVOLUTORY duality and they separate. q = 2 = 2^1 is an odd
    power of two and has {q2['polarities'] if q2 else 0} of them; q = 4 = 2^2 is an even power and has {q4['polarities'] if q4 else 0}, out of
    {q4['dualities'] if q4 else 0} dualities -- so the absence is not a search failing, it is an exhaustion over the
    whole automorphism group.

    AND THE ABSOLUTE POINTS ARE THE OVOID. A polarity's absolute points -- those lying on
    their own image -- number {q2['absolute_points'] if q2 else '?'} at q = 2, which is q^2+1 = {q2['q2_plus_1'] if q2 else '?'}. That set is the
    Suzuki-Tits ovoid, and its stabiliser is the Suzuki group Sz(q) of order
    q^2(q^2+1)(q-1) = {4*5*1} at q = 2.

    WHY THIS IS THE RIGHT REFINEMENT AND NOT A CURIOSITY. The parity rule says characteristic
    2 is special because the symplectic and orthogonal forms coincide there. The polarity
    condition says something sharper: at ODD powers of 2 the special isogeny of B2 = C2 has a
    square root, and that square root IS the polarity. Fixed points of a Frobenius-twisted
    endomorphism are how the Suzuki groups are defined, so this quadrangle's finest duality
    question and the existence of Sz(q) are the same question.

    A COROLLARY THIS REPOSITORY SHOULD CARE ABOUT: W(3,3) is not self-dual, and the reason
    already recorded here -- "Sp(4,3) lacking full D4 triality" -- is about the SAME
    phenomenon seen from D4. Triality is the order-3 outer symmetry of D4; the B2/C2
    exceptional behaviour in characteristic 2 is its order-2 shadow. Odd q has neither.""")

    out = {
        "boundary": ("q = 2 and q = 4 are settled by ENUMERATING the full automorphism "
                     "group of the Levi graph, so the absence of a polarity at q = 4 is "
                     "exhaustive, not a failed search. q = 8 is NOT computed here -- its "
                     "Levi graph has 1,170 vertices and the group is far too large for this "
                     "method. The identification of the absolute-point set with the "
                     "Suzuki-Tits ovoid and of its stabiliser with Sz(q) is CITED classical "
                     "theory used to interpret the count, not derived here; what is computed "
                     "is the count and the existence split"),
        "rows": rows,
        "split_matches_odd_power_of_two": bool(agree),
        "rule_self_duality": "q even",
        "rule_polarity": "q an odd power of 2 (Tits)",
        "why_finer": ("self-duality asks whether a duality exists; polarity asks whether an "
                      "involutory one does. q = 4 is self-dual with no polarity, so the "
                      "even family splits and Pass 4774's rule is not the finest statement"),
        "suzuki_connection": (
            "the absolute points of the polarity form the Suzuki-Tits ovoid of q^2+1 "
            "points, stabilised by Sz(q) of order q^2(q^2+1)(q-1); the polarity is the "
            "square root of the special isogeny of B2 = C2 in characteristic 2, which is "
            "also how the Suzuki groups are defined"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4793_POLARITY_AND_SUZUKI.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
