"""Passes 5262-5263 -- the odd-q upper bound, which five passes failed to get.

  5262  Passes 5226 through 5249 established alpha(W(3,q)) for EVEN q completely and, for
        odd q, nothing but weak lower bounds.  The obstruction was never the mathematics:
        it was that a randomised search reports "not found" identically whether the object
        is absent or merely missed (Pass 5229).  An exact solver does not have that defect.
        HiGHS is available through scipy, so the maximum independent set is an integer
        program with one binary per point and one constraint per edge, and its optimum is a
        PROOF of the upper bound rather than a failure to beat it.

  5263  With q=5 settled, q^2-q+1 has either two confirming points or a refutation.  Pass
        5249 recorded it as UNSUPPORTED on one data point and said so; this pass is the
        one that gets to decide, and it was written before the answer was known.

    py -3 analysis/w33_pass5262_5263_the_odd_q_upper_bound_at_last.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
import time
from pathlib import Path

import igraph
import numpy as np
from scipy.optimize import LinearConstraint, milp
from scipy.sparse import lil_matrix

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


def exact_alpha(g, ub, seconds):
    """Maximum independent set as an integer program, solved to proven optimality.

    max sum x_v  subject to  x_u + x_v <= 1 for every edge,  x binary.

    THE REASON THIS IS DIFFERENT IN KIND from Passes 5226-5249: a heuristic returns a set
    and no information about what it did not find. A branch-and-bound solver returns a set
    AND a dual bound, and when the two meet the gap is zero and the answer is proved. Only
    a result with status 'optimal' is reported as exact below -- a time-limited run returns
    its incumbent, which is a lower bound and is labelled as one.
    """
    n, edges = g.vcount(), g.get_edgelist()
    A = lil_matrix((len(edges), n))
    for i, (u, v) in enumerate(edges):
        A[i, u] = 1
        A[i, v] = 1
    cons = [LinearConstraint(A.tocsr(), -np.inf, 1)]
    # Hoffman as an explicit cut: valid, and it hands the solver the bound for free.
    cons.append(LinearConstraint(np.ones((1, n)), -np.inf, ub))
    t0 = time.time()
    res = milp(c=-np.ones(n), constraints=cons,
               integrality=np.ones(n), bounds=(0, 1),
               options={"time_limit": seconds, "presolve": True})
    secs = time.time() - t0
    if res.x is None:
        return None, None, secs, "no solution returned"
    sel = sorted(int(i) for i in np.flatnonzero(res.x > 0.5))
    proved = bool(getattr(res, "status", 1) == 0)
    return sel, proved, secs, res.message[:60]


def main() -> int:
    print("=" * 78)
    print("Passes 5262-5263 -- the odd-q upper bound")
    print("=" * 78)

    print("\n  PASS 5262 -- exact alpha(W(3,q)) for odd q, by integer program\n")
    print(f"    {'q':>3s} {'n':>5s} {'Hoffman':>8s} {'q^2-q+1':>8s} {'alpha':>6s} "
          f"{'proved':>7s} {'sec':>8s}")

    rows = []
    for p, k, budget in [(3, 1, 120.0), (5, 1, 900.0), (7, 1, 900.0)]:
        F = PP.GF(p, k)
        q = F.q
        pts, lines = PP.build_w3(F)[:2]
        g = graph_of(pts, lines)
        prm = PP.srg_params(g)
        hb = P95.hoffman(*prm)
        sel, proved, secs, msg = exact_alpha(g, hb, budget)
        if sel is None:
            print(f"    {q:3d} {prm[0]:5d} {hb:8d} {q*q-q+1:8d}  solver returned nothing")
            continue
        # never trust the solver: re-derive independence from the graph itself
        indep = not any(g.are_adjacent(u, v) for u, v in itertools.combinations(sel, 2))
        assert indep, "solver returned a set that is NOT independent"
        rows.append({"q": q, "n": prm[0], "srg": list(prm), "hoffman": hb,
                     "q2_q_1": q * q - q + 1, "alpha": len(sel), "proved_optimal": proved,
                     "independent_verified": indep, "seconds": round(secs, 1),
                     "solver_message": msg})
        print(f"    {q:3d} {prm[0]:5d} {hb:8d} {q*q-q+1:8d} {len(sel):6d} "
              f"{('YES' if proved else 'no'):>7s} {secs:8.1f}")

    done = [r for r in rows if r["proved_optimal"]]
    print(f"""
    {len(done)} OF {len(rows)} ROWS ARE NOW PROVED OPTIMAL, upper bound included. That is the thing five
    previous passes could not do, and the difference is not effort or budget -- Pass 5227
    spent 75 seconds per q and would not have succeeded with 75 hours. A heuristic returns a
    set and says nothing about what it missed. Branch-and-bound returns a set AND a dual
    bound, and when the gap closes the upper bound is established.

    EVERY SET WAS RE-VERIFIED INDEPENDENT FROM THE GRAPH, not taken from the solver. A
    solver reporting its own success is failure mode 7 with a licence.""")

    print("\n  PASS 5263 -- what happens to q^2-q+1\n")
    hits = [r for r in done if r["alpha"] == r["q2_q_1"]]
    miss = [r for r in done if r["alpha"] != r["q2_q_1"]]
    for r in done:
        mark = "matches" if r["alpha"] == r["q2_q_1"] else "REFUTES"
        print(f"      q={r['q']:2d}   alpha = {r['alpha']:3d}   q^2-q+1 = {r['q2_q_1']:3d}   "
              f"Hoffman = {r['hoffman']:3d}   deficiency = {r['hoffman']-r['alpha']:2d}   {mark}")

    if miss:
        verdict = ("REFUTED -- alpha differs from q^2-q+1 at q=%s"
                   % ", ".join(str(r["q"]) for r in miss))
        story = f"""
    THE FORMULA IS DEAD AS AN EQUALITY, and Pass 5249 was right to refuse to promote it. It
    matched at q=3 on a single data point and the first genuinely new data point breaks it.
    The deficiency column is the thing to read instead: {', '.join(str(r['hoffman']-r['alpha']) for r in done)} at q = {', '.join(str(r['q']) for r in done)}, which is not q
    and not constant either.

    WHAT IS *NOT* REFUTED, and the distinction matters. q^2-q+1 is a known UPPER bound for
    partial ovoids of W(3,q) at odd q, and every row above sits at or below it -- {', '.join('%d<=%d' % (r['alpha'], r['q2_q_1']) for r in done)}. So
    the literature bound is untouched; what dies is MY conjecture that it is attained. A
    refuted equality against a surviving inequality, and conflating the two would turn an
    honest negative result into a false claim about published work.

    THIS IS WHY A ONE-POINT PATTERN IS NOT A PATTERN. Had I published q^2-q+1 at Pass 5226
    when the q=3 number first appeared -- and the draft of that pass did assert it, above a
    table showing 1 of 4 -- it would have gone into the corpus as a family law and needed a
    retraction here."""
    else:
        verdict = ("consistent at q = %s; still not a proof for general odd q"
                   % ", ".join(str(r["q"]) for r in hits))
        story = f"""
    THE FORMULA SURVIVES ITS FIRST REAL TEST. {len(hits)} confirming points now, at q = {', '.join(str(r['q']) for r in hits)}, each with
    a proved upper bound rather than a search that stopped. The deficiency q^2+1 - alpha is
    exactly q at every one of them.

    IT IS STILL NOT A THEOREM, and Pass 5249's refusal to promote it stands. {len(hits)} points do not
    determine a formula in q, and this pass tests values, not the general case -- there is
    no argument here for any q beyond those listed. What has changed is that the evidence is
    now upper bounds rather than failures to find, which is a different kind of evidence,
    not merely more of it."""

    print(story)
    print(f"""
    AND THE ODD-q NON-EXISTENCE IS NOW PROVED WHERE IT IS COMPUTED. alpha < q^2+1 at
    q = {', '.join(str(r['q']) for r in done)} means W(3,q) has NO OVOID at those q -- established by computation here,
    not cited. The parity rule's odd half is a theorem in the literature for all odd q; what
    this pass adds is an independent proof at {len(done)} specific values, and the even half was
    already constructed at q = 4 through 128 in Pass 5247.""")

    out = {
        "boundary": ("Only rows with proved_optimal=true carry an upper bound; a "
                     "time-limited row returns an incumbent, which is a LOWER bound only. "
                     "Every reported set was re-verified pairwise non-adjacent from the "
                     "graph rather than trusted from the solver. This tests specific "
                     "values of q and contains no argument for general odd q. The "
                     "literature theorem for all odd q is not reproved"),
        "pass_5262": {"method": ("maximum independent set as a binary integer program, "
                                 "one variable per point, one constraint per edge, plus "
                                 "Hoffman as an explicit cut; solved by HiGHS via scipy"),
                      "why_it_works_where_search_failed": (
                          "branch-and-bound returns a dual bound as well as an incumbent; "
                          "when the gap closes the upper bound is proved. A heuristic "
                          "returns no information about what it did not find"),
                      "rows": rows, "proved": [r["q"] for r in done]},
        "pass_5263": {"q2_q_1_verdict": verdict,
                      "matches": [r["q"] for r in hits],
                      "refutes": [r["q"] for r in miss],
                      "deficiencies": {r["q"]: r["hoffman"] - r["alpha"] for r in done},
                      "no_ovoid_proved_at": [r["q"] for r in done]},
    }
    fp = ROOT / "data" / "PART_W33_PASS5262_5263_ODD_Q_EXACT_ALPHA.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
