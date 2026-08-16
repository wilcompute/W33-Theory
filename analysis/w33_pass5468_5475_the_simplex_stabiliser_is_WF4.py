"""Passes 5468-5475 -- the 13-simplex's symmetry group is the Weyl group W(F4), which
resolves two order-576 descriptions that looked like a disagreement.

  5468  Pass 5416 found the setwise stabiliser of the other lane's 13-cover has order 1152
        and acts on the thirteen with image 576 and kernel 2.  An external check says
        |W(F4)| = 1152 and W(F4) = GO4+(3).  Tested by IsomorphismGroups, not by matching
        orders: the stabiliser IS W(F4).

  5469  So the two order-576 groups in this corpus are a SUBGROUP and a QUOTIENT of the
        same W(F4), which is why their invariants differ and why neither lane was wrong.

  5470  The 4x4 toroidal knight graph is Q4 -- verified from scratch, since the repo
        asserts it twice from one source -- and its automorphism group is 384, not 576.

  5471  Which corrects a premise worth stating plainly: 576 is LARGER than the whole
        automorphism group of the hypercube, so it is not any hypercube symmetry group.

    py -3 analysis/w33_pass5468_5475_the_simplex_stabiliser_is_WF4.py
"""

from __future__ import annotations

import itertools
import json
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


def knight_and_cube():
    """4x4 toroidal knight graph and Q4, built independently of every repo builder."""
    cells = [(r, c) for r in range(4) for c in range(4)]
    idx = {p: i for i, p in enumerate(cells)}
    MOVES = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
    E = set()
    for (r, c) in cells:
        for dr, dc in MOVES:
            t = ((r + dr) % 4, (c + dc) % 4)
            a, b = idx[(r, c)], idx[t]
            if a != b:
                E.add((min(a, b), max(a, b)))
    K = igraph.Graph(n=16, edges=sorted(E))
    QE = [(a, b) for a in range(16) for b in range(a + 1, 16)
          if bin(a ^ b).count("1") == 1]
    return K, igraph.Graph(n=16, edges=QE)


def n_latin(n=4):
    c = 0
    for rows in itertools.product(itertools.permutations(range(n)), repeat=n):
        if all(len({rows[r][k] for r in range(n)}) == n for k in range(n)):
            c += 1
    return c


