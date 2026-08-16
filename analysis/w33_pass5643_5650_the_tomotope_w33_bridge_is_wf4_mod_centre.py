"""Passes 5643-5650 -- the corpus had the wrong 16, and the right one bridges to W(3,3).

  5643  BT1413 carries the Reye 12_4 16_3 configuration; its 16 is Q4 EDGE classes.
  5644  Coincidence ten: the 16-face graph's 1152 is S4 wr S2, NOT W(F4).
  5645  THE BRIDGE: Aut(Levi) = W(F4)/Z, the same 576 as the W(3,3) simplex stabiliser.
  5646  BT1413 never sees the 24+84+84 codec partition.
  5647  84+84 = 168 = |PSL(2,7)| left OPEN rather than killed, and why.
  5648  The 96+96 orbit pair is not the other lane's deck involution.
  5649  A transitivity work list: 35 order/size co-occurrences across the corpus.
  5650  alpha(W(3,9)): the dual bound beats Hoffman.

    py -3 analysis/w33_pass5643_5650_the_tomotope_w33_bridge_is_wf4_mod_centre.py
"""

from __future__ import annotations

import collections
import itertools
import json
import sys
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BT1413 = ROOT / "data" / "bt1413_q4_plaquette_tomotope_face_compiler.json"
FACE = "tomotope_face_label_from_q4_edge_pair"
EDGE = "tomotope_edge_label_from_q4_face_pair"

# GAP, analysis/w33_pass5643_reye16_aut_identify.g and w33_pass5644_levi576_identify.g
GAP = {
    "face_graph_aut": 1152,
    "face_graph_structure": "(((((C2 x C2 x C2 x C2) : C3) : C2) : C3) : C2) : C2",
    "wf4": 1152,
    "wf4_structure": "((((C2 x C2 x C2) : (C2 x C2)) : (C3 x C3)) : C2) : C2",
    "s4wrs2": 1152, "s4wrs2_structure": "(S4 x S4) : C2",
    "face_aut_iso_wf4": False, "face_aut_iso_s4wrs2": True, "wf4_iso_s4wrs2": False,
    "complement_is_rook_4x4": True, "rook_aut": 1152,
    "levi_aut": 576, "levi_structure": "((A4 x A4) : C2) : C2",
    "wf4_centre": 2, "wf4_mod_centre": 576,
    "wf4_mod_centre_structure": "((A4 x A4) : C2) : C2",
    "levi_iso_wf4_mod_centre": True,
    "levi_iso_s4wrs2_index2": False, "wf4modZ_iso_s4wrs2_index2": False,
}
ORDER_AUDIT = [(24, "S4", 11), (192, "Rot(Q4)", 6), (25920, "PSp(4,3)", 5),
               (51840, "Sp(4,3)/W(E6)", 5), (96, "Aut(tomotope)", 4),
               (168, "PSL(2,7)", 4)]
Q9 = {"points": 820, "lines": 820, "hoffman": 82, "lp_relaxation": 82,
      "dual_bound": 80.83841179, "incumbent": 47, "proved": False}


def load_incidence():
    d = json.loads(BT1413.read_text(encoding="utf-8", errors="replace"))
    inc = collections.defaultdict(set)
    for r in d["flag_rows"]:
        inc[r[FACE]].add(r[EDGE])
    return d, inc


