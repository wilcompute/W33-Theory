#!/usr/bin/env python3
"""Witness for the Pass 1021 corollary: E8 selects the orientation with no ovoid.

This verifies a CROSS-TRACK claim before citing it, rather than trusting the prose.
Everything about contextuality here is PRIOR ART and none of it is claimed:

  * analysis/w33_ovoid_construct.py (in CI) -- "W(q) is contextual iff q is odd,
    because an ovoid -- a Kochen-Specker 0/1 assignment satisfying every context --
    exists iff q is even".  Constructs the ovoid for q = 2, 4 and exhibits the
    q = 3 obstruction (max partial ovoid 7 < 10).
  * Pass 216 (docs/index.html) -- "Q(4,3) Has the Dual Ovoid Carrier",
    Q(4,3) = (0 spreads, 36 ovoids).
  * Thas -- W(q) has ovoids iff q is even (cited at docs/index.html:8406).
  * docs/archive/FINAL_TOE_PROOF.md 1.8 -- the Witting 40-ray set is
    KS-uncolourable and critical.

What this script adds is only the independent recount of the duality pair, so the
Pass 1021 corollary cites a verified number:

    W(3,3) = (36 spreads, 0 ovoids)        Q(4,3) = (0 spreads, 36 ovoids)

Under the standard dictionary (points = the 40 Witting rays, lines = orthonormal
tetrads, collinear = orthogonal) a KS 0/1 colouring is exactly an ovoid, of the
forced size st + 1 = 10.  Pass 1021 showed the E8 fibration lands on the POINT
action, not the dual, so the orientation E8 selects is the one with no ovoid.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

F = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1021_corollary_ovoid_orientation.json"


def canon(v):
    """Canonical representative of a projective point of PG(3,3)."""
    for a in v:
        if a % F:
            inv = 1 if a % F == 1 else 2
            return tuple((inv * x) % F for x in v)
    return None


def build():
    """The 40 points and 40 totally isotropic lines of W(3,3)."""
    pts, seen = [], set()
    for v in itertools.product(range(F), repeat=4):
        if any(v):
            c = canon(v)
            if c not in seen:
                seen.add(c)
                pts.append(c)
    idx = {p: i for i, p in enumerate(pts)}

    def form(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % F

    lines = set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if form(pts[i], pts[j]) == 0:
                span = set()
                for a in range(F):
                    for b in range(F):
                        w = tuple(
                            (a * pts[i][k] + b * pts[j][k]) % F for k in range(4)
                        )
                        if any(w):
                            span.add(idx[canon(w)])
                if len(span) == 4:
                    lines.add(frozenset(span))
    return pts, [sorted(L) for L in lines]


def count_ovoids(lines, onpt, npts):
    """Ovoid = set of points meeting every line exactly once (exact cover)."""
    sols = []

    def rec(chosen, covered):
        if len(covered) == len(lines):
            sols.append(tuple(sorted(chosen)))
            return
        li = min(l for l in range(len(lines)) if l not in covered)
        for p in lines[li]:
            if any(p in lines[c] for c in covered):
                continue
            newc = covered | set(onpt[p])
            if len(newc) != len(covered) + len(onpt[p]):
                continue
            rec(chosen + [p], newc)

    rec([], set())
    return sols


def count_spreads(lines, onpt, npts):
    """Spread = set of pairwise disjoint lines covering every point."""
    sols = []

    def rec(chosen, used):
        if len(used) == npts:
            sols.append(tuple(sorted(chosen)))
            return
        p = min(x for x in range(npts) if x not in used)
        for li in onpt[p]:
            L = set(lines[li])
            if L & used:
                continue
            rec(chosen + [li], used | L)

    rec([], set())
    return sols


def main():
    pts, lines = build()
    npts = len(pts)
    onpt = [[li for li, L in enumerate(lines) if p in L] for p in range(npts)]

    assert npts == 40, npts
    assert len(lines) == 40, len(lines)
    assert {len(L) for L in lines} == {4}
    assert {len(x) for x in onpt} == {4}

    ovoids = count_ovoids(lines, onpt, npts)
    spreads = count_spreads(lines, onpt, npts)

    assert len(ovoids) == 0, len(ovoids)
    assert len(spreads) == 36, len(spreads)

    out = {
        "schema": "w33.pass1021.corollary.ovoid_orientation.v1",
        "status": "PASS",
        "headline": (
            "W(3,3) = (36 spreads, 0 ovoids) and Q(4,3) = (0 spreads, 36 ovoids), "
            "recounted independently. A KS 0/1 colouring is an ovoid of size "
            "st+1 = 10, so the point reading is KS-uncolourable and the dual "
            "reading is colourable. Pass 1021 showed E8 lands on the point "
            "action, so E8 selects the orientation with no ovoid."
        ),
        "W33": {"points": npts, "lines": len(lines), "spreads": len(spreads),
                "ovoids": len(ovoids)},
        "Q43_dual": {"spreads": len(ovoids), "ovoids": len(spreads)},
        "forced_ovoid_size": 10,
        "prior_art": [
            "analysis/w33_ovoid_construct.py -- ovoid = KS colouring, exists iff q even",
            "Pass 216 (docs/index.html) -- Q(4,3) = (0 spreads, 36 ovoids)",
            "Thas -- W(q) has ovoids iff q is even (docs/index.html:8406)",
            "docs/archive/FINAL_TOE_PROOF.md 1.8 -- Witting 40-ray KS-uncolourable, critical",
        ],
        "scope": (
            "Adds only the link to Pass 1021's point-versus-line determination. "
            "The contextuality result is prior art and is not strengthened here. "
            "The dual reading is combinatorial, not physical: the lines of W(3,3) "
            "are not rays in C^4."
        ),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": out["status"], "W33": out["W33"],
                      "Q43_dual": out["Q43_dual"]}, sort_keys=True))


if __name__ == "__main__":
    main()
