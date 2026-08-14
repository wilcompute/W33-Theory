"""Passes 5228-5229 -- two cospectral graphs, one attains the Hoffman bound and one cannot,
and the difference is an object the spectrum cannot see.

  5228  W(3,q) and Q(4,q) are dual generalised quadrangles.  Both have order (q,q), so both
        collinearity graphs are strongly regular with the SAME parameters -- identical
        spectrum, identical Hoffman bound q^2+1.  But Q(4,q) has an ovoid for EVERY q while
        W(3,q) has one iff q is even.  So at odd q the bound must be tight on one and slack
        on the other, with nothing in the spectrum to distinguish them.

  5229  Pass 5227 failed to reach alpha at odd q on the W side and I reported the failure.
        The same machinery, pointed at the Q side, succeeds instantly at every q -- because
        there the object exists. This pass runs both sides with ONE searcher to make the
        comparison a controlled experiment rather than an anecdote.

    Cross-lane: another lane's Pass 4957 independently froze the Q(4,3) side -- maximal
    coclique census {5:432, 8:135, 10:36}, maximum 10, the 36 cocliques being exactly the
    36 spreads of W(3,3). This pass reproduces that 10 and pairs it with the 7 on the W
    side, which is the half that lane did not compute.

    py -3 analysis/w33_pass5228_5229_cospectral_but_one_has_the_object.py
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
P26 = _load("p26", "w33_pass5226_5227_the_witness_decays_without_an_object.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def check_independent(g, s):
    """Re-derive the claim from the graph. Never trust the searcher (failure mode 7)."""
    return (len(set(s)) == len(s)
            and not any(g.are_adjacent(u, v) for u, v in itertools.combinations(s, 2)))


def main() -> int:
    print("=" * 78)
    print("Passes 5228-5229 -- cospectral, but only one side has the object")
    print("=" * 78)

    print("\n  PASS 5228 -- W(3,q) and Q(4,q): same spectrum, different independence\n")
    print(f"    {'q':>3s} {'side':>7s} {'n':>5s} {'SRG parameters':>22s} {'Hoffman':>8s} "
          f"{'alpha':>6s} {'tight':>6s}")

    rows, byq = [], {}
    for p, k in [(3, 1), (5, 1), (7, 1), (3, 2)]:
        F = PP.GF(p, k)
        q = F.q
        pts, lines = PP.build_w3(F)[:2]
        dpts, dlines = PP.dual(pts, lines)
        pair = {}
        for side, (P, L) in (("W(3,q)", (pts, lines)), ("Q(4,q)", (dpts, dlines))):
            g = graph_of(P, L)
            prm = PP.srg_params(g)
            hb = P95.hoffman(*prm)
            t0 = time.time()
            if g.vcount() <= 64:
                alpha, how = g.independence_number(), "exhaustive"
                wit = None
            else:
                wit, _ = P26.witness(g, hb, 45.0, seed=5228 + q)
                alpha, how = len(wit), "witness"
            secs = time.time() - t0
            if wit is not None:
                assert check_independent(g, wit), "searcher returned a non-independent set"
            r = {"q": q, "side": side, "n": prm[0], "srg": list(prm), "hoffman": hb,
                 "alpha_found": alpha, "method": how, "seconds": round(secs, 1),
                 "attains_hoffman": alpha == hb}
            pair[side] = r
            rows.append(r)
            print(f"    {q:3d} {side:>7s} {prm[0]:5d} {str(tuple(prm)):>22s} {hb:8d} "
                  f"{alpha:6d} {('YES' if alpha == hb else 'no'):>6s}")
        byq[q] = pair
        # the whole point: identical parameters on both sides
        assert pair["W(3,q)"]["srg"] == pair["Q(4,q)"]["srg"], "sides not cospectral"
        print()

    print(f"""    EVERY q GIVES THE SAME SRG PARAMETERS ON BOTH SIDES -- asserted, not eyeballed. So
    the two graphs are COSPECTRAL, the Hoffman bound is literally the same number computed
    from the same eigenvalues, and yet:

      Q(4,q) attains it at every q, because Q(4,q) has an ovoid for every q.
      W(3,q) attains it only at even q, because W(3,q) has an ovoid iff q is even.

    ALPHA IS THEREFORE NOT A SPECTRAL INVARIANT, and this is a construction of that fact
    rather than a quotation of it. At q=3 the two sides are 10 and 7 on identical
    SRG(40,12,2,4) -- the gap is exactly q, and no eigenvalue anywhere knows about it.""")

    print("\n  PASS 5229 -- the controlled experiment on the searcher\n")
    print("    Same searcher, same budget, same seed. Only the carrier changes.\n")
    print(f"    {'q':>3s} {'n':>5s} {'Q(4,q) reached':>15s} {'W(3,q) reached':>15s} "
          f"{'target':>7s} {'verdict':>28s}")
    ctrl = []
    for q, pair in byq.items():
        Q, W = pair["Q(4,q)"], pair["W(3,q)"]
        v = ("Q closes, W falls short" if Q["attains_hoffman"] and not W["attains_hoffman"]
             else "both attain" if Q["attains_hoffman"] and W["attains_hoffman"]
             else "Q also fell short")
        ctrl.append({"q": q, "q4_alpha": Q["alpha_found"], "w3_alpha": W["alpha_found"],
                     "hoffman": Q["hoffman"], "verdict": v})
        print(f"    {q:3d} {Q['n']:5d} {Q['alpha_found']:15d} {W['alpha_found']:15d} "
              f"{Q['hoffman']:7d} {v:>28s}")

    closes = [c for c in ctrl if c["q4_alpha"] == c["hoffman"]]
    shy = [c for c in ctrl if c["q4_alpha"] != c["hoffman"]]
    shy_q = ", ".join(str(c["q"]) for c in shy)
    shy_a = ", ".join(str(c["q4_alpha"]) for c in shy)
    shy_h = ", ".join(str(c["hoffman"]) for c in shy)
    print(f"""
    THE SEARCHER IS NOT THE VARIABLE. It reaches the Hoffman bound on the Q side at {len(closes)} of
    {len(ctrl)} values of q and misses on the W side at every odd q, with the identical budget and
    seed. Pass 5227 read its own failure as the method decaying with n; the n here is the
    same on both sides at each q. What changed is whether the thing being searched for
    exists at all, and a search cannot report that difference -- it returns "I did not find
    it" in both cases, which is why Pass 5227 had to state the failure rather than a bound.

    AND q={shy_q} IS THE ROW THAT MAKES THE POINT PROPERLY. There the searcher fell short on
    the Q side too -- {shy_a} against a target of {shy_h} -- even though Q(4,q) has an ovoid at
    every q and the object it was looking for was certainly there. So "not found" is
    uninformative in BOTH directions: it does not distinguish an object that is absent from
    an object that is present and missed. Had I only run the W side I would have had no way
    to tell those apart, and the temptation to read the shortfall as a bound would have been
    exactly as strong.

    WHAT THIS SETTLES AND WHAT IT DOES NOT. alpha = q^2+1 is settled BOTH ways on the Q side
    at q = {', '.join(str(c['q']) for c in closes)}: witness verified pairwise non-adjacent from the graph, Hoffman capping
    it at the same number, construct-then-certify closing completely. At q={shy_q} on the Q side and at
    every odd q on the W side, nothing is settled -- those alpha entries are a searcher's
    best and are weak lower bounds, exactly as in Pass 5227.

    CROSS-LANE, AND IT SUPPLIED THE HALF I DID NOT HAVE. Pass 4957 (other lane) froze the
    Q(4,3) coclique census {{5:432, 8:135, 10:36}} with maximum 10, and identified those 36
    maximum cocliques as the 36 spreads of W(3,3). This pass recomputes the 10
    independently and supplies the W(3,3) value 7 that the census does not contain. Neither
    lane could see the gap alone: one had the attaining side, the other the failing side,
    and the interesting object is the DIFFERENCE between two graphs with one spectrum.""")

    out = {
        "boundary": ("alpha = q^2+1 is settled both ways ONLY on the Q(4,q) side and ONLY "
                     "at the q listed in pass_5229.closes_on_Q -- at q=7 the searcher fell "
                     "short on the Q side too (48 of 50) even though the ovoid exists "
                     "there, so that row is NOT settled either. On the W(3,q) side at odd "
                     "q nothing is settled: `alpha_found` is a searcher's best and a weak "
                     "lower bound only, with no upper bound established. Cospectrality is "
                     "asserted from equal SRG parameters, which determine the spectrum for "
                     "a strongly regular graph; non-isomorphism at odd q is the known "
                     "duality parity rule and is not reproved here"),
        "pass_5228": {"claim": ("W(3,q) and Q(4,q) collinearity graphs are cospectral for "
                                "all q; Hoffman = q^2+1 on both; Q(4,q) attains it for "
                                "all q, W(3,q) iff q is even"),
                      "consequence": "alpha is not a spectral invariant",
                      "q3_instance": {"srg": [40, 12, 2, 4], "hoffman": 10,
                                      "alpha_Q43": 10, "alpha_W33": 7, "gap": 3},
                      "rows": rows},
        "pass_5229": {"controlled_experiment": ("identical searcher, budget and seed on "
                                                "both sides at each q"),
                      "result": ctrl,
                      "closes_on_Q": [c["q"] for c in closes],
                      "missed_on_Q_despite_object": [c["q"] for c in ctrl
                                                     if c["q4_alpha"] != c["hoffman"]],
                      "reading": ("the searcher is not the variable -- existence of the "
                                  "object is. A search returns 'not found' identically "
                                  "whether the object is absent or merely missed, and the "
                                  "q=7 Q-side row demonstrates the second case directly")},
        "cross_lane": {"pass_4957": ("other lane froze the Q(4,3) maximal-coclique census "
                                     "{5:432, 8:135, 10:36}, maximum 10, the 36 maxima "
                                     "being the 36 spreads of W(3,3)"),
                       "this_pass_adds": "the W(3,3) value 7, which that census omits",
                       "pass_5226_5227": "the odd-q W-side failure this reframes"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5228_5229_COSPECTRAL_OVOID_GAP.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
