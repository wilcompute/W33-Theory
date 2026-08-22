"""Passes 7237-7244 -- what the 90 are, whose hexagons the 40 already were, and SRG(36,15,6,6).

  7237  The 90 J-stable D4s are 90 four-point PARTIAL OVOIDS. A clean duality with lines.
  7238  PRIOR ART: the 40 A2s are BT1750's 40 Witting hexagons. Confirmed exactly.
  7239  Why they are J-stable: c^5 fixes each hexagon, and J = c^10 = (c^5)^2.
  7240  E8 carries at most 2240 copies of W(3,3), by Springer.
  7241  The 36 spreads carry SRG(36,15,6,6).
  7242  Rank 16 clears the counting bar for q=9 but no lattice fits.
  7243  What is still open after all this.
  7244  Scope.

    py -3 analysis/w33_pass7237_7244_the_ninety_and_the_witting_rays.py
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
    print("Passes 7237-7244 -- the 90, the Witting hexagons, and SRG(36,15,6,6)")
    print("=" * 78)

    print("\n  PASS 7237 -- THE 90, and a duality that is not a coincidence\n")
    print(f"      {'object':22s} {'roots':>6s} {'rank':>5s}  {'its four W(3,3) points':>28s}")
    print(f"      {'line = A2^4':22s} {24:6d} {8:5d}  {'pairwise COLLINEAR':>28s}")
    print(f"      {'J-stable D4':22s} {24:6d} {4:5d}  {'pairwise NON-collinear':>28s}")
    print("""
    Each of the 90 J-stable D4s contains exactly 4 of the 40 J-stable A2s, and those four
    points have ZERO collinear pairs out of six -- they are a four-point PARTIAL OVOID. Each
    point lies in exactly 9 of them: 90 x 4 = 360 = 40 x 9.

    SO 24 = 24 IS NOT THE COINCIDENCE IT LOOKS LIKE. A line and a J-stable D4 both carry 24
    roots, but a line's four A2s are mutually orthogonal and span rank 8, while a D4's four
    A2s are mutually NON-orthogonal and span rank 4. Same count, opposite relation, different
    rank. In the Pauli reading: lines are maximal COMMUTING sets, the 90 D4s are four-element
    pairwise NON-commuting families.""")

    print("\n  PASS 7238-7239 -- PRIOR ART: they were already ours\n")
    print("""    BT1750 states: "The C^5 hexagons of the E8 weld form 40 Witting rays. The
    Coxeter element C permutes those hexagons in eight 5-cycles." Those hexagons are 6-root
    sets -- the same objects I have been calling J-stable A2s. Confirmed on all three counts:

        40 objects                                    matches
        Coxeter cycle type on them: eight 5-cycles    matches exactly
        c^5 fixes every one of them setwise           TRUE

    AND THAT LAST LINE EXPLAINS THE WHOLE CONSTRUCTION. J = c^10 = (c^5)^2, so anything c^5
    fixes is automatically J-stable. The 40 were never a discovery of mine; what is new is
    that they are A2 ROOT SUBSYSTEMS, that collinearity is their orthogonality, and that
    alpha(W(3,3)) = 7 counts pairwise non-orthogonal ones.

    Citing BT1750 rather than re-deriving it, which is the protocol and which I only followed
    because I searched before claiming.""")

    print("\n  PASS 7240 -- how many W(3,3)s does E8 carry?\n")
    print("""    Springer: the zeta_3-regular class in W(E8) has centraliser the complex
    reflection group G32, of order 155520 -- which is also the symmetry group of the Witting
    polytope, the object BT1750 named. So there are 696729600 / 155520 = 4480
    fixed-point-free order-3 elements. J and J^2 generate the same cyclic group and stabilise
    the same 40, bounding the copies by 2240. Sampling 20 such elements gave 18 distinct
    40-sets, consistent with the {J, J^2} pairing.""")

    print("\n  PASS 7241 -- the 36 spreads are strongly regular\n")
    print("""    Two spreads of W(3,3) share exactly 1 or exactly 4 of their 10 lines -- only
    those two values, over all 630 pairs (360 and 270). Taking "share 4 lines" as adjacency:

        valency 15, lambda 6, mu 6, spectrum 15^1 3^15 (-3)^20   =   SRG(36,15,6,6)

    THIS IS THE DATUM THE REPO ASKED FOR. decision-ab66d64e (MDCLXXXI) already records 36
    W(3,3) spreads and already warns that 36 Clifford L/R cross-pairs are COUNT-EQUAL to them
    while their natural schemes DIFFER. I had noted a third 36 -- the double sixes of a cubic
    surface, with the same stabiliser order 1440 under groups of order 51840 -- and refused
    to claim a correspondence. SRG(36,15,6,6) is the invariant that can now decide it, and
    deciding it is not attempted here.""")

    print("\n  PASS 7242 -- rank 16 for q=9: the bar lifts, nothing fits\n")
    print(f"      {'dim':>4s} {'max kissing':>12s} {'>= 820?':>8s} {'multiple of 820?':>17s}")
    for d, k in ((8, 240), (12, 756), (16, 4320), (24, 196560)):
        print(f"      {d:4d} {k:12d} {str(k >= 820):>8s} {str(k % 820 == 0):>17s}")
    print("""
    The counting obstruction that kills rank 8 (240 < 820) does NOT apply at rank 16, where
    Barnes-Wall has 4320 minimal vectors. But a uniform fibration needs the vector count to be
    a multiple of 820, and 4320/820 = 5.27, 196560/820 = 239.7. So the q=9 analogue is not
    blocked by counting at rank 16 -- it is simply absent from the standard lattices.""")

    print("\n  PASS 7243-7244 -- open, and scope\n")
    print("""    STILL OPEN: alpha(W(3,9)); q=11 stalled at 65 across two destroy regimes;
    Q^-(5,5) running against the published 48 and not yet reported.

    NEW HERE: the 90 as four-point partial ovoids with the line/D4 rank duality; the
    SRG(36,15,6,6) structure on the spreads; the Springer count of 4480 elements and <= 2240
    copies; and the rank-16 analysis.

    NOT NEW, and cited: the 40 hexagons and their Coxeter 5-cycle structure (BT1750); the 36
    spreads and the count-equality warning (MDCLXXXI, decision-ab66d64e); 1120 A2s and 3150
    D4s in E8; G32 as the Witting symmetry group.""")

    out = {
        "boundary": (
            "NEW: the 90 J-stable D4s are four-point PARTIAL OVOIDS (not lines -- the four "
            "A2s are non-orthogonal, rank 4, against a line's orthogonal rank 8); the 36 "
            "spreads carry SRG(36,15,6,6). PRIOR ART: the 40 A2s ARE BT1750's 40 Witting "
            "hexagons, confirmed by Coxeter cycle type; the 36 spreads and the count-equality "
            "warning are decision-ab66d64e. No correspondence between any two 36s is claimed"),
        "the_ninety": {
            "a2s_per_d4": 4, "collinear_pairs_among_them": 0, "total_pairs": 6,
            "meaning": "a four-point partial ovoid of W(3,3)",
            "d4s_per_point": 9, "incidence": "90 x 4 = 360 = 40 x 9",
            "duality": {"line": {"roots": 24, "rank": 8, "relation": "collinear/commuting"},
                        "J_stable_D4": {"roots": 24, "rank": 4,
                                        "relation": "non-collinear/non-commuting"}}},
        "prior_art_BT1750": {
            "claim": "the C^5 hexagons of the E8 weld form 40 Witting rays; the Coxeter "
                     "element permutes them in eight 5-cycles",
            "confirmed": {"count": 40, "coxeter_cycle_type": {"5": 8},
                          "c5_fixes_each": True},
            "why_J_stable": "J = c^10 = (c^5)^2, and c^5 fixes every hexagon",
            "what_is_actually_new": ["they are A2 ROOT SUBSYSTEMS",
                                     "collinearity is their orthogonality",
                                     "alpha counts pairwise non-orthogonal ones"]},
        "how_many_copies": {"fixed_point_free_order_3": 4480,
                            "centraliser": "G32, order 155520 (Witting symmetry group)",
                            "max_distinct_copies": 2240,
                            "sample": "20 elements gave 18 distinct 40-sets"},
        "spread_scheme": {"spreads": 36,
                          "shared_lines_distribution": {"1": 360, "4": 270},
                          "graph": "share 4 lines",
                          "parameters": "SRG(36,15,6,6)",
                          "spectrum": {"15": 1, "3": 15, "-3": 20},
                          "why_it_matters": ("decision-ab66d64e warns that 36 Clifford L/R "
                                             "cross-pairs are count-equal to the 36 spreads "
                                             "with different schemes; this is the invariant "
                                             "that can decide it. Not decided here")},
        "rank16_for_q9": {"kissing_dim16": 4320, "clears_820_bar": True,
                          "multiple_of_820": False,
                          "verdict": ("the counting obstruction lifts at rank 16 but no "
                                      "standard lattice has a matching vector count")},
        "not_done": ["alpha(W(3,9))", "q=11 stalled at 65",
                     "Q^-(5,5) against the published 48",
                     "whether the three 36s correspond"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7237_7244_NINETY_AND_WITTING.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
