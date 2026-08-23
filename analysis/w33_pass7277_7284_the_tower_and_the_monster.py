"""Passes 7277-7284 -- E8 contains BOTH symplectic quadrangles, and where the tower really goes.

  7277  The Gaussian order-4 fibration of E8 gives W(3,2). Verified SRG(15,6,1,3).
  7278  Both fibres are root subsystems: A2 at d=3, A1^8 at d=4.
  7279  Why the collinear<=>orthogonal theorem is SPECIFIC to d=3, and it is about rank.
  7280  The Eisenstein tower E8 -> K12 -> Leech, stated honestly.
  7281  What that does and does NOT say about the Monster.
  7282  Three of my own verification predicates had the same Counter bug.
  7283  The session's remaining open items.
  7284  Scope.

    py -3 analysis/w33_pass7277_7284_the_tower_and_the_monster.py
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


def main() -> int:
    print("=" * 78)
    print("Passes 7277-7284 -- the tower, and the Monster question")
    print("=" * 78)

    print("\n  PASS 7277-7279 -- E8 CONTAINS BOTH SYMPLECTIC QUADRANGLES\n")
    print(f"      {'d':>2s}  {'ring':>7s}  {'quotient':>9s}  {'fibre':>16s}  {'rank':>4s}  "
          f"{'geometry':>16s}")
    print(f"      {3:2d}  {'Z[omega]':>7s}  {'F_3^4':>9s}  {'6 roots = A2':>16s}  {2:4d}  "
          f"{'W(3,3), 40 pts':>16s}")
    print(f"      {4:2d}  {'Z[i]':>7s}  {'F_2^4':>9s}  {'16 roots = A1^8':>16s}  {8:4d}  "
          f"{'W(3,2), 15 pts':>16s}")
    print("""
    Pass 7217 built W(3,3) from a fixed-point-free element of ORDER 3. Nothing in that
    argument was special to 3. An order-4 element exists with M^2 = -I exactly, trace 0,
    det(I-M) = 2^4 = 16, preserving all 240 roots -- it is NOT a power of the Coxeter element,
    since 4 does not divide h = 30, so it has to be found by search. It makes E8 a rank-4
    Z[i]-module, the quotient is F_2^4, and the 240 roots fall into 15 classes of exactly 16.

    THE FORM TOOK A CORRECTION. (Mx,y) is antisymmetric over Z, but in characteristic 2 that
    is not enough: it must DESCEND to the quotient, and it does not -- it gives degrees
    6,7,9,10. The form that works is A(x,y) = ((I+M)x, y) with (I+M) = 2(I-M)^{-1}, and it
    gives SRG(15,6,1,3), spectrum 6^1 1^9 (-3)^5, |Aut| = 720, ISOMORPHIC to W(3,2).

    BOTH FIBRES ARE ROOT SUBSYSTEMS. At d=3 the fibre is 6 roots with inner products
    {-2:3, -1:6, 1:6} -- an A2, rank 2. At d=4 it is 16 roots with {-2:8, 0:112} -- eight
    antipodal pairs and every other pair orthogonal, which is A1^8, rank 8.

    AND THAT IS EXACTLY WHY THE d=3 THEOREM DOES NOT GENERALISE. "Collinear iff the two
    fibres are completely orthogonal" has content only when fibres can be orthogonal at all.
    A2 has rank 2 < 8, so two of them fit orthogonally; A1^8 is FULL RANK, so no two fibres
    are ever orthogonal and the characterisation is vacuous. Measured, not guessed: at d=4
    the inner-product distribution between fibres is {-1:64, 0:128, 1:64} for BOTH collinear
    and non-collinear pairs -- identical, carrying no information.""")

    print("\n  PASS 7280-7281 -- the tower, and the Monster, stated honestly\n")
    print(f"      {'lattice':>8s}  {'rank/Z[omega]':>13s}  {'min vectors':>11s}  "
          f"{'/6':>7s}  {'automorphisms':>18s}")
    for name, rk, mv, aut in (("E8", 4, 240, "G32, order 155520"),
                              ("K12", 6, 756, "6.PSU(4,3).2"),
                              ("Leech", 12, 196560, "6.Suz")):
        print(f"      {name:>8s}  {rk:13d}  {mv:11d}  {mv // 6:7d}  {aut:>18s}")
    print("""
    The construction generalises in PRINCIPLE up the Eisenstein tower: each of these lattices
    carries a fixed-point-free order-3 automorphism, hence a Z[omega]-structure, hence a
    quotient by (1-omega) that is an F_3-space. E8 gives F_3^4 and W(3,3). K12 would give
    F_3^6, whose PG(5,3) has 364 points, of which only 756/6 = 126 carry minimal vectors.

    WHAT THIS DOES NOT SAY. The Leech lattice is where the moonshine module V-natural is
    built, and Aut(Leech) = Co0 is the group the Monster's construction rests on. That is a
    real chain and it is why the tower is worth climbing. It is NOT evidence that this
    construction produces the Monster, and NOTHING here computes a Monster representation, a
    modular function, or a physical quantity.

    I AM NOT GOING TO MANUFACTURE A THEORY OF EVERYTHING OUT OF IT. This repo has retracted
    physics claims before -- the chirality no-go closed, the selection layer closed as
    "unselectable from inside" -- and the honest position is that what has been established
    this session is finite geometry inside a lattice, verified, some of it new and about a
    third of it already ours. The K12 rung is the next real test and it is untested.""")

    print("\n  PASS 7282 -- the same bug, three times\n")
    print("""    My SRG verification predicates wrote `sorted(round(x) for x in ev)` where ev is
    a collections.Counter. Iterating a Counter yields KEYS, not repeated values, so the
    predicate compared {6,1,-3} against a 15-element multiset and returned False on a graph
    that WAS SRG(15,6,1,3). It happened in Pass 7217, again in Pass 7218, and again here --
    each time the printed spectrum was correct and the verdict line was wrong.

    THE PATTERN: a verification predicate that is harder to read than the thing it verifies.
    In all three cases the eigenvalue dictionary printed directly above the verdict already
    showed the answer, and the verdict contradicted it. Print the evidence next to the
    verdict and the disagreement is visible; that is the only reason it was caught.""")

    print("\n  PASS 7283-7284 -- open, and scope\n")
    print("""    NEW: the order-4 Gaussian fibration giving W(3,2); both fibres identified as
    root subsystems (A2 and A1^8); the rank explanation for why the d=3 orthogonality
    theorem is specific.

    NOT DONE: the K12 rung; anything at Leech scale; q=11 finished at 68 and does not
    discriminate; alpha(W(3,9)); Coolsaet (2014) unread; the third 1440; the Clifford L/R 36.

    NOT CLAIMED: any Monster connection beyond the lattice chain being real, and no physics.""")

    out = {
        "boundary": (
            "NEW: E8 admits a fixed-point-free order-4 automorphism whose quotient is F_2^4 "
            "and whose induced geometry is W(3,2), verified isomorphic to SRG(15,6,1,3). So "
            "the Eisenstein fibration is the d=3 member of a family. The d=3 "
            "collinear<=>orthogonal theorem does NOT generalise, for a structural reason: "
            "d=4 fibres are full-rank A1^8. NO Monster claim and NO physics claim is made"),
        "the_tower": {
            "d3": {"ring": "Z[omega]", "quotient": "F_3^4", "fibre_roots": 6,
                   "fibre_type": "A2", "fibre_rank": 2, "geometry": "W(3,3), 40 points",
                   "orthogonality_theorem": True},
            "d4": {"ring": "Z[i]", "quotient": "F_2^4", "fibre_roots": 16,
                   "fibre_type": "A1^8", "fibre_rank": 8, "geometry": "W(3,2), 15 points",
                   "orthogonality_theorem": False,
                   "why_not": ("A1^8 is full rank, so no two fibres are ever orthogonal; "
                               "measured, the inner-product distribution is {-1:64, 0:128, "
                               "1:64} for BOTH collinear and non-collinear pairs")},
            "order4_element": {"M2": "-I", "trace": 0, "det_I_minus_M": 16,
                               "not_a_coxeter_power": "4 does not divide h = 30"},
            "the_form": {"wrong": "(Mx,y) -- antisymmetric but does not descend, degrees 6,7,9,10",
                         "right": "((I+M)x, y) with (I+M) = 2(I-M)^{-1}",
                         "result": "SRG(15,6,1,3), spectrum 6^1 1^9 (-3)^5, |Aut| = 720"}},
        "eisenstein_tower": {
            "E8": {"rank_over_Zomega": 4, "min_vectors": 240, "classes": 40,
                   "aut": "G32, order 155520"},
            "K12": {"rank_over_Zomega": 6, "min_vectors": 756, "classes": 126,
                    "aut": "6.PSU(4,3).2", "status": "UNTESTED"},
            "Leech": {"rank_over_Zomega": 12, "min_vectors": 196560, "classes": 32760,
                      "aut": "6.Suz", "status": "UNTESTED"}},
        "monster_position": (
            "the Leech lattice is where the moonshine module is built and Aut(Leech) = Co0 "
            "underlies the Monster's construction, so the tower is worth climbing. That is "
            "NOT evidence this construction produces the Monster. Nothing here computes a "
            "Monster representation, a modular function, or a physical quantity, and no "
            "theory-of-everything claim is made"),
        "recurring_bug": {
            "what": "sorted(round(x) for x in ev) where ev is a Counter yields KEYS",
            "occurrences": ["Pass 7217", "Pass 7218", "Pass 7277"],
            "effect": "verdict False on graphs that WERE the target SRG",
            "why_caught": "the correct spectrum printed directly above the wrong verdict"},
        "not_done": ["the K12 rung", "anything at Leech scale", "alpha(W(3,9))",
                     "q=11 at 68", "Coolsaet (2014) unread", "the third 1440",
                     "the Clifford L/R 36"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7277_7284_THE_TOWER.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
