"""Passes 5651-5658 -- the bridge is abstract, not equivariant, and 84 is why.

  5651  W(F4)/Z has three inequivalent faithful degree-12 actions: equivariance is NOT free.
  5652  CORRECTION to Pass 5644: W(F4)/Z IS an index-2 subgroup of S4 wr S2.
  5653  8,681 groups share order 576, which prices every 576 match in this corpus.
  5654  84 does not divide 576: the codec split is incompatible with the bridge group.
  5655  The transitivity work list is mostly undecidable from certificates alone.
  5656  The rook's graph is not a hidden recurring object; the recurring thing is 1152.
  5657  A transitivity guard, self-tested, firing on 2.4% of the corpus.
  5658  alpha(W(3,9)) >= 51 by construction, up from 47.

    py -3 analysis/w33_pass5651_5658_the_bridge_is_not_equivariant_and_84_is_the_obstruction.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# GAP: analysis/w33_pass5651_bridge_equivariance.g
IDX12 = [("(C2 x C2 x C2 x C2) : C3", False), ("A4 : C4", True),
         ("C2 x C2 x A4", False), ("C2 x S4", True),
         ("(C2 x C2 x C2 x C2) : C3", False), ("C2 x S4", True),
         ("C2 x S4", True)]
IMAGES = [12, 576, 36, 576, 12, 576, 576]
PERM_ISO = [(1, 5), (4, 7)]          # 1-indexed pairs that ARE permutation isomorphic
S576 = 8681
WF4Z_ID = [576, 8654]
S4WRS2_NORMAL_576 = [([576, 8653], "S4 x S4"), ([576, 8652], "(A4 x A4) : C4"),
                     ([576, 8654], "((A4 x A4) : C2) : C2")]
GUARD = {"findings": 547, "files": 119, "corpus": 5058, "selftest": "6/6"}
Q9 = {"incumbent_before": 47, "incumbent_now": 51, "dual_bound": 80.83841179,
      "hoffman": 82, "proved": False}


def main() -> int:
    print("=" * 78)
    print("Passes 5651-5658 -- the bridge is abstract, and 84 is the obstruction")
    print("=" * 78)

    print("\n  PASS 5651 -- equivariance is not free\n")
    print(f"    conjugacy classes of index-12 subgroups of W(F4)/Z : {len(IDX12)}")
    for s, core in IDX12:
        print(f"      |H| = 48   {s:28s} core trivial: {core}")
    faithful = [i + 1 for i, o in enumerate(IMAGES) if o == 576]
    print(f"    degree-12 images                                   : {len(IMAGES)}")
    print(f"    of which FAITHFUL (order 576)                      : {faithful}")
    print(f"    permutation-isomorphic pairs among all seven       : {PERM_ISO}")
    print(f"""
    THREE INEQUIVALENT FAITHFUL DEGREE-12 ACTIONS. Images {faithful} all have order 576,
    and only 4 and 7 are permutation isomorphic -- so the faithful ones fall into three
    classes. Pass 5645 proved Aut(Reye Levi) =~ W(F4)/Z as ABSTRACT groups; this settles
    that the abstract isomorphism does NOT determine the 12-point action, because the
    group has three inequivalent ones to choose from.

    SO THE BRIDGE STILL NEEDS ITS MAP. Had there been a unique class, equivariance would
    have followed for free and the Reye 12 and the q=5 moving 12 would be the same G-set
    on general grounds. They are not forced to be. That is a real constraint on the next
    step, and it is the difference between a bridge and a coincidence of group names.""")

    print("\n  PASS 5652 -- correcting Pass 5644\n")
    print(f"    W(F4)/Z SmallGroup id                    : {WF4Z_ID}")
    print(f"    index-2 normal subgroups of S4 wr S2 of order 576:")
    for sid, desc in S4WRS2_NORMAL_576:
        mark = "  <-- THIS IS W(F4)/Z" if sid == WF4Z_ID else ""
        print(f"      {str(sid):14s} {desc:26s}{mark}")
    print("""
    PASS 5644 REPORTED `wf4modZ_iso_s4wrs2_index2: False` AND THAT WAS WRONG. The test
    used GAP's First(NormalSubgroups(...), Size = 576), which returned S4 x S4 -- one of
    THREE index-2 normal subgroups. Against the right one, W(F4)/Z and the S4 wr S2
    subgroup are the same group, SmallGroup(576, 8654).

    THE 1152 KILL STANDS: W(F4) is still not isomorphic to S4 wr S2, so the face-adjacency
    graph's automorphism group is still not W(F4). But the two objects are far more
    closely related than Pass 5644 said -- the decoy 1152 sits directly ABOVE the real 576
    as an index-2 overgroup. The face graph and the Levi graph are two levels of one
    tower, not two unrelated coincidences.""")

    print("\n  PASS 5653 -- what a 576 match is worth\n")
    print(f"    groups of order 576 up to isomorphism : {S576:,}")
    print(f"""
    {S576:,}. An order match at 576 carries essentially no information, and this corpus
    matches on 576 repeatedly -- the W(3,3) simplex stabiliser image, the Reye Levi, the
    Latin-square V4 autoparatopy, the q=5 design action. Pass 5645 typed one of them
    properly. The others are named by order alone and each is one SmallGroup id away from
    being settled.""")

    print("\n  PASS 5654 -- 84 does not divide 576\n")
    for n in (24, 84, 168, 192):
        print(f"      {n:4d} divides 576 : {576 % n == 0}")
    print("""
    THE CODEC SPLIT IS INCOMPATIBLE WITH THE BRIDGE GROUP, on divisibility alone. Every
    orbit length of a group of order 576 = 2^6 * 3^2 divides 576; 84 = 2^2 * 3 * 7 does
    not, because of the 7. So W(F4)/Z cannot act on the 192 flags with 24+84+84 as its
    orbits -- not by any embedding, not for any choice of action.

    AND THE 7 IS EXACTLY THE 7 OF CSASZAR AND SZILASSI, seven vertices and seven faces,
    and of PSL(2,7). The codec stratification lives on the 7-side of this object and the
    bridge group lives on the {2,3}-side. That is why Pass 5646 found no common
    refinement, and it upgrades that empirical observation to a structural one.""")

    print("\n  PASS 5655 -- the work list, worked\n")
    print("    35 order/size pairs tested for an unequal partition recorded in the")
    print("    same certificate:  0 decidable, 35 needing the orbit computation")
    print("""
    MOSTLY UNDECIDABLE FROM THE CERTIFICATE ALONE, which is itself the finding: the
    certificates that assert an order/size match are precisely the ones that did not
    compute the orbits. The test cannot be run retrospectively over the corpus; it has to
    run at write time, which is what Pass 5657 does.""")

    print("\n  PASS 5656 -- the rook's graph is not hiding anywhere\n")
    print("    4x4 rook's graph : 6-regular, 32 triangles;  Q4 : 4-regular, 0 triangles")
    print("    corpus mentions  : K44 32, rook 19, shrikhande 7")
    print("""
    NO. Q4 is not the rook's graph and the corpus's recurring 16-vertex object really is
    Q4. WHAT RECURS IS THE ORDER 1152, attached to two different graphs -- and Pass 5652
    now explains why that keeps happening: the two groups share an index-2 relationship,
    so both appear wherever this tower does.""")

    print("\n  PASS 5657 -- the guard\n")
    print(f"    scripts/check_transitivity.py, selftest {GUARD['selftest']}")
    print(f"    corpus sweep : {GUARD['findings']} findings over {GUARD['files']} of "
          f"{GUARD['corpus']:,} certificates "
          f"({100*GUARD['files']/GUARD['corpus']:.1f}%)")
    print("""
    2.4% IS THE POINT. The certificate-rediscovery guard fires on 70% and is therefore
    nearly information-free; this one tests a specific impossibility and fires on one file
    in forty. It reports two things: an unequal partition summing to a matching order (no
    regular action), and an orbit length not dividing an asserted group order.

    ITS KNOWN LIMITATION, STATED: it pairs every order key in a certificate with every
    partition key, so a file carrying several unrelated groups will over-report. 547 is
    an upper bound on findings; the 119 files are the work list.""")

    print("\n  PASS 5658 -- alpha(W(3,9)) moves\n")
    print(f"    incumbent before : {Q9['incumbent_before']}")
    print(f"    incumbent now    : {Q9['incumbent_now']}  (randomised greedy + plateau swaps)")
    print(f"    dual bound       : {Q9['dual_bound']:.2f}  ->  alpha <= 80")
    print(f"""
    51 AGAINST 80, BOTH ENDS IMPROVED THIS SESSION and the value still OPEN. Construction
    moved 47 -> 51 in 67 seconds of local search, which says the earlier MILP incumbent
    was not close to what a heuristic finds cheaply; the bound moved 82 -> 80.84 by
    branching on the clique formulation. Neither end is tight.""")

    out = {
        "boundary": (
            "Pass 5651 shows equivariance is NOT implied by the abstract isomorphism; it "
            "does NOT construct or refute a specific map. Pass 5652 CORRECTS Pass 5644's "
            "wf4modZ_iso_s4wrs2_index2 field from False to True; the 1152 kill is "
            "unaffected. Pass 5654 is a divisibility argument, which rules out the codec "
            "split as ORBITS of the bridge group and says nothing about other relations. "
            "Pass 5657's 547 is an upper bound -- the guard over-pairs. Pass 5658 leaves "
            "alpha(W(3,9)) OPEN at 51 <= alpha <= 80"),
        "pass_5651": {"index12_classes": len(IDX12),
                      "degree12_images": IMAGES,
                      "faithful_images": faithful,
                      "permutation_isomorphic_pairs": PERM_ISO,
                      "inequivalent_faithful_actions": 3,
                      "verdict": ("the abstract isomorphism does not determine the "
                                  "12-point action; the bridge still needs its map")},
        "pass_5652": {"wf4_mod_z_smallgroup": WF4Z_ID,
                      "s4wrs2_index2_normal": [{"id": i, "structure": d}
                                               for i, d in S4WRS2_NORMAL_576],
                      "corrects": ("Pass 5644 field wf4modZ_iso_s4wrs2_index2: "
                                   "False -> True; GAP First() returned S4 x S4, one of "
                                   "three index-2 normal subgroups"),
                      "unaffected": ("W(F4) is still not isomorphic to S4 wr S2, so the "
                                     "coincidence-ten kill stands"),
                      "new_reading": ("the decoy 1152 is an index-2 OVERGROUP of the real "
                                      "576; face graph and Levi graph are two levels of "
                                      "one tower")},
        "pass_5653": {"groups_of_order_576": S576,
                      "reading": ("an order match at 576 carries essentially no "
                                  "information; this corpus matches on 576 repeatedly and "
                                  "has typed exactly one of them")},
        "pass_5654": {"bridge_group_order": 576, "factorisation": "2^6 * 3^2",
                      "codec_split": [24, 84, 84],
                      "divides": {24: True, 84: False, 168: False, 192: True},
                      "obstruction": 7,
                      "verdict": ("W(F4)/Z cannot have the codec split as orbits, by "
                                  "divisibility; the codec layer is on the 7-side and the "
                                  "bridge group on the {2,3}-side")},
        "pass_5655": {"pairs": 35, "decidable_from_certificate": 0,
                      "finding": ("the certificates asserting an order/size match are "
                                  "precisely those that did not compute orbits; the test "
                                  "must run at write time")},
        "pass_5656": {"rook_regular": 6, "q4_regular": 4,
                      "rook_triangles": 32, "q4_triangles": 0,
                      "corpus_mentions": {"K44": 32, "rook": 19, "shrikhande": 7},
                      "verdict": ("Q4 is the corpus's recurring 16-vertex object; what "
                                  "recurs is the ORDER 1152 on two graphs, explained by "
                                  "the index-2 relation of Pass 5652")},
        "pass_5657": {**GUARD, "script": "scripts/check_transitivity.py",
                      "firing_rate_pct": round(100 * GUARD["files"] / GUARD["corpus"], 1),
                      "compare": "check_certificate_rediscovery fires on 70%",
                      "limitation": ("pairs every order key with every partition key in a "
                                     "certificate; 547 is an upper bound, the 119 files "
                                     "are the work list")},
        "pass_5658": {**Q9, "status": "OPEN", "bounds": [51, 80],
                      "note": ("construction moved 47 -> 51 in 67s of local search, so "
                               "the MILP incumbent was far from cheap heuristic reach")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5651_5658_BRIDGE_NOT_EQUIVARIANT_84_IS_THE_OBSTRUCTION.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
