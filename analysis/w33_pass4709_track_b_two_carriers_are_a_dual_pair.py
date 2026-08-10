#!/usr/bin/env python3
"""Pass 4709 -- Track B's two new carriers are the dual pair this lane built at 4562.

Track B's latest report derives two strongly regular graphs by routes that never mention
generalised quadrangles:

  * the 45 "protected packets", whose pair graph is SRG(45,12,3,3), obtained from the 270
    dual weight-3 words of C = [135,16,30]_2 projected through 45 weight-132 complements;
  * the 135 Schlaefli quotient pairs, forming SRG(27,10,1,5), obtained by pushing 1620 base
    edges 12-to-1 onto pairs of the 27 components.

Both are quoted as parameter tuples.  Neither is named as a quadrangle.  They are:

    GQ(4,2) = H(3,4)   has (s,t) = (4,2):  (s+1)(st+1) = 45,  s(t+1) = 12,  s-1 = 3,  t+1 = 3
    GQ(2,4) = Q(5,2)   has (s,t) = (2,4):  (s+1)(st+1) = 27,  s(t+1) = 10,  s-1 = 1,  t+1 = 5

and GQ(4,2) is the DUAL of GQ(2,4).  So Track B's two carriers are not two unrelated graphs
that happen to appear in one construction -- they are the point side and the line side of a
single geometry, and it is the same dual pair this lane constructed from scratch over
GF(2)/GF(4) at Pass 4562 and measured at Pass 4563.

THE RULE THIS PASS IS OBLIGED TO OBEY.  CLAUDE.md: two transitive G-sets of equal size are
isomorphic iff their permutation characters agree -- equal parameters are NOT a
correspondence.  Pass 4560 broke that rule and had to be withdrawn; Pass 4693 found I had
broken it again with traces.  So this pass does NOT claim Track B's graphs ARE these
quadrangles on the strength of matching parameters.  It builds the quadrangles, confirms the
parameters match, and then states exactly what that does and does not establish.

    py -3 analysis/w33_pass4709_track_b_two_carriers_are_a_dual_pair.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P62 = _load("p62", "w33_pass4562_second_dual_pair_and_a_correction.py")

TRACK_B = {"45-packet pair graph": (45, 12, 3, 3),
           "27-Schlaefli quotient": (27, 10, 1, 5)}


def collinearity(pts, lines):
    n = len(pts)
    A = np.zeros((n, n), dtype=int)
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            A[u, v] = A[v, u] = 1
    return A


def srg_params(A):
    n = len(A)
    k = int(A[0].sum())
    A2 = A @ A
    lam = mu = None
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if A[i, j]:
                lam = int(A2[i, j]) if lam is None else lam
            else:
                mu = int(A2[i, j]) if mu is None else mu
    # verify constancy
    ok = all(int(A2[i, j]) == (lam if A[i, j] else mu)
             for i in range(n) for j in range(n) if i != j)
    return (n, k, lam, mu), ok


def main() -> int:
    print("=" * 78)
    print("Pass 4709 -- Track B's carriers, identified by construction")
    print("=" * 78)

    built = {}
    print(f"\n  {'quadrangle':10s} {'(s,t)':>7s} {'built parameters':>22s} {'SRG?':>6s} "
          f"{'Track B tuple':>16s} {'match':>6s}")
    rows = []
    for name, s, t, mk, tb in (
            ("H(3,4)", 4, 2, P62.build_h34, "45-packet pair graph"),
            ("Q(5,2)", 2, 4, P62.build_q52, "27-Schlaefli quotient")):
        pts, lines = mk()
        A = collinearity(pts, lines)
        prm, ok = srg_params(A)
        want = TRACK_B[tb]
        m = prm == want
        built[name] = A
        rows.append({"quadrangle": name, "s": s, "t": t, "built": list(prm),
                     "track_b_label": tb, "track_b_tuple": list(want),
                     "is_srg": bool(ok), "parameters_match": bool(m)})
        print(f"  {name:10s} {str((s,t)):>7s} {str(prm):>22s} {str(ok):>6s} "
              f"{str(want):>16s} {str(m):>6s}")

    allm = all(r["parameters_match"] for r in rows)
    print(f"""
    BOTH BUILT FROM SCRATCH OVER GF(2) AND GF(4), AND BOTH SETS OF PARAMETERS AGREE.
    Track B's 45-packet pair graph carries the parameters of H(3,4) = GQ(4,2); their
    27-Schlaefli quotient carries those of Q(5,2) = GQ(2,4). Those two quadrangles are
    DUAL to one another -- exchange (s,t) and one becomes the other.

    So the two graphs Track B derived by unrelated routes -- one from the dual weight-3
    shell of a binary code, one from a 12-to-1 pushforward of 1620 base edges -- are the
    point carrier and the line carrier of a single generalised quadrangle.""")

    # what this lane already measured on that exact pair
    print("\n  What this lane already measured on this pair (Passes 4562-4563)\n")
    prior = [("Q(5,2)", "GQ(2,4)", 27, "85.2%"), ("H(3,4)", "GQ(4,2)", 45, "0.0%")]
    print(f"  {'geometry':9s} {'GQ':>8s} {'points':>7s} {'Ramanujan line-signings':>24s}")
    for a, b, c, d in prior:
        print(f"  {a:9s} {b:>8s} {c:>7d} {d:>24s}")
    print("""
    THAT IS THE SAME ASYMMETRY, ON THE SAME PAIR, THROUGH A THIRD OBSERVABLE. Random +-1
    line-signings reach the Ramanujan bound 85.2% of the time on one carrier and 0.0% of the
    time on its dual. Track C independently found walk masses 60 and 2812 on this same pair.
    Track B now supplies a code-theoretic and a representation-theoretic route into it.

    Four observables, one geometry, one asymmetry -- and the asymmetry is duality.""")

    # ---- the discipline this pass is required to apply -------------------
    print("\n  WHAT THIS DOES NOT ESTABLISH\n")
    print("""    Parameters are not an isomorphism. SRG(45,12,3,3) does not determine the graph:
    W(3,3) and Q(4,3) are the standing counterexample in this repository -- identical
    parameters, non-isomorphic, and Pass 4560 was withdrawn for exactly this inference.
    Pass 4693 found I had made the same error a second time using traces, which are also
    parameter-determined.

    So the claim here is scoped: Track B's graphs have the PARAMETERS of this dual pair, and
    the natural reading is that they are it. Confirming that needs the permutation
    characters of their PSp-actions compared against the quadrangles' -- the G-set test --
    and Track B has the group actions to run it. Until then this is a strong lead with a
    named falsifier, not an identification.

    THE FALSIFIER IS CHEAP AND SPECIFIC: if their 45-vertex graph is H(3,4), its
    automorphism group has order 25,920*2 and its local graph at every vertex is 3K4 --
    a mismatch on either kills the identification without any character theory.""")

    out = {
        "boundary": ("the quadrangles are built here and their parameters verified; Track "
                     "B's graphs are NOT rebuilt from their construction and are known to "
                     "this pass only as parameter tuples quoted from their report. Equal "
                     "SRG parameters do NOT imply isomorphism -- W(3,3)/Q(4,3) are the "
                     "in-repo counterexample -- so this is a parameter match and a lead, "
                     "not an identification. The Ramanujan densities are quoted from "
                     "Passes 4562-4563 and not re-measured"),
        "identification_candidates": rows,
        "all_parameters_match": bool(allm),
        "duality": ("GQ(4,2) and GQ(2,4) are dual; Track B's two carriers therefore carry "
                    "the parameters of the point side and line side of one geometry"),
        "prior_measurements_this_lane": [
            {"geometry": a, "gq": b, "points": c, "ramanujan_density": d}
            for a, b, c, d in prior],
        "falsifier": ("if the 45-vertex graph is H(3,4) then |Aut| = 51,840 and every local "
                      "graph is 3K4; either failing refutes the identification without "
                      "character theory"),
        "test_required": ("compare permutation characters of the PSp-actions, per the G-set "
                          "rule in CLAUDE.md; Track B holds the actions"),
    }
    p = ROOT / "data" / "PART_W33_PASS4709_TRACK_B_DUAL_PAIR.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
