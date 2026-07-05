#!/usr/bin/env python3
"""
Every node of the fabric carries a qutrit phase space: the tax ground states form the affine plane
AG(2,q), with the defect lines as its parallel classes. Pass 60 identified the perp states and left
the ground states as anatomized-but-unnamed. This witness names them, with an exhaustive closure at
two odd orders:

  THE ILP-FREE CHARACTERIZATION (q=3). Among the 27 non-neighbors of a center p there are exactly 81
  triads (pairwise non-collinear triples) with 4 centers, each point on 9, each pair on at most 1.
  Their center-quads split {all 4 in Gamma(p): 9 triads; exactly 1 in Gamma(p): 72}. The nine ground
  states are EXACTLY the nine all-centers-in-Gamma(p) triads (each extended by its forced 8 in-perp
  points): the ILP and the geometric characterization agree set-for-set. The defect's ground states
  need no optimizer -- they are the triads whose centers all live in the perp.

  THE AFFINE PLANE LAW (verified at q=3 AND q=5, both exhaustive). Per defect center of W(q), q odd:
    - the optima number exactly 2(q^2+1) = twice the Hoffman bound (20 at q=3; 52 at q=5, closed
      exhaustively here at 52 < cap, upgrading Pass 59's capped sample to a theorem at q=5);
    - the ground states number exactly q^2, and they carry the structure of the affine plane AG(2,q):
      grounds = the q^2 points; the q(q+1) neighbors in Gamma(p) = the q(q+1) lines; incidence =
      "this neighbor is unlit in this ground"; each ground's unlit set = the q+1 lines through its
      point, a TRANSVERSAL of the defect star; and the q+1 parallel classes of the plane are EXACTLY
      the q+1 defect lines (same-defect-line neighbors are never co-unlit; different, exactly once);
    - the two remaining optima are the perp states (deleted perp, load q; full perp, load q+1);
    - ground lit-sets are pairwise equidistant (intersection 5 at q=3; 19 at q=5).
  At q=3 this affine plane is the HESSE CONFIGURATION (9_4, 12_3) -- the single-qutrit Wigner phase
  space of the corpus witness w33_hesse_mermin, whose 4 striations/MUBs are here the 4 defect
  contexts. The machine's defect bookkeeping at each node is literally a qutrit phase space.

  THE LOCAL SYMMETRY. The point stabilizer (order 648 in PSp(4,3)) acts on the nine grounds with the
  orbital structure computed here (transitivity was Pass 60; the pair-orbit count sharpens it).

Honest scope: exact finite computations throughout; the q=5 enumeration terminated below its cap, so
both odd-order closures are exhaustive, not sampled. The AG(2,q) identification is verified by its
defining incidence properties (pairwise unique co-unlit, transversality, parallel classes); the
phase-space reading at q=3 is the corpus's committed Hesse identification, cited not re-derived.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402
import w33_tax_orbits as orb  # noqa: E402


def four_centric_triads(q=3):
    """All pairwise non-collinear triples among the non-neighbors of point 0 with |common perp| = 4."""
    pts, A, lines, B = audit._build(q)
    n = len(pts)
    nb = frozenset(j for j in range(n) if A[0][j])
    nonn = sorted(set(range(1, n)) - nb)
    triads = []
    for t in combinations(nonn, 3):
        a, b, c = t
        if A[a][b] or A[a][c] or A[b][c]:
            continue
        perp = tuple(j for j in range(n) if A[j][a] and A[j][b] and A[j][c])
        if len(perp) == 4:
            triads.append((t, perp))
    return triads, nb, nonn


def affine_plane_checks(q, sols, lines, nb, star):
    """Verify the AG(2,q) incidence structure of the ground states; return (facts, ok)."""
    grounds = [
        frozenset(i for i, v in enumerate(s) if v)
        for s in sols
        if s[0] == 0
        and tuple(sorted(sum(s[p] for p in lines[li]) for li in star))
        == tuple([q - 1] * (q + 1))
    ]
    unlits = [tuple(sorted(set(nb) - g)) for g in grounds]
    sl = {}
    for li in star:
        for u in lines[li]:
            if u != 0:
                sl[u] = li
    pair_ints = {
        len(set(a) & set(b)) for i, a in enumerate(unlits) for b in unlits[i + 1 :]
    }
    per = {x for x in Counter(x for u in unlits for x in u).values()}
    transversal = all(
        sorted(Counter(sl[u] for u in ul).values()) == [1] * (q + 1) for ul in unlits
    )
    co_same = {
        sum(1 for ul in unlits if u in ul and v in ul)
        for u, v in combinations(sorted(nb), 2)
        if sl[u] == sl[v]
    }
    co_diff = {
        sum(1 for ul in unlits if u in ul and v in ul)
        for u, v in combinations(sorted(nb), 2)
        if sl[u] != sl[v]
    }
    lit_int = {len(a & b) for i, a in enumerate(grounds) for b in grounds[i + 1 :]}
    facts = {
        "q": q,
        "n_grounds": len(grounds),
        "unlit_size": sorted({len(u) for u in unlits}),
        "pairwise_co_unlit": sorted(pair_ints),
        "line_size_on_grounds": sorted(per),
        "unlit_transversal_of_defect_lines": bool(transversal),
        "same_class_co_unlit": sorted(co_same),
        "diff_class_co_unlit": sorted(co_diff),
        "ground_lit_pairwise_intersection": sorted(lit_int),
    }
    ok = (
        len(grounds) == q * q
        and facts["unlit_size"] == [q + 1]
        and facts["pairwise_co_unlit"] == [1]
        and facts["line_size_on_grounds"] == [q]
        and transversal
        and facts["same_class_co_unlit"] == [0]
        and facts["diff_class_co_unlit"] == [1]
    )
    return facts, ok, grounds


def main():
    print(
        "== the ground states are an affine plane: AG(2,q) at every node, Hesse at q=3 ==\n"
    )
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    # A. the ILP-free characterization at q=3
    triads, nb3, nonn = four_centric_triads(3)
    chk(
        f"the 27 non-neighbors carry exactly 81 four-centric triads (got {len(triads)})",
        len(triads) == 81,
    )
    deg = Counter(x for (t, _) in triads for x in t)
    pairs = Counter(frozenset(pr) for (t, _) in triads for pr in combinations(t, 2))
    chk(
        "each of the 27 lies on exactly 9 triads; each pair on at most one",
        set(deg.values()) == {9} and max(pairs.values()) == 1,
    )
    in_nb = Counter(sum(1 for c in perp if c in nb3) for (t, perp) in triads)
    chk(
        f"center-quads split {{all-4-in-perp: 9, exactly-1-in-perp: 72}} (got {dict(in_nb)})",
        in_nb == Counter({4: 9, 1: 72}),
    )
    all4 = {t for (t, perp) in triads if all(c in nb3 for c in perp)}

    pts, A, lines, B = audit._build(3)
    n = len(pts)
    star3 = [li for li, L in enumerate(lines) if 0 in L]
    sols3, _ = anat._enumerate_optima_for_center(lines, n, 0)
    facts3, ok3, grounds3 = affine_plane_checks(3, sols3, lines, nb3, star3)
    gtriples = {tuple(sorted(g - nb3)) for g in grounds3}
    chk(
        "ILP-FREE CHARACTERIZATION: the ground states are EXACTLY the all-centers-in-perp triads",
        gtriples == all4,
    )

    # B. the affine plane law at q=3 (= the Hesse configuration)
    chk(
        "q=3: grounds form AG(2,3) -- 9 points, 12 neighbor-lines of size 3, unlit = the 4 lines "
        "through a point (transversal), parallel classes = the 4 defect lines",
        ok3,
    )
    chk(
        f"q=3: ground lit-sets pairwise equidistant (intersection {facts3['ground_lit_pairwise_intersection']})",
        facts3["ground_lit_pairwise_intersection"] == [5],
    )

    # C. the affine plane law at q=5, exhaustively
    pts5, A5, lines5, B5 = audit._build(5)
    n5 = len(pts5)
    nb5 = frozenset(j for j in range(n5) if A5[0][j])
    star5 = [li for li, L in enumerate(lines5) if 0 in L]
    sols5, _ = anat._enumerate_optima_for_center(lines5, n5, 0, cap=400)
    chk(
        f"q=5: the closure is EXHAUSTIVE -- exactly 52 = 2(q^2+1) optima (got {len(sols5)}; "
        "upgrades Pass 59's capped sample)",
        len(sols5) == 52,
    )
    occ_classes = Counter(
        (s[0], tuple(sorted(sum(s[p] for p in lines5[li]) for li in star5)))
        for s in sols5
    )
    chk(
        "q=5: classes are 25+1 (unlit: grounds + deleted perp) and 25+1 (their flips), all uniform",
        occ_classes
        == Counter(
            {
                (0, tuple([4] * 6)): 25,
                (1, tuple([5] * 6)): 25,
                (0, tuple([5] * 6)): 1,
                (1, tuple([6] * 6)): 1,
            }
        ),
    )
    special5 = [
        frozenset(i for i, v in enumerate(s) if v)
        for s in sols5
        if s[0] == 0
        and tuple(sorted(sum(s[p] for p in lines5[li]) for li in star5))
        == tuple([5] * 6)
    ]
    chk(
        "q=5: the load-5 singleton IS the deleted perp Gamma(p) (perp state, as proven)",
        len(special5) == 1 and special5[0] == nb5,
    )
    facts5, ok5, grounds5 = affine_plane_checks(5, sols5, lines5, nb5, star5)
    chk(
        "q=5: grounds form AG(2,5) -- 25 points, 30 neighbor-lines of size 5, unlit = the 6 lines "
        "through a point, parallel classes = the 6 defect lines",
        ok5,
    )
    chk(
        f"q=5: ground lit-sets pairwise equidistant (intersection {facts5['ground_lit_pairwise_intersection']})",
        facts5["ground_lit_pairwise_intersection"] == [19],
    )

    # D. local symmetry: pair-orbits of the point stabilizer on the 9 grounds
    gens, G = orb.build_group(pts, B)
    stab = [g for g in G if g[0] == 0]
    glist = sorted(grounds3, key=sorted)
    gidx = {g: i for i, g in enumerate(glist)}
    pair_orbits = set()
    seen = set()
    for i in range(9):
        for j in range(9):
            if i == j or (i, j) in seen:
                continue
            o = set()
            frontier = [(glist[i], glist[j])]
            while frontier:
                nxt = []
                for a, b in frontier:
                    for g in stab:
                        im = (frozenset(g[x] for x in a), frozenset(g[x] for x in b))
                        if im not in o:
                            o.add(im)
                            nxt.append(im)
                frontier = nxt
            seen |= {(gidx[a], gidx[b]) for a, b in o}
            pair_orbits.add(len(o))
            break
        break
    two_transitive = pair_orbits == {72}
    chk(
        f"the point stabilizer is 2-TRANSITIVE on the 9 grounds (single pair-orbit of 72: {sorted(pair_orbits)})",
        two_transitive,
    )

    all_ok = all(ok for _, ok in checks)
    print(
        "\nTHE LAW: per defect center of W(q) (q odd), the optima number exactly 2(q^2+1) = twice the"
        "\nHoffman bound: q^2 ground states forming the affine plane AG(2,q) (neighbors = lines, defect"
        "\nlines = parallel classes) plus the two perp states, all uniformly loaded -- exhaustive at q=3"
        "\nand q=5. At q=3 the plane is the Hesse configuration: the single-qutrit Wigner phase space,"
        "\nwith the 4 defect contexts as its 4 striations. Every node's defect bookkeeping is a qutrit"
        "\nphase space."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "triad_space_q3": {
            "four_centric_triads": len(triads),
            "per_point": 9,
            "center_quad_split": {str(k): v for k, v in in_nb.items()},
            "ilp_free_characterization": "grounds = the all-centers-in-perp triads",
        },
        "affine_plane_q3": facts3,
        "affine_plane_q5": facts5,
        "q5_closure": {
            "n_optima": len(sols5),
            "exhaustive": True,
            "classes": {str(k): v for k, v in occ_classes.items()},
        },
        "stabilizer_two_transitive_on_grounds": bool(two_transitive),
        "all_pass": bool(all_ok),
        "summary": (
            "the ground states are an affine plane. ILP-FREE CHARACTERIZATION (q=3): the 27 non-neighbors "
            "carry exactly 81 four-centric triads (9 per point, pairs on at most one); their center-quads "
            "split {all-4-in-perp: 9, exactly-1: 72}, and the nine ground states are EXACTLY the nine "
            "all-centers-in-perp triads -- the defect's ground states need no optimizer. AFFINE PLANE LAW "
            "(exhaustive at q=3 AND q=5): per defect center the optima number 2(q^2+1) = twice the Hoffman "
            "bound (20 and 52, the q=5 closure terminating below cap and upgrading Pass 59's sample); the "
            "q^2 grounds carry AG(2,q) -- grounds = points, the q(q+1) neighbors = lines (incidence = "
            "unlit), each ground's unlit set = the q+1 lines through its point = a transversal of the "
            "defect star, and the q+1 parallel classes ARE the q+1 defect lines; the two remaining optima "
            "are the perp states; ground lit-sets are pairwise equidistant (5 at q=3, 19 at q=5). At q=3 "
            "the plane is the HESSE CONFIGURATION -- the corpus's single-qutrit Wigner phase space "
            "(w33_hesse_mermin), its 4 striations/MUBs realized as the 4 defect contexts: every node's "
            "defect bookkeeping is a qutrit phase space. LOCAL SYMMETRY: the point stabilizer (648) is "
            "2-transitive on the 9 grounds. HONEST: exact and exhaustive at both odd orders; the "
            "phase-space reading cites the committed Hesse identification."
        ),
        "sources": [
            "w33_perp_states (Pass 60); w33_tax_orbits (Pass 59); w33_spread_star_anatomy (Pass 58)",
            "w33_hesse_mermin_contextuality (Hesse = AG(2,3) = single-qutrit phase space, committed corpus witness)",
            "exhaustive ILP closures at q=3 (20) and q=5 (52); exact triad enumeration",
        ],
    }
    with open("data/w33_ground_affine_plane.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_ground_affine_plane.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
