"""Passes 8925-8940 -- the top rung of every tower is ORTHOGONAL, not symplectic.

  8925  An even lattice gives L/2L more than a symplectic form. It gives a QUADRATIC one.
  8926  Verified: q polarises to the symplectic form, and it is well defined mod 2L.
  8927  E8/2E8 = 135 singular + 120 non-singular, and 135 = |Q+(7,2)|.
  8928  The 120 non-singular points are EXACTLY the 120 root classes.
  8929  So W(E8) cannot surject onto Sp(8,2) -- it is too small, and it lands in O.
  8930  Leech/2Leech is PLUS type, and Conway's type split IS the singular/non-singular split.
  8931  And d=4, d=8 have NO such refinement -- proven by the full-Sp image, not assumed.
  8932  Which is exactly why the Clifford identification held there and failed at d=2.
  8933  A refinement of earlier passes, not a retraction. The distinction stated precisely.
  8934  Open.
  8935  Scope.

WHERE THIS COMES FROM. Pass 8909-8924 verified that the Springer centraliser IS the Clifford
group of its own geometry at d=4 and d=8, and noticed in passing that d=2 does not fit:
|W(E8)| = 696729600 is SMALLER than |Sp(8,2)| = 47377612800, so the d=2 image cannot be the
full symplectic group whatever it is. That looked like an awkward exception. It is not an
exception -- it is the signature of extra structure.

CLASSICAL, AND CITED AS SUCH: that E8 mod 2 carries a plus-type quadratic form with
W(E8)/{+-1} = O_8^+(2).2, and that Conway's Leech classes split 98280 + 8386560 + 8292375
by type, are both classical. What this pass adds is where they sit in the tower of Passes
8022-8924, and that they EXPLAIN the d=2 anomaly rather than merely coexisting with it.

    py -3 analysis/w33_pass8925_8940_the_top_rung_is_orthogonal.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "analysis"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN, roots_in_root_basis  # noqa: E402

# Conway's type split of the 2^24 - 1 nonzero classes of Leech/2Leech
CONWAY = {4: 98280, 6: 8386560, 8: 8292375}


def sp_order(m, q):
    o = q ** (m * m)
    for i in range(1, m + 1):
        o *= q ** (2 * i) - 1
    return o


def main() -> int:
    print("=" * 78)
    print("Passes 8925-8940 -- the top rung is orthogonal")
    print("=" * 78)

    G = CARTAN
    n = 8
    V = [np.array(v, dtype=np.int64) for v in itertools.product([0, 1], repeat=n)]

    def q(x):
        return (int(x @ G @ x) // 2) % 2

    def b(x, y):
        return int(x @ G @ y) % 2

    print("\n  PASS 8925-8926 -- the quadratic refinement\n")
    print("""    For an EVEN lattice, q(x) = (x,x)/2 mod 2 is well defined on L/2L, because

        (x + 2y, x + 2y)/2  =  (x,x)/2 + 2(x,y) + 2(y,y)  ==  (x,x)/2   mod 2,

    and it POLARISES to the symplectic form already in use:

        q(x+y) - q(x) - q(y)  =  (x,y)  mod 2.

    So the d=2 rung of every tower in Passes 8022-8924 carries strictly more structure than
    the symplectic form those passes used.""")
    pol = all(((q((x + y) % 2) - q(x) - q(y)) % 2) == b(x, y)
              for x in V[:120] for y in V[:120])
    print(f"\n      polarisation identity, checked on 120x120 pairs : {pol}")

    print("\n  PASS 8927-8928 -- E8, counted\n")
    sing = [x for x in V if x.any() and q(x) == 0]
    nons = [x for x in V if x.any() and q(x) == 1]
    qplus7 = (2 ** 3 + 1) * (2 ** 4 - 1)
    R = roots_in_root_basis()
    rc = {tuple(np.array(r, dtype=np.int64) % 2) for r in R}
    rc_nonsing = all(q(np.array(c, dtype=np.int64)) == 1 for c in rc)
    same = rc == {tuple(x) for x in nons}
    e8 = {"singular": len(sing), "non_singular": len(nons),
          "total_nonzero": len(sing) + len(nons),
          "Qplus_7_2": qplus7, "singular_matches_Qplus": len(sing) == qplus7,
          "root_classes": len(rc), "root_classes_all_non_singular": bool(rc_nonsing),
          "root_classes_ARE_the_non_singular_points": bool(same)}
    for k, v in e8.items():
        print(f"      {k:44s} {v}")
    print("""
    So E8/2E8 is a plus-type quadratic space: 135 singular points, which is exactly
    |Q+(7,2)|, and 120 non-singular ones -- and those 120 are precisely the classes of the
    240 roots, in antipodal pairs. The root system IS the non-singular locus.""")

    print("\n  PASS 8929 -- and that caps the automorphism group\n")
    aut = {"|Sp(8,2)|": sp_order(4, 2), "|W(E8)|": 696729600,
           "W(E8) smaller than Sp(8,2)": 696729600 < sp_order(4, 2),
           "|O_8^+(2).2|": 174182400 * 2, "|W(E8)|/2": 696729600 // 2,
           "match": 696729600 // 2 == 174182400 * 2}
    for k, v in aut.items():
        print(f"      {k:30s} {v}")
    print("""
    W(E8) is an order of magnitude too small to surject onto Sp(8,2), and |W(E8)|/2 is
    exactly |O_8^+(2).2|. The image is ORTHOGONAL. Nothing was going to make the d=2 rung
    behave like d=4 and d=8, and now the reason is structural rather than numerical.""")

    print("\n  PASS 8930 -- Leech, via Conway's type split\n")
    print(f"      {'type':>5s} {'q = t/2 mod 2':>14s} {'singular?':>10s} {'count':>10s}")
    s_tot = 0
    for t, c in sorted(CONWAY.items()):
        qq = (t // 2) % 2
        if qq == 0:
            s_tot += c
        print(f"      {t:5d} {qq:14d} {str(qq == 0):>10s} {c:10d}")
    non_tot = CONWAY[6]
    qplus23 = (2 ** 11 + 1) * (2 ** 12 - 1)
    qmin23 = (2 ** 11 - 1) * (2 ** 12 + 1)
    leech = {"singular": s_tot, "non_singular": non_tot,
             "total_nonzero": s_tot + non_tot, "two24_minus_1": 2 ** 24 - 1,
             "totals_agree": s_tot + non_tot == 2 ** 24 - 1,
             "Qplus_23_2": qplus23, "Qminus_23_2": qmin23,
             "type_is_PLUS": s_tot == qplus23}
    print(f"\n      singular = {CONWAY[4]} + {CONWAY[8]} = {s_tot}")
    print(f"      |Q+(23,2)| = {qplus23}   |Q-(23,2)| = {qmin23}")
    print(f"      Leech/2Leech is PLUS type : {leech['type_is_PLUS']}")
    print("""
    So Conway's classical type split is the singular/non-singular split of a plus-type
    quadratic form: type 4 and type 8 classes are the singular points, type 6 the
    non-singular ones. The 98280 minimal-vector classes sit inside the quadric.""")

    print("\n  PASS 8931-8932 -- and the deeper rungs have no such refinement\n")
    print("""    This is PROVEN by the previous pass rather than assumed here. Pass 8909-8924
    computed the image of the centraliser on the d=4 quotient and found the FULL Sp(4,2), of
    order 720; |O_4^+(2)| = 72 and |O_4^-(2)| = 120. A symplectic group preserves no
    quadratic form, so a full-Sp image RULES OUT any invariant quadratic refinement at d=4.
    The same argument applies at d=8, where the image was all of Sp(2,2).

    THAT IS THE WHOLE DICHOTOMY:

        d = 2      quotient L/2L      carries a QUADRATIC form   image is ORTHOGONAL
        d = 4, 8   deeper quotients   symplectic only            image is FULL SYMPLECTIC

    and it is why the Clifford identification of Pass 8909-8924 held at d=4 and d=8 and
    could never have held at d=2. The Clifford group needs the full symplectic group on the
    quotient; at d=2 the lattice will not give it up.""")

    print("\n  PASS 8933 -- refinement, not retraction\n")
    print("""    Earlier passes called the d=2 rung W(7,2) for E8 and W(23,2) for Leech, and
    read them as 4 and 12 qubits. The SYMPLECTIC statements are correct and stand: the form
    is alternating and nondegenerate on F_2^8 and F_2^24 respectively.

    What was incomplete is the reading. The lattice supplies a quadratic refinement at that
    level, the automorphism group respects it, and the natural object is therefore the
    QUADRIC inside the symplectic space, not the symplectic space itself. So "twelve qubits"
    at the top of the Leech tower is a statement about a form, not about a Pauli geometry
    with the expected symmetry group -- because the symmetry group is orthogonal. The tower
    maps, the odd-part law and the kernel classifications are untouched; only the
    identification of the TOP rung is sharpened.""")

    print("\n  PASS 8936 -- and the same thing happens at p=3, which closes an open item\n")
    iso = sum(1 for v in itertools.product(range(3), repeat=8)
              if any(v) and int(np.array(v, dtype=np.int64) @ G
                                @ np.array(v, dtype=np.int64)) % 3 == 0)
    m = 4
    p3plus, p3minus = (3 ** (m - 1) + 1) * (3 ** m - 1), (3 ** (m - 1) - 1) * (3 ** m + 1)
    p3 = {"nonzero_vectors": 3 ** 8 - 1, "isotropic": iso, "anisotropic": 3 ** 8 - 1 - iso,
          "plus_count": p3plus, "minus_count": p3minus, "is_plus_type": iso == p3plus}
    for k, v in p3.items():
        print(f"      {k:24s} {v}")
    print("""
    The pi-adic filtration has ramification e = deg Phi_{p^m}, and its TOP level is ALWAYS
    L/pL -- level 1 when d=2, level 4 when d=8, level 2 when d=3, level 6 when d=9. That
    level always carries the symmetric form G mod p, so it is ORTHOGONAL at every prime.

    At p=2 an even lattice makes that same form ALTERNATING as well, which is why it looked
    symplectic and got recorded as W(7,2) or W(23,2). At odd p symmetric and alternating are
    genuinely different, so it never looked symplectic -- and Pass 8861-8884 recorded level 6
    at p=3 as carrying no alternating form and left "what is it?" open. This is the answer:
    it is the orthogonal space of G mod 3, and for E8 it is PLUS type.

    One law, two disguises.""")

    print("\n  PASS 8934-8935 -- open, and scope\n")
    print("""    NEW HERE: the placement of the quadratic refinement inside the tower, and the
    fact that it EXPLAINS the d=2 anomaly of Pass 8909-8924 rather than merely sitting
    beside it; the verification that E8's 120 root classes are exactly the non-singular
    points; and the observation that Conway's type split is the singular/non-singular split
    of a plus-type form.
    CLASSICAL, CITED NOT CLAIMED: E8 mod 2 as a plus-type quadratic space with
    W(E8)/{+-1} = O_8^+(2).2, and Conway's 98280 + 8386560 + 8292375 type split of
    Leech/2Leech.
    NOT DONE: the orthogonal geometry at the p=3 top rung (Pass 8861-8884 left level 6 as
    whether the d=2 image for LEECH
    is likewise the full orthogonal group (Co0 order versus |O_24^+(2)| is not checked here);
    alpha(W(3,9)); K12 built.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED: an even lattice gives L/2L a QUADRATIC form q(x) = (x,x)/2 mod 2 "
            "polarising to the symplectic form, so the d=2 rung of every tower in Passes "
            "8022-8924 is ORTHOGONAL, not symplectic. E8/2E8 has 135 singular points = "
            "|Q+(7,2)| and 120 non-singular ones which are EXACTLY the root classes; "
            "|W(E8)|/2 = |O_8^+(2).2|. Leech/2Leech is PLUS type, with Conway's type-4 and "
            "type-8 classes the singular points. Deeper rungs have no such refinement, "
            "proven by the full-Sp images of Pass 8909-8924 -- which is exactly why the "
            "Clifford identification held at d=4,8 and could not at d=2"),
        "quadratic_refinement": {
            "form": "q(x) = (x,x)/2 mod 2",
            "well_defined": "(x+2y,x+2y)/2 = (x,x)/2 + 2(x,y) + 2(y,y) == (x,x)/2 mod 2",
            "polarises_to_symplectic": bool(pol),
            "checked_on": "120x120 pairs"},
        "e8": e8,
        "e8_automorphism_cap": aut,
        "p3_top_rung": {"note": "answers the open item left by Pass 8861-8884",
                        "statement": ("the top level of the pi-adic filtration is always "
                                      "L/pL, carrying the symmetric form G mod p, hence "
                                      "ORTHOGONAL at every prime; at p=2 an even lattice "
                                      "makes it alternating too, which is the disguise"),
                        "levels": {"d=2": "e=1, level 1 is L/2L", "d=8": "e=4, level 4 is L/2L",
                                   "d=3": "e=2, level 2 is L/3L", "d=9": "e=6, level 6 is L/3L"}},
        "leech": {**leech, "conway_split": CONWAY,
                  "reading": ("Conway's type split IS the singular/non-singular split: type "
                              "4 and 8 are singular, type 6 non-singular")},
        "dichotomy": {
            "d2": {"quotient": "L/2L", "structure": "quadratic", "image": "orthogonal"},
            "d4_d8": {"quotient": "deeper", "structure": "symplectic only",
                      "image": "full symplectic"},
            "proof_that_deeper_rungs_have_no_refinement": (
                "Pass 8909-8924 computed the d=4 image as the FULL Sp(4,2) of order 720, "
                "against |O_4^+(2)| = 72 and |O_4^-(2)| = 120; a symplectic group preserves "
                "no quadratic form, so a full-Sp image rules one out. Same at d=8"),
            "explains": ("why the Clifford identification held at d=4 and d=8 and could "
                         "never hold at d=2: a Clifford group needs the full symplectic "
                         "group on the quotient")},
        "refinement_not_retraction": {
            "what_stands": ("the symplectic statements: the form is alternating and "
                            "nondegenerate on F_2^8 and F_2^24, so W(7,2) and W(23,2) are "
                            "correct descriptions of the FORM"),
            "what_is_sharpened": ("the reading. The lattice supplies a quadratic refinement "
                                  "the automorphism group respects, so the natural object at "
                                  "d=2 is the quadric, and 'twelve qubits' at the top of the "
                                  "Leech tower is a statement about a form rather than a "
                                  "Pauli geometry with the expected symmetry group"),
            "unaffected": ["the tower maps", "the odd-part law", "the kernel classifications"]},
        "classical_cited": ["E8 mod 2 is a plus-type quadratic space, W(E8)/{+-1} = O_8^+(2).2",
                            "Conway's 98280 + 8386560 + 8292375 type split of Leech/2Leech"],
        "not_done": [
                     "whether the Leech d=2 image is the full orthogonal group",
                     "alpha(W(3,9))", "K12 built"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8925_8940_TOP_RUNG_ORTHOGONAL.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