def main() -> int:
    print("=" * 78)
    print("Passes 5643-5650 -- the corpus had the wrong 16")
    print("=" * 78)
    d, inc = load_incidence()
    faces, edges = sorted(inc), sorted({e for v in inc.values() for e in v})

    print("\n  PASS 5643 -- BT1413's 16 is Q4 EDGE classes, not Q4 vertices\n")
    fdeg = {len(v) for v in inc.values()}
    rev = collections.defaultdict(set)
    for f, es in inc.items():
        for e in es:
            rev[e].add(f)
    edeg = {len(v) for v in rev.values()}
    print(f"    tomotope faces (from Q4 edge pairs) : {len(faces)}, degree {fdeg}")
    print(f"    tomotope edges (from Q4 face pairs) : {len(edges)}, degree {edeg}")
    print(f"    configuration                       : "
          f"{len(edges)}_{max(edeg)} {len(faces)}_{max(fdeg)}   (Reye)")
    print(f"    Q4 edge classes mod antipodal       : 32/2 = 16")
    print(f"    Q4 face classes mod antipodal       : 24/2 = 12")
    print("""
    THAT IS THE WHOLE ERROR OF 2026-05-29. It wrote "16 = Q4 vertices = codec slots".
    Q4 has 16 VERTICES and, mod the antipodal map, 16 EDGE CLASSES. Two different 16s,
    and the working compiler uses the second. Pass 5638 refuted the vertex reading; this
    identifies what should have been there instead, and it was already in BT1413.""")

    print("\n  PASS 5644 -- coincidence ten\n")
    G = nx.Graph()
    G.add_nodes_from(faces)
    for a, b in itertools.combinations(faces, 2):
        if inc[a] & inc[b]:
            G.add_edge(a, b)
    print(f"    16-face adjacency : {G.number_of_edges()} edges, "
          f"degrees {sorted(set(dict(G.degree()).values()))}, "
          f"triangles {sum(nx.triangles(G).values()) // 3}")
    print(f"    |Aut|             : {GAP['face_graph_aut']}")
    print(f"    complement is the 4x4 rook's graph : {GAP['complement_is_rook_4x4']}")
    print(f"    Aut =~ W(F4)      : {GAP['face_aut_iso_wf4']}")
    print(f"    Aut =~ S4 wr S2   : {GAP['face_aut_iso_s4wrs2']}")
    print(f"    W(F4) =~ S4 wr S2 : {GAP['wf4_iso_s4wrs2']}")
    print("""
    1152 = |W(F4)| = |S4 wr S2| AND THE TWO GROUPS ARE NOT ISOMORPHIC. The 16-face graph
    is the complement of the 4x4 rook's graph, so its automorphism group is S4 wr S2.
    This is the coincidence that would have caught me: Pass 5468-5475 PROVED the W(3,3)
    simplex stabiliser is W(F4), also of order 1152, and a second 1152 in the tomotope
    is exactly the shape of a bridge. It is not one. Coincidence ten, killed the way
    Pass 5468 was decided -- by IsomorphismGroups, never by order.""")

    print("\n  PASS 5645 -- and the bridge is the OTHER group\n")
    print(f"    Levi graph of the 12_4 16_3   : |Aut| = {GAP['levi_aut']}")
    print(f"      structure                   : {GAP['levi_structure']}")
    print(f"    |Z(W(F4))| = {GAP['wf4_centre']},  |W(F4)/Z| = {GAP['wf4_mod_centre']}")
    print(f"      structure                   : {GAP['wf4_mod_centre_structure']}")
    print(f"    Aut(Levi) =~ W(F4)/Z          : {GAP['levi_iso_wf4_mod_centre']}")
    print("""
    PROVED, NOT MATCHED. Aut of the Reye Levi graph IS W(F4) modulo its centre, by
    IsomorphismGroups, and the structure descriptions agree character for character:
    ((A4 x A4) : C2) : C2.

    AND THAT IS THE GROUP I ALREADY HAD. Pass 5416-5419 computed the W(3,3) simplex
    setwise stabiliser as order 1152 with image in S_13 of order 576 and structure
    ((A4 x A4) : C2) : C2; Pass 5468-5475 identified the stabiliser as W(F4) and resolved
    the two-576 puzzle as subgroup-versus-quotient. So the tomotope's Reye configuration
    and the W(3,3) simplex stabiliser carry THE SAME GROUP, and it is the quotient
    W(F4)/{+-1} on both sides.

    THE TOMOTOPE-W33 BRIDGE IS THEREFORE AT THE LEVI/CONFIGURATION LEVEL, not at the
    face-adjacency level where the decoy 1152 sits. One of the two 1152s in this object
    is real and one is S4 wr S2, and only an isomorphism test separates them.""")

    print("\n  PASS 5646 -- BT1413 never sees the codec partition\n")
    for f in (FACE, EDGE, "ternary_sheet", "flag_residue"):
        sizes = sorted(collections.Counter(r[f] for r in d["flag_rows"]).values(),
                       reverse=True)
        print(f"    {f:40s} blocks {sizes[:4]}{' ...' if len(sizes) > 4 else ''}")
    print("""
    EVERY BT1413 FIELD PARTITIONS 192 INTO EQUAL BLOCKS. The codec partition 24+84+84 is
    unequal, by source polyhedron. So the two maps onto the same 192 flags share no
    common refinement, which is a stronger statement than Pass 5638's: the plaquette
    chain does not merely dodge the vertex obstruction, it never meets the codec
    stratification at all.""")

    print("\n  PASS 5647 -- 168 = 84 + 84 = |PSL(2,7)|, left OPEN\n")
    print("""    A regular action of an order-168 group is transitive, and the flag set
    splits 84|84 by source polyhedron -- so the same argument that killed coincidence
    nine should apply. IT DOES NOT CLEANLY, because Csaszar and Szilassi are DUALS: an
    exchange of the two halves exists, so the invariant split does not by itself forbid
    transitivity.

    BUT DUALITY GENERATES C2, NOT PSL(2,7). No order-168 action is exhibited, and none
    is refuted. Recording this as OPEN rather than as coincidence eleven -- the honest
    verdict is weaker than a kill and weaker than a result, and calling it either would
    be the over-read failure mode.""")

    print("\n  PASS 5648 -- the 96+96 is not the deck involution\n")
    print("""    bt1371's two regular orbits of 96 on the 192 flags are separated by
    q6_direction, an orientation label on Q6 edges. The other lane's D: v <-> -v is an
    antipodal map on a 32-state magnetic lift at q=3. Different carriers (192 vs 32),
    different acting orders (96 vs 2). Identifying them would need a map between the
    carriers and none is built. NOT the same involution, on carrier grounds.""")

    print("\n  PASS 5649 -- a transitivity work list\n")
    print(f"    {'order':>7s}  {'group':18s} {'certificates':>12s}")
    for o, name, c in ORDER_AUDIT:
        print(f"    {o:7d}  {name:18s} {c:12d}")
    print(f"    total flagged pairs: {sum(c for _, _, c in ORDER_AUDIT)}")
    print("""
    35 PLACES WHERE AN ORDER AND A SET SIZE COINCIDE IN ONE CERTIFICATE. The
    order-coincidence guard flags the PHRASING; this scans the DATA. Each pair is a
    candidate for the test that killed coincidences nine and ten: exhibit the action, or
    find an invariant partition into unequal parts and conclude the two n's differ.""")

    print("\n  PASS 5650 -- alpha(W(3,9)), and the bound moves\n")
    print(f"    points {Q9['points']}, lines {Q9['lines']}, Hoffman {Q9['hoffman']}")
    print(f"    LP relaxation with LINE constraints : {Q9['lp_relaxation']} "
          f"(equals Hoffman exactly)")
    print(f"    MILP dual bound after branching     : {Q9['dual_bound']:.4f}")
    print(f"    best incumbent                      : {Q9['incumbent']}  (not proved)")
    print(f"""
    THE FORMULATION BUG IS FIXED and the bound now beats Hoffman: alpha(W(3,9)) <= 80,
    strictly below 82, because the dual bound fell to {Q9['dual_bound']:.2f}. The clique LP
    relaxation lands exactly on Hoffman, which is the expected behaviour and a check on
    the model. The gap is still wide -- 47 against 80 -- so alpha(W(3,9)) remains OPEN,
    with a strictly better upper bound than before.""")

    out = {
        "boundary": (
            "Pass 5645 proves an isomorphism of ABSTRACT GROUPS between Aut(Levi) and "
            "W(F4)/Z; it does NOT construct an equivariant map between the tomotope "
            "configuration and the W(3,3) simplex, and does not claim the two actions "
            "are equivalent as permutation groups. Pass 5647 leaves 168 OPEN, neither "
            "killed nor established. Pass 5650 reports alpha(W(3,9)) OPEN with a new "
            "upper bound of 80; 47 is an unproved incumbent"),
        "pass_5643": {"configuration": "12_4 16_3 (Reye)",
                      "faces": len(faces), "edges": len(edges),
                      "face_degree": sorted(fdeg), "edge_degree": sorted(edeg),
                      "q4_edge_classes_mod_antipodal": 16,
                      "q4_face_classes_mod_antipodal": 12,
                      "correction": ("2026-05-29 wrote '16 = Q4 vertices'; the working "
                                     "compiler's 16 is Q4 EDGE classes mod antipodal. "
                                     "Two different 16s")},
        "pass_5644": {**{k: GAP[k] for k in
                         ("face_graph_aut", "face_aut_iso_wf4", "face_aut_iso_s4wrs2",
                          "wf4_iso_s4wrs2", "complement_is_rook_4x4", "rook_aut")},
                      "face_graph_degree": 9,
                      "face_graph_triangles": sum(nx.triangles(G).values()) // 3,
                      "verdict": ("1152 = |W(F4)| = |S4 wr S2|, non-isomorphic; the "
                                  "16-face graph is the rook's-graph complement so its "
                                  "Aut is S4 wr S2"),
                      "coincidence_number": 10},
        "pass_5645": {**{k: GAP[k] for k in
                         ("levi_aut", "levi_structure", "wf4_centre", "wf4_mod_centre",
                          "wf4_mod_centre_structure", "levi_iso_wf4_mod_centre")},
                      "prior_art": ["Pass 5416-5419 (stabiliser 1152, image 576)",
                                    "Pass 5468-5475 (stabiliser IS W(F4))",
                                    "Pass 5488-5491 (Reye = Q4 face-edge / <1111>)"],
                      "bridge": ("the tomotope's Reye configuration and the W(3,3) "
                                 "simplex stabiliser carry the SAME group, W(F4)/{+-1}, "
                                 "at the Levi level -- proved by IsomorphismGroups")},
        "pass_5646": {"bt1413_blocks_are_equal": True,
                      "codec_partition": [24, 84, 84],
                      "finding": ("no common refinement: the plaquette chain never meets "
                                  "the codec stratification")},
        "pass_5647": {"sum": 168, "halves": [84, 84], "psl27": 168,
                      "status": "OPEN",
                      "why": ("duality supplies an exchange of the two 84s so the "
                              "invariant split does not forbid transitivity; but duality "
                              "generates C2, not an order-168 regular action")},
        "pass_5648": {"orbits": [96, 96], "separator": "q6_direction",
                      "other_lane_carrier": 32, "this_carrier": 192,
                      "verdict": "not the same involution, on carrier grounds"},
        "pass_5649": {"audit": [{"order": o, "group": g, "certificates": c}
                                for o, g, c in ORDER_AUDIT],
                      "total_pairs": 35,
                      "method": ("scan for an order and a set size coinciding in one "
                                 "certificate; the guard flags phrasing, this flags data"),
                      "cross_lane": {
                          "file": "analysis/w33_pass5623_cover_f4_fixed_vertex_physics_gate.py:5",
                          "phrase": "the same order-576 automorphism action",
                          "why_it_matters": (
                              "Pass 5644 proves 576 has at least TWO non-isomorphic "
                              "realizations in this corpus: W(F4)/Z and the index-2 "
                              "subgroup of S4 wr S2. So 'the same order-576 action' does "
                              "not establish the same group"),
                          "settling_test": (
                              "IsomorphismGroups on the q=5 2-(13,6,60) design's "
                              "automorphism group against W(F4)/Z -- cheap, and it "
                              "decides their cover-to-F4 gate"),
                          "status": "FLAGGED, not run -- reported to the other lane"},
                      "prior_art_found_by_the_reranked_guard": {
                          "certificate": "PART_MMCCCLXXV_DENSITY_DUAL_GENERATOR_results.json",
                          "records": {"Aut_K44": 1152, "PSL27": 168,
                                      "dual_PSL": "24*7 = 28*6 = 168"},
                          "note": ("the corpus ALREADY recorded a 1152 that is S4 wr S2 "
                                   "-- Aut(K_{4,4}) -- which is prior art for the "
                                   "coincidence-ten kill, and it surfaced because the "
                                   "guard now ranks by stem reach")},
        "pass_5650": {**Q9, "status": "OPEN",
                      "improvement": ("dual bound 80.84 < Hoffman 82, so alpha <= 80; "
                                      "the clique LP relaxation equals Hoffman exactly")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5643_5650_TOMOTOPE_W33_BRIDGE_IS_WF4_MOD_CENTRE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
