#!/usr/bin/env python3
"""Pass 4563 -- W(3,3) is NOT self-dual, and that gives the discriminating experiment.

Pass 4560 asserted "W(3,3) is self-dual and therefore shows neither effect", and used it to
explain why four thousand passes on W(3,3) never surfaced the carrier asymmetry.

THE CORPUS ALREADY SAYS THAT IS FALSE, in two places, neither of which I cited:

    CROSS_TRACK_LEDGER.md          "W(q) is self-dual only for EVEN q"
    BREAKTHROUGH_JULY_2026_...     "W(3,3) is NOT self-dual, so 'nonedge of the point
      PERPLEXITY_PASS3.md, Pass     graph' and 'nonedge of the line graph' are different
      1117                          sets, both of size 540, NOT CONJUGATE AS G-SETS"

And the way I got it wrong is the one CLAUDE.md documents at length.  W(3,3) has 40 points
and 40 lines, and I read equal counts as duality -- in a pass whose own method section said
the duality was "verified from the counts alone, with no theory needed".  Equal size is not
correspondence.  Pass 1117 had already found two sets of size 540 that are not isomorphic
as G-sets; that is the same trap, in the same geometry, already recorded.

W(3,q) is dual to Q(4,q), and they are isomorphic only for even q.  At q = 3 the dual of
W(3,3) is Q(4,3), a DIFFERENT generalised quadrangle with the same parameters.

SO THE ERROR PRODUCES THE EXPERIMENT THE WHOLE ARC NEEDED.

Both W(3,3) and Q(4,3) are SRG(40,12,2,4): same point count, same degree, same s = 3, and
therefore the SAME gauge block size of C(4,2) = 6 edges per line.  The two competing
explanations of the carrier asymmetry now make opposite predictions:

    COARSENESS (Pass 4442)   block size is the variable -> the two must AGREE
    DUALITY    (Pass 4560)   the carrier is the variable -> they must DIFFER

Every earlier comparison confounded these, because every dual pair tested so far also
changed the block size (6 vs 45, 3 vs 10).  This pair does not.

    py -3 analysis/w33_pass4563_w33_is_not_self_dual.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

RNG = np.random.default_rng(4563)
F = 3


def proj(dim, q=F):
    out = []
    for lead in range(dim):
        for tail in itertools.product(range(q), repeat=dim - lead - 1):
            out.append((0,) * lead + (1,) + tail)
    return out


def norm(v, q=F):
    for c in v:
        if c:
            inv = pow(c, q - 2, q)
            return tuple((inv * z) % q for z in v)
    raise ValueError


def build_w33():
    """Symplectic W(3,3): 40 points, 40 lines, GQ(3,3)."""
    pts = proj(4)
    idx = {p: i for i, p in enumerate(pts)}

    def B(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

    lines = set()
    for i, x in enumerate(pts):
        for y in pts[i + 1:]:
            if B(x, y):
                continue
            span = {norm(tuple((a * u + b * w) % F for u, w in zip(x, y)))
                    for a in range(F) for b in range(F) if a or b}
            lines.add(frozenset(idx[v] for v in span))
    return pts, sorted(lines, key=sorted)


def build_q43():
    """Parabolic quadric Q(4,3) in PG(4,3): the DUAL of W(3,3).  40 points, 40 lines."""
    def Q(x):
        return (x[0] * x[0] + x[1] * x[2] + x[3] * x[4]) % F

    def Bil(x, y):
        return (Q(tuple((a + b) % F for a, b in zip(x, y))) - Q(x) - Q(y)) % F

    pts = [p for p in proj(5) if Q(p) == 0]
    idx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for i, x in enumerate(pts):
        for y in pts[i + 1:]:
            if Bil(x, y):
                continue
            span = {norm(tuple((a * u + b * w) % F for u, w in zip(x, y)))
                    for a in range(F) for b in range(F) if a or b}
            if all(Q(v) == 0 for v in span) and len(span) == F + 1:
                lines.add(frozenset(idx[v] for v in span))
    return pts, sorted(lines, key=sorted)


def graph_and_blocks(pts, lines):
    n = len(pts)
    A = np.zeros((n, n))
    blocks = []
    for L in lines:
        es = list(itertools.combinations(sorted(L), 2))
        blocks.append(es)
        for u, v in es:
            A[u, v] = A[v, u] = 1
    return A, blocks


def srg_params(A):
    n = len(A)
    d = int(A.sum(1)[0])
    lam = mu = None
    for u in range(n):
        for v in range(u + 1, n):
            common = int(A[u] @ A[v])
            if A[u, v]:
                lam = common if lam is None else lam
                assert common == lam, "not strongly regular"
            else:
                mu = common if mu is None else mu
                assert common == mu, "not strongly regular"
    return n, d, lam, mu


def measure(A, blocks, samples=800):
    n = len(A)
    d = int(A.sum(1)[0])
    bound = 2 * np.sqrt(d - 1)
    rh = []
    for _ in range(samples):
        sel = RNG.integers(0, 2, len(blocks))
        S = np.zeros((n, n))
        for j, es in enumerate(blocks):
            s = -1.0 if sel[j] else 1.0
            for u, v in es:
                S[u, v] = S[v, u] = s
        rh.append(float(np.abs(np.linalg.eigvalsh(S)).max()))
    rh = np.array(rh)
    return {"bound": float(bound), "mean_rho": float(rh.mean()),
            "std_rho": float(rh.std()), "min_rho": float(rh.min()),
            "fraction_ramanujan": float((rh <= bound + 1e-9).mean()),
            "samples": samples}


def main() -> int:
    print("=" * 78)
    print("Pass 4563 -- W(3,3) is not self-dual; the discriminating test")
    print("=" * 78)

    wp, wl = build_w33()
    qp, ql = build_q43()
    print(f"\n  W(3,3): {len(wp)} points, {len(wl)} lines")
    print(f"  Q(4,3): {len(qp)} points, {len(ql)} lines   (the DUAL of W(3,3))")

    Aw, Bw = graph_and_blocks(wp, wl)
    Aq, Bq = graph_and_blocks(qp, ql)
    pw, pq = srg_params(Aw), srg_params(Aq)
    print(f"\n  W(3,3) point graph: SRG{pw}, {len(Bw[0])} edges per gauge block")
    print(f"  Q(4,3) point graph: SRG{pq}, {len(Bq[0])} edges per gauge block")
    same_params = pw == pq and len(Bw[0]) == len(Bq[0])
    print(f"  identical parameters and block size: {same_params}")

    # spectra -- identical for SRGs with identical parameters, so NOT a distinguisher
    ew = np.round(np.linalg.eigvalsh(Aw), 8)
    eq = np.round(np.linalg.eigvalsh(Aq), 8)
    same_spec = np.allclose(np.unique(ew), np.unique(eq))
    print(f"  identical spectra: {same_spec}  "
          f"({sorted(set(np.unique(ew).tolist()), reverse=True)})")

    rw = measure(Aw, Bw)
    rq = measure(Aq, Bq)
    print(f"\n  {'carrier':30s} {'bound':>8s} {'mean rho':>10s} {'std':>7s} {'%Ram':>7s}")
    print(f"  {'W(3,3) point graph':30s} {rw['bound']:8.4f} {rw['mean_rho']:10.4f} "
          f"{rw['std_rho']:7.4f} {rw['fraction_ramanujan']:6.1%}")
    print(f"  {'Q(4,3) point graph (dual)':30s} {rq['bound']:8.4f} {rq['mean_rho']:10.4f} "
          f"{rq['std_rho']:7.4f} {rq['fraction_ramanujan']:6.1%}")

    a, b = rw["fraction_ramanujan"], rq["fraction_ramanujan"]
    se = float(np.sqrt(max(a * (1 - a), 1e-9) / rw["samples"]
                       + max(b * (1 - b), 1e-9) / rq["samples"]))
    z = (a - b) / se if se else 0.0
    differ = abs(z) > 3
    print(f"\n  difference: {a:.1%} vs {b:.1%}   z = {z:+.2f}")

    print(f"""
  {'DUALITY WINS: the two carriers DIFFER at identical block size.' if differ else 'COARSENESS WINS: the two carriers AGREE once block size is held fixed.'}

  This is the first comparison in the arc that separates the two explanations. Every
  earlier dual pair changed the block size at the same time -- 6 against 45 for
  H(3,9)/Q(5,3), 3 against 10 for H(3,4)/Q(5,2) -- so coarseness and duality were
  confounded in all of them. W(3,3) and Q(4,3) are SRG(40,12,2,4) with 6 edges per block on
  both sides, identical spectra, and differ only in being dual rather than equal.

  {'So the carrier matters beyond the block size, and Pass 4442s coarseness law is not the' if differ else 'So the effect measured across the earlier pairs was the BLOCK SIZE all along, and'}
  {'whole story.' if differ else 'duality was along for the ride. Pass 4560s carrier framing is an over-read: the'}
  {'' if differ else 'variable is C(s+1,2), exactly as Pass 4442 originally said, and the dual pairs simply'}
  {'' if differ else 'happened to be the convenient way to vary it.'}

  AND THE CORRECTION THAT PRODUCED THIS TEST IS WORTH MORE THAN THE TEST. Pass 4560 read
  40 points and 40 lines as self-duality. Pass 1117 had ALREADY found two sets of size 540
  in this very geometry that are not conjugate as G-sets, and CLAUDE.md's standing rule is
  that equal size is never correspondence. The corpus held the refutation before I wrote
  the claim, in a file no sweep of mine reaches, and a subagent searching by RESULT found
  it in three minutes.""")

    out = {
        "boundary": ("both quadrangles constructed and their SRG parameters verified from "
                     "the incidence; the percentages are 800 random line-signings each, so "
                     "they carry sampling error of about 1.5 points. Isomorphism of the "
                     "two graphs is NOT tested here -- identical SRG parameters and spectra "
                     "do not decide it, and the classical non-isomorphism at odd q is "
                     "cited rather than reproved"),
        "correction": {
            "pass_4560_claim": "W(3,3) is self-dual",
            "status": "FALSE -- W(3,q) is self-dual only for even q; the dual of W(3,3) "
                      "is Q(4,3), a different quadrangle with the same parameters",
            "how_it_was_wrong": "equal counts (40 points, 40 lines) read as duality, the "
                                "exact 'equal size is not correspondence' error CLAUDE.md "
                                "documents",
            "already_in_corpus": ["CROSS_TRACK_LEDGER.md: W(q) self-dual only for even q",
                                  "BREAKTHROUGH_JULY_2026_PERPLEXITY_PASS3.md Pass 1117: "
                                  "the two 540-sets are not conjugate as G-sets"],
        },
        "discriminating_test": {
            "W(3,3)": {"srg": list(pw), "block": len(Bw[0]), **rw},
            "Q(4,3)": {"srg": list(pq), "block": len(Bq[0]), **rq},
            "identical_parameters": bool(same_params),
            "identical_spectra": bool(same_spec),
            "z": round(z, 3),
            "verdict": ("duality: carriers differ at fixed block size" if differ
                        else "coarseness: carriers agree once block size is fixed, so the "
                             "earlier dual-pair effects were block size, not duality"),
        },
    }
    p = ROOT / "data" / "PART_W33_PASS4563_NOT_SELF_DUAL.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
