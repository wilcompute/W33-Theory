#!/usr/bin/env python3
"""Pass 4795 -- the same characteristic-2 dichotomy, seen a third time, as a gap between
W(3,3)'s independence number and its own Hoffman bound.

Three questions about W(3,q) have now been asked and each split the family differently:

    duality exists?      q even                    (Pass 4774, seven values)
    polarity exists?     q an odd power of 2       (Pass 4793, exhaustive at q = 2,4)
    OVOID exists?        q even                    [classical]

An ovoid is q^2+1 pairwise non-collinear points -- an INDEPENDENT SET in the collinearity
graph -- and the Hoffman ratio bound for a strongly regular graph gives

    alpha <= n(-s)/(k-s)

which for W(3,q) evaluates to exactly q^2+1 at every q.  So the ovoid question is: does
W(3,q) MEET its own Hoffman bound?  For even q it does.  For odd q the classical answer is
no, and that means the bound is not tight -- there is a gap, and the gap is computable.

That reframes the whole arc.  W(3,3) is not merely "not self-dual"; it fails to meet a
spectral bound that its parameters permit, and the same characteristic-2 obstruction is
responsible for all three failures.

Also settled here: Pass 4793 found 36 polarities at q = 2 and 720 dualities, and
720/20 = 36 exactly with |Sz(2)| = 20.  Coincidence or coset?

    py -3 analysis/w33_pass4795_the_ovoid_gap_and_the_polarity_coset.py
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


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def hoffman(n, k, lam, mu):
    """Ratio bound alpha <= n(-s)/(k-s) with s the least eigenvalue."""
    d = (lam - mu) ** 2 + 4 * (k - mu)
    r = int(round(d ** 0.5))
    s = ((lam - mu) - r) // 2
    return (n * (-s)) // (k - s)


def main() -> int:
    print("=" * 78)
    print("Pass 4795 -- does W(3,q) meet its own Hoffman bound?")
    print("=" * 78)

    print(f"\n  {'q':>3s} {'n':>5s} {'SRG':>20s} {'Hoffman':>8s} {'q^2+1':>6s} "
          f"{'alpha':>6s} {'ovoid':>6s} {'even?':>6s} {'gap':>4s} {'sec':>6s}")
    rows = []
    for p, k in ((2, 1), (3, 1), (2, 2)):
        q = p ** k
        pts, lines = PP.build_w3(PP.GF(p, k))
        g = graph_of(pts, lines)
        prm = PP.srg_params(g)
        hb = hoffman(*prm)
        t0 = time.time()
        alpha = g.independence_number()
        dt = time.time() - t0
        ovoid = alpha == q * q + 1
        rows.append({"q": q, "n": g.vcount(), "srg": list(prm), "hoffman": hb,
                     "q2_plus_1": q * q + 1, "alpha": alpha,
                     "ovoid_exists": bool(ovoid), "even": q % 2 == 0,
                     "agrees": bool(ovoid == (q % 2 == 0)),
                     "gap": hb - alpha, "seconds": round(dt, 1)})
        print(f"  {q:3d} {g.vcount():5d} {str(prm):>20s} {hb:8d} {q*q+1:6d} "
              f"{alpha:6d} {str(ovoid):>6s} {str(q%2==0):>6s} {hb-alpha:4d} {dt:6.1f}")

    agree = all(r["agrees"] for r in rows)
    q3 = next((r for r in rows if r["q"] == 3), None)
    print(f"""
    {'THE THIRD SPLIT MATCHES THE FIRST TWO.' if agree else 'THE SPLIT DOES NOT MATCH -- READ THE ROWS.'}

    The Hoffman bound is q^2+1 at every q, so the parameters ALLOW an ovoid everywhere. Even
    q attains it. W(3,3) does not: alpha = {q3['alpha'] if q3 else '?'} against a bound of {q3['hoffman'] if q3 else '?'}, a gap of {q3['gap'] if q3 else '?'}.

    AND THE GAP IS NOT ARBITRARY. alpha = 7 at q = 3, and q^2 - q + 1 = 9 - 3 + 1 = 7. That
    is the known maximum partial-ovoid size for W(3,q) at odd q, so the computation lands on
    a formula rather than on a number. The deficit from the Hoffman bound is then

        (q^2 + 1) - (q^2 - q + 1) = q

    exactly -- 3 at q = 3. ONE DATA POINT, so this is a match to a cited formula and not a
    verification of it; the falsifiable form is that alpha(W(3,5)) should be 25 - 5 + 1 = 21
    against a Hoffman bound of 26, a gap of 5. That is computable and is not computed here.

    THIS IS A SHARPER STATEMENT THAN "NOT SELF-DUAL". Self-duality is a property of the
    incidence structure as a whole; the Hoffman gap is a failure to achieve something the
    SPECTRUM permits. The eigenvalues of W(3,3) are 12, 2, -4 whatever the field, and they
    license an independent set of 10. The geometry refuses to supply one.

    THREE QUESTIONS, THREE SPLITS, ONE MECHANISM:

        duality exists      q even                 Pass 4774, seven values
        polarity exists     q odd power of 2       Pass 4793, exhaustive at q = 2,4
        ovoid exists        q even                 here, alpha computed

    The first and third coincide; the second is strictly finer and picks out the Suzuki
    line. All three fail at odd q, and the reason recorded in this repository in July --
    Sp(4,3) lacking full D4 triality -- is the same obstruction seen from D4.""")

    # ---- the polarity coset ------------------------------------------------
    print("\n  Pass 4793's 36 polarities: coincidence or coset?\n")
    sz2 = 2 ** 2 * (2 ** 2 + 1) * (2 - 1)
    dualities, polarities = 720, 36
    print(f"    dualities at q=2         : {dualities}")
    print(f"    polarities at q=2        : {polarities}")
    print(f"    |Sz(2)| = q^2(q^2+1)(q-1): {sz2}")
    print(f"    dualities / |Sz(2)|      : {dualities // sz2}"
          f"   {'== polarity count' if dualities // sz2 == polarities else '!= polarity count'}")
    exact = dualities == polarities * sz2
    print(f"""
    {dualities} = {polarities} x {sz2} EXACTLY. Each polarity determines its absolute-point set -- an
    ovoid of 5 points -- and the stabiliser of that ovoid is Sz(2) of order 20. So the 720
    dualities partition into {polarities} classes of size {sz2}, one per ovoid.

    STATED AS AN OBSERVATION, NOT A THEOREM. The arithmetic is exact and the reading is the
    natural one, but this pass does not compute the stabiliser of a single ovoid, so the
    partition is inferred from the count rather than exhibited. Counting is how this project
    has produced false correspondences before -- three of them, per CLAUDE.md -- and the
    honest form of this claim names the missing computation: stabilise one ovoid and check
    the orbit has {polarities} members.""")

    out = {
        "boundary": ("independence numbers are exact (igraph exhaustive). q = 5 and above "
                     "are not computed -- alpha on a 156-vertex SRG is expensive and the "
                     "classical result is cited for the general pattern. The polarity coset "
                     "claim is ARITHMETIC ONLY: 720 = 36 x 20 is exact, but no stabiliser "
                     "is computed here, so the partition into Sz(2)-cosets is inferred from "
                     "the count and not exhibited"),
        "rows": rows,
        "third_split_matches": bool(agree),
        "three_questions": {
            "duality_exists": "q even",
            "polarity_exists": "q an odd power of 2",
            "ovoid_exists": "q even"},
        "hoffman_gap_at_q3": q3["gap"] if q3 else None,
        "gap_formula": {
            "alpha_odd_q": "q^2 - q + 1 (cited; matched at q = 3 only)",
            "hoffman": "q^2 + 1",
            "deficit": "q",
            "prediction_q5": {"alpha": 21, "hoffman": 26, "gap": 5,
                              "computed": False}},
        "polarity_coset": {"dualities": dualities, "polarities": polarities,
                           "sz2_order": sz2, "product_exact": bool(exact),
                           "missing_computation": "stabilise one ovoid, check orbit size 36"},
    }
    fp = ROOT / "data" / "PART_W33_PASS4795_OVOID_GAP_AND_COSET.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
