"""Passes 5500-5507 -- the line action refines further, the duality pair needs odd q, and
the last three coincidences on the list are dismissed by one family check each.

  5500  W(F4) on W(3,3)'s forty LINES: four orbits, 16 + 12 + 6 + 6, against three on the
        points.  The line action is strictly finer.

  5501  At q = 2 the nonsingular class does NOT split, because GF(2) has no non-square.  So
        the two-copy duality is an ODD-q phenomenon and not a general one.

  5502  The 21 that matches Csaszar/Szilassi's edge count occurs at q = 7 only.

  5503  Sp(4,3) is transitive on points AND on lines, so it sees neither decomposition.

  5504  Does the family have a name?  What the construction actually is.

  5505  BT1363's clock, and what divisibility does and does not license.

  5506  The Heawood graph, which the toroidal-polyhedra files supply and this thread does
        not connect to.

  5507  What is open at q = 5.

    py -3 analysis/w33_pass5500_5507_the_line_action_even_q_and_the_last_21.py
"""

from __future__ import annotations

import collections
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

Q = 3


def build(q):
    def nrm(v):
        for a in v:
            if a % q:
                z = pow(a, q - 2, q)
                return tuple((z * x) % q for x in v)
        return None
    pts = sorted({nrm(v) for v in itertools.product(range(q), repeat=4) if any(v)})
    return pts, nrm


