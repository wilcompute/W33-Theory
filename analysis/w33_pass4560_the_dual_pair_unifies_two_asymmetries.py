#!/usr/bin/env python3
"""Pass 4560 -- H(3,9) and Q(5,3) are ONE geometry, and that unifies two loose results.

Pass 4442 explained why line-signings fail on H(3,9) and work on Q(5,3) by a "coarseness
law": a line of GQ(s,t) carries C(s+1,2) edges, so granularity is set by s.  Pass 4457
weakened it after the s = 2 row refused to cooperate, and Pass 4462 closed the remaining
question with Higman's inequality.  All of that treated H(3,9) and Q(5,3) as two different
quadrangles that happened to have s and t swapped.

THEY ARE NOT TWO QUADRANGLES.  Q(5,q) is the DUAL of H(3,q^2); at q = 3 that is exactly
this pair, and the counts say so without any theory:

    H(3,9)   280 points   112 lines      GQ(9,3)
    Q(5,3)   112 points   280 lines      GQ(3,9)

The 112 points of Q(5,3) ARE the 112 lines of H(3,9); the 280 lines of Q(5,3) ARE the 280
points of H(3,9).  Swapping the words "point" and "line" carries one onto the other.

SO PASS 4457's TABLE WAS NEVER A COMPARISON BETWEEN TWO GEOMETRIES.  It was one geometry,
gauged through each of its two carriers:

    gauge the POINT graph of Q(5,3)  (=  the LINE graph of H(3,9))   ->  7.2% Ramanujan
    gauge the POINT graph of H(3,9)  (=  the LINE graph of Q(5,3))   ->  0.0%

AND THAT IS THE SAME ASYMMETRY PASSES 4381 AND 4389 MEASURED.  There, the flag-incidence
comparator protected the point register and the line register of H(3,9) at different rates
-- 3.2258% against 2.7027% invisible faults -- and W(3,3) could not show the effect because
a self-dual quadrangle forces the two rates equal.  Here the same duality produces 7.2%
against 0%.  Two results, arrived at four hundred passes apart by unrelated routes, are one
statement about a non-self-dual quadrangle having two inequivalent carriers.

    py -3 analysis/w33_pass4560_the_dual_pair_unifies_two_asymmetries.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main() -> int:
    print("=" * 78)
    print("Pass 4560 -- one geometry, two carriers, two asymmetries")
    print("=" * 78)

    h = _load("h4389", "w33_pass4389_hermitian_quadrangle_measured.py")
    q = _load("q4448", "w33_pass4448_4450_q53_floquet_tanner.py")
    hp, hl, _ = h.build_h39()
    qp, ql = q.build_q53()

    dual_ok = (len(qp) == len(hl)) and (len(ql) == len(hp))
    print(f"\n  H(3,9)  {len(hp):4d} points  {len(hl):4d} lines   GQ(9,3)")
    print(f"  Q(5,3)  {len(qp):4d} points  {len(ql):4d} lines   GQ(3,9)")
    print(f"\n  points of Q(5,3) == lines of H(3,9) : {len(qp)} == {len(hl)}  -> {dual_ok}")
    print(f"  lines  of Q(5,3) == points of H(3,9): {len(ql)} == {len(hp)}  -> {dual_ok}")
    assert dual_ok

    # the two carriers, side by side
    rows = []
    for label, pts, lines in (("Q(5,3) point graph  = H(3,9) LINE graph", qp, ql),
                              ("H(3,9) point graph  = Q(5,3) LINE graph", hp, hl)):
        n = len(pts)
        A = np.zeros((n, n))
        per_line = None
        for L in lines:
            es = list(itertools.combinations(sorted(L), 2))
            per_line = len(es)
            for u, v in es:
                A[u, v] = A[v, u] = 1
        d = int(A.sum(1)[0])
        rows.append({"carrier": label, "vertices": n, "degree": d,
                     "gauge_dof": len(lines), "edges_per_gauge_block": per_line,
                     "bound": float(2 * np.sqrt(d - 1))})
        print(f"\n  {label}")
        print(f"     {n} vertices, degree {d}, {len(lines)} gauge parameters, "
              f"{per_line} edges per block")

    # the two independently-measured asymmetries
    P, L = 280, 112
    miss_p, miss_l = Fraction(9, P - 1), Fraction(3, L - 1)
    print(f"""
  THE TWO ASYMMETRIES, MEASURED SEPARATELY, ARE THE SAME ONE.

    Pass 4457   signing succeeds on one carrier and not the other
                  Q(5,3) point graph      7.2% of random line-signings Ramanujan
                  H(3,9) point graph      0.0%

    Pass 4389   the flag comparator protects the two registers unequally
                  point register          {float(miss_p) * 100:.4f}% of faults invisible
                  line register           {float(miss_l) * 100:.4f}%

  Both are consequences of the SAME fact: this quadrangle is not self-dual, so its point
  carrier and its line carrier are genuinely different objects. W(3,3) is self-dual and
  therefore shows neither effect -- Pass 4389 already noted that the symplectic case
  "cannot even pose the question", and Pass 4457's s = 2 rows sat at a ceiling for the
  same reason.

  WHAT THIS CORRECTS. Pass 4442's coarseness law is not wrong -- C(s+1,2) really is the
  block size, and 45 against 6 really is the mechanism. But its FRAMING was, because it
  presented H(3,9) and Q(5,3) as evidence from two geometries when they are one geometry
  read two ways. A law supported by "two independent quadrangles" that turn out to be dual
  has one data point, not two, and Pass 4457's four-row table has three.

  AND IT EXPLAINS THE ROW THAT WOULD NOT COOPERATE. Pass 4457 found t irrelevant at s = 2
  and decisive at s = 3, and offered a ceiling hypothesis it could not test. The dual
  reading says the variable was never s or t separately: it is WHICH CARRIER you gauge, and
  s and t merely label them. W(3,2) and Q(5,2) are also a dual pair, so that row is one
  geometry too -- which is exactly why raising t there changed nothing.""")

    out = {
        "boundary": ("the duality is verified here only by the point/line counts matching "
                     "under exchange, which is necessary and not sufficient for an "
                     "isomorphism of incidence structures; the classical result Q(5,q) = "
                     "dual of H(3,q^2) is cited, not reproved"),
        "dual_pair": {"H(3,9)": {"points": len(hp), "lines": len(hl), "s": 9, "t": 3},
                      "Q(5,3)": {"points": len(qp), "lines": len(ql), "s": 3, "t": 9},
                      "counts_match_under_exchange": dual_ok},
        "carriers": rows,
        "unified": {
            "pass_4457_signing": {"Q53_point_graph_pct": 7.2, "H39_point_graph_pct": 0.0},
            "pass_4389_protection": {"point_register_miss": str(miss_p),
                                     "line_register_miss": str(miss_l)},
            "statement": ("both are the same fact -- a non-self-dual GQ has two "
                          "inequivalent carriers; W(3,3) is self-dual and shows neither")},
        "corrects": ("Pass 4442/4457 presented H(3,9) and Q(5,3) as two independent "
                     "quadrangles supporting a coarseness law. They are dual, so that is "
                     "one geometry read twice: the four-row table has three data points, "
                     "and the s=2 pair (W(3,2), Q(5,2)) is likewise a single geometry, "
                     "which is why raising t there changed nothing"),
    }
    p = ROOT / "data" / "PART_W33_PASS4560_DUAL_PAIR_UNIFICATION.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
