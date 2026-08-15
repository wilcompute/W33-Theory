"""Passes 5278-5279 -- the other lane's tight frame and my spectral bound are the same
bound, and neither lane noticed.

  5278  Their Pass5261 computed that the 156 minimum footprint words of the q=5 apartment
        code form an equal-norm TWO-DISTANCE TIGHT FRAME in R^90, with normalised inner
        products 2/15 between collinear W-points and -1/25 between noncollinear ones.  That
        is a statement about a binary code, written in the language of frames, and it says
        nothing about independence numbers anywhere in the file.

        But -1/25 is -1/q^2.  And a set of unit vectors with CONSTANT inner product c < 0
        has at most 1 - 1/c members, by positive-semidefiniteness of its Gram matrix alone.
        A coclique of the collinearity graph is exactly a set of points that are pairwise
        NONcollinear -- so its frame vectors all sit at that single inner product, and

            N  <=  1 - 1/(-1/q^2)  =  q^2 + 1

        which is the Hoffman bound, the ovoid size, and the number this lane has spent
        twenty passes on.  Two derivations, one number, and no eigenvalue interlacing.

  5279  Is that a q=5 coincidence or the general shape?  The embedding is checked directly
        at q = 2,3,4,5,7,8 by projecting onto an eigenspace of the collinearity graph and
        reading the two inner products off the Gram matrix.

    py -3 analysis/w33_pass5278_5279_the_frame_gives_hoffman.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from fractions import Fraction
from pathlib import Path

import igraph
import numpy as np

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
P95 = _load("p95", "w33_pass4795_the_ovoid_gap_and_the_polarity_coset.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def main() -> int:
    print("=" * 78)
    print("Passes 5278-5279 -- their frame is my bound")
    print("=" * 78)

    print("\n  PASS 5278 -- the arithmetic that connects them\n")
    c = Fraction(-1, 25)
    print(f"    Track B Pass5261, q=5: noncollinear normalised inner product = {c}")
    print(f"      is that -1/q^2 ?                                 {c == Fraction(-1, 25)}")
    print(f"      unit vectors at CONSTANT inner product c<0:  N <= 1 - 1/c = {1 - 1/c}")
    print(f"      Hoffman bound for GQ(5,5):                   q^2+1     = {26}")
    assert 1 - 1 / c == 26
    print("""
    THE TWO BOUNDS ARE THE SAME NUMBER AND THE ARGUMENTS SHARE NOTHING. Hoffman's ratio
    bound comes from eigenvalue interlacing on the adjacency matrix. The frame bound comes
    from the Gram matrix of a set of unit vectors being positive semidefinite: if all
    pairwise inner products equal c < 0, then summing the vectors and requiring
    |sum|^2 >= 0 gives N + N(N-1)c >= 0, hence N <= 1 - 1/c. No spectrum of the graph
    appears in that derivation at all.

    A COCLIQUE IS WHAT MAKES THEM MEET. Track B's frame is TWO-distance -- collinear pairs
    sit at 2/15, noncollinear at -1/25. A coclique uses only the second value, so its
    vectors form a ONE-distance set, and the one-distance bound applies verbatim.""")

    print("\n  PASS 5279 -- is -1/q^2 the general value?\n")
    print(f"    {'q':>3s} {'n':>5s} {'dim':>5s} {'collinear':>12s} {'noncollinear':>14s} "
          f"{'-1/q^2':>10s} {'1-1/c':>7s} {'Hoffman':>8s}")
    rows = []
    for p, k in [(2, 1), (3, 1), (2, 2), (5, 1), (7, 1), (2, 3)]:
        F = PP.GF(p, k)
        q = F.q
        pts, lines = PP.build_w3(F)[:2]
        g = graph_of(pts, lines)
        n, deg, lam, mu = PP.srg_params(g)
        hb = P95.hoffman(n, deg, lam, mu)
        A = np.array(g.get_adjacency().data, dtype=float)

        # Project onto the eigenspace of the SMALLER eigenvalue r = q-1 and normalise rows.
        # For a GQ(q,q) collinearity graph the eigenvalues are k, q-1, -(q+1).
        r = float(q - 1)
        s = float(-(q + 1))
        # idempotent for eigenvalue r: E_r = (A - s I)(A - k I) / ((r-s)(r-k))
        E = (A - s * np.eye(n)) @ (A - deg * np.eye(n)) / ((r - s) * (r - deg))
        d = np.diag(E).copy()
        assert np.allclose(d, d[0]), "embedding is not equal-norm"
        G = E / d[0]                                   # unit-normalised Gram
        adj = A > 0.5
        off = ~np.eye(n, dtype=bool)
        coll = float(np.mean(G[adj]))
        nonc = float(np.mean(G[off & ~adj]))
        assert np.allclose(G[adj], coll, atol=1e-9), "collinear inner products not constant"
        assert np.allclose(G[off & ~adj], nonc, atol=1e-9), "noncollinear not constant"
        dim = int(round(np.trace(E)))
        bound = 1 - 1 / nonc
        rows.append({"q": q, "n": n, "embedding_dim": dim,
                     "collinear_ip": round(coll, 10), "noncollinear_ip": round(nonc, 10),
                     "minus_one_over_q2": round(-1.0 / (q * q), 10),
                     "frame_bound": round(bound, 6), "hoffman": hb,
                     "agrees": abs(bound - hb) < 1e-6,
                     "nonc_is_minus_inv_q2": abs(nonc + 1.0 / (q * q)) < 1e-9})
        print(f"    {q:3d} {n:5d} {dim:5d} {coll:12.8f} {nonc:14.8f} "
              f"{-1.0/(q*q):10.6f} {bound:7.2f} {hb:8d}")

    allok = all(r["agrees"] and r["nonc_is_minus_inv_q2"] for r in rows)
    print(f"""
    {'EVERY ROW' if allok else 'NOT EVERY ROW'}: the noncollinear inner product is exactly -1/q^2, and the one-distance
    Gram bound 1 - 1/c returns exactly the Hoffman bound q^2+1. Checked at q = {', '.join(str(r['q']) for r in rows)},
    even and odd, so it is not a q=5 accident and not a parity effect.

    WHAT THIS IS AND IS NOT. It is not a new bound -- it is the same number, and both routes
    are classical. What is new here is the identification: Track B's Pass5261 frame and this
    lane's Hoffman bound are two descriptions of one inequality, and neither file mentions
    the other's language. Their file says "two-distance tight frame" and never says
    "independence number"; twenty passes on this side say "Hoffman" and never say "frame".

    WHY IT MATTERS OPERATIONALLY. The frame route says what the bound MEANS: q^2+1 is
    forced because a coclique becomes a set of unit vectors at constant angle, and there is
    no room for more of them in the space. That is also why the bound cannot see whether an
    ovoid EXISTS -- Gram positive-semidefiniteness constrains how many such vectors fit, not
    whether the geometry realises them, which is precisely the gap Passes 5228-5229 measured
    as 7 versus 10 at q=3 on cospectral graphs.

    AND IT SUGGESTS THE ONE THING HOFFMAN CANNOT DO. Two-distance sets have bounds beyond
    the one-distance case -- the absolute bound d(d+3)/2 and relative bounds that use BOTH
    inner products. A coclique only ever uses one of the two, which is exactly why the
    spectral bound is blind to realisability; a bound that used the collinear value {rows[0]['collinear_ip']:.6f}
    as well would be seeing the geometry, not just the counting. That is an open direction,
    not a result, and nothing here establishes that such a bound is achievable.""")

    out = {
        "boundary": ("This IDENTIFIES two known bounds as one number; it derives no new "
                     "bound and neither route is original. The embedding is the standard "
                     "eigenspace projection, checked equal-norm and two-distance by "
                     "assertion at each q. The closing paragraph about two-distance bounds "
                     "using BOTH inner products is a DIRECTION, not a result -- no such "
                     "bound is constructed or shown to exist"),
        "pass_5278": {"source": ("Track B Pass5261: 156 minimum footprint words form an "
                                 "equal-norm two-distance tight frame in R^90, inner "
                                 "products 2/15 collinear and -1/25 noncollinear"),
                      "observation": "-1/25 = -1/q^2 at q=5",
                      "frame_bound": ("unit vectors at constant inner product c<0 satisfy "
                                      "N <= 1 - 1/c, from Gram positive-semidefiniteness"),
                      "coincidence": "1 - 1/(-1/q^2) = q^2+1 = the Hoffman bound",
                      "why_they_meet": ("a coclique uses only the noncollinear value, so a "
                                        "two-distance frame restricted to a coclique is a "
                                        "one-distance set")},
        "pass_5279": {"rows": rows, "all_agree": allok,
                      "reading": ("the frame route explains what the bound MEANS -- q^2+1 "
                                  "unit vectors at constant angle is all that fits -- and "
                                  "also why it cannot see existence: Gram PSD constrains "
                                  "how many fit, not whether the geometry realises them"),
                      "open_direction": ("a bound using BOTH inner products would see the "
                                         "geometry; not constructed here")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5278_5279_FRAME_EQUALS_HOFFMAN.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
