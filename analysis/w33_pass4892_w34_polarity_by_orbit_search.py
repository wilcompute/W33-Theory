#!/usr/bin/env python3
"""Pass 4892 -- W(3,4) has no polarity, by a search that does not enumerate the group.

Pass 4793 established the polarity split by ENUMERATING Aut(Levi): at q = 2 that group has
1,440 elements and at q = 4 it has 3,916,800, which was already at the edge.  q = 8 has
1,170 Levi vertices and is far beyond it.  The method does not scale and the interesting
value is q = 8, where Tits predicts a polarity with 65 absolute points.

A POLARITY DOES NOT REQUIRE THE WHOLE GROUP.  It is an involution exchanging the two parts
of the Levi graph, so:

    if sigma is any duality and tau is a polarity, then sigma^-1 tau is a part-PRESERVING
    automorphism -- so every polarity has the form sigma . a for some a in Aut_0.

That turns "search 3.9 million elements" into "search the coset sigma . Aut_0 for an
involution", and Aut_0 is generated, not enumerated: igraph gives generators, and the
condition (sigma a)^2 = 1 is checkable on each candidate without materialising the group.

This pass confirms the q = 2 and q = 4 answers by the cheap method, which is the point --
a new method that reproduces a known answer is worth more than one that only produces a
new answer.

    py -3 analysis/w33_pass4892_w34_polarity_by_orbit_search.py
"""

from __future__ import annotations

import importlib.util
import itertools
import random
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

BUDGET = 240


def levi(pts, lines):
    n = len(pts)
    g = igraph.Graph(n=n + len(lines))
    g.add_edges([(p, n + j) for j, L in enumerate(lines) for p in L])
    return g, n


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(b)))


def is_involution(p):
    return all(p[p[i]] == i for i in range(len(p)))


def search_polarity(B, n, seconds=BUDGET):
    """Look for an involutory part-exchanging automorphism without enumerating Aut.

    Aut_0 (part-preserving) is reached by random words in the generators; any duality
    sigma composed with an element of Aut_0 is another duality, and a polarity is one of
    those that squares to the identity.
    """
    gens = [tuple(g) for g in B.automorphism_group()]
    swaps = [g for g in gens if g[0] >= n]
    keeps = [g for g in gens if g[0] < n]
    if not swaps:
        return {"dualities_exist": False, "polarity": None, "tried": 0}
    sigma = swaps[0]
    rng = random.Random(4892)
    seen, tried = set(), 0
    t0 = time.time()
    cur = tuple(range(B.vcount()))
    while time.time() - t0 < seconds:
        # random walk in Aut_0, then test sigma . a
        for _ in range(rng.randint(1, 6)):
            cur = compose(rng.choice(keeps or gens), cur)
        cand = compose(sigma, cur)
        if cand in seen:
            continue
        seen.add(cand)
        tried += 1
        if cand[0] >= n and is_involution(cand):
            return {"dualities_exist": True, "polarity": list(cand[:12]),
                    "tried": tried}
    return {"dualities_exist": True, "polarity": None, "tried": tried}


def main() -> int:
    print("=" * 78)
    print("Pass 4892 -- polarity search without enumerating the automorphism group")
    print("=" * 78)

    print(f"\n  {'q':>3s} {'Levi n':>7s} {'dualities':>10s} {'polarity found':>15s} "
          f"{'candidates':>11s} {'predicted':>10s} {'agrees':>7s}")
    rows = []
    for p, k in ((2, 1), (2, 2)):
        q = p ** k
        pts, lines = PP.build_w3(PP.GF(p, k))
        B, n = levi(pts, lines)
        r = search_polarity(B, n)
        found = r["polarity"] is not None
        pred = (p == 2 and k % 2 == 1)          # Tits: odd powers of 2
        rows.append({"q": q, "levi_vertices": B.vcount(),
                     "dualities_exist": r["dualities_exist"],
                     "polarity_found": found, "candidates_tried": r["tried"],
                     "predicted": pred, "agrees": found == pred})
        print(f"  {q:3d} {B.vcount():7d} {str(r['dualities_exist']):>10s} "
              f"{str(found):>15s} {r['tried']:11,d} {str(pred):>10s} "
              f"{str(found == pred):>7s}")

    agree = all(x["agrees"] for x in rows)
    q4 = next((x for x in rows if x["q"] == 4), None)
    print(f"""
    {'THE CHEAP METHOD REPRODUCES PASS 4793.' if agree else 'THE CHEAP METHOD DISAGREES WITH PASS 4793 -- READ THE ROWS.'} q = 2 finds a polarity;
    q = 4 finds none in {q4['candidates_tried'] if q4 else 0:,} distinct duality candidates.

    AND THE ASYMMETRY IN WHAT THAT PROVES IS THE WHOLE POINT. Finding a polarity is a
    CONSTRUCTION -- one witness settles it. Not finding one is a SEARCH RESULT, and this
    method cannot turn it into a proof: Pass 4793 established q = 4 has zero polarities by
    exhausting all 1,958,400 dualities, and nothing here replaces that.

    SO THE METHOD SCALES ONLY IN THE DIRECTION THAT NEEDS A WITNESS. At q = 8 it could
    confirm a polarity if one exists, which is what Tits predicts, and could never
    establish its absence. That is still the useful direction: the q = 8 prediction is
    positive (a polarity with 65 = q^2+1 absolute points), so a witness is exactly what
    would settle it.

    NOT RUN AT q = 8 HERE. The Levi graph has 1,170 vertices and igraph's generator set for
    it is large enough that a random walk over compositions of 1,170-element permutations is
    a different engineering problem from this one. Recorded as the next step rather than
    attempted and abandoned.""")

    out = {
        "boundary": ("finding a polarity is a construction and settles the question; NOT "
                     "finding one is a search result and does not. Pass 4793's q = 4 zero "
                     "came from exhausting all 1,958,400 dualities and is not replaced by "
                     "this. q = 8 is NOT attempted -- 1,170 Levi vertices is a different "
                     "engineering problem, and it is recorded as the next step rather than "
                     "attempted and abandoned"),
        "rows": rows,
        "reproduces_pass_4793": bool(agree),
        "method": ("every polarity is sigma . a for a duality sigma and a part-preserving "
                   "a, so the search is a coset walk using generators instead of an "
                   "enumeration of the group"),
        "scales_in_one_direction": ("can confirm a polarity by witness at any q; can never "
                                    "establish absence"),
        "q8_prediction_unchanged": {"polarity": True, "absolute_points": 65,
                                    "sz_order": 8 ** 2 * (8 ** 2 + 1) * 7},
    }
    fp = ROOT / "data" / "PART_W33_PASS4892_POLARITY_COSET_SEARCH.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
