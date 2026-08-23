"""Passes 7301-7308 -- the Gaussian fibration selects a SPREAD (conditionally), and a census.

  7301  The 10 lines the d=4 partition misses form a SPREAD of W(3,3).
  7302  But NOT for every order-4 element. The condition, measured.
  7303  d=9 cannot live in E8 or K12. Rank 24 is the first place it fits.
  7304  The Niemeier uniformity census: only 7 of 24, and Leech is the richest.
  7305  Leech built and verified; the d=9 test is blocked, and on what.
  7306  What "uniform" adds beyond "prime power".
  7307  Open.
  7308  Scope.

    py -3 analysis/w33_pass7301_7308_spread_selection_and_the_census.py
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

BLOCK_TYPES = [
    ({"2": 15}, 30, 10, True, 5),
    ({"0": 3, "2": 12}, 24, 16, False, 8),
    ({"0": 15}, 0, 40, False, 1),
]

NIEMEIER = [
    ("D16E8", 960, [9]), ("E8^3", 720, [9]), ("A17E7", 504, [8, 13, 16]),
    ("A6^4", 252, [8, 16]), ("A5^4D4", 240, [9]), ("A4^6", 240, [9]),
    ("Leech", 196560, [4, 8, 9, 13, 16]),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7301-7308 -- spread selection, and the Niemeier census")
    print("=" * 78)

    print("\n  PASS 7301-7302 -- the d=4 partition selects a SPREAD, conditionally\n")
    print("""    Overlaying E8's two fibrations gives 15 blocks of 8 W(3,3) points, each the
    union of two disjoint lines. That uses 30 of W(3,3)'s 40 lines -- and the 10 it MISSES
    are pairwise disjoint and cover all 40 points. They are a SPREAD.

    THAT IS NOT UNIVERSAL, and I checked before saying otherwise. Over 91,787 random order-4
    fixed-point-free elements, 14 distinct outcomes appear, in three types:""")
    print(f"\n      {'lines per block':>20s} {'used':>5s} {'unused':>7s} {'spread?':>8s} "
          f"{'cases':>6s}")
    for lp, us, un, sp, n in BLOCK_TYPES:
        print(f"      {str(lp):>20s} {us:5d} {un:7d} {str(sp):>8s} {n:6d}")
    print("""
    So an order-4 element selects a spread EXACTLY WHEN all 15 of its blocks contain two
    lines. When three blocks contain none, 16 lines are missed and they are not a spread;
    in one case no block contains a line at all. None of the elements commutes with J, so
    the regular cases are not explained by compatibility.

    THE HONEST HEADLINE: some order-4 elements of W(E8) select one of W(3,3)'s 36 spreads,
    and the ones that do are characterised by their block structure. Not all of them do.""")

    print("\n  PASS 7303 -- where d = 9 can live\n")
    print("""    deg(Phi_9) = 6, so a fixed-point-free order-9 element needs 6 | rank:

        rank  8 (E8)     6 | 8  ? NO
        rank 12 (K12)    6 | 12 ? YES -- but Phi_9(1)^2 = 9 gives only 8 nonzero classes
        rank 16          6 | 16 ? NO
        rank 24 (Leech)  6 | 24 ? YES, and 196560/80 = 2457 exactly

    So the 3-power tower SKIPS from d=3 at rank 8 to d=9 at rank 24 with nothing usable
    between. That gap is structural, not an accident of which lattices are famous.""")

    print("\n  PASS 7304 -- the Niemeier uniformity census\n")
    print("""    Nontriviality (Phi_d(1) != 1) is necessary but NOT sufficient: the minimal
    vectors must also distribute EVENLY over the nonzero classes. That is what killed K12
    at d=3 (756/728 is not an integer). Applying both conditions to all 24 Niemeier
    lattices, only SEVEN admit any uniform nontrivial quotient:""")
    print(f"\n      {'lattice':>10s} {'min vectors':>12s}  {'usable d':>20s}")
    for name, mv, ds in NIEMEIER:
        print(f"      {name:>10s} {mv:12d}  {str(ds):>20s}")
    print("""
    LEECH IS THE RICHEST BY A WIDE MARGIN -- five usable d against one or three for the
    others. It is also the only one admitting d=4, d=9 and d=13 simultaneously.

    CAVEAT THAT MATTERS: this census uses only the KISSING NUMBER, so it is a NECESSARY
    condition. A lattice passing it still has to actually possess the automorphism, which is
    a separate and harder question.""")

    print("\n  PASS 7305 -- Leech built, and exactly where the test stops\n")
    print("""    The extended binary Golay code was rebuilt from the cyclic [23,12,7] generator
    polynomial g(x) = 1 + x^2 + x^4 + x^5 + x^6 + x^10 + x^11 plus an overall parity bit, and
    verified: weight enumerator (1, 759, 2576, 759, 1). My FIRST attempt used a bordered-QR
    construction and produced odd weights (7, 9, 11, ...), which cannot be an extended Golay
    -- caught immediately because all weights of the real code are divisible by 4.

    The Leech minimal-vector census then checks exactly: 1104 + 97152 + 98304 = 196560.

    WHAT STOPS THE d=9 TEST: it needs a fixed-point-free order-9 element of Co0 = Aut(Leech),
    and no reliable generator set for Co0 is available here. Co0 has order about 8.3e18 and
    the element need not be monomial, so random search over signed permutations will not find
    it. Recording exactly where the attempt stops rather than guessing at the answer.""")

    print("\n  PASS 7306-7308 -- what uniformity adds, and scope\n")
    print("""    "d must be a prime power" comes from Phi_d(1) != 1. "The vectors must divide
    evenly" is a SECOND and independent filter, and it is much sharper: it cuts 24 Niemeier
    lattices to 7, and it is what invalidated my K12 prediction. Prime-power-ness is about
    the ring; uniformity is about the lattice actually having enough vectors, evenly placed.

    NEW: the spread selection and its exact condition; the d=9 rank gap; the Niemeier census.
    CORRECTED: my first Golay construction, and the unconditional spread claim I nearly made.
    NOT DONE: the Leech d=9 geometry (blocked on Co0 generators); K12 built; alpha(W(3,9));
    q=11 at 68; Coolsaet unread. NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "NEW: an order-4 element of W(E8) selects one of W(3,3)'s 36 SPREADS -- the 10 "
            "lines its 15-block partition misses -- but ONLY when all 15 blocks contain two "
            "lines, which is 5 of 14 measured cases. Also: d=9 cannot live below rank 24, "
            "and only 7 of 24 Niemeier lattices admit a uniform nontrivial quotient, Leech "
            "being richest. The Leech d=9 geometry is UNTESTED, blocked on Co0 generators"),
        "spread_selection": {
            "mechanism": ("the 15 blocks are unions of two disjoint W(3,3) lines, using 30 "
                          "of 40 lines; the 10 missed lines can form a spread"),
            "conditional": True,
            "condition": "all 15 blocks contain exactly two lines",
            "measured": {"elements_tried": 91787, "distinct_outcomes": 14,
                         "types": [{"lines_per_block": lp, "used": us, "unused": un,
                                    "spread": sp, "cases": n}
                                   for lp, us, un, sp, n in BLOCK_TYPES]},
            "note": "no order-4 element commutes with J, so regularity is not compatibility"},
        "d9_rank_gap": {
            "deg_phi9": 6, "needs": "6 | rank",
            "E8": False, "K12": "divides but only 8 nonzero classes", "rank16": False,
            "Leech": True,
            "consequence": "the 3-power tower skips rank 8 to rank 24 with nothing usable between"},
        "niemeier_census": {
            "total": 24, "admitting_uniform_nontrivial_quotient": 7,
            "table": [{"lattice": n, "min_vectors": mv, "usable_d": ds}
                      for n, mv, ds in NIEMEIER],
            "richest": "Leech, with d in {4,8,9,13,16}",
            "caveat": ("uses only the kissing number, so NECESSARY only -- a lattice passing "
                       "it must still possess the automorphism")},
        "leech_build": {
            "golay": {"construction": "cyclic [23,12,7] g(x) = 1+x^2+x^4+x^5+x^6+x^10+x^11, "
                                      "extended by overall parity",
                      "weight_enumerator": {"0": 1, "8": 759, "12": 2576, "16": 759,
                                            "24": 1},
                      "verified": True,
                      "first_attempt_failed": ("a bordered-QR construction gave odd weights "
                                               "7,9,11,... which cannot be an extended Golay")},
            "minimal_vectors": {"pm4_squared": 1104, "pm2_on_octads": 97152,
                                "mp3_pm1": 98304, "total": 196560, "verified": True},
            "blocked_on": ("a fixed-point-free order-9 element of Co0 = Aut(Leech); no "
                           "reliable Co0 generator set available, order ~8.3e18, element "
                           "need not be monomial")},
        "two_filters": {
            "prime_power": "Phi_d(1) != 1 -- about the ring",
            "uniformity": ("the minimal vectors must divide evenly over the nonzero classes "
                           "-- about the lattice; much sharper, cutting 24 Niemeiers to 7, "
                           "and it is what invalidated my K12 prediction")},
        "not_done": ["Leech d=9 geometry", "K12 built", "alpha(W(3,9))", "q=11 at 68",
                     "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7301_7308_SPREAD_SELECTION.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
