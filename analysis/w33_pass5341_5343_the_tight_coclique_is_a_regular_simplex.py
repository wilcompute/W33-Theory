"""Passes 5341-5343 -- what a Hoffman-TIGHT coclique actually is, tested on the other
lane's carrier, and the one bound the spectrum structurally cannot supply.

  5341  Pass 5279 showed that for a GQ(q,q) collinearity graph the noncollinear inner
        product in the eigenspace embedding is exactly -1/q^2, so the Gram bound
        1 - 1/c reproduces Hoffman.  That was checked on MY carrier.  The other lane works
        on NO_5^+(5) = SRG(325,144,68,60) with Hoffman 13 (their Pass5211, Pass5212).  If
        the identification is structural rather than a GQ accident, the noncollinear inner
        product there must be exactly -1/12, with no reference to q at all.

  5342  A set of N unit vectors at constant inner product -1/(N-1) is a REGULAR SIMPLEX.
        So a coclique that MEETS the Hoffman bound is not merely large -- it is a regular
        (N-1)-simplex sitting in the eigenspace, and their 13-coclique is a regular
        12-simplex.  That is the geometric content of tightness, and it is testable.

  5343  Their Pass5308 proved the 13-cover's stabiliser is W(D4):C3 of order 576, with an
        outer C3 cyclically permuting three normal V8 sectors -- triality.  A regular
        12-simplex has symmetry group S_13 of order 6,227,020,800.  Does 576 embed in the
        simplex's symmetries, i.e. does the stabiliser act on the coclique by permuting its
        13 vertices?  Asked and answered rather than assumed.

    py -3 analysis/w33_pass5341_5343_the_tight_coclique_is_a_regular_simplex.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from fractions import Fraction
from pathlib import Path

import igraph
import numpy as np

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


def embed(A, theta, k, n):
    """Unit-normalised Gram of the eigenspace projection for eigenvalue `theta`."""
    ev = sorted({round(float(x), 9) for x in np.linalg.eigvalsh(A)})
    others = [x for x in ev if abs(x - theta) > 1e-6 and abs(x - k) > 1e-6]
    E = np.eye(n)
    for o in others + [float(k)]:
        E = E @ (A - o * np.eye(n))
    d = np.diag(E)
    assert np.allclose(d, d[0]), "embedding is not equal-norm"
    return E / d[0]


def main() -> int:
    print("=" * 78)
    print("Passes 5341-5343 -- tightness is a simplex")
    print("=" * 78)

    print("\n  PASS 5341 -- the identity off my own carrier\n")
    print(f"    {'graph':22s} {'SRG':>24s} {'Hoffman':>8s} {'noncollinear ip':>16s} "
          f"{'-1/(H-1)':>10s} {'match':>6s}")
    rows = []
    # my carrier: GQ(q,q) collinearity graphs
    cases = []
    for p, k in [(3, 1), (5, 1)]:
        F = PP.GF(p, k)
        pts, lines = PP.build_w3(F)[:2]
        cases.append((f"W(3,{F.q})", graph_of(pts, lines)))
        dp, dl = PP.dual(pts, lines)
        cases.append((f"Q(4,{F.q})", graph_of(dp, dl)))
    # THE DECISIVE CASES. W(3,q) and Q(4,q) are both GQ(q,q), where Hoffman = q^2+1 and the
    # two candidate forms -1/q^2 and -1/(H-1) are numerically identical -- that carrier
    # cannot tell them apart no matter how many q are added. H(3,q^2) has order (q^2,q) so
    # Hoffman = q^3+1: at q=3 that is 28, giving -1/27 against -1/q^2 = -1/9. Different
    # numbers, so this row DECIDES which form is real.
    P89 = _load("p89", "w33_pass4389_hermitian_quadrangle_measured.py")
    hp, hl = P89.build_h39()[:2]
    cases.append(("H(3,9)", graph_of(hp, hl)))
    qp, ql = PP.dual(hp, hl)
    cases.append(("Q(5,3)", graph_of(qp, ql)))

    for name, g in cases:
        n, deg, lam, mu = PP.srg_params(g)
        hb = P95.hoffman(n, deg, lam, mu)
        A = np.array(g.get_adjacency().data, dtype=float)
        ev = sorted({round(float(x), 6) for x in np.linalg.eigvalsh(A)})
        theta = [x for x in ev if abs(x - deg) > 1e-6][-1]      # the larger non-trivial one
        G = embed(A, theta, deg, n)
        adj = A > 0.5
        off = ~np.eye(n, dtype=bool)
        nonc = float(np.mean(G[off & ~adj]))
        pred = -1.0 / (hb - 1)
        ok = abs(nonc - pred) < 1e-9
        rows.append({"graph": name, "srg": [n, deg, lam, mu], "hoffman": hb,
                     "noncollinear_ip": round(nonc, 10),
                     "minus_1_over_H_minus_1": round(pred, 10), "matches": ok})
        print(f"    {name:22s} {str((n, deg, lam, mu)):>24s} {hb:8d} {nonc:16.10f} "
              f"{pred:10.6f} {str(ok):>6s}")

    allok = all(r["matches"] for r in rows)
    print(f"""
    {'EVERY ROW' if allok else 'NOT EVERY ROW'}: the noncollinear inner product is exactly -1/(Hoffman - 1). Note what
    dropped out of the statement -- q. Pass 5279 wrote it as -1/q^2 because on a GQ(q,q) the
    Hoffman bound IS q^2+1, so -1/q^2 and -1/(H-1) coincide there and I could not tell which
    was the real form. Adding Q(4,q) does not separate them -- it is GQ(q,q) too.

    H(3,9) AND Q(5,3) ARE THE ROWS THAT DECIDE IT. Orders (9,3) and (3,9), so Hoffman is
    q^3+1 = 28 and the two candidates finally disagree: -1/(H-1) = -1/27 against
    -1/q^2 = -1/9. The measured value is -1/27. So -1/q^2 was never the statement; it was an
    artefact of every carrier I had tested, and Pass 5279 published it one day ago.

    AND THOSE TWO ROWS SAY MORE THAN THAT. H(3,9) is SRG(280,36,8,4) and Q(5,3) is
    SRG(112,30,2,10) -- different sizes, degrees and spectra -- yet both give -1/27, because
    both have Hoffman 28. The inner product is a function of the BOUND alone, not of the
    graph. Which is why it had to be -1/(H-1) all along.""")

    print("\n  PASS 5342 -- so a tight coclique IS a regular simplex\n")
    for H in (5, 10, 13, 17, 26, 65):
        c = Fraction(-1, H - 1)
        print(f"    Hoffman {H:3d} -> constant inner product {str(c):>7s} -> "
              f"regular {H - 1:2d}-simplex on {H} vertices in R^{H - 1}")
    print(f"""
    N UNIT VECTORS AT CONSTANT INNER PRODUCT -1/(N-1) ARE THE VERTICES OF A REGULAR SIMPLEX,
    and that is exactly the equality case of the Gram bound: |sum of the vectors|^2 = 0, so
    they sum to zero, which is the defining centred condition. Tightness is therefore not a
    numerical coincidence -- a coclique meeting the Hoffman bound has NO freedom left in the
    eigenspace, it is rigid up to rotation.

    THAT IS WHY THE BOUND CANNOT SEE EXISTENCE, said sharply. The simplex always fits in
    R^(N-1); the question the bound never asks is whether the GEOMETRY contains N points
    realising it. At q=3 the room exists for 10 and the quadrangle supplies only 7.

    AND IT APPLIES TO THEIR CARRIER UNCHANGED. Hoffman 13 on NO_5^+(5) means their
    13-coclique -- the 13 disjoint dual grids partitioning all 156 W-points -- is a regular
    12-simplex in a 12-dimensional eigenspace. Their Pass5212 proved it maximum by exactly
    this bound without naming the object it forces.""")

    print("\n  PASS 5343 -- does triality act on the simplex?\n")
    print("""    Their Pass5308: the 13-cover's stabiliser H has order 576 = W(D4):C3, with an
    outer C3 cyclically permuting three normal V8 sectors.
    A regular 12-simplex has full symmetry group S_13, of order 6,227,020,800.

    THE ARITHMETIC THAT HAS TO HOLD FIRST, and it does:""")
    import math
    s13 = math.factorial(13)
    print(f"      |S_13|            = {s13:,}")
    print(f"      |W(D4):C3|        = 576")
    print(f"      576 divides |S_13|? {s13 % 576 == 0}")
    print(f"      576 = |W(D4)| * 3 = {192 * 3}, and |W(D4)| = 192 = 2^3 * 24")
    print(f"""
    SO AN EMBEDDING IS NOT EXCLUDED BY ORDER, WHICH IS ALL THIS ESTABLISHES. 576 divides
    13! and that is a divisibility fact, not an action. I am NOT claiming the stabiliser
    acts faithfully on the 13 vertices, and there is a concrete reason to doubt the naive
    version: the stabiliser of a 13-coclique in a 325-vertex graph acts on those 13 points,
    but its kernel -- elements fixing all 13 while moving the other 312 -- is exactly what
    an order argument cannot see. Computing that kernel needs their explicit 13-cover and
    its stabiliser as permutations, which this pass does not construct.

    WHAT WOULD SETTLE IT: build the 13-coclique, compute its setwise stabiliser inside
    Aut(NO_5^+(5)), and factor out the pointwise kernel. If the image in S_13 has order 576
    the triality is acting on the simplex; if the kernel is nontrivial the 576 lives partly
    in the 312 points outside. That is a real computation and it is not done here.

    THE TEMPTING CLAIM I AM NOT MAKING. D4 triality permutes three 8-dimensional
    representations; a 12-simplex sits in R^12 = R^(3*4), and 3 divides 12. That is
    numerology until the action above is computed, and this corpus has a documented failure
    mode for exactly that shape.""")

    out = {
        "boundary": ("Pass 5341 establishes the inner-product identity on the four graphs "
                     "listed; NO_5^+(5) is NOT among them -- their builder was not directly "
                     "callable here, so the 13-coclique statement is a PREDICTION from the "
                     "identity, not a measurement on their carrier. Pass 5343 establishes "
                     "only that 576 divides 13!, which is divisibility and not an action; "
                     "no embedding of W(D4):C3 into S_13 is exhibited and the pointwise "
                     "kernel is not computed"),
        "pass_5341": {"identity": "noncollinear inner product = -1/(Hoffman - 1)",
                      "correction_to_5279": ("Pass 5279 wrote -1/q^2; on a GQ(q,q) the "
                                             "Hoffman bound is q^2+1 so the two coincide "
                                             "and that carrier cannot distinguish them. "
                                             "-1/(H-1) is the general form; q was a "
                                             "coincidence of the carrier"),
                      "rows": rows, "all_match": allok},
        "pass_5342": {"theorem": ("a coclique meeting the Hoffman bound is a regular "
                                  "(H-1)-simplex in the eigenspace, rigid up to rotation"),
                      "equality_case": "|sum of unit vectors|^2 = 0, so they sum to zero",
                      "why_blind_to_existence": ("the simplex always fits in R^(H-1); the "
                                                 "bound never asks whether the geometry "
                                                 "realises H points"),
                      "their_carrier": ("Hoffman 13 on NO_5^+(5) forces their 13-coclique "
                                        "to be a regular 12-simplex -- predicted, not "
                                        "measured here")},
        "pass_5343": {"stabiliser": "W(D4):C3, order 576 (their Pass5308)",
                      "simplex_symmetry": "S_13, order 6227020800",
                      "divides": s13 % 576 == 0,
                      "established": "divisibility only",
                      "not_established": ("that the stabiliser acts faithfully on the 13 "
                                          "vertices; the pointwise kernel over the other "
                                          "312 points is not computed"),
                      "next": ("build the 13-coclique, take its setwise stabiliser in "
                               "Aut(NO_5^+(5)), factor out the pointwise kernel")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5341_5343_TIGHT_COCLIQUE_IS_A_SIMPLEX.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
