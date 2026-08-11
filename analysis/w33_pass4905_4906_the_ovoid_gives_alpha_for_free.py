"""Passes 4905-4906 -- the q=8 polarity hands over an independence number no direct
computation could reach, and the ovoid is exhibited.

Pass 4800 spent 2,075 seconds computing alpha(W(3,5)) = 18 on a 156-vertex graph, and
Pass 4812 could not finish 112 or 280 vertices at all.  W(3,8) has 585 vertices; exhaustive
independence is hopeless there.

But Pass 4897 found a polarity of W(3,8) with 65 absolute points, and the absolute points of
a polarity are pairwise NON-COLLINEAR -- that is what an ovoid is.  So:

    * the 65 absolute points are an independent set, giving alpha >= 65
    * the Hoffman ratio bound for W(3,q) is exactly q^2+1 = 65, giving alpha <= 65

The two meet.  alpha(W(3,8)) = 65, obtained from a witness plus a spectral bound, with no
search of any kind.  Pass 4795's table -- "even q attains its bound" -- gains a fourth value
at a size where the direct method has no chance.

  4905  verify the absolute points are genuinely independent, and close the bound
  4906  exhibit the ovoid: its 65 points, and the orbit structure of the polarity

    py -3 analysis/w33_pass4905_4906_the_ovoid_gives_alpha_for_free.py
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
import time
from collections import Counter
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


def main() -> int:
    print("=" * 78)
    print("Passes 4905-4906 -- alpha(W(3,8)) without a search")
    print("=" * 78)

    q = 8
    pts, lines = PP.build_w3(PP.GF(2, 3))
    n = len(pts)
    B = igraph.Graph(n=n + len(lines))
    B.add_edges([(p, n + j) for j, L in enumerate(lines) for p in L])

    # collinearity graph, for the independence check and the Hoffman bound
    g = igraph.Graph(n=n)
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    prm = PP.srg_params(g)
    hb = P95.hoffman(*prm)

    print(f"\n    W(3,8) collinearity graph : SRG{prm}")
    print(f"    Hoffman ratio bound       : {hb}   (= q^2+1 = {q*q+1})")

    # re-find the polarity (fast: Pass 4897 took 36,300 candidates in 10s)
    gens = [tuple(x) for x in B.automorphism_group()]
    swaps = [x for x in gens if x[0] >= n]
    keeps = [x for x in gens if x[0] < n]

    def comp(a, b):
        return tuple(a[b[i]] for i in range(len(b)))

    inc = {(u, v) for u, v in B.get_edgelist()}
    inc |= {(v, u) for u, v in list(inc)}
    rng = random.Random(4897)
    cur = tuple(range(B.vcount()))
    pol, tried, t0 = None, 0, time.time()
    while pol is None and time.time() - t0 < 900:
        for _ in range(rng.randint(1, 8)):
            cur = comp(rng.choice(keeps or gens), cur)
        c = comp(swaps[0], cur)
        tried += 1
        if c[0] >= n and all(c[c[i]] == i for i in range(len(c))):
            pol = c
    if pol is None:
        print("    polarity not re-found in budget; nothing further computed")
        return 0

    ovoid = sorted(i for i in range(n) if (i, pol[i]) in inc)
    print(f"    polarity re-found         : {tried:,} candidates, "
          f"{time.time()-t0:.0f}s")
    print(f"    absolute points           : {len(ovoid)}")

    # ---- 4905: is it independent? ---------------------------------------
    nb = [set(g.neighbors(v)) for v in range(n)]
    bad = [(u, v) for u, v in itertools.combinations(ovoid, 2) if v in nb[u]]
    independent = not bad
    print(f"\n  PASS 4905 -- independence and the bound\n")
    print(f"    pairs checked             : {len(ovoid)*(len(ovoid)-1)//2}")
    print(f"    collinear pairs found     : {len(bad)}")
    print(f"    independent set           : {independent}")
    print(f"    therefore alpha >=        : {len(ovoid) if independent else '?'}")
    print(f"    Hoffman says alpha <=     : {hb}")
    closed = independent and len(ovoid) == hb
    print(f"    bounds meet, alpha =      : {hb if closed else 'not closed'}")

    print(f"""
    {'ALPHA(W(3,8)) = 65, WITH NO SEARCH.' if closed else 'THE BOUNDS DO NOT MEET -- READ THE ROWS.'} The 65 absolute points are pairwise
    non-collinear, verified over all {len(ovoid)*(len(ovoid)-1)//2} pairs, so they are an independent set and
    alpha >= 65. The Hoffman ratio bound is q^2+1 = 65, so alpha <= 65. The two meet.

    THIS IS A SIZE THE DIRECT METHOD CANNOT REACH. Pass 4800 spent 2,075 seconds on 156
    vertices; Pass 4812 failed at 112 and 280. W(3,8) has 585, and exhaustive independence
    there is out of the question. A witness plus a spectral bound settles it in seconds,
    and neither half would have done it alone.

    PASS 4795'S TABLE GAINS A FOURTH VALUE, at the one size where it could not have been
    filled in by computation:

        q=2   alpha =  5 = bound      q=3   alpha =  7 < bound 10
        q=4   alpha = 17 = bound      q=5   alpha = 18 < bound 26
        q=8   alpha = 65 = bound                       <- here

    Even q attains its bound; odd q misses. Now with a witness on the even side at 585
    vertices rather than an exhaustive search at 85.""")

    # ---- 4906: exhibit the ovoid ----------------------------------------
    print("\n  PASS 4906 -- the ovoid, exhibited\n")
    cyc = Counter()
    seen = set()
    for s in range(len(pol)):
        if s in seen:
            continue
        c, x = 0, s
        while x not in seen:
            seen.add(x)
            x = pol[x]
            c += 1
        cyc[c] += 1
    print(f"    polarity cycle type       : "
          f"{' '.join(f'{L}^{m}' for L, m in sorted(cyc.items()))}")
    print(f"    fixed points of the map   : {cyc.get(1, 0)}")
    print(f"    first 12 ovoid points     : {ovoid[:12]}")
    print(f"    each lies on its image line: {all((i, pol[i]) in inc for i in ovoid)}")
    print(f"""
    THE CYCLE TYPE IS NOT AN INVARIANT and is reported as description only -- composing this
    polarity with any automorphism gives another, so what BLISS and a seeded random walk
    happened to produce says nothing about the geometry. What is invariant is that the
    absolute-point set has 65 elements and is independent, both verified above.""")

    out = {
        "boundary": ("alpha = 65 is established by a WITNESS (the 65 absolute points, "
                     "verified pairwise non-collinear over all 2,080 pairs) meeting a "
                     "SPECTRAL bound (Hoffman = q^2+1). No exhaustive search was run and "
                     "none is possible at 585 vertices. The polarity's cycle type describes "
                     "the representative found, not the geometry"),
        "q": q, "srg": list(prm), "hoffman": hb,
        "ovoid_size": len(ovoid),
        "pairs_checked": len(ovoid) * (len(ovoid) - 1) // 2,
        "collinear_pairs": len(bad),
        "independent": bool(independent),
        "alpha": hb if closed else None,
        "bounds_meet": bool(closed),
        "ovoid_first_12": ovoid[:12],
        "polarity_cycle_type": {str(k): v for k, v in sorted(cyc.items())},
        "table": {"q=2": [5, 5], "q=3": [7, 10], "q=4": [17, 17],
                  "q=5": [18, 26], "q=8": [len(ovoid), hb]},
        "why_this_matters": ("585 vertices is far beyond exhaustive independence -- Pass "
                             "4800 needed 2,075 s for 156 and Pass 4812 failed at 112. A "
                             "witness plus a spectral bound settles it in seconds"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4905_4906_ALPHA_FROM_THE_OVOID.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
