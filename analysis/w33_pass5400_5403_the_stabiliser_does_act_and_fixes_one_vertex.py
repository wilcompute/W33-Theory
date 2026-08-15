"""Passes 5400-5403 -- the action exists, it fixes a vertex, and the Lean layer has
nothing to say about any of it.

  5400  Pass 5343 established that 576 divides 13! and refused to call that an action.
        Pass 5377 tried again with igraph, got generator counts, and refused again.  GAP
        settles it: the setwise stabiliser of the 13-cover in Aut(P-block graph) has order
        1152, its image in S_13 has order EXACTLY 576, and the pointwise kernel has order 2.
        So the group does act faithfully on the simplex vertices, modulo a central
        involution -- which is the centre their Pass5308 already reported.

  5401  And the action is NOT transitive.  Orbit sizes are [1, 12]: one dual grid among the
        thirteen is fixed by everything, and the other twelve form a single orbit.  The
        simplex has a distinguished vertex.

  5402  GAP's structure description of the image is ((A4 x A4) : C2) : C2, order 576,
        solvable, derived subgroup 144, trivial centre.  Their Pass5308 describes their
        order-576 group as W(D4):C3.  Both are order 576; the descriptions differ, and that
        is reported rather than resolved.

  5403  The Lean library was checked for anything bearing on this.  It has nothing, and the
        reason is structural and stated in its own headers.

    py -3 analysis/w33_pass5400_5403_the_stabiliser_does_act_and_fixes_one_vertex.py
"""

