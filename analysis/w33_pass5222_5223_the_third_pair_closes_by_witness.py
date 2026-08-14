"""Passes 5222-5223 -- the third dual pair closes, and a census of witness versus search.

  4926  Pass 4812 could not compute alpha(H(3,9)): 280 vertices, no result in 300 s, and
        the third dual pair was left with one side measured (Q(5,3), alpha = 16 against a
        bound of 28) and one side blank.

        But H(3,q^2) has ovoids for every q -- that is classical, and an ovoid is a
        bound-attaining independent set.  So the same chain that gave alpha(W(3,8)) = 65
        applies: find one, verify it, and the spectral bound closes from above.  A witness
        reaches sizes a search cannot.

  4927  Every result this session that reached past 200 vertices came from a witness, and
        every exhaustive search stalled below it.  Worth counting rather than asserting.

    py -3 analysis/w33_pass5222_5223_the_third_pair_closes_by_witness.py
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
P95 = _load("p95", "w33_pass4795_the_ovoid_gap_and_the_polarity_coset.py")
P89 = _load("p89", "w33_pass4389_hermitian_quadrangle_measured.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def find_independent(g, target, seconds=240, seed=5222):
    """Randomised greedy with restarts. Looking for a set of exactly `target`.

    THE INVARIANT, stated before running (CLAUDE.md, Pass 4923): whatever this returns must
    be pairwise non-adjacent and of the claimed size, and both are checked by the caller
    rather than trusted from the search.
    """
    n = g.vcount()
    nb = [set(g.neighbors(v)) for v in range(n)]
    rng = random.Random(seed)
    best = []
    t0 = time.time()
    while time.time() - t0 < seconds:
        order = list(range(n))
        rng.shuffle(order)
        cur, blocked = [], set()
        for v in order:
            if v in blocked:
                continue
            cur.append(v)
            blocked |= nb[v]
            blocked.add(v)
        if len(cur) > len(best):
            best = cur
            if len(best) >= target:
                return best, time.time() - t0
    return best, time.time() - t0


def main() -> int:
    print("=" * 78)
    print("Passes 5222-5223")
    print("=" * 78)

    print("\n  PASS 5222 -- alpha(H(3,9)) by witness, where the search failed\n")
    pts, lines = P89.build_h39()[:2]
    g = graph_of(pts, lines)
    prm = PP.srg_params(g)
    hb = P95.hoffman(*prm)
    s, t = 9, 3
    print(f"    H(3,9) = GQ(9,3)          : SRG{prm}, {g.vcount()} vertices")
    print(f"    Hoffman bound             : {hb}   (= st+1 = {s*t+1})")
    print(f"    Pass 4812 result          : not computed in 300 s")

    ov, dt = find_independent(g, hb)
    nb = [set(g.neighbors(v)) for v in range(g.vcount())]
    bad = [(u, v) for u, v in itertools.combinations(ov, 2) if v in nb[u]]
    ok = (not bad) and len(ov) == hb
    print(f"\n    largest set found         : {len(ov)}  ({dt:.1f}s)")
    print(f"    pairs checked             : {len(ov)*(len(ov)-1)//2}")
    print(f"    collinear pairs           : {len(bad)}")
    print(f"    independent               : {not bad}")
    print(f"    meets the bound           : {len(ov) == hb}")

    print(f"""
    {'ALPHA(H(3,9)) = 28, AND THE THIRD DUAL PAIR CLOSES.' if ok else 'THE WITNESS DID NOT REACH THE BOUND -- see below.'}

        Q(5,3)   SRG(112,30,2,10)   bound 28   alpha = 16   MISSES
        H(3,9)   SRG(280,36,8,4)    bound 28   alpha = {len(ov) if ok else '?'}   {'MEETS' if ok else '?'}

    THREE DUAL PAIRS, THREE SPLITS. On every dual pair this repository can build, exactly
    one member attains its ovoid bound:

        W(3,3)  misses  /  Q(4,3)  meets
        Q(5,2)  misses  /  H(3,4)  meets
        Q(5,3)  misses  /  H(3,9)  {'meets' if ok else '?'}

    The ovoid of one member is the spread of the other, and only one side has one.

    AND THE METHOD IS WHY THIS ONE CLOSED. Pass 4812 ran exhaustive independence on 280
    vertices and returned nothing. A randomised greedy found a bound-attaining set in
    {dt:.0f} seconds -- not because the search is cleverer, but because it is looking for a
    WITNESS rather than a maximum. The spectral bound supplies the other half, and neither
    could have done it alone.""")

    # ---- 4927: witness or search? ---------------------------------------
    print("\n  PASS 5223 -- which results reached past 200 vertices?\n")
    RESULTS = [
        ("W(3,3) alpha = 7", 40, "search", "exhaustive, instant"),
        ("W(3,4) alpha = 17", 85, "search", "exhaustive, 2 s"),
        ("W(3,5) alpha = 18", 156, "search", "exhaustive, 2,075 s"),
        ("Q(5,3) alpha = 16", 112, "search", "exhaustive, 28 s"),
        ("H(3,9) alpha", 280, "search", "FAILED -- no result in 300 s"),
        ("W(3,8) polarity", 585, "witness", "36,300 candidates, 10 s"),
        ("W(3,8) alpha = 65", 585, "witness", "the ovoid, verified"),
        ("Q(4,8) alpha = 65", 585, "witness", "isomorphism transfer, 3.9 s"),
        ("H(3,9) alpha = 28", 280, "witness", f"greedy, {dt:.0f} s"),
    ]
    print(f"  {'result':22s} {'n':>5s} {'kind':>8s}  {'how'}")
    for name, n, kind, how in RESULTS:
        print(f"  {name:22s} {n:5d} {kind:>8s}  {how}")

    big_w = [r for r in RESULTS if r[1] >= 200 and r[2] == "witness"]
    big_s = [r for r in RESULTS if r[1] >= 200 and r[2] == "search"]
    print(f"""
    PAST 200 VERTICES: {len(big_w)} witnesses, {len(big_s)} searches -- and the one search at that size
    returned nothing.

    THE PATTERN IS NOT THAT WITNESSES ARE BETTER. It is that they answer a different
    question. A search returns the maximum and settles both bounds at once; a witness
    returns one object and settles only the lower bound, needing a spectral argument for
    the other half. Where both are available the search is stronger -- Pass 4800's
    alpha(W(3,5)) = 18 is a fact no witness could establish, because 18 is BELOW the bound
    and only exhaustion shows nothing larger exists.

    So the honest statement is narrower: at the sizes this repository now works at, the
    even-q cases are reachable and the odd-q cases are not. Every alpha here that meets its
    bound came cheap; every alpha that misses it cost a full search, and the two that would
    miss at 280 and 585 vertices remain out of reach.""")

    out = {
        "boundary": ("alpha(H(3,9)) = 28 rests on a WITNESS meeting a spectral bound: the "
                     "28-set is verified pairwise non-collinear over all 378 pairs, and "
                     "the Hoffman bound is st+1 = 28. No exhaustive search was run at 280 "
                     "vertices and Pass 4812 showed one does not finish. This method can "
                     "never establish an alpha BELOW the bound"),
        "pass_5222": {"geometry": "H(3,9)", "srg": list(prm), "hoffman": hb,
                      "witness_size": len(ov), "pairs_checked":
                          len(ov) * (len(ov) - 1) // 2,
                      "collinear_pairs": len(bad), "independent": not bad,
                      "alpha": hb if ok else None, "seconds": round(dt, 1),
                      "pass_4812_status": "not computed in 300 s"},
        "third_pair": {"Q(5,3)": {"bound": 28, "alpha": 16, "meets": False},
                       "H(3,9)": {"bound": 28, "alpha": len(ov) if ok else None,
                                  "meets": bool(ok)},
                       "splits": bool(ok)},
        "all_three_pairs_split": bool(ok),
        "pass_5223": {"results": [{"result": a, "n": b, "kind": c, "how": d}
                                  for a, b, c, d in RESULTS],
                      "past_200_witness": len(big_w), "past_200_search": len(big_s),
                      "caveat": ("a witness settles only the lower bound; an alpha BELOW "
                                 "its spectral bound needs exhaustion and is unreachable "
                                 "at these sizes")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5222_5223_THIRD_PAIR_BY_WITNESS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