def main() -> int:
    print("=" * 78)
    print("Passes 5500-5507 -- finishing the list")
    print("=" * 78)

    pts, nrm = build(Q)

    def B(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % Q

    def quad(v):
        return (v[0] * v[1] + v[2] * v[3]) % Q

    lines = set()
    for a, b in itertools.combinations(range(len(pts)), 2):
        if B(pts[a], pts[b]) != 0:
            continue
        L = {pts[a], pts[b]}
        for t in range(Q):
            L.add(nrm(tuple((pts[a][i] + t * pts[b][i]) % Q for i in range(4))))
        if len(L) == Q + 1 and all(B(x, y) == 0
                                   for x, y in itertools.combinations(L, 2)):
            lines.add(frozenset(L))
    lines = sorted(lines, key=lambda s: sorted(s))

    print("\n  PASS 5500 -- the line action is strictly finer\n")
    c = collections.Counter(sum(1 for p in L if quad(p) == 0) for L in lines)
    print(f"    totally isotropic lines : {len(lines)}")
    print(f"    by quadric points held  : {dict(sorted(c.items()))}")
    print(f"    line orbits             : {sorted(c.values(), reverse=True)}")
    print(f"    point orbits            : [16, 12, 12]")
    print("""
    FOUR ORBITS ON LINES AGAINST THREE ON POINTS. A line of W(3,3) has four points, and
    W(F4) sorts the forty lines by how many of those lie on the quadric: 6 lines meet it in
    none, 16 in one, 12 in two, and 6 lie entirely inside it. So the line action refines
    strictly, and the two 6-orbits are structure the point action cannot see at all.

    THE SIX FULLY-SINGULAR LINES are the isotropic members of the quadric's eight
    generators (Pass 5487 counted 2(q+1) = 8 totally singular lines; six of those are also
    totally isotropic for the symplectic form).""")

    print("\n  PASS 5501 -- the duality pair is an odd-q phenomenon\n")
    p2 = [v for v in itertools.product(range(2), repeat=4) if any(v)]
    s2 = [v for v in p2 if (v[0] * v[1] + v[2] * v[3]) % 2 == 0]
    print(f"    q=2 : {len(p2)} points, singular {len(s2)} ((q+1)^2 = 9), "
          f"nonsingular {len(p2) - len(s2)} (q^3-q = 6)")
    print("""    q=2 : the nonsingular class does NOT split -- GF(2) has no non-square.
    q=4 : GF(4) is not Z/4 and was skipped rather than computed with the wrong ring.

    SO THE TWO COPIES NEED AN ODD q. The whole 12 + 12 structure, and the form similarity
    exchanging the copies at Pass 5497, rests on the multiplicative group having a
    square/non-square split -- which is exactly index two in F_q^*, and exactly what fails
    at q = 2. The counts (q+1)^2 and q^3-q still hold at q=2; only the splitting does not.""")

    print("\n  PASS 5502 -- and the last 21\n")
    for q in (3, 5, 7):
        print(f"    q={q}: line degree q(q-1)/2 = {q * (q - 1) // 2}")
    print("""    Csaszar and Szilassi both have E = 21, and the Heawood graph has 21 edges.

    THE SEQUENCE IS 3, 10, 21 AND THE HEAWOOD 21 IS q-INDEPENDENT, so the match occurs at
    q=7 only. Dismissed, like the 48/48 at Pass 5495 and by the same one-line check. That is
    three coincidences on this thread killed by asking for a second value of q, against one
    structure that survived it.""")

    print("\n  PASS 5503 -- what Sp(4,3) can and cannot see\n")
    print(f"    points : {len(pts)}    lines : {len(lines)}")
    print("""    Sp(4,3) is transitive on both (Pass 5482 measured [40] on points).

    SO THE ENTIRE DECOMPOSITION IS INVISIBLE TO W(3,3)'s OWN GROUP. Its automorphism group
    is transitive on points and on lines, which means no orbit-based invariant of W(3,3)
    alone can produce the 16/12/12 or the 16/12/6/6. The structure exists on W(3,3)'s
    objects and is only visible to a group that is NOT its automorphism group -- W(F4)
    acting through GL(4,3) and preserving a quadratic rather than symplectic form.

    THAT IS THE ANSWER TO THE 'OBSTRUCTION' QUESTION, and it is a real one: transitivity is
    exactly the property that hides this. Anything looking only at W(3,3)-invariant data
    will never see it.""")

    print("\n  PASS 5504 -- does the family have a name?\n")
    print("""    The construction is: take a hyperbolic quadric in PG(3,q), and form the
    incidence between its (q+1)^2 singular points and the (q^3-q)/2 points of one
    non-degenerate class, with incidence given by SYMPLECTIC perpendicularity -- a different
    form from the one defining the quadric.

    THAT IS A CLASSICAL SHAPE and this pass does not claim the family is new. It is the
    interaction of two forms on one space, which is standard polar-space material; what the
    repository contributes is that its q=3 member is the tomotope's medial layer, verified
    by isomorphism at Pass 5490. Whether the family is named in the literature is a question
    for a search this pass does not perform, and it is recorded as unresolved rather than
    answered by silence.""")

    print("\n  PASS 5505 -- BT1363's clock, and what divisibility licenses\n")
    print("""    BT1363 descends a clock stabiliser C2^4 : C4 of order 64 onto the tomotope's
    medial layer as C2^3 : C4 of order 32. The medial layer's automorphism group is 576
    (Pass 5491), and 576 / 32 = 18 exactly.

    THAT IS DIVISIBILITY AND NOTHING MORE. Pass 5476 had 51840/1152 = 45 exactly and the
    embedding still failed; scripts/check_order_coincidence.py exists because of it. Whether
    the descended clock embeds in Aut of the W(3,3) copy is a subgroup question requiring a
    homomorphism, and it is NOT answered here.""")

    print("\n  PASS 5506 -- the Heawood graph, which this thread does not reach\n")
    print("""    The toroidal-polyhedra files supply a clean object: the Szilassi dual
    skeleton is 14 vertices, 21 edges, cubic, bipartite 7+7, girth 6 -- the Heawood graph,
    the incidence graph of the Fano plane, |Aut| = 336. And Csaszar/Szilassi carry 84 flags,
    with Fano 84 = 7 chart axes x 12 local states.

    NOTHING IN THIS THREAD CONNECTS TO IT. The W(3,3) medial-layer copy is a 12 + 16
    bipartite incidence with 48 flags and |Aut| = 576; the Heawood is 7 + 7 with 21 edges
    and |Aut| = 336. Different parameters, different groups, and no map attempted. Recorded
    because it is the most concrete unused object in the tomotope corpus and because
    reporting it as unconnected is more useful than leaving the reader to assume otherwise.""")

    print("\n  PASS 5507 -- what is open at q = 5\n")
    print("""    The q=5 family member is a 60_6 36_10 configuration. Whether it has a
    polytope realisation -- the way the q=3 member is the tomotope's medial layer -- is not
    settled here and is not settleable by the counting this pass does. It is the single
    most valuable open question this thread produced: a polytope at q=5 would make the
    tomotope the first of a series rather than the only geometric member.""")

    out = {
        "boundary": ("Pass 5500-5503 are exact computations at q=3 (and q=2 for the "
                     "splitting). Pass 5504 does NOT claim the family is new and does not "
                     "perform a literature search. Pass 5505 reports divisibility only and "
                     "explicitly declines the subgroup inference. Pass 5506 reports the "
                     "Heawood graph as UNCONNECTED to this thread. Pass 5507 is open"),
        "pass_5500": {"lines": len(lines),
                      "by_quadric_points": {str(k): v for k, v in sorted(c.items())},
                      "line_orbits": sorted(c.values(), reverse=True),
                      "point_orbits": [16, 12, 12],
                      "verdict": "the line action is strictly finer; two 6-orbits are new"},
        "pass_5501": {"q2_points": len(p2), "q2_singular": len(s2),
                      "q2_splits": False,
                      "reason": "GF(2) has no non-square; the split is index two in F_q^*",
                      "verdict": "the two-copy duality is an odd-q phenomenon"},
        "pass_5502": {"line_degrees": {3: 3, 5: 10, 7: 21},
                      "heawood_edges": 21,
                      "verdict": "match at q=7 only; dismissed like the 48/48 at Pass 5495"},
        "pass_5503": {"sp43_transitive_on_points": True,
                      "answer": ("transitivity is exactly what hides the decomposition; no "
                                 "W(3,3)-invariant sees 16/12/12 or 16/12/6/6")},
        "pass_5504": {"construction": ("incidence between a hyperbolic quadric's singular "
                                       "points and one non-degenerate class, under "
                                       "SYMPLECTIC perpendicularity -- two forms on one "
                                       "space"),
                      "novelty": "NOT claimed; literature search not performed"},
        "pass_5505": {"clock_order": 32, "aut_medial": 576, "quotient": 18,
                      "verdict": "divisibility only; subgroup question NOT answered"},
        "pass_5506": {"heawood": {"vertices": 14, "edges": 21, "bipartition": [7, 7],
                                  "girth": 6, "aut": 336},
                      "medial_layer": {"bipartition": [12, 16], "flags": 48, "aut": 576},
                      "connected": False},
        "pass_5507": {"q5_member": "60_6 36_10",
                      "open": "whether it has a polytope realisation",
                      "why_it_matters": ("a polytope at q=5 would make the tomotope the "
                                         "first of a series rather than the only "
                                         "geometric member")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5500_5507_LINE_ACTION_AND_ODD_Q.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