from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main() -> int:
    print("=" * 78)
    print("Passes 5400-5403 -- it acts, and it fixes one")
    print("=" * 78)

    stab = json.loads((ROOT / "data" / "_gap_cover_stab.json").read_text(encoding="utf-8"))
    orb = json.loads((ROOT / "data" / "_gap_cover_orbits.json").read_text(encoding="utf-8"))

    print("\n  PASS 5400 -- the question three passes declined to answer\n")
    for k in ("aut_order", "setwise_stabiliser_order", "image_in_S13_order",
              "pointwise_kernel_order"):
        print(f"    {k:28s} : {stab[k]:,}")
    print(f"""
    THE IMAGE IN S_13 IS EXACTLY 576. Pass 5343 could only say that 576 divides 13!, which
    is divisibility and not an action, and said so. Pass 5377 tried igraph and got
    generator counts, which are not group orders, and said so. GAP gives the group.

    THE ORDER-2 KERNEL IS THEIR CENTRAL INVOLUTION. The setwise stabiliser has order
    {stab['setwise_stabiliser_order']:,} = 2 x 576, and the element acting trivially on all thirteen is the centre
    their Pass5308 reported as "central_involution_fixed_by_triality". Two lanes, two
    computations, the same order-2 centre -- theirs from the group side, this one from the
    kernel of an action they did not compute.""")

    print("\n  PASS 5401 -- the simplex has a distinguished vertex\n")
    print(f"    orbit sizes on the 13 : {orb['orbit_sizes']}")
    print(f"    number of orbits      : {orb['n_orbits']}")
    print(f"    transitive            : {orb['orbit_sizes'] == [13]}")
    print(f"""
    ONE VERTEX IS FIXED BY EVERYTHING and the other twelve form a single orbit. A regular
    12-simplex is the most symmetric object of its size -- its own symmetry group is S_13,
    acting 13-transitively -- and the subgroup arriving from the geometry does not use that
    freedom at all. It singles out one of the thirteen dual grids.

    WHY THAT IS THE INTERESTING PART. Passes 5342 and 5376 showed the coclique is a regular
    simplex, which is a statement that it has NO distinguishing structure: every vertex
    looks like every other, rigid up to rotation. The geometry then supplies a stabiliser
    that breaks exactly that symmetry down to 1 + 12. The simplex is homogeneous; its
    embedding in the quadrangle is not, and the 1+12 split is invisible to every spectral
    or Gram argument used this week.

    WHAT IS NOT ESTABLISHED: which grid is fixed, or why. The orbit computation names a
    partition, not a reason, and identifying the fixed block geometrically is open.""")

    print("\n  PASS 5402 -- two descriptions of one order\n")
    print(f"    image structure (GAP)   : {orb['structure']}")
    print(f"    order                   : {orb['image_order']}")
    print(f"    derived subgroup        : {orb['derived_order']}")
    print(f"    centre                  : {orb['centre_order']}")
    print(f"    solvable                : {orb['is_solvable']}")
    print(f"    their Pass5308 says     : W(D4):C3, order 576, |W(D4)| = 192")
    print(f"""
    BOTH ARE ORDER 576 AND THE DESCRIPTIONS DIFFER. Mine has a normal subgroup of order 144
    (A4 x A4); W(D4):C3 has a normal subgroup of order 192. GAP's StructureDescription is
    canonical up to isomorphism, so two different strings usually means two different
    groups -- but these are stabilisers computed in DIFFERENT ambient settings, theirs from
    the cover's own symmetry and mine as an image in S_13, and a faithful image can present
    differently from the group it came from.

    REPORTED, NOT RESOLVED, and deliberately so. My Pass 5252 prior says that when a
    cross-lane number disagrees the base rate favours re-deriving mine first -- 2 of 2
    disagreements have been my error. Here the ORDERS agree exactly and only the structural
    description differs, which is the weakest kind of disagreement and the most likely to be
    a difference of setting rather than of fact. Deciding it needs their group as
    permutations, which their certificate does not carry.""")

    print("\n  PASS 5403 -- the Lean library, checked and empty on this\n")
    mods = sorted(glob.glob(str(ROOT / "formal" / "W33" / "*.lean")))
    hits = []
    for m in mods:
        txt = Path(m).read_text(encoding="utf-8", errors="replace")
        if re.search(r"ovoid|hoffman|coclique|simplex|independence number", txt, re.I):
            hits.append(Path(m).name)
    print(f"    repo Lean modules (formal/W33) : {len(mods)}")
    print(f"    mentioning ovoid/Hoffman/coclique/simplex : {len(hits)}")
    print(f"""
    NOTHING, AND THE HEADERS EXPLAIN WHY. Each module states its own scope in the negative:
    OddQRank says "No incidence matrix, finite field, Fourier decomposition, or matrix rank
    is defined here, so the geometric rank theorem remains an external input". RankLaw says
    "It does not define W(3,q), an incidence matrix, or an F2 rank". ShadowDichotomy says
    "It does not define W(3,q), a permutation module, a filtration, or a quadratic form".

    SO THE FORMAL LAYER IS AN ARITHMETIC CONSISTENCY CHECKER, not a proof of the theorems it
    accompanies. It verifies closed forms, recurrences and parities; the geometry is cited
    to Python and GAP in every case. That is an honest design and the headers are unusually
    clear about it -- but it means "formalized in Lean" in this corpus never means the
    geometric statement is proved, and anyone reading the module list without the headers
    would conclude otherwise.

    FOR THIS WEEK'S WORK SPECIFICALLY: no prior art, no conflict, and nothing to reuse.""")

    out = {
        "boundary": ("Pass 5400-5401 are GAP computations over the P-block graph built from "
                     "the other lane's Pass5212 geometry(5); the SELECTED 13-cover is "
                     "theirs. Pass 5402 REPORTS a structural-description difference and "
                     "does not resolve it -- the orders agree and the ambient settings "
                     "differ. Pass 5403 is a scope check of formal/W33 only, by keyword"),
        "pass_5400": {"aut_order": stab["aut_order"],
                      "setwise_stabiliser_order": stab["setwise_stabiliser_order"],
                      "image_in_S13_order": stab["image_in_S13_order"],
                      "pointwise_kernel_order": stab["pointwise_kernel_order"],
                      "settles": ("the group DOES act faithfully on the 13 simplex "
                                  "vertices modulo an order-2 kernel"),
                      "supersedes": ("Pass 5343's divisibility-only statement and Pass "
                                     "5377's generator counts"),
                      "cross_lane": ("the order-2 kernel matches the centre their Pass5308 "
                                     "reports, computed from the other side")},
        "pass_5401": {"orbit_sizes": orb["orbit_sizes"], "n_orbits": orb["n_orbits"],
                      "transitive": orb["orbit_sizes"] == [13],
                      "reading": ("the simplex is homogeneous but its embedding is not; "
                                  "the geometry breaks S_13 down to a fixed vertex plus a "
                                  "12-orbit, and that split is invisible to every spectral "
                                  "or Gram argument used this week"),
                      "open": "which grid is fixed, and why"},
        "pass_5402": {"image_structure": orb["structure"],
                      "image_order": orb["image_order"],
                      "derived": orb["derived_order"], "centre": orb["centre_order"],
                      "solvable": orb["is_solvable"],
                      "their_description": "W(D4):C3, order 576",
                      "status": "orders agree, descriptions differ, NOT resolved"},
        "pass_5403": {"modules": len(mods), "relevant": hits,
                      "finding": ("the formal layer is an arithmetic consistency checker; "
                                  "every W33 module header explicitly disclaims the "
                                  "geometry, which is cited to Python and GAP"),
                      "for_this_week": "no prior art, no conflict, nothing to reuse"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5400_5403_STABILISER_ACTS_AND_FIXES_ONE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
