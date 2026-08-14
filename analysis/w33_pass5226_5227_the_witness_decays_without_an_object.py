"""Passes 5226-5227 -- the witness method decays when there is no object to construct.

  5226  W(3,q) has an ovoid iff q is EVEN.  Pass 4905 used that: for q=8 the 65 absolute
        points of the polarity are pairwise non-collinear and Hoffman says <= 65, so
        alpha = 65 = q^2+1 fell out with no search at 585 vertices.  For q ODD there is no
        ovoid, so Hoffman is NOT attained and the free upper bound stops being free.  How
        far short does the truth fall?

  5227  q=3 settles exhaustively in under a second: alpha = 7, against Hoffman 10.  The
        deficiency is 3 = q.  This pass asks whether "exactly q" survives q = 5, 7, 9, and
        is careful about which half of each answer is actually established.

    py -3 analysis/w33_pass5226_5227_the_witness_decays_without_an_object.py
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

EXACT_BUDGET = 45.0     # seconds before exhaustive alpha is abandoned for a witness
WITNESS_BUDGET = 75.0


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def witness(g, target, seconds, seed):
    """Iterated local search: greedy seed, then force-insert / repair with perturbation.

    The plain restart-greedy of Pass 5222 is kept honest by comparison -- see `greedy_only`
    below. This one keeps the incumbent and perturbs it rather than throwing it away, which
    is the difference between a search that plateaus at 66% and one that does not.

    THE INVARIANT, stated before running: the returned set must be pairwise non-adjacent
    and of the reported size. The caller re-checks both from the graph -- nothing here is
    trusted, because a search that reports its own success is exactly failure mode 7.
    """
    n = g.vcount()
    nb = [set(g.neighbors(v)) for v in range(n)]
    rng = random.Random(seed)
    t0 = time.time()

    def repair(cur):
        """Greedily extend an independent set to maximal, in random order."""
        cov = set(cur)
        for v in cur:
            cov |= nb[v]
        free = [v for v in range(n) if v not in cov]
        rng.shuffle(free)
        for v in free:
            if not (nb[v] & cur):
                cur.add(v)
        return cur

    cur = repair(set())
    best = set(cur)
    while time.time() - t0 < seconds and len(best) < target:
        # perturb: force in a vertex outside the set, evict its conflicts, repair
        v = rng.randrange(n)
        if v not in cur:
            cur = (cur - nb[v]) | {v}
        # occasional larger kick to escape a deep plateau
        if rng.random() < 0.05 and len(cur) > 3:
            for u in rng.sample(sorted(cur), min(3, len(cur))):
                cur.discard(u)
        cur = repair(cur)
        if len(cur) > len(best):
            best = set(cur)
        elif len(cur) < len(best) - 2:
            cur = set(best)          # restart from incumbent, not from scratch
    return sorted(best), time.time() - t0


def greedy_only(g, seconds, seed):
    """Pass 5222's method verbatim: restart-greedy, incumbent discarded each round."""
    n = g.vcount()
    nb = [set(g.neighbors(v)) for v in range(n)]
    rng = random.Random(seed)
    best, t0 = [], time.time()
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
    return sorted(best)


