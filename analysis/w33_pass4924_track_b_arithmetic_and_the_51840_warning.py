#!/usr/bin/env python3
"""Pass 4924 -- Track B's dual-shell arithmetic checks out, and their item 3 is testing a
group two geometries share.

Track B's latest packet reports that the [2025,399,14]_2 code intrinsically reconstructs the
router: 2,025 columns falling into 405 four-element classes and 135 three-element classes,
a weight-two dual shell of 2,835 words spanning dimension 1,485, and a quotient
[540, 141, 4] whose 135 minimum words have block profile (4,4,4,3) and partition all 540
coordinates exactly once.

Every one of those numbers is determined by the two class counts, so the internal
consistency is checkable without reconstructing the code -- and a packet whose arithmetic
does not close is worth knowing about before anyone builds on it.

Separately, their open item 3 asks whether the design's automorphism group is exactly
PGSp(4,3) of order 51,840, and treats a positive answer as a purely coding-theoretic
reconstruction of the router symmetry.  Pass 4727 and Pass 4735 in this lane say that
inference needs care.

    py -3 analysis/w33_pass4924_track_b_arithmetic_and_the_51840_warning.py
"""

from __future__ import annotations

import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

COLD, COLD_SIZE = 405, 4          # K_{2,2} blocks
HOT, HOT_SIZE = 135, 3            # Petersen-hot triples

CLAIMED = {
    "columns": 2025,
    "weight_two_dual_words": 2835,
    "repetition_span_dim": 1485,
    "quotient_length": 540,
    "min_words": 135,
    "levi_edges_of_gq42": 135,
}


def main() -> int:
    print("=" * 78)
    print("Pass 4924 -- does Track B's dual-shell arithmetic close?")
    print("=" * 78)

    derived = {
        "columns": COLD * COLD_SIZE + HOT * HOT_SIZE,
        "weight_two_dual_words": COLD * comb(COLD_SIZE, 2) + HOT * comb(HOT_SIZE, 2),
        # a length-m repetition block contributes m-1 independent weight-two relations
        "repetition_span_dim": COLD * (COLD_SIZE - 1) + HOT * (HOT_SIZE - 1),
        "quotient_length": COLD + HOT,
        "min_words": HOT,
        "levi_edges_of_gq42": HOT,
    }

    print(f"\n  {'quantity':26s} {'Track B':>10s} {'derived here':>13s} {'agree':>7s}")
    rows, ok = [], True
    for k, v in CLAIMED.items():
        d = derived[k]
        a = v == d
        ok &= a
        rows.append({"quantity": k, "track_b": v, "derived": d, "agree": bool(a)})
        print(f"  {k:26s} {v:>10,d} {d:>13,d} {str(a):>7s}")

    # the (4,4,4,3) partition: 135 relations x 3 cold + 1 hot each
    cold_used = CLAIMED["min_words"] * 3
    hot_used = CLAIMED["min_words"] * 1
    partition = (cold_used == COLD and hot_used == HOT)
    print(f"\n    (4,4,4,3) profile uses 3 cold + 1 hot per relation")
    print(f"      135 x 3 cold = {cold_used}  vs {COLD} cold blocks   {cold_used == COLD}")
    print(f"      135 x 1 hot  = {hot_used}  vs {HOT} hot blocks    {hot_used == HOT}")
    print(f"      partitions all {COLD+HOT} quotient coordinates exactly once: {partition}")

    print(f"""
    {'THE ARITHMETIC CLOSES COMPLETELY.' if ok and partition else 'SOMETHING DOES NOT CLOSE -- READ THE ROWS.'} Every reported figure follows from the two class
    counts alone: 2,025 columns, 2,835 weight-two dual words, a repetition span of 1,485
    (each length-m block giving m-1 independent relations), a quotient of length 540, and a
    (4,4,4,3) profile that uses each cold block three times and each hot block once.

    THIS IS CONSISTENCY, NOT VERIFICATION, and the distinction is the whole point. It shows
    the packet's numbers are mutually compatible; it does NOT show that the code has 405
    four-classes and 135 three-classes, which is the claim doing the work. That needs their
    generator matrix, which this lane does not have.

    ONE INDEPENDENT ANCHOR DOES EXIST. Their 135 is the number of Levi edges of GQ(4,2),
    which Pass 4824 computed here from a Hermitian construction over GF(4) sharing nothing
    with their code, and which agreed along with five other invariants. So the 135 is
    cross-verified even though the classification producing it is not.""")

    print("\n  Their open item 3, and a warning this lane can supply\n")
    print("""    They ask whether the intrinsic design's automorphism group is exactly PGSp(4,3),
    order 51,840, and read a positive answer as a coding-theoretic reconstruction of the
    router symmetry.

    THAT INFERENCE NEEDS A QUALIFIER. Pass 4727 computed |Aut(H(3,4))| = 51,840, and the
    reason is the exceptional isomorphism PSU(4,2) = PSp(4,3): H(3,4) is Hermitian over
    GF(4) with a unitary group, W(3,3) is symplectic over GF(3), and the two simple groups
    coincide at order 25,920. Both geometries have the group independently.

    Since their design is built on GQ(4,2) = H(3,4), an automorphism group of order 51,840
    is what H(3,4) has ANYWAY. Landing on it would confirm the design retains the symmetry
    of the geometry it was built from -- which is worth knowing -- but would not be evidence
    of contact with W(3,3), and the phrase "the full router symmetry" invites that reading.

    Pass 4735 measured the hazard: 56% of this corpus's 1,733 sightings of 51,840 do not say
    which of the several order-51,840 objects they mean.""")

    out = {
        "boundary": ("this checks INTERNAL CONSISTENCY of Track B's reported figures against "
                     "the two class counts they report. It does NOT reconstruct their code "
                     "or verify the classification into 405 four-classes and 135 "
                     "three-classes, which is the load-bearing claim. The only independently "
                     "anchored figure is 135 = Levi edges of GQ(4,2), computed at Pass 4824"),
        "comparison": rows,
        "arithmetic_closes": bool(ok),
        "profile_partitions": bool(partition),
        "independently_anchored": ["135 = Levi edges of GQ(4,2), Pass 4824"],
        "warning_on_item_3": (
            "|Aut(H(3,4))| = 51,840 already, by the exceptional isomorphism "
            "PSU(4,2) = PSp(4,3). A design built on GQ(4,2) landing on that order shows it "
            "retains the geometry's symmetry, not that it reconstructs W(3,3)'s"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4924_TRACK_B_ARITHMETIC.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
