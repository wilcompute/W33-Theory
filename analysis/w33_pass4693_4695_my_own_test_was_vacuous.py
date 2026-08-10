#!/usr/bin/env python3
"""Passes 4693-4695 -- the exchange test I ran at 4685 could not have failed, and s = t is
not the condition I said it was.

  4693  RETRACTION OF THE TEST, NOT THE CONSTRAINT.  Pass 4685 reported "the constraint
        survives the attempt to break it" because tr(A^k) agreed for W(3,3)/Q(4,3) and
        disagreed for the two genuine dual pairs.  But tr(A^k) is a function of the strongly
        regular parameters ALONE -- the spectrum is determined by (v,k,lambda,mu), so the
        traces are too.  W(3,3) and Q(4,3) have identical parameters, so agreement was
        forced before any matrix was built, and the dual pairs have different parameters, so
        disagreement was forced too.  The test had no power to detect duality.  That is
        failure mode 7 -- a vacuous check -- committed two passes after I shipped a checker
        for vacuous checks.

  4694  AND THE CONDITION IS SELF-DUALITY, NOT s = t.  Pass 4682 wrote "the search should be
        restricted to s = t."  Wrong: GQ(3,3) has s = t and W(3,3) is NOT self-dual (W(3,q)
        is self-dual iff q is even).  Track C's data already shows this -- their cancellation
        FAILS at GQ(3,3), 712 != 180, exactly where my stated condition predicted it could
        hold.  The correct class is strictly smaller.

  4695  A PREDICTION THAT CAN FAIL.  If self-duality is the condition, the cancellation holds
        at W(3,4) and fails at W(3,5).  Stated before either is computed.

    py -3 analysis/w33_pass4693_4695_my_own_test_was_vacuous.py
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


P63 = _load("p63", "w33_pass4563_w33_is_not_self_dual.py")
P62 = _load("p62", "w33_pass4562_second_dual_pair_and_a_correction.py")


def srg_spectrum(v, k, lam, mu):
    """Eigenvalues and multiplicities of an SRG from its parameters alone."""
    d = (lam - mu) ** 2 + 4 * (k - mu)
    s = int(round(d ** 0.5))
    assert s * s == d, "non-integral discriminant"
    r = ((lam - mu) + s) // 2
    t = ((lam - mu) - s) // 2
    f = int(round(0.5 * ((v - 1) - (2 * k + (v - 1) * (lam - mu)) / s)))
    g = v - 1 - f
    return [(k, 1), (r, f), (t, g)]


def trace_from_params(v, k, lam, mu, power):
    return sum(m * e ** power for e, m in srg_spectrum(v, k, lam, mu))


def collinearity(pts, lines):
    n = len(pts)
    A = np.zeros((n, n), dtype=object)
    for L in lines:
        for u, w in itertools.combinations(sorted(L), 2):
            A[u, w] = A[w, u] = 1
    return A


def local_graph_profile(A):
    """Degree sequence of the subgraph induced on a vertex's neighbourhood.

    NOT determined by the SRG parameters in general -- this is the kind of invariant that
    can separate parameter-equal graphs, which traces cannot.
    """
    n = len(A)
    Af = np.array(A, dtype=int)
    profiles = set()
    for v in range(n):
        nb = [u for u in range(n) if Af[v, u]]
        sub = Af[np.ix_(nb, nb)]
        profiles.add(tuple(sorted(int(x) for x in sub.sum(axis=1))))
    return profiles


def main() -> int:
    print("=" * 78)
    print("Passes 4693-4695 -- retracting a test of my own")
    print("=" * 78)

    # ---- 4693: the traces were forced --------------------------------------
    print("\n  PASS 4693 -- was Pass 4685's agreement forced by the parameters?\n")
    fam = [
        ("W(3,3)", (40, 12, 2, 4), lambda: P63.build_w33()),
        ("Q(4,3)", (40, 12, 2, 4), lambda: P63.build_q43()),
        ("Q(5,2)", (27, 10, 1, 5), lambda: P62.build_q52()),
        ("H(3,4)", (45, 12, 3, 3), lambda: P62.build_h34()),
    ]
    print(f"  {'geometry':10s} {'(v,k,lam,mu)':>18s} {'tr(A^3) built':>14s} "
          f"{'from params':>13s} {'tr(A^4) built':>15s} {'from params':>13s}")
    rows = []
    forced = True
    for name, prm, mk in fam:
        pts, lines = mk()
        A = collinearity(pts, lines)
        Af = np.array(A, dtype=float)
        t3 = int(round(np.trace(np.linalg.matrix_power(Af, 3))))
        t4 = int(round(np.trace(np.linalg.matrix_power(Af, 4))))
        p3 = int(round(trace_from_params(*prm, 3)))
        p4 = int(round(trace_from_params(*prm, 4)))
        ok = (t3 == p3) and (t4 == p4)
        forced &= ok
        rows.append({"geometry": name, "params": list(prm), "tr3_built": t3,
                     "tr3_from_params": p3, "tr4_built": t4, "tr4_from_params": p4,
                     "match": bool(ok)})
        print(f"  {name:10s} {str(prm):>18s} {t3:14d} {p3:13d} {t4:15d} {p4:13d}"
              f"  {'OK' if ok else 'MISMATCH'}")

    print(f"""
    EVERY TRACE IS REPRODUCED FROM THE PARAMETERS WITHOUT TOUCHING A MATRIX. So Pass 4685
    measured parameter equality and reported it as evidence about duality. W(3,3) and Q(4,3)
    are parameter-equal, so they HAD to agree; the dual pairs are not, so they HAD to
    disagree. No arrangement of the data could have broken the constraint, which means the
    attempt to break it was not an attempt.

    This is the exact error Track B named -- equal parameters are not an equivalent action --
    and the exact error I made at Pass 4560 reading 40 points and 40 lines as self-duality.
    Second time, subtler dress. The constraint itself is untouched: it is still a necessary
    condition and still correct. What is withdrawn is the claim that it was TESTED.""")

    # ---- 4694: s = t is not self-duality -----------------------------------
    print("\n  PASS 4694 -- what the condition actually is\n")
    print(f"  {'quadrangle':12s} {'s':>3s} {'t':>3s} {'s=t?':>6s} {'self-dual?':>11s} "
          f"{'Track C cancellation':>21s}")
    tab = [("GQ(2,2)=W(3,2)", 2, 2, True, "yes (q even)", "HOLDS  288 = 288"),
           ("GQ(2,4)=Q(5,2)", 2, 4, False, "no", "fails  60 != 36"),
           ("GQ(4,2)=H(3,4)", 4, 2, False, "no", "fails  2812 != 792"),
           ("GQ(3,3)=W(3,3)", 3, 3, True, "NO (q odd)", "fails  712 != 180")]
    for nm, s, t, eq, sd, tc in tab:
        print(f"  {nm:12s} {s:3d} {t:3d} {str(eq):>6s} {sd:>11s} {tc:>21s}")

    print("""
    THE FOURTH ROW REFUTES MY STATED CONDITION. GQ(3,3) has s = t, so Pass 4682's rule
    ("can only hold identically when s = t") permitted the cancellation there -- and Track C
    already measured it failing. I did not notice, because I read their GQ(2,2) result as
    confirming my rule and never checked their GQ(3,3) result against it. The confirming
    case was in the same four-row table as the refuting one.

    s = t IS NECESSARY FOR SELF-DUALITY BUT NOT SUFFICIENT. W(3,q) and its dual Q(4,q) share
    all four parameters at every q, yet are isomorphic only for q even. So the class my
    constraint should have named is the SELF-DUAL quadrangles -- strictly smaller than s = t,
    and the difference is not cosmetic: it is the difference between an infinite family and
    the even-q half of it.""")

    # ---- an invariant that is NOT forced by the parameters ------------------
    print("\n  What could a real test use? Not traces.\n")
    prof = {}
    for name in ("W(3,3)", "Q(4,3)"):
        pts, lines = dict((n, m) for n, _, m in fam)[name]()
        prof[name] = local_graph_profile(collinearity(pts, lines))
        print(f"    {name:8s} local-graph degree profiles: {len(prof[name])} distinct")
    same = prof["W(3,3)"] == prof["Q(4,3)"]
    print(f"    identical between the two: {same}")
    print("""
    Local structure does not separate these two either, which is expected -- both are
    parameter-equal SRGs and locally regular. The separating invariant is the PERMUTATION
    CHARACTER, per this repository's own G-set rule, and comparing characters is the test
    Pass 4685 should have run instead of comparing traces.""")

    # ---- 4695: a prediction stated before computing ------------------------
    print("\n  PASS 4695 -- the prediction, recorded before anyone computes it\n")
    pred = [("W(3,4)", 4, "even", "SELF-DUAL", "cancellation HOLDS"),
            ("W(3,5)", 5, "odd", "not self-dual", "cancellation FAILS"),
            ("W(3,8)", 8, "even", "SELF-DUAL", "cancellation HOLDS"),
            ("W(3,9)", 9, "odd", "not self-dual", "cancellation FAILS")]
    print(f"  {'quadrangle':11s} {'q':>3s} {'parity':>7s} {'duality':>14s} {'prediction':>20s}")
    for nm, q, par, du, pr in pred:
        print(f"  {nm:11s} {q:3d} {par:>7s} {du:>14s} {pr:>20s}")
    print("""
    Every one of these has s = t, so the OLD rule permits the cancellation in all four and
    predicts nothing. The corrected rule splits them by parity of q and forbids it in two.
    That is what makes it a prediction rather than a restatement: W(3,5) is the cheapest
    place it can die, and if Track C computes their six masses there and the cancellation
    holds, the self-duality reading is wrong.""")

    out = {
        "boundary": ("4693's trace-from-parameters identity is exact and settles that Pass "
                     "4685's comparison was determined in advance; the constraint from Pass "
                     "4682 is NOT withdrawn, only the claim that it was tested. 4694's table "
                     "quotes Track C's four cancellation results as stated and does NOT "
                     "re-derive their six walk masses -- the refutation of my s=t rule rests "
                     "on their GQ(3,3) number being correct. 4695 is a prediction, not a "
                     "result: neither W(3,4) nor W(3,5) is computed here"),
        "pass_4693_traces_are_forced": {"rows": rows, "all_reproduced": bool(forced),
                                        "verdict": "Pass 4685's test had no power"},
        "pass_4694_condition": {
            "old_condition": "s = t",
            "corrected_condition": "self-dual, i.e. W(3,q) with q even",
            "refuting_case": "GQ(3,3) has s=t, is not self-dual, and Track C's "
                             "cancellation fails there (712 != 180)",
            "table": [{"quadrangle": a, "s": b, "t": c, "s_eq_t": d, "self_dual": e,
                       "track_c": f} for a, b, c, d, e, f in tab]},
        "pass_4695_prediction": [
            {"quadrangle": a, "q": b, "parity": c, "duality": d, "prediction": e}
            for a, b, c, d, e in pred],
        "local_profiles_separate": not same,
    }
    p = ROOT / "data" / "PART_W33_PASS4693_4695_VACUOUS_TEST_RETRACTED.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