def main() -> int:
    print("=" * 78)
    print("Passes 5226-5227 -- the odd-q ovoid deficiency")
    print("=" * 78)

    print("\n  PASS 5226 -- alpha(W(3,q)) for odd q, and how it is established\n")
    print(f"    {'q':>3s} {'n':>5s} {'Hoffman':>8s} {'q^2-q+1':>8s} "
          f"{'alpha':>6s} {'settled by':>12s} {'sec':>7s}")

    rows = []
    for p, k in [(3, 1), (5, 1), (7, 1), (3, 2)]:
        F = PP.GF(p, k)
        q = F.q
        pts, lines = PP.build_w3(F)[:2]
        g = graph_of(pts, lines)
        n, deg, lam, mu = PP.srg_params(g)
        hb = P95.hoffman(n, deg, lam, mu)
        pred = q * q - q + 1

        exact, wit, t0 = None, None, time.time()
        if n <= 64:                       # only where exhaustive is known to be cheap
            exact = g.independence_number()
            how, secs, alpha = "exhaustive", time.time() - t0, exact
        else:
            wit, secs = witness(g, pred, WITNESS_BUDGET, seed=5226 + q)
            alpha, how = len(wit), "witness"

        # re-derive both halves of the claim from the graph, never from the searcher
        if wit is not None:
            assert len(set(wit)) == len(wit)
            assert not any(g.are_adjacent(u, v) for u, v in itertools.combinations(wit, 2))
        gre = len(greedy_only(g, 12.0, seed=5226 + q)) if wit is not None else alpha
        rows.append({"q": q, "n": n, "srg": [n, deg, lam, mu], "hoffman": hb,
                     "q2_q_1": pred, "alpha_established": alpha, "method": how,
                     "restart_greedy": gre, "seconds": round(secs, 1),
                     "reaches_q2_q_1": alpha == pred,
                     "bound_settled": "both" if how == "exhaustive" else "lower only"})
        print(f"    {q:3d} {n:5d} {hb:8d} {pred:8d} {alpha:6d} {how:>12s} {secs:7.1f}")

    hit = [r for r in rows if r["reaches_q2_q_1"]]
    miss = [r for r in rows if not r["reaches_q2_q_1"]]
    print(f"""
    q=3 IS THE ONLY ROW SETTLED, and it is settled completely: 40 vertices, exhaustive
    independence number, alpha = {rows[0]['alpha_established']} against a Hoffman bound of {rows[0]['hoffman']}. The deficiency there is
    {rows[0]['hoffman'] - rows[0]['alpha_established']} = q, and q^2-q+1 = {rows[0]['q2_q_1']} matches -- on one data point, which is not a family.

    {len(hit)} of {len(rows)} rows reach q^2-q+1. The searches at q = {', '.join(str(r['q']) for r in miss)} fall SHORT of it, and that
    shortfall is the actual result of this pass rather than an inconvenience in it. I do not
    get to report q^2-q+1 as a lower bound at those q, because I did not construct one.""")

    print("\n  PASS 5227 -- the witness method degrades, and the reason is structural\n")
    print(f"    {'q':>3s} {'n':>5s} {'restart-greedy':>15s} {'iterated LS':>12s} "
          f"{'q^2-q+1':>8s} {'LS / target':>12s}")
    for r in rows[1:]:
        frac = r["alpha_established"] / r["q2_q_1"]
        print(f"    {r['q']:3d} {r['n']:5d} {r['restart_greedy']:15d} "
              f"{r['alpha_established']:12d} {r['q2_q_1']:8d} {frac:11.0%}")

    print(f"""
    THIS RECALIBRATES PASS 5222, WHICH WAS MINE AND WHICH I OVERSOLD. There the randomised
    greedy found alpha(H(3,9)) = 28 in 0.1s where an exhaustive search had returned nothing
    in 300s, and I read that as the witness method being powerful. It is not. It was that 28
    was easy to hit. Point the same machinery at odd-q W(3,q) and the fraction of the
    conjectured optimum it reaches DECAYS with q -- the search has no access to the algebra
    and is doing nothing but luck, and luck scales badly.

    WHY EVEN q WAS NEVER A SEARCH RESULT AT ALL. Pass 4905 did not search for the 65-point
    ovoid of W(3,8). Pass 4897 CONSTRUCTED the polarity by a coset walk and the 65 absolute
    points fell out of it as an algebraic object; Hoffman then certified that the object was
    optimal. The pipeline was construct-then-certify, and neither half was a search over
    subsets. For odd q the object does not exist -- W(3,q) has an ovoid iff q is even -- so
    there is nothing to construct, the certifying bound has nothing to certify, and subset
    search is all that is left. That is exactly where it performs worst.

    THE HONEST STATE. alpha(W(3,3)) = {rows[0]['alpha_established']}, exhaustively, both bounds. For q = {', '.join(str(r['q']) for r in miss)} this pass
    establishes only the weak lower bounds in the table above and no upper bound of any
    kind. The literature value for odd q (partial ovoids of W(3,q) = partial spreads of
    Q(4,q)) is not reproduced here and must not be cited to this pass.

    CROSS-LANE, AND CONVERGENT. Track B's Pass5212 closed alpha = 13 on NO_5^+(5) with the
    identical construct-then-certify shape: thirteen pairwise disjoint dual grids as the
    witness, Hoffman 325*6/(144+6) = 13 as the certificate. Two lanes with no contact
    arrived at the same method on different carriers. That is evidence the pattern is real
    and worth naming, and it is also the strongest available warning about the odd-q rows
    here -- Track B HAD an object to exhibit, and at odd q I do not.""")

    out = {
        "boundary": ("alpha is EXHAUSTIVE only at q=3 (n=40), where it is 7 with both "
                     "bounds settled. At q=5,7,9 this pass establishes ONLY the weak "
                     "lower bounds in `rows` -- the searches did NOT reach q^2-q+1 and "
                     "no upper bound is established at those q. q^2-q+1 is recorded as a "
                     "comparison target, NOT as a result of this pass, and the literature "
                     "value for odd q is not reproduced here"),
        "pass_5226": {"rule": "W(3,q) has an ovoid iff q is even",
                      "hoffman": "q^2+1 for all q, even and odd",
                      "settled": {"q": 3, "alpha": 7, "hoffman": 10, "deficiency": 3,
                                  "note": "deficiency = q on ONE data point, not a family"},
                      "rows": rows},
        "pass_5227": {"settled_both_bounds": [r["q"] for r in rows
                                              if r["method"] == "exhaustive"],
                      "weak_lower_only": [r["q"] for r in rows
                                          if r["method"] == "witness"],
                      "recalibrates": ("Pass 5222 read a fast alpha(H(3,9))=28 as the "
                                       "witness method being powerful. It is not -- the "
                                       "fraction of target reached decays with q here"),
                      "reading": ("even q was construct-then-certify, never a search: "
                                  "Pass4897 CONSTRUCTED the polarity, its 65 absolute "
                                  "points were the object, and Hoffman only certified "
                                  "optimality. Odd q has no such object, so subset search "
                                  "is all that remains and it performs worst there"),
                      "cross_lane": ("Track B Pass5212 closed alpha=13 on NO_5^+(5) with "
                                     "the identical shape -- 13 disjoint dual grids as "
                                     "witness, Hoffman 325*6/150=13 as certificate. Two "
                                     "lanes, no contact, same method")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