def main() -> int:
    print("=" * 78)
    print("Passes 5468-5475 -- it is W(F4)")
    print("=" * 78)

    f4 = json.loads((ROOT / "data" / "_gap_f4.json").read_text(encoding="utf-8"))
    sub = json.loads((ROOT / "data" / "_gap_sub576.json").read_text(encoding="utf-8"))
    lat = json.loads((ROOT / "data" /
                      "PART_W33_PASS5300_HOFFMAN576_LATIN_GROUP_BRIDGE.json")
                     .read_text(encoding="utf-8"))

    print("\n  PASS 5468 -- the stabiliser is the Weyl group W(F4)\n")
    for k in ("stabiliser_order", "WF4_order", "stab_centre", "WF4_centre",
              "stab_derived", "WF4_derived"):
        print(f"    {k:22s} : {f4[k]}")
    print(f"    {'spectra identical':22s} : "
          f"{f4['stab_spectrum'] == f4['WF4_spectrum']}")
    print(f"    {'ISOMORPHIC':22s} : {f4['stab_iso_WF4']}   "
          f"(IsomorphismGroups, not an order match)")
    print(f"    {'image = W(F4)/centre':22s} : {f4['A_iso_WF4_mod_centre']}")
    print(f"""
    THE HOFFMAN-TIGHT 13-COCLIQUE ON NO_5^+(5) IS A REGULAR 12-SIMPLEX WHOSE SYMMETRY GROUP
    IS W(F4). Order 1152, centre of order 2, derived subgroup 288, and the same
    element-order spectrum -- and then IsomorphismGroups confirms it rather than leaving it
    at coincidence. The centre is exactly the pointwise kernel on the thirteen, so the
    action on the simplex vertices is W(F4)/{{+-1}} of order 576.

    W(F4) = W(D4):S3 IS THE FULL TRIALITY EXTENSION. 192 x 6 = 1152. The other lane's
    Pass5308 found W(D4):C3 of order 576 = 192 x 3, which is triality's rotation half. Both
    lanes were looking at the same F4 tower from different sides.""")

    print("\n  PASS 5469 -- two 576s, and neither lane was wrong\n")
    L = lat["klein_latin"]
    H = lat["hoffman"]
    print(f"    {'group':34s} {'order':>6s} {'centre':>7s} {'derived':>8s}")
    print(f"    {'their H (Pass5308)':34s} {H['order']:6d} {H['center']:7d} "
          f"{H['derived']:8d}")
    print(f"    {'my image in S_13 (Pass5416)':34s} {576:6d} {1:7d} {144:8d}")
    print(f"    {'their AutPar(V4), Latin':34s} {L['V4_autoparatopy_order']:6d} "
          f"{L['center']:7d} {L['derived']:8d}")
    print(f"\n    order-576 SUBGROUP classes of W(F4)   : "
          f"{sub['n_classes_of_order_576_subgroups']}")
    print(f"    their centres                          : {sub['centres']}")
    print(f"    their derived orders                   : {sub['deriveds']}")
    print(f"""
    THE RESOLUTION IS SUBGROUP VERSUS QUOTIENT. W(F4) has {sub['n_classes_of_order_576_subgroups']} classes of order-576
    subgroups, all with centre 2, and two of them with derived subgroup 96 -- which is
    exactly their H. So their H is a SUBGROUP of W(F4).

    My image has centre 1 and derived 144, which no subgroup on that list has, because it is
    not a subgroup at all: it is the QUOTIENT W(F4)/{{+-1}}. Quotienting by the centre is
    precisely what kills a centre of 2 and doubles a derived order from 144's preimage.

    SO THE "DISAGREEMENT" AT PASS 5462 WAS NEVER ONE. Two groups of order 576, both attached
    to one W(F4), one as a subgroup and one as a quotient, described correctly by each lane.
    My Pass5252 prior said to re-derive mine first when a cross-lane number disagrees; here
    the right move was to find the group that contains both.

    AND MY IMAGE MATCHES THE LATIN GROUP ON EVERY INVARIANT TESTED -- order 576, centre 1,
    derived 144, and the full element-order spectrum 1:1, 2:75, 3:80, 4:180, 6:240. Their
    Pass5300 proved H/Z(H) of order 288 is conjugate to the even-parastrophe subgroup of
    AutPar(V4); this is the same bridge one level up, at 576 rather than 288, on a different
    object.""")

    print("\n  PASS 5470 -- the knight graph, checked from scratch\n")
    K, Q = knight_and_cube()
    iso = K.isomorphic(Q)
    autK = K.count_automorphisms_vf2()
    autQ = Q.count_automorphisms_vf2()
    print(f"    toroidal knight graph : {K.vcount()} vertices, {K.ecount()} edges, "
          f"{sorted(set(K.degree()))}-regular")
    print(f"    hypercube Q4          : {Q.vcount()} vertices, {Q.ecount()} edges")
    print(f"    ISOMORPHIC            : {iso}")
    print(f"    |Aut| (both)          : {autK:,} and {autQ:,}")
    nl = n_latin(4)
    print(f"    4x4 Latin squares     : {nl}   = 24^2 = |S4|^2 : {nl == 24 ** 2}")
    print(f"""
    A KNIGHT'S TOUR GRAPH ON A 4x4 TORUS IS THE 4-CUBE. Verified here rather than taken from
    the repo, which asserts it in Pass5311 and Pass5316 from one source. Both are 4-regular
    on 16 vertices with 32 edges and igraph confirms the isomorphism.

    AND THE AUTOMORPHISM GROUP IS 384, NOT 576. {autQ:,} = 2^4 * 4! is the full signed
    permutation group B4 = W(B4) = W(C4).""")

    print("\n  PASS 5471 -- the ladder, with the sizes attached correctly\n")
    ladder = [
        (96, "W(D4)/{+-1} = the tomotope group (C2)^4:S3 (their Pass5309)"),
        (192, "W(D4)  AND, separately, the tesseract rotation group -- NOT isomorphic "
              "(their Pass5310: R has 48 elements of order 8, W(D4) has none)"),
        (384, "|Aut(Q4)| = B4 = W(B4), the full signed permutations of the 4-cube"),
        (576, "TWO different groups: W(D4):C3 (subgroup of W(F4)) and W(F4)/{+-1} "
              "(quotient); also the number of 4x4 Latin squares, = 24^2"),
        (1152, "W(F4) = W(D4):S3 = GO4+(3) -- the 13-cover's setwise stabiliser"),
    ]
    for k, v in ladder:
        print(f"    {k:5d}  {v}")
    print(f"""
    576 IS BIGGER THAN 384, so it is not a symmetry group of the hypercube at all -- not the
    rotation group, which is 192, and not the full group, which is 384. The 576 in the Latin
    story is the SQUARE COUNT and the autoparatopy group of one particular square; the 576 in
    the F4 story is a subgroup or a quotient of W(F4). They meet, but not through the cube.

    WHAT IS GENUINELY ONE OBJECT: the F4/D4 Weyl tower. 96, 192, 1152 are W(D4)/+-1, W(D4)
    and W(F4); 384 is the neighbouring W(B4). That the 13-cover stabiliser lands exactly on
    W(F4) is the connection, and it is an isomorphism rather than a shared integer.""")

    out = {
        "boundary": ("The W(F4) identification is by GAP IsomorphismGroups on the setwise "
                     "stabiliser of the other lane's Pass5212 13-cover in Aut of their "
                     "P-block graph. The AutPar(V4) match is on ORDER, CENTRE, DERIVED "
                     "ORDER and ELEMENT-ORDER SPECTRUM taken from their Pass5300 "
                     "certificate -- a full isomorphism test against their group object "
                     "was not run, so that identification is 'agrees on every invariant "
                     "tested', not 'proved isomorphic'. Coincidences of order are not "
                     "bridges and 576 has independent sources here"),
        "pass_5468": {**{k: f4[k] for k in
                         ("stabiliser_order", "image_order", "WF4_order", "stab_iso_WF4",
                          "stab_centre", "WF4_centre", "stab_derived", "WF4_derived",
                          "A_iso_WF4_mod_centre")},
                      "spectra_identical": f4["stab_spectrum"] == f4["WF4_spectrum"],
                      "theorem": ("the Hoffman-tight 13-coclique is a regular 12-simplex "
                                  "whose symmetry group is W(F4); the centre is the "
                                  "pointwise kernel and the action on the 13 is "
                                  "W(F4)/{+-1}"),
                      "external": "|W(F4)| = 1152, W(F4) = GO4+(3) (ATLAS)"},
        "pass_5469": {"their_H": {"order": H["order"], "centre": H["center"],
                                  "derived": H["derived"]},
                      "my_image": {"order": 576, "centre": 1, "derived": 144},
                      "autpar_V4": {"order": L["V4_autoparatopy_order"],
                                    "centre": L["center"], "derived": L["derived"]},
                      "WF4_order576_subgroup_classes": sub,
                      "resolution": ("their H is a SUBGROUP of W(F4) (centre 2, derived "
                                     "96, matching two of the three classes); my image is "
                                     "the QUOTIENT W(F4)/{+-1} (centre 1, derived 144). "
                                     "Both correct, one group, different constructions"),
                      "supersedes": "the Pass 5462 'descriptions differ' open question"},
        "pass_5470": {"knight_is_Q4": bool(iso), "vertices": 16, "edges": K.ecount(),
                      "aut_order": autQ, "latin_4x4": nl,
                      "note": "verified from scratch; the repo asserts it from one source"},
        "pass_5471": {"ladder": {str(k): v for k, v in ladder},
                      "correction": ("576 exceeds |Aut(Q4)| = 384, so it is not a "
                                     "hypercube symmetry group; the rotation group is 192")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5468_5475_SIMPLEX_STABILISER_IS_WF4.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
