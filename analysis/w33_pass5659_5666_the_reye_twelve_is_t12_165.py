"""Passes 5659-5666 -- typing the orders, and naming the exact test the bridge needs.

  5659  The Reye 12 carries TransitiveGroup(12, 165), stabiliser C2 x S4.
  5660  Nine transitive degree-12 groups have order 576; exactly three are W(F4)/Z.
  5661  Every constructible 576 and 1152 in this corpus, typed by SmallGroup id.
  5662  The 7-side and the {2,3}-side do not meet below order 4032.
  5663  The q=5 design cannot be typed here, and the settling test is now one integer.
  5664  Scoping the transitivity guard: 547 findings -> 130.
  5665  Typing its order keys: 130 -> 124, and 0.8% of the corpus.
  5666  The other lane's whole 5600-block: zero findings, and what that does not mean.

    py -3 analysis/w33_pass5659_5666_the_reye_twelve_is_t12_165.py
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

# GAP: analysis/w33_pass5659_typing_the_orders.g
T12_576 = {158: [576, 8656], 159: [576, 8278], 160: [576, 8652], 161: [576, 8654],
           162: [576, 8652], 163: [576, 8654], 164: [576, 8664], 165: [576, 8654],
           166: [576, 8661]}
WF4Z = [576, 8654]
TYPED = [("W(F4)", 1152, [1152, 157478]), ("W(F4)/Z", 576, WF4Z),
         ("S4 wr S2", 1152, [1152, 157849]), ("Aut(Reye Levi)", 576, WF4Z),
         ("Aut(Q4)", 384, [384, 5602]), ("Reye 12-action", 576, WF4Z),
         ("Reye 16-action", 576, WF4Z)]
REYE12 = {"transitive_id": 165, "stabiliser_order": 48,
          "stabiliser": "C2 x S4", "stabiliser_id": [48, 48], "faithful": True}
GUARD = [("Pass 5657, as shipped", 547, 119), ("scoped to the enclosing dict", 130, 43),
         ("order keys typed", 124, 42)]
CORPUS = 5060


def main() -> int:
    print("=" * 78)
    print("Passes 5659-5666 -- the Reye 12 is T12_165")
    print("=" * 78)

    print("\n  PASS 5659 -- which action the Reye 12 carries\n")
    print(f"    Aut(Reye Levi) orbits on the Levi graph : [16, 12]")
    print(f"    action on the 12 : faithful, transitive, order 576")
    print(f"    action on the 16 : faithful, transitive, order 576")
    print(f"    point stabiliser of the 12 : order {REYE12['stabiliser_order']}, "
          f"{REYE12['stabiliser']}, id {REYE12['stabiliser_id']}")
    print(f"    TransitiveIdentification : T12_{REYE12['transitive_id']}")
    print("""
    NAMED, NOT MATCHED. Pass 5651 established that W(F4)/Z has three inequivalent
    faithful degree-12 actions and that the abstract isomorphism does not pick one. This
    picks it: the Reye 12 is TransitiveGroup(12, 165), with point stabiliser C2 x S4.
    Both the 12-action and the 16-action are faithful, so the configuration's two sides
    each see the whole group.""")

    print("\n  PASS 5660 -- how much a degree-12 order-576 match is worth\n")
    print(f"    {'group':10s} {'SmallGroup id':18s} {'is W(F4)/Z':>12s}")
    for k, sid in T12_576.items():
        mark = "YES" if sid == WF4Z else "no"
        star = "  <-- the Reye 12" if k == REYE12["transitive_id"] else ""
        print(f"    T12_{k:<6d} {str(sid):18s} {mark:>12s}{star}")
    same = [k for k, v in T12_576.items() if v == WF4Z]
    print(f"""
    NINE TRANSITIVE DEGREE-12 GROUPS HAVE ORDER 576, and exactly three are W(F4)/Z:
    T12_{', T12_'.join(map(str, same))}. That is the same three that Pass 5651 found as
    inequivalent faithful actions, reached from the other direction -- the transitive
    groups library and the subgroup lattice agree.

    SO "ORDER 576, TRANSITIVE ON 12" NARROWS THE FIELD TO NINE AND NOT TO ONE, and
    "isomorphic to W(F4)/Z" narrows it to three. Only the TransitiveIdentification
    settles it.""")

    print("\n  PASS 5661 -- the corpus's orders, typed\n")
    print(f"    {'object':18s} {'order':>7s}  {'SmallGroup id'}")
    for name, o, sid in TYPED:
        print(f"    {name:18s} {o:7d}  {sid}")
    print("""
    THE TWO 1152s ARE [1152, 157478] AND [1152, 157849]. That is the coincidence-ten kill
    at the level of an identifier rather than an isomorphism test, and it is now citable
    as a number. And the four 576s here -- W(F4)/Z, Aut(Reye Levi), and both Reye actions
    -- are all [576, 8654], one group wearing four names.""")

    print("\n  PASS 5662 -- the 7-side and the {2,3}-side\n")
    print(f"    |PSL(2,7)| = 168 = 2^3 * 3 * 7, id [168, 42]")
    print(f"    |W(F4)/Z|  = 576 = 2^6 * 3^2,  7 divides it: False")
    print(f"    lcm(576, 168) = 4032 = 576 * 7")
    print("""
    THEY DO NOT MEET BELOW ORDER 4032. PSL(2,7) has no subgroup of order 576 (it is
    smaller), W(F4)/Z has no element of order 7, and any group containing both needs order
    divisible by lcm(576,168) = 4032. S12 contains both, but that is a statement about S12
    and not about this object.

    SO THE SEPARATION PASS 5654 FOUND IS REAL AND NOT AN ARTEFACT of how the flags were
    counted: the codec layer's 7 and the bridge group's {2,3} have no common home in
    anything this corpus has built. NOTHING OF ORDER 4032 IS EXHIBITED ANYWHERE, and
    finding one -- or proving none exists in the relevant setting -- is the open question
    that this pass replaces the vague "chase the 7" with.""")

    print("\n  PASS 5663 -- the q=5 design, and why it is not typed here\n")
    print("""    The 2-(13,6,60) design's blocks are not stored as a list in any
    certificate -- Pass 5414 recorded its parameters, not its incidence -- and rebuilding
    it needs the 325-vertex q=5 cover, which is beyond what this pass could carry.

    BUT THE SETTLING TEST IS NOW ONE INTEGER. Their Pass 5623 says the design has "the
    same order-576 automorphism action". Compute TransitiveIdentification of that action
    on the moving 12:

        = 165        the Reye 12 and the q=5 moving 12 are the SAME G-set; the bridge
                     is equivariant and the cross-q map has a target
        = 161 or 163 the groups are isomorphic and the ACTIONS are not; equivariance
                     fails and the bridge stays abstract
        anything else  the design's group is not even W(F4)/Z, and Pass 5623's sentence
                     is an order match rather than an identification

    THREE OUTCOMES, ONE COMPUTATION, AND ALL THREE ARE INFORMATIVE. That is a better
    handoff than typing it here would have been, because it names what each answer
    would mean before the answer is known.""")

    print("\n  PASS 5664-5665 -- the guard, twice narrowed\n")
    print(f"    {'version':30s} {'findings':>9s} {'files':>7s} {'rate':>7s}")
    for label, f, n in GUARD:
        print(f"    {label:30s} {f:9d} {n:7d} {100*n/CORPUS:6.1f}%")
    print("""
    SCOPING WAS THE BIG CUT. Pairing every order key in a certificate with every partition
    key produced a finding per cross pair; restricting to the enclosing dict -- so an order
    and a partition are compared only when ONE object records both -- took 547 to 130.
    Typing the order keys took another six: `centralizer_order_digits` is a digit count
    and `abelianization_order` is a quotient that does not act on the set being
    partitioned. Both were reported as impossibilities and neither was one.

    0.8% IS A RATE A GUARD CAN BE READ AT. Selftest is 8/8, and the two new cases lock
    exactly the false positives that the corpus sweep exposed -- which is the only reason
    to trust the number.""")

    print("\n  PASS 5666 -- their whole 5600-block: zero\n")
    print("    seven summary certificates, Pass 5603 through 5658, 0 findings")
    print("""
    AND THAT IS NOT A CLEAN BILL. The guard tests one thing: a group order asserted
    against a partition of a set in the same object. Their packet is spectral and
    algebraic -- eigenvalue multiplicities, commutants, cochain degrees, BdG classes --
    and it mostly does not assert group actions on partitioned sets at all. Zero findings
    means THE GUARD DOES NOT APPLY, not that the work is verified.

    Saying otherwise would be exactly the over-read this repo has a failure mode for. The
    honest cross-lane result stays the Pass 5649 one: a single order-based identification
    flagged at w33_pass5623 line 5, still unsettled, and Pass 5663 now says precisely how
    to settle it.""")

    out = {
        "boundary": (
            "Pass 5659-5661 are GAP computations on constructed objects. Pass 5662 rules "
            "out a common home below order 4032 and does NOT prove no such object exists "
            "in this corpus -- none is exhibited. Pass 5663 does NOT type the q=5 design; "
            "it specifies the computation. Pass 5666 reports zero findings as "
            "INAPPLICABILITY of the guard, not as verification of the other lane's work"),
        "pass_5659": {**REYE12,
                      "levi_orbits": [16, 12],
                      "action_on_16_faithful": True,
                      "finding": ("the Reye 12 is TransitiveGroup(12,165); Pass 5651 "
                                  "showed the abstract isomorphism does not pick an "
                                  "action, and this picks it")},
        "pass_5660": {"transitive_degree12_order576": len(T12_576),
                      "ids": {str(k): v for k, v in T12_576.items()},
                      "isomorphic_to_wf4z": same,
                      "agreement": ("the transitive-groups library and the subgroup "
                                    "lattice both give three")},
        "pass_5661": {"typed": [{"object": n, "order": o, "smallgroup": s}
                                for n, o, s in TYPED],
                      "the_two_1152s": [[1152, 157478], [1152, 157849]],
                      "the_576s_are_all": WF4Z},
        "pass_5662": {"psl27": [168, 42], "psl27_order": 168,
                      "wf4z_order": 576, "seven_divides_576": False,
                      "lcm": 4032,
                      "verdict": ("no common home below order 4032; nothing of that order "
                                  "is exhibited anywhere in this corpus")},
        "pass_5663": {"design": "2-(13,6,60)", "blocks": 312,
                      "typed_here": False,
                      "reason": "blocks are not stored; rebuilding needs the 325-vertex cover",
                      "settling_test": "TransitiveIdentification of the action on the moving 12",
                      "outcomes": {"165": "same G-set as the Reye 12; bridge is equivariant",
                                   "161_or_163": "isomorphic groups, inequivalent actions",
                                   "other": "not W(F4)/Z at all; an order match only"}},
        "pass_5664_5665": {"progression": [{"version": l, "findings": f, "files": n}
                                           for l, f, n in GUARD],
                           "corpus": CORPUS, "final_rate_pct": 0.8, "selftest": "8/8",
                           "scoping": ("compare an order and a partition only when one "
                                       "object records both"),
                           "typed_keys": ["digits", "abelianization"]},
        "pass_5666": {"their_block": "PASS5603 through PASS5658", "certificates": 7,
                      "findings": 0,
                      "reading": ("INAPPLICABLE, not verified -- their packet is spectral "
                                  "and algebraic and mostly does not assert group actions "
                                  "on partitioned sets"),
                      "outstanding_cross_lane": ("w33_pass5623 line 5, an order-based "
                                                 "identification; Pass 5663 gives the test")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5659_5666_THE_REYE_TWELVE_IS_T12_165.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
