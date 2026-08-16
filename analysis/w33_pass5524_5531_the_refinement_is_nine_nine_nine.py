"""Passes 5524-5531 -- the two decompositions of the forty points refine to 9+9+9 and 7+3+3,
the 27 is not the cubic surface's, and the result index now reads the bundles.

  5524  The bundle REPORT.md files were invisible to RESULTS_INDEX.  Fixed, measured.
  5525  The affine/hyperplane split (13+27) against the quadric split (16+12+12).
  5526  Is the 27 the cubic surface's 27 lines?
  5527  DCCLXXXIV's level 4 and 5, which this thread never reached -- and its C332c, which
        already had the 576 I proved at Pass 5516.

    py -3 analysis/w33_pass5524_5531_the_refinement_is_nine_nine_nine.py
"""

from __future__ import annotations

import collections
import itertools
import re
import sys
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

Q = 3


def main() -> int:
    print("=" * 78)
    print("Passes 5524-5531 -- nine, nine, nine")
    print("=" * 78)

    def nrm(v):
        for a in v:
            if a % Q:
                z = pow(a, Q - 2, Q)
                return tuple((z * x) % Q for x in v)
        return None

    pts = sorted({nrm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})

    def B(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % Q

    def quad(v):
        return (v[0] * v[1] + v[2] * v[3]) % Q

    print("\n  PASS 5524 -- the index now reads the bundles\n")
    idx = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8", errors="replace")
    files = set(re.findall(r"`([^`]+\.(?:py|md|tex|g|lean))`", idx))
    usual = ("analysis/", "scripts/", "docs/", "tests/", "tools/", "exploration/",
             "manuscripts/", "formal/", "passes/")
    outside = [f for f in files if not f.startswith(usual)]
    bundles = [f for f in outside
               if "BUNDLE" in f.upper() or f.startswith("NOTES/")
               or "bundle" in f or "deliverable" in f]
    print(f"    files indexed              : {len(files):,}   (was 4,917)")
    print(f"    outside the usual subtrees : {len(outside)}")
    print(f"    from bundles and NOTES     : {len(bundles)}")
    print("""
    ADDED .md ONLY, DELIBERATELY. The bundles also hold thousands of .json certificates and
    250 .zip archives; JSON is machine output whose numbers would flood the token grammar,
    and Pass 328 measured what that costs. The prose reports are the half a human wrote.

    SP43_TO_WE6's REPORT.md carries an explicit Sp(4,3) -> W(E6) isomorphism and had been
    unindexed for months. That is the concrete cost of the gap.""")

    print("\n  PASS 5525 -- the two decompositions, crossed\n")
    cross = collections.Counter(
        (("inf" if p[0] == 0 else "aff"),
         ("S" if quad(p) == 0 else ("A" if quad(p) == 1 else "B")))
        for p in pts)
    print(f"    {'':6s} {'S (quadric)':>12s} {'A':>4s} {'B':>4s}   total")
    for h in ("aff", "inf"):
        r = [cross[(h, c)] for c in ("S", "A", "B")]
        print(f"    {h:6s} {r[0]:12d} {r[1]:4d} {r[2]:4d}   {sum(r)}")
    print(f"    {'total':6s} {sum(cross[(h,'S')] for h in ('aff','inf')):12d} "
          f"{sum(cross[(h,'A')] for h in ('aff','inf')):4d} "
          f"{sum(cross[(h,'B')] for h in ('aff','inf')):4d}   {sum(cross.values())}")
    print("""
    THE AFFINE PART SPLITS 9 + 9 + 9, PERFECTLY EVENLY, and the hyperplane splits 7 + 3 + 3.
    Two decompositions built from unrelated structures -- one a hyperplane at infinity, the
    other a quadratic form -- and their common refinement has six cells with the affine
    thirds exactly equal.

    9 + 9 + 9 = 27 and 7 + 3 + 3 = 13. The evenness on the affine side is the content: a
    quadratic form restricted to AG(3,3) hits its three value classes equally, while on the
    hyperplane at infinity the quadric takes 7 of 13.

    NOT CLAIMED: that this is more than the standard count of a conic's points in an affine
    space. It is recorded because the refinement was asked for and 9+9+9 is what it is.""")

    print("\n  PASS 5526 -- the 27, and the cubic surface\n")
    aff = [p for p in pts if p[0] != 0]
    g = igraph.Graph(n=len(aff))
    g.add_edges([(i, j) for i, j in itertools.combinations(range(len(aff)), 2)
                 if B(aff[i], aff[j]) == 0])
    n = g.vcount()
    A = [[0] * n for _ in range(n)]
    for a, b in g.get_edgelist():
        A[a][b] = A[b][a] = 1
    lam = {sum(A[i][x] * A[x][j] for x in range(n))
           for i in range(n) for j in range(n) if A[i][j]}
    mu = {sum(A[i][x] * A[x][j] for x in range(n))
          for i in range(n) for j in range(n) if i != j and not A[i][j]}
    deg = sorted(set(g.degree()))
    aut = g.count_automorphisms_vf2()
    schlafli = deg == [16] and lam == {10} and mu == {8}
    print(f"    induced graph on the 27 : {g.ecount()} edges, degrees {deg}")
    print(f"    lambda {sorted(lam)}   mu {sorted(mu)}")
    print(f"    Schlafli SRG(27,16,10,8)? {schlafli}")
    print(f"    |Aut| = {aut:,}   (Schlafli has 51,840 = |W(E6)|)")
    print("""
    NO. Eight-regular with 108 edges, lambda = 1 and mu taking two values, so not strongly
    regular and not the Schlafli graph. |Aut| = 1296 against 51,840.

    THE 27 IS AG(3,3)'s POINT COUNT, 3^3, and not the cubic surface's 27 lines. Those are a
    W(E6) object and this is an affine one; they share an integer and nothing tested here.
    Sixth coincidence dismissed on this thread by looking at the structure instead of the
    number.""")

    print("\n  PASS 5527 -- DCCLXXXIV's upper levels, and its C332c\n")
    print("""    Levels 4 and 5, which this thread never reached:

      Level 4  K12 horizon surface : genus 6, vertices 12, chi = -10
               3456 = |W(F4)|/2 * genus = 576 * 6 = 96 * 36
      Level 5  [72, 66, 3]_3 horizon code
               n = 72 = C(12,2) + 6,  k = 66 = C(12,2),  rate 11/12

    AND ITS C332c ALREADY HAD MY 576. The file states |W(F4)|/2 = f^2 = 576, where f = 24 is
    the face count of Q4 and the vertex count of the 24-cell. That is exactly the group
    Pass 5516 proved isomorphic to the Klein Latin autoparatopy group -- reached there as an
    arithmetic identity in a tower three months ago, and here as an actual stabiliser acting
    on thirteen points.

    SO THE HONEST SPLIT OF CREDIT IS: DCCLXXXIV owns 576 = |W(F4)|/2 = f^2 and the tower it
    sits in. This thread owns that the group ACTS -- on the 13-cover, faithfully modulo its
    centre, with orbits 1 + 12 -- and that it is isomorphic to AutPar(V4), which is a
    statement about groups rather than about integers.""")

    out = {
        "boundary": ("Pass 5524 adds .md globs only and does not index JSON or zip. Pass "
                     "5525 reports a refinement and claims nothing beyond the counts. Pass "
                     "5526 rejects the Schlafli identification under the SYMPLECTIC "
                     "adjacency on the affine points; another adjacency is not ruled out. "
                     "Pass 5527 quotes DCCLXXXIV and does not re-verify its levels 4 and 5"),
        "pass_5524": {"files_indexed": len(files), "was": 4917,
                      "outside_usual": len(outside), "from_bundles": len(bundles),
                      "scope": ".md only; JSON would flood the token grammar",
                      "concrete_cost": ("SP43_TO_WE6's REPORT.md carries an explicit "
                                        "Sp(4,3) -> W(E6) isomorphism and was unindexed")},
        "pass_5525": {"refinement": {f"{h}/{c}": cross[(h, c)]
                                     for h in ("aff", "inf") for c in ("S", "A", "B")},
                      "affine_split": [9, 9, 9], "hyperplane_split": [7, 3, 3],
                      "cells": len(cross),
                      "note": "not claimed to be more than the standard affine conic count"},
        "pass_5526": {"vertices": n, "edges": g.ecount(), "degrees": deg,
                      "lambda": sorted(lam), "mu": sorted(mu),
                      "is_schlafli": schlafli, "aut": aut, "schlafli_aut": 51840,
                      "verdict": ("the 27 is AG(3,3)'s point count 3^3, not the cubic "
                                  "surface's 27 lines")},
        "pass_5527": {"level4": "K12 horizon, genus 6, 12 vertices, 3456 = 576*6 = 96*36",
                      "level5": "[72,66,3]_3 horizon code, rate 11/12",
                      "C332c": "|W(F4)|/2 = f^2 = 576, f = 24",
                      "credit": ("DCCLXXXIV owns 576 = |W(F4)|/2 = f^2 and the tower; this "
                                 "thread owns that the group ACTS on the 13-cover with "
                                 "orbits 1+12 and is isomorphic to AutPar(V4)")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5524_5531_REFINEMENT_AND_CREDIT.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
