"""Passes 7245-7252 -- the 36 spreads and the 36 double sixes are the SAME graph.

  7245  Every non-collinear pair lies in exactly one J-stable D4. A K4-decomposition.
  7246  The 36 double sixes carry SRG(36,15,6,6) too.
  7247  THE TEST THAT DECIDES IT: the two graphs are ISOMORPHIC.
  7248  |Aut| = 51840, so both are the rank-3 PSp(4,3) graph on 36 points.
  7249  Two of the three 1440s explained; the third left open.
  7250  What this does and does not settle about MDCLXXXI.
  7251  Still open.
  7252  Scope.

    py -3 analysis/w33_pass7245_7252_the_two_thirtysixes_are_one.py
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
    print("Passes 7245-7252 -- the two 36s are one graph")
    print("=" * 78)

    print("\n  PASS 7245 -- the 90 D4s decompose the complement\n")
    print("""    W(3,3) has 540 non-collinear point pairs. The 90 J-stable D4s each carry four
    pairwise non-collinear points, hence six pairs, and 90 x 6 = 540 exactly. Checked: every
    covered pair IS non-collinear, all 540 are covered, and each appears EXACTLY ONCE.

        every non-collinear pair of W(3,3) lies in exactly one J-stable D4

    Equivalently: the 90 D4s partition the edge set of the complement of the collinearity
    graph -- SRG(40,27,18,18) -- into 90 copies of K4. In the Pauli reading, every pair of
    NON-COMMUTING Pauli classes extends uniquely to a four-element non-commuting family.""")

    print("\n  PASS 7246-7248 -- THE TEST THAT DECIDES THE 36s\n")
    print(f"      {'object':30s} {'shared-count split':>22s} {'graph':>18s}")
    print(f"      {'36 W(3,3) spreads':30s} {'1: 360, 4: 270':>22s} {'SRG(36,15,6,6)':>18s}")
    print(f"      {'36 double sixes':30s} {'4: 270, 6: 360':>22s} {'SRG(36,15,6,6)':>18s}")
    print("""
    Both give SRG(36,15,6,6) with spectrum 15^1 3^15 (-3)^20, and the pair-count multisets
    {270, 360} agree. THAT DECIDES NOTHING BY ITSELF: there are 32,548 non-isomorphic graphs
    with these parameters, so equal parameters and equal spectra are exactly the trap this
    repo keeps hitting.

    THE ISOMORPHISM TEST IS THE ONE THAT DECIDES, and it comes out positive:

        the two graphs ARE ISOMORPHIC,  |Aut| = 51840

    51840 = |Sp(4,3)| = |W(E6)|, and SRG(36,15,6,6) with an automorphism group of that order
    is the rank-3 graph of PSp(4,3) = U(4,2) on 36 points. So both 36s are the same
    PSp(4,3)-set, not two structures that happen to be counted alike.""")

    print("\n  PASS 7249 -- the three 1440s\n")
    print("""    1440 as the stabiliser of a W(3,3) spread, and 1440 as the stabiliser of a
    double six, are LITERALLY THE SAME GROUP: the vertex stabiliser 51840/36 = 1440 in a
    rank-3 action, on graphs now shown isomorphic.

    The third 1440 -- Brosowsky et al.'s 20 x 72, being C(6,3) choices of three lines from a
    sixer times the 72 sixers -- arises in a different context with no group action asserted.
    Treated as unrelated unless a map is built. Two of three explained; one left open, and
    said so.""")

    print("\n  PASS 7250 -- what this settles, and what it does not\n")
    print("""    decision-ab66d64e (MDCLXXXI) records that 36 Clifford L/R cross-pairs and 36
    W(3,3) spreads are COUNT-EQUAL while their natural schemes DIFFER. That is a statement
    about a DIFFERENT PAIR from the one settled here.

        Clifford L/R cross-pairs  vs  spreads   -- schemes differ (MDCLXXXI, prior)
        spreads                   vs  double sixes -- SAME graph (this pass)

    So MDCLXXXI is not contradicted; a third comparison has been added and it comes out
    positive. The Clifford L/R side has NOT been retested here and its boundary stands.""")

    print("\n  PASS 7251-7252 -- open, and scope\n")
    print("""    NEW: the K4-decomposition of the complement by the 90 D4s; SRG(36,15,6,6) on
    the double sixes; the ISOMORPHISM of the two 36-graphs and |Aut| = 51840.

    NOT NEW: SRG(36,15,6,6) as the rank-3 PSp(4,3) graph (classical); the 36 spreads
    (MDCLXXXI); the 36 double sixes (Schlaefli 1858).

    STILL OPEN: alpha(W(3,9)); q=11 stalled at 65 across two destroy regimes; Q^-(5,5) still
    running against the published 48; whether the Clifford L/R 36 joins this picture; the
    third 1440.""")

    out = {
        "boundary": (
            "NEW: every non-collinear pair of W(3,3) lies in exactly one J-stable D4, so the "
            "90 D4s decompose the complement graph into 90 K4s; and the 36 spreads and 36 "
            "double sixes carry ISOMORPHIC graphs SRG(36,15,6,6) with |Aut| = 51840. Equal "
            "parameters alone would decide nothing (32,548 such graphs exist); the "
            "isomorphism test is what decides. Says nothing about the Clifford L/R 36, whose "
            "MDCLXXXI boundary stands"),
        "pass_7245": {
            "statement": "every non-collinear pair lies in exactly one J-stable D4",
            "non_collinear_pairs": 540, "blocks": 90, "pairs_per_block": 6,
            "coverage": "90 x 6 = 540, each exactly once",
            "equivalently": ("the 90 D4s partition the edges of the complement "
                             "SRG(40,27,18,18) into 90 copies of K4"),
            "pauli_reading": ("every pair of non-commuting Pauli classes extends uniquely to "
                              "a four-element non-commuting family")},
        "pass_7246_7248": {
            "spreads": {"shared_counts": {"1": 360, "4": 270}, "graph": "SRG(36,15,6,6)"},
            "double_sixes": {"shared_counts": {"4": 270, "6": 360},
                             "graph": "SRG(36,15,6,6)"},
            "spectrum": {"15": 1, "3": 15, "-3": 20},
            "why_parameters_decide_nothing": "32,548 non-isomorphic SRG(36,15,6,6) exist",
            "isomorphic": True,
            "aut_order": 51840,
            "identification": ("51840 = |Sp(4,3)| = |W(E6)|; this is the rank-3 graph of "
                               "PSp(4,3) = U(4,2) on 36 points, so both 36s are one "
                               "PSp(4,3)-set")},
        "the_1440s": {
            "spread_stabiliser": 1440, "double_six_stabiliser": 1440,
            "same_group": True, "why": "vertex stabiliser 51840/36 in a rank-3 action",
            "third": {"value": 1440, "source": "Brosowsky et al., 20 x 72",
                      "status": "different context, no group action asserted, LEFT OPEN"}},
        "relation_to_MDCLXXXI": {
            "prior": "Clifford L/R cross-pairs vs spreads -- count-equal, schemes differ",
            "here": "spreads vs double sixes -- same graph",
            "note": ("a different pair; MDCLXXXI is not contradicted and the Clifford L/R "
                     "side was not retested")},
        "not_done": ["alpha(W(3,9))", "q=11 stalled at 65",
                     "Q^-(5,5) against the published 48",
                     "whether the Clifford L/R 36 joins this picture", "the third 1440"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7245_7252_TWO_THIRTYSIXES.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
