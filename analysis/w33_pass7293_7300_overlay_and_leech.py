"""Passes 7293-7300 -- the two E8 fibrations overlaid, and where the arithmetic points next.

  7293  The classification runs on ANY rank. The whole tower, mapped before climbing.
  7294  LEECH at d=9 gives 40 points -- the same target as E8 at d=3. Untested.
  7295  A correction to my own K12 prediction: the quotient is NOT uniform.
  7296  Overlaying the two E8 fibrations: a regular 40 x 15 incidence.
  7297  The 15 blocks are unions of two disjoint W(3,3) LINES.
  7298  Why q must be a prime power, from two directions, and why that is one fact.
  7299  What is still open.
  7300  Scope.

    py -3 analysis/w33_pass7293_7300_overlay_and_leech.py
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

TOWER = [
    ("E8", 8, 240, 3, 81, 80, 3, 40, "W(3,3)  VERIFIED"),
    ("E8", 8, 240, 4, 16, 15, 16, 15, "W(3,2)  VERIFIED"),
    ("E8", 8, 240, 5, 25, 24, 10, 6, "PG(1,5), a line"),
    ("K12", 12, 756, 4, 64, 63, 12, 63, "untested"),
    ("Leech", 24, 196560, 4, 4096, 4095, 48, 4095, "all of PG(11,2), untested"),
    ("Leech", 24, 196560, 9, 81, 80, 2457, 40, "SAME TARGET AS E8 d=3, untested"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7293-7300 -- the overlay, and where the arithmetic points")
    print("=" * 78)

    print("\n  PASS 7293-7294 -- the tower, mapped by arithmetic alone\n")
    print("""    det(I-M) = Phi_d(1)^k with k = rank/deg(Phi_d), and Phi_d(1) = p iff d = p^m.
    That needs no lattice, so the whole tower can be mapped before any of it is built.
    Keeping only the rows where the quotient is nontrivial AND the minimal vectors
    distribute uniformly over the nonzero classes:""")
    print(f"\n      {'lattice':>7s} {'rank':>5s} {'d':>3s} {'|quot|':>7s} {'nonzero':>8s} "
          f"{'vecs/class':>11s} {'proj pts':>9s}  {'status':>26s}")
    for lat, n, mv, d, q, nz, vc, pp, st in TOWER:
        print(f"      {lat:>7s} {n:5d} {d:3d} {q:7d} {nz:8d} {vc:11d} {pp:9d}  {st:>26s}")
    print("""
    THE LEECH d=9 ROW IS THE ONE TO LOOK AT. deg(Phi_9) = 6, so the Leech lattice is rank 4
    over Z[zeta_9]; Phi_9(1) = 3, so the quotient is F_3^4 with 80 nonzero classes and 40
    projective points -- the SAME target as E8 at d=3 -- and 196560/80 = 2457 exactly, so the
    fibration is uniform.

    Since 9 = 3^2, that is the second rung of the 3-power tower: d=3 on E8, d=9 on Leech,
    both landing on PG(3,3). Whether Leech actually yields W(3,3) is UNTESTED, and the
    Leech lattice is not built here.""")

    print("\n  PASS 7295 -- correcting my own K12 prediction\n")
    print("""    I predicted the K12 Eisenstein quotient would give 126 points carrying
    SRG(126,45,12,18). That rested on a conflation. K12 at d=3 gives F_3^6 = 729 with 728
    nonzero classes, and 756/728 is NOT an integer -- so the quotient is not uniform and
    most classes carry no minimal vector at all. My "126" was 756/6 = the number of UNIT
    ORBITS on minimal vectors, which is a different count from quotient classes.

    The 126 and the U(4,3) rank-3 action on 126 points may still be related, but the
    argument I gave for it does not hold, and the prediction is weaker than I stated.""")

    print("\n  PASS 7296-7297 -- overlaying the two E8 fibrations\n")
    print(f"      {'quantity':44s} {'value':>8s}")
    for k, v in (("grid cells (40 W(3,3) points x 15 d=4 classes)", 600),
                 ("cells actually occupied", 120),
                 ("roots in every occupied cell", 2),
                 ("d=4 classes met by each W(3,3) point", 3),
                 ("W(3,3) points met by each d=4 class", 8),
                 ("flags: 40 x 3 = 15 x 8", 120)):
        print(f"      {k:44s} {v:8d}")
    print("""
    PERFECTLY REGULAR -- and J and M do NOT commute, so that regularity is not forced by
    the elements being compatible. The incidence is a 1-design: 15 blocks of size 8 on
    W(3,3)'s 40 points with replication 3.

    AND THE BLOCKS ARE NOT ARBITRARY. Since alpha(W(3,3)) = 7, an 8-set cannot be a partial
    ovoid, so the blocks must carry collinearity -- and they do, in the most structured way
    available: EVERY block is the union of exactly TWO disjoint W(3,3) LINES, covering all 8
    of its points. Each block has 16 collinear pairs, 12 inside the two lines and 4 across
    them. Block pairs meet in 0 points (45 pairs) or 2 points (60 pairs).

    So the Gaussian fibration, read through the Eisenstein one, is a set of 15 line-pairs of
    W(3,3). That is the only place the two fibrations of E8 touch.""")

    print("\n  PASS 7298 -- why q must be a prime power, and why that is one fact\n")
    print("""    Finite geometry says PG(n,q) exists only for q a prime power, because F_q does.
    This construction says the quotient is nontrivial only when Phi_d(1) != 1, i.e. only when
    d is a prime power. Two different necessities landing on the same condition.

    IT IS NOT TWO INDEPENDENT FACTS. Both are the statement that Phi_d has a repeated root
    mod p exactly when d is a p-power -- one fact wearing two hats. Recording it because the
    coincidence LOOKS like a derivation of "why prime powers" and is not one, and this repo
    has a documented history of promoting exactly that kind of look-alike.""")

    print("\n  PASS 7299-7300 -- open, and scope\n")
    print("""    NEW: the rank-general classification and the tower map; the Leech d=9 row; the
    40 x 15 overlay and its identification as 15 line-pairs.

    CORRECTED: my K12 prediction, which conflated unit orbits with quotient classes.

    NOT DONE: K12 built (the Construction-A route is proved impossible); Leech built;
    whether Leech d=9 gives W(3,3); alpha(W(3,9)); q=11 finished at 68; Coolsaet unread.

    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "NEW: the classification det(I-M) = Phi_d(1)^k is rank-general, so the whole "
            "lattice tower maps by arithmetic; LEECH at d=9 gives 40 projective points "
            "uniformly, the same target as E8 at d=3, UNTESTED; and overlaying E8's two "
            "fibrations gives a regular 40x15 1-design whose 15 blocks are each a union of "
            "two disjoint W(3,3) lines. CORRECTED: my K12 prediction conflated unit orbits "
            "with quotient classes"),
        "tower_map": [{"lattice": lat, "rank": n, "min_vectors": mv, "d": d, "quotient": q,
                       "nonzero": nz, "vectors_per_class": vc, "projective_points": pp,
                       "status": st}
                      for lat, n, mv, d, q, nz, vc, pp, st in TOWER],
        "leech_d9": {"deg_phi9": 6, "rank_over_zeta9": 4, "phi9_of_1": 3,
                     "quotient": "F_3^4", "projective_points": 40,
                     "vectors_per_class": 2457, "uniform": True,
                     "note": ("same target as E8 at d=3; 9 = 3^2 makes this the second rung "
                              "of the 3-power tower"),
                     "status": "UNTESTED, Leech not built"},
        "k12_correction": {
            "what_i_predicted": "126 points carrying SRG(126,45,12,18)",
            "the_conflation": ("756/6 = 126 counts UNIT ORBITS on minimal vectors, not "
                               "quotient classes"),
            "the_fact": ("K12 at d=3 gives F_3^6 with 728 nonzero classes and 756/728 is not "
                         "an integer, so the quotient is NOT uniform"),
            "status": "prediction weaker than stated; the argument for it does not hold"},
        "overlay": {
            "grid": "40 W(3,3) points x 15 d=4 classes = 600 cells",
            "occupied": 120, "roots_per_occupied_cell": 2,
            "degrees": {"per_W33_point": 3, "per_d4_class": 8},
            "flags": 120,
            "elements_commute": False,
            "blocks": {"count": 15, "size": 8,
                       "structure": "each is a union of exactly TWO disjoint W(3,3) lines",
                       "collinear_pairs_inside": 16,
                       "breakdown": "12 within the two lines, 4 across",
                       "pair_intersections": {"0": 45, "2": 60}}},
        "prime_power_observation": {
            "geometry_side": "PG(n,q) needs q a prime power because F_q does",
            "lattice_side": "the quotient is nontrivial only when Phi_d(1) != 1, i.e. d = p^m",
            "verdict": ("NOT two independent facts -- both are 'Phi_d has a repeated root "
                        "mod p iff d is a p-power'. One fact, two hats. It looks like a "
                        "derivation of 'why prime powers' and is not one")},
        "not_done": ["K12 built (Construction A proved impossible)", "Leech built",
                     "whether Leech d=9 gives W(3,3)", "alpha(W(3,9))", "q=11 at 68",
                     "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7293_7300_OVERLAY_AND_LEECH.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
