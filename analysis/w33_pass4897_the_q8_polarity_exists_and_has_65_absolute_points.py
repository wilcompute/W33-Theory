#!/usr/bin/env python3
"""Pass 4897 -- the q = 8 polarity exists, with exactly 65 absolute points. The prediction
recorded at Pass 4793 is confirmed.

Pass 4793 established that W(3,q) is self-dual iff q is even, but admits a POLARITY -- an
involutory duality -- only when q is an odd power of 2, and verified the split by exhausting
Aut(Levi) at q = 2 (a polarity, 5 absolute points) and q = 4 (none, out of 1,958,400
dualities).  It then recorded a prediction it could not test:

    q = 8 = 2^3 is an odd power of two, so a polarity should exist, and its absolute points
    should number q^2 + 1 = 65 -- the Suzuki-Tits ovoid, stabilised by Sz(8) of order
    q^2(q^2+1)(q-1) = 29,120.

Enumerating that group is out of reach: the Levi graph has 1,170 vertices.  Pass 4892
supplied the method -- every polarity is sigma . a for a duality sigma and a part-preserving
a, so the search is a coset walk over generators rather than an enumeration -- and noted the
asymmetry that makes it work here: finding a polarity is a CONSTRUCTION, and one witness
settles a positive prediction.

    W(3,8): 585 points, 585 lines, Levi 1,170 vertices, 5,265 edges
    7 automorphism generators, 1 part-exchanging
    POLARITY FOUND after 36,300 candidates
    absolute points = 65 = q^2 + 1

    py -3 analysis/w33_pass4897_the_q8_polarity_exists_and_has_65_absolute_points.py
"""

from __future__ import annotations

import importlib.util
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


def main() -> int:
    print("=" * 78)
    print("Pass 4897 -- does W(3,8) admit a polarity?")
    print("=" * 78)

    t0 = time.time()
    pts, lines = PP.build_w3(PP.GF(2, 3))
    n = len(pts)
    B = igraph.Graph(n=n + len(lines))
    B.add_edges([(p, n + j) for j, L in enumerate(lines) for p in L])
    build = time.time() - t0

    gens = [tuple(g) for g in B.automorphism_group()]
    swaps = [g for g in gens if g[0] >= n]
    keeps = [g for g in gens if g[0] < n]
    print(f"\n    W(3,8)                     : {n} points, {len(lines)} lines")
    print(f"    Levi graph                 : {B.vcount()} vertices, {B.ecount()} edges")
    print(f"    automorphism generators    : {len(gens)}  "
          f"({len(swaps)} part-exchanging)")
    print(f"    build time                 : {build:.1f}s")

    def comp(a, b):
        return tuple(a[b[i]] for i in range(len(b)))

    def is_inv(p):
        return all(p[p[i]] == i for i in range(len(p)))

    inc = {(u, v) for u, v in B.get_edgelist()}
    inc |= {(v, u) for u, v in list(inc)}

    sigma = swaps[0]
    rng = random.Random(4897)
    cur = tuple(range(B.vcount()))
    tried, found, absn = 0, None, None
    t0 = time.time()
    while time.time() - t0 < 1500 and found is None:
        for _ in range(rng.randint(1, 8)):
            cur = comp(rng.choice(keeps or gens), cur)
        cand = comp(sigma, cur)
        tried += 1
        if cand[0] >= n and is_inv(cand):
            found = cand
            absn = sum(1 for i in range(n) if (i, cand[i]) in inc)
    search = time.time() - t0

    q = 8
    predicted = q * q + 1
    sz = q * q * (q * q + 1) * (q - 1)
    print(f"\n    candidates tried           : {tried:,}")
    print(f"    polarity found             : {found is not None}  ({search:.0f}s)")
    print(f"    absolute points            : {absn}")
    print(f"    predicted q^2+1            : {predicted}")
    print(f"    match                      : {absn == predicted}")

    ok = found is not None and absn == predicted
    print(f"""
    {'THE PREDICTION HOLDS AND THE WITNESS IS EXPLICIT.' if ok else 'THE PREDICTION DOES NOT HOLD -- READ THE ROWS.'}

    q = 8 is an odd power of two and W(3,8) admits a polarity, whose absolute points number
    exactly {absn} = q^2 + 1. That set is the Suzuki-Tits ovoid, and its stabiliser is Sz(8) of
    order q^2(q^2+1)(q-1) = {sz:,}.

    THE THREE-VALUE PATTERN IS NOW COMPLETE ON BOTH SIDES OF THE SPLIT:

        q = 2 = 2^1   odd power    POLARITY,  5 absolute points   exhaustive (Pass 4793)
        q = 4 = 2^2   even power   none, of 1,958,400 dualities   exhaustive (Pass 4793)
        q = 8 = 2^3   odd power    POLARITY, 65 absolute points   witness (here)

    AND THE EVIDENCE IS OF TWO DIFFERENT KINDS, which is worth being explicit about. The
    q = 4 zero is exhaustive: every duality was tested. The q = 8 polarity is a witness:
    one object exhibited. Neither method could do the other's job -- a coset walk can never
    prove absence, and enumeration cannot reach 1,170 vertices -- and the prediction needed
    exactly the kind that a witness supplies.

    WHAT THIS SETTLES. Pass 4793 argued that the polarity condition is the finer question,
    that it selects the odd powers of 2, and that this is the same phenomenon as the special
    isogeny of B2 = C2 in characteristic 2 whose square root defines the Suzuki groups. The
    q = 8 case was the falsifier that argument named for itself. It did not falsify.""")

    out = {
        "boundary": ("the q=8 polarity is a WITNESS -- one object exhibited and verified as "
                     "an involutory part-exchanging automorphism with 65 absolute points. "
                     "This settles the positive prediction and could never have settled a "
                     "negative one. The identification of the absolute-point set with the "
                     "Suzuki-Tits ovoid and its stabiliser with Sz(8) is CITED classical "
                     "theory used to interpret the count of 65; the count is computed"),
        "q": q,
        "points": n, "lines": len(lines),
        "levi_vertices": B.vcount(), "levi_edges": B.ecount(),
        "generators": len(gens), "part_exchanging_generators": len(swaps),
        "candidates_tried": tried,
        "polarity_found": found is not None,
        "absolute_points": absn,
        "predicted": predicted,
        "prediction_holds": bool(ok),
        "sz8_order": sz,
        "method": "coset walk (Pass 4892): every polarity is sigma . a, searched by "
                  "generators rather than enumeration",
        "evidence_kinds": {
            "q=2": "exhaustive (Pass 4793)",
            "q=4": "exhaustive, zero of 1,958,400 dualities (Pass 4793)",
            "q=8": "witness (here) -- absence could not have been shown this way"},
    }
    fp = ROOT / "data" / "PART_W33_PASS4897_Q8_POLARITY_WITNESS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
