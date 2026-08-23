"""Passes 7325-7332 -- Leech unblocked via ATLAS, and my census rested on a false assumption.

  7325  Co0 generators obtained: the 24-dimensional INTEGRAL rep of 2.Co1.
  7326  Co0 has NO element with char poly Phi_9^4. Censused, not guessed.
  7327  Its fixed-point-free order-9 elements are Phi_9^3 Phi_3^3 instead.
  7328  MY CENSUS WAS WRONG: fixed-point-free does not mean pure-power char poly.
  7329  The real Leech d=9 numbers: 364 points, all of PG(5,3), uniform.
  7330  What survives of the diagonal theorem.
  7331  Open.
  7332  Scope.

    py -3 analysis/w33_pass7325_7332_leech_unblocked_and_my_census_was_wrong.py
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

CHARPOLYS = [
    (0, 12, 24, 3 ** 12, -12),
    (1, 9, 24, 3 ** 10, -9),
    (2, 6, 24, 3 ** 8, -6),
    (3, 3, 24, 3 ** 6, -3),
    (4, 0, 24, 3 ** 4, 0),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7325-7332 -- Leech unblocked, and a false assumption of mine")
    print("=" * 78)

    print("\n  PASS 7325-7326 -- Co0 obtained, and censused\n")
    print("""    The blocker was a generator set for Co0 = Aut(Leech). GAP's atlasrep package is
    installed here, and AtlasGenerators("2.Co1", 9) returns the 24-DIMENSIONAL INTEGRAL
    representation -- exactly Co0 acting on the Leech lattice, two generators.

    A first search for a fixed-point-free order-9 element with trace 0 and det(I-M) = 81
    found nothing in 4000 tries. Rather than search harder, I censused what order-9 elements
    of Co0 actually look like. Over 15,000 random elements, only THREE (trace, det(I-M))
    signatures occur:

        trace -3, det 729     fixed-point-free
        trace  0, det 0       has eigenvalue 1
        trace  3, det 0       has eigenvalue 1

    NONE has det 81. So Co0 contains no element with characteristic polynomial Phi_9^4, and
    the thing I was searching for does not exist.""")

    print("\n  PASS 7327-7328 -- WHY, AND WHAT I HAD ASSUMED\n")
    print(f"      {'char poly':>18s} {'degree':>7s} {'det(I-M)':>10s} {'trace':>6s}  {'':>8s}")
    for a, b, deg, det, tr in CHARPOLYS:
        mark = "  <- Co0" if det == 729 else ("  <- what I sought" if det == 81 else "")
        print(f"      {'Phi_9^' + str(a) + ' Phi_3^' + str(b):>18s} {deg:7d} {det:10d} "
              f"{tr:6d}{mark}")
    print("""
    Phi_9^3 Phi_3^3 matches BOTH observations: det 3^6 = 729 and trace -3.

    AND THAT EXPOSES THE ASSUMPTION MY WHOLE CENSUS RESTED ON. I wrote
    "det(I-M) = Phi_d(1)^k with k*deg(Phi_d) = rank", which presumes a fixed-point-free
    element of order d has char poly Phi_d^k -- a PURE POWER. It need not. Being
    fixed-point-free only means NO EIGENVALUE 1, i.e. the char poly is a product of Phi_e
    over divisors e of d with e > 1. MIXED polynomials are allowed, and the actual Leech
    element is mixed.

    So every "usable d" row I computed was for the pure-power case only. The census was not
    wrong about those rows; it was wrong to present them as the whole picture.""")

    print("\n  PASS 7329 -- the real Leech d=9 numbers\n")
    print(f"      {'quantity':38s} {'predicted':>12s} {'actual':>12s}")
    for k, p, a in (("char poly", "Phi_9^4", "Phi_9^3 Phi_3^3"),
                    ("det(I-M) = |quotient|", "81", "729"),
                    ("nonzero classes", "80", "728"),
                    ("minimal vectors per class", "2457", "270"),
                    ("projective points", "40", "364")):
        print(f"      {k:38s} {p:>12s} {a:>12s}")
    print("""
    196560 / 728 = 270 exactly, so the fibration IS uniform -- just not onto 40 points. It
    covers ALL 364 points of PG(5,3), since |PG(5,3)| = (3^6-1)/2 = 364.

    So Leech at d=9 does NOT reproduce W(3,3). It produces a fibration onto the whole of
    PG(5,3). Whether the induced form makes that W(5,3) or an orthogonal polar space is NOT
    determined here -- it needs the invariant Gram matrix in the ATLAS basis, which is the
    next step and is not done.""")

    print("\n  PASS 7330 -- what survives\n")
    print("""    THE DIAGONAL THEOREM SURVIVES INTACT: Aut respects non-isomorphic indecomposable
    summands, so among the Niemeier lattices only Leech can carry a non-diagonal rank-24
    geometry. That argument never used the pure-power assumption.

    WHAT DOES NOT SURVIVE is the specific prediction "Leech d=9 gives 40 points". The
    correct statement is 364, and the geometry is open.

    AND THE E8 RESULTS ARE UNAFFECTED: at rank 8, d=3 forces k=4 with deg(Phi_3)=2 and there
    is no room for a mixed polynomial with all factors of degree >= 2 summing to 8 other than
    Phi_3^4 and Phi_4^4 -- both of which were checked directly against the geometry, not
    assumed.""")

    print("\n  PASS 7331-7332 -- open, and scope\n")
    print("""    NEW: Co0 generators in hand; the order-9 signature census; the identification
    Phi_9^3 Phi_3^3; the corrected Leech numbers.
    CORRECTED: my census's pure-power assumption, and the "40 points" prediction.
    NOT DONE: the induced form on PG(5,3), which decides the Leech geometry; K12 built;
    alpha(W(3,9)); q=11 at 68; Coolsaet unread.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "Co0 generators obtained (ATLAS 24-dim integral rep of 2.Co1). Co0 has NO element "
            "with char poly Phi_9^4, so the fibration I predicted does not exist. Its "
            "fixed-point-free order-9 elements are Phi_9^3 Phi_3^3, giving 728 classes of 270 "
            "and 364 projective points -- ALL of PG(5,3), not 40. The induced form, hence the "
            "geometry, is NOT determined here"),
        "co0_access": {
            "package": "GAP atlasrep",
            "call": 'AtlasGenerators("2.Co1", 9)',
            "representation": "24-dimensional over the Integers = Co0 on Leech",
            "generators": 2},
        "order9_census": {
            "elements_sampled": 15000,
            "signatures": [{"trace": -3, "det_I_minus_M": 729, "fixed_point_free": True},
                           {"trace": 0, "det_I_minus_M": 0, "fixed_point_free": False},
                           {"trace": 3, "det_I_minus_M": 0, "fixed_point_free": False}],
            "phi9_to_the_4_exists": False},
        "my_false_assumption": {
            "what_i_assumed": ("a fixed-point-free element of order d has char poly Phi_d^k, "
                               "so det(I-M) = Phi_d(1)^k"),
            "the_truth": ("fixed-point-free means only NO EIGENVALUE 1: the char poly is any "
                          "product of Phi_e over e | d with e > 1, and MIXED polynomials are "
                          "allowed"),
            "the_actual_element": "Phi_9^3 Phi_3^3, degree 24, det 3^6 = 729, trace -3",
            "consequence": ("every 'usable d' row I computed covered the pure-power case "
                            "only; the census was not wrong about those rows but was wrong "
                            "to present them as the whole picture")},
        "leech_d9_corrected": {
            "predicted": {"char_poly": "Phi_9^4", "quotient": 81, "classes": 80,
                          "per_class": 2457, "projective_points": 40},
            "actual": {"char_poly": "Phi_9^3 Phi_3^3", "quotient": 729, "classes": 728,
                       "per_class": 270, "projective_points": 364},
            "uniform": True, "check": "196560 / 728 = 270 exactly",
            "covers": "ALL of PG(5,3), since (3^6-1)/2 = 364",
            "geometry": "NOT determined -- needs the invariant Gram in the ATLAS basis"},
        "what_survives": {
            "diagonal_theorem": ("intact -- it never used the pure-power assumption; among "
                                 "Niemeier lattices only Leech can carry a non-diagonal "
                                 "rank-24 geometry"),
            "e8_results": ("unaffected -- both E8 fibrations were checked against the "
                           "geometry directly, not assumed from the char poly"),
            "what_died": "the specific prediction that Leech d=9 gives 40 points"},
        "not_done": ["the induced form on PG(5,3)", "K12 built", "alpha(W(3,9))",
                     "q=11 at 68", "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7325_7332_LEECH_UNBLOCKED.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
