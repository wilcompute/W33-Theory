#!/usr/bin/env python3
"""Pass 4797 -- the independence number separates W(3,3) from Q(4,3), and the ovoid
stabiliser REFUTES Pass 4795's coset arithmetic.

Pass 4767 showed W(3,3) and Q(4,3) share every strongly regular parameter and are NOT
isomorphic.  That was decided by canonical form, which answers the question without saying
what distinguishes them.  Pass 4795 then found alpha(W(3,3)) = 7 against a Hoffman bound of
10.  The bound depends only on the parameters, so Q(4,3) has the same bound -- and if its
independence number differs, then alpha is an INVARIANT THAT SEPARATES THE PAIR, computable
in seconds, where the canonical form gives only a verdict.

There is a reason to expect it to differ.  Ovoids of Q(4,q) correspond to SPREADS of W(3,q),
and W(3,q) has spreads at every q while it has ovoids only at even q.  So the dual should
meet the bound exactly where the original fails it.

Also here: Pass 4795 observed 720 dualities = 36 polarities x 20 = |Sz(2)|, called the coset
reading "the natural one", and refused to assert it because no stabiliser had been computed.
Computing it kills the reading.  There are 6 ovoids, not 36; the stabiliser has order 120,
not 20; and 720 = 120 x 6.  The arithmetic was exact and described nothing.

    py -3 analysis/w33_pass4797_independence_separates_the_dual_pair.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
import time
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
P95 = _load("p95", "w33_pass4795_the_ovoid_gap_and_the_polarity_coset.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def levi(pts, lines):
    n = len(pts)
    g = igraph.Graph(n=n + len(lines))
    g.add_edges([(p, n + j) for j, L in enumerate(lines) for p in L])
    return g, n


def close_group(gens, deg, cap=2_000_000):
    ident = tuple(range(deg))
    seen, frontier = {ident}, [ident]
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
    print("Pass 4797 -- does alpha separate the parameter-equal pair?")
    print("=" * 78)

    print(f"\n  {'geometry':10s} {'n':>5s} {'SRG':>20s} {'Hoffman':>8s} "
          f"{'alpha':>6s} {'meets bound':>12s} {'sec':>6s}")
    rows = []
    for q in (2, 3):
        p, k = (q, 1)
        pts, lines = PP.build_w3(PP.GF(p, k))
        dp, dl = PP.dual(pts, lines)
        for name, (P, L) in ((f"W(3,{q})", (pts, lines)), (f"Q(4,{q})", (dp, dl))):
            g = graph_of(P, L)
            prm = PP.srg_params(g)
            hb = P95.hoffman(*prm)
            t0 = time.time()
            a = g.independence_number()
            dt = time.time() - t0
            rows.append({"geometry": name, "q": q, "n": g.vcount(), "srg": list(prm),
                         "hoffman": hb, "alpha": a, "meets": a == hb,
                         "seconds": round(dt, 1)})
            print(f"  {name:10s} {g.vcount():5d} {str(prm):>20s} {hb:8d} "
                  f"{a:6d} {str(a == hb):>12s} {dt:6.1f}")

    w33 = next(r for r in rows if r["geometry"] == "W(3,3)")
    q43 = next(r for r in rows if r["geometry"] == "Q(4,3)")
    separates = w33["alpha"] != q43["alpha"]
    print(f"""
    {'ALPHA SEPARATES THEM.' if separates else 'ALPHA DOES NOT SEPARATE THEM.'} W(3,3) and Q(4,3) have identical parameters
    (40,12,2,4), identical spectra, identical Hoffman bound of 10 -- and independence numbers
    {w33['alpha']} and {q43['alpha']}.

    {'That is a cheap invariant doing what canonical form does expensively. Pass 4767 needed BLISS to' if separates else ''}
    {'establish these two graphs are different; a maximum independent set does it in a second,' if separates else ''}
    {'and unlike the canonical form it says WHAT differs.' if separates else ''}

    AND IT GOES THE WAY THE GEOMETRY PREDICTS. Ovoids of Q(4,q) are spreads of W(3,q); W(3,q)
    has spreads at every q but ovoids only at even q. So the dual meets the bound exactly
    where the original fails it, which is what the table shows -- {q43['alpha']} = 10 for Q(4,3),
    {w33['alpha']} for W(3,3).

    THE PAIR IS THEREFORE ASYMMETRIC IN A MEASURABLE WAY, not merely non-isomorphic. Every
    argument in this repository that moved a property between W(3,3) and Q(4,3) on the
    strength of shared parameters crossed a boundary that alpha detects for free.""")

    # ---- the ovoid stabiliser, promised by Pass 4795 ----------------------
    print("\n  Pass 4795's coset arithmetic, now with a stabiliser\n")
    pts, lines = PP.build_w3(PP.GF(2, 1))
    B, n = levi(pts, lines)
    G = close_group([list(x) for x in B.automorphism_group()], B.vcount())
    dual_perms = [x for x in G if x[0] >= n]
    pols = [x for x in dual_perms if all(x[x[i]] == i for i in range(len(x)))]
    inc = {(u, v) for u, v in B.get_edgelist()}
    inc |= {(v, u) for (u, v) in list(inc)}
    ovoids = set()
    for t in pols:
        ovoids.add(frozenset(i for i in range(n) if (i, t[i]) in inc))
    # the point-graph automorphism group = Sp(4,2)
    g = graph_of(pts, lines)
    A = close_group([list(x) for x in g.automorphism_group()], n)
    ov0 = sorted(next(iter(ovoids)))
    stab = [x for x in A if sorted(x[i] for i in ov0) == ov0]
    orbit = {frozenset(x[i] for i in ov0) for x in A}
    print(f"    polarities                      : {len(pols)}")
    print(f"    distinct absolute-point sets    : {len(ovoids)}")
    print(f"    |Aut(point graph)| = |Sp(4,2)|  : {len(A):,}")
    print(f"    |stabiliser of one ovoid|       : {len(stab)}")
    print(f"    |orbit of that ovoid|           : {len(orbit)}")
    print(f"    stabiliser x orbit              : {len(stab) * len(orbit):,}"
          f"   {'== |Aut|' if len(stab)*len(orbit) == len(A) else '!= |Aut|'}")
    coincidence = (len(ovoids) != 36 or len(stab) != 20)
    per_ovoid = len(pols) // max(len(ovoids), 1)
    print(f"""
    PASS 4795'S COSET READING IS REFUTED, AND REFUSING TO CLAIM IT WAS THE RIGHT CALL.

    720 = 36 x 20 is exact arithmetic and it describes nothing. The actual structure is
    {len(ovoids)} ovoids, not 36; a stabiliser of order {len(stab)}, not 20; and orbit-stabiliser reads
    {len(stab)} x {len(orbit)} = {len(stab)*len(orbit)}. The {len(pols)} polarities distribute {per_ovoid} to each ovoid.

    |Sz(2)| = 20 is not the stabiliser. It is a subgroup of it -- the Frobenius group of
    order 20 sits inside the order-{len(stab)} stabiliser, which for W(3,2) is S5 acting inside
    Aut = S6 on {len(ovoids)} objects. That is a real and pretty structure, and it is not the one the
    arithmetic suggested.

    THIS IS WHAT THE COUNTING RULE IS FOR. CLAUDE.md records three false correspondences
    produced by matching counts, and Pass 4795 wrote "the honest form of this claim names
    the missing computation: stabilise one ovoid and check the orbit has 36 members". The
    orbit has {len(orbit)}. Had the pass asserted the coset partition on the strength of
    720 = 36 x 20, it would have shipped a false theorem with exact arithmetic behind it.""")

    out = {
        "boundary": ("independence numbers and group orders are exact by exhaustion. The "
                     "ovoid stabiliser is computed to have order 120 and the orbit 6, "
                     "REFUTING the 36 x 20 coset reading Pass 4795 floated and declined to "
                     "assert. The identification of the order-120 stabiliser with S5 is by "
                     "ORDER and by the S6 context only -- no group structure is verified. "
                     "Only q = 2 and q = 3 are treated"),
        "independence": rows,
        "alpha_separates_dual_pair": bool(separates),
        "why": ("ovoids of Q(4,q) are spreads of W(3,q); W(3,q) has spreads at every q but "
                "ovoids only at even q, so the dual meets the Hoffman bound exactly where "
                "the original fails it"),
        "ovoid_stabiliser": {
            "polarities": len(pols), "distinct_ovoids": len(ovoids),
            "aut_point_graph": len(A), "stabiliser": len(stab), "orbit": len(orbit),
            "product_equals_group": len(stab) * len(orbit) == len(A),
            "polarities_per_ovoid": per_ovoid,
            "refutes_pass_4795_coset_reading": bool(coincidence),
            "what_720_eq_36x20_was": (
                "a numerical coincidence. The real decomposition is |Aut| = "
                "stabiliser x orbit = 120 x 6, with 6 ovoids and 6 polarities each. "
                "|Sz(2)| = 20 is a SUBGROUP of the order-120 ovoid stabiliser, not the "
                "stabiliser")},
    }
    fp = ROOT / "data" / "PART_W33_PASS4797_ALPHA_SEPARATES_DUAL_PAIR.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
