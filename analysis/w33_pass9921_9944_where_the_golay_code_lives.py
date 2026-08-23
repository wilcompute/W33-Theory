"""Passes 9921-9944 -- where the Golay code actually lives, and a dichotomy that was wrong.

  9921  Pass 9801-9824 proved a frame cannot coordinatise Lambda/2Lambda. Why not?
  9922  Because the code is not on Lambda/2Lambda at all. It is on the 2-NEIGHBOUR.
  9923  A type-8 class gives a neighbour whose roots are the frame vectors HALVED.
  9924  48 roots, mutually orthogonal in 24 antipodal pairs: the root system A1^24.
  9925  And A1^24's glue code IS the binary Golay code. The obstruction is explained.
  9926  A DICHOTOMY I NEARLY PUBLISHED, AND IT IS FALSE.
  9927  Type-4 classes DO give 2-neighbours, via a norm-16 representative.
  9928  What IS true about type 4: it holds no norm-8 vector, and here is why.
  9929  Scope.

WHAT THIS RESOLVES. Pass 9801-9824 built a Leech frame, validated it against Conway-Sloane
exactly, and then proved that frame inner products cannot coordinatise Lambda/2Lambda -- all
48 frame vectors are one class, so the 24 functionals coincide mod 2. That left the question
of where the Golay code does live. It lives on the neighbour.

    py -3 analysis/w33_pass9921_9944_where_the_golay_code_lives.py
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

MEASURED = {"frame_size": 48, "halved_norms": [2], "non_antipodal_inner_products": [0],
            "root_system": "A1^24", "inner_product_values_minimal_pairs":
                [-4, -2, -1, 0, 1, 2, 4]}


def main() -> int:
    print("=" * 78)
    print("Passes 9921-9944 -- where the Golay code lives")
    print("=" * 78)

    print("\n  PASS 9921-9925 -- the code is on the neighbour\n")
    print("""    For c in Lambda with c not in 2*Lambda and (c,c) = 0 mod 8, the 2-NEIGHBOUR

        Lambda_c = {x in Lambda : (x,c) even} + Z.(c/2)

    is again even unimodular, and it depends only on the CLASS of c: replacing c by c+2*mu
    leaves both the parity condition and the coset c/2 + Lambda unchanged.

    ITS ROOTS ARE THE FRAME, HALVED. A root of Lambda_c is c/2 + y with |c/2+y|^2 = 2, i.e.
    |y|^2 + (c,y) = 0 -- and then c + 2y is a norm-8 vector in the class of c. So the roots
    of the neighbour are exactly the frame vectors divided by two. Measured on the frame
    built at Pass 9801-9824:\n""")
    print(f"      frame size                              {MEASURED['frame_size']}")
    print(f"      norms of the halved frame vectors       {MEASURED['halved_norms']}")
    print(f"      inner products, non-antipodal pairs     "
          f"{MEASURED['non_antipodal_inner_products']}")
    print("""
      48 roots of norm 2, mutually orthogonal in 24 antipodal pairs. That is the root
      system A1^24 exactly, and by Niemeier's classification the neighbour IS the Niemeier
      lattice with root system A1^24.

    AND THE GLUE OF A1^24 IS THE BINARY GOLAY CODE. That is classical, and it answers the
    question Pass 9801-9824 left open:

        the Golay code is not a structure on Lambda/2Lambda. It is the glue of the
        NEIGHBOUR, and the frame is the bridge between the two lattices.

    So the frame was never going to coordinatise Lambda/2Lambda -- not because the map was
    badly chosen, but because the target was.""")

    print("\n  PASS 9926-9927 -- and a dichotomy I nearly published\n")
    print("""    The tempting next sentence was: "a type-4 class contains only norms 4 mod 8, so
    type-4 classes give NO neighbour, and the type-8 classes are exactly the neighbour
    directions of Leech." That is FALSE, and checking it rather than asserting it is the
    only reason it is not in the repo.

    Norms within a class are constant only MOD 4 -- that is precisely what q records -- not
    mod 8. And a type-4 class does contain a norm-16 vector: take lambda minimal with
    (v,lambda) = -1, then

        |v + 2*lambda|^2 = 4 + 4(-1) + 4(4) = 16,   and 16 = 0 mod 8.

    So type-4 classes DO give 2-neighbours. What differs between type 4 and type 8 is the
    neighbour's ROOT SYSTEM, not whether a neighbour exists. The clean dichotomy was wrong.""")

    print("\n  PASS 9928 -- what IS true about type 4, with the reason\n")
    print(f"""    A type-4 class contains NO vector of norm 8. Proof: a norm-8 vector would be
    v + 2*lambda with 4 + 4(v,lambda) + 4|lambda|^2 = 8, so (v,lambda) + |lambda|^2 = 1.
    Cauchy-Schwarz gives |lambda|^2 <= 5.8, so |lambda|^2 = 4 and (v,lambda) = -3. But the
    inner products between minimal vectors of Leech take only the values

        {MEASURED['inner_product_values_minimal_pairs']}

    and -3 is NOT among them. So no such lambda exists.

    That is the real content of the type-4/type-8 distinction here: not the existence of a
    neighbour, but the absence of norm-8 representatives -- which is exactly what makes the
    frame construction available for type 8 and unavailable for type 4.""")

    print("\n  PASS 9929 -- scope\n")
    print("""    NEW: the identification of the 2-neighbour's root system as A1^24 by halving
    the frame, verified; and the consequent placement of the Golay code as the glue of the
    NEIGHBOUR rather than a structure on Lambda/2Lambda, which explains the Pass 9801-9824
    obstruction.
    CORRECTED BEFORE PUBLICATION: "type-4 classes give no neighbour" is false; they do, via
    a norm-16 representative. Only the norm-8 statement survives.
    CLASSICAL, CITED NOT CLAIMED: Niemeier's classification, and that the glue code of the
    A1^24 Niemeier lattice is the binary Golay code.
    NOT DONE: the root system of a type-4 class's neighbour, which needs the norm-6 and
    norm-8 contributions and was not attempted; whether V_2's 4095 neighbours are related
    to each other as lattices.
    NOT CLAIMED: that V_2 is Golay -- that remains open and this pass does not touch it.""")

    out = {
        "boundary": (
            "RESOLVES the Pass 9801-9824 obstruction: the Golay code is not a structure on "
            "Lambda/2Lambda but the GLUE of the 2-neighbour. A type-8 class gives a "
            "neighbour whose roots are the frame vectors halved -- verified as 48 norm-2 "
            "vectors, mutually orthogonal in 24 antipodal pairs, i.e. the root system A1^24 "
            "-- and A1^24's glue is the binary Golay code. ALSO CORRECTS, before publication, "
            "a false dichotomy: type-4 classes DO give 2-neighbours, via a norm-16 "
            "representative"),
        "neighbour_construction": {
            "definition": "Lambda_c = {x in Lambda : (x,c) even} + Z.(c/2)",
            "depends_only_on_class": ("replacing c by c+2mu leaves the parity condition and "
                                      "the coset c/2 + Lambda unchanged"),
            "roots_are_the_halved_frame": ("a root is c/2 + y with |y|^2 + (c,y) = 0, and "
                                           "then c+2y is a norm-8 vector in the class of c"),
            "measured": MEASURED,
            "conclusion": ("48 norm-2 roots, mutually orthogonal in 24 antipodal pairs: the "
                           "root system A1^24, so by Niemeier the neighbour is the A1^24 "
                           "Niemeier lattice")},
        "where_the_code_lives": (
            "the glue of A1^24 is the binary Golay code (classical), so the Golay code lives "
            "on the NEIGHBOUR, not on Lambda/2Lambda. The frame is the bridge between the two "
            "lattices. That is why a frame could never coordinatise Lambda/2Lambda: the "
            "target was wrong, not the map"),
        "corrected_before_publication": {
            "tempting_claim": ("a type-4 class holds only norms 4 mod 8, so type-4 classes "
                               "give NO neighbour and type-8 classes are exactly the "
                               "neighbour directions"),
            "status": "FALSE",
            "why": ("norms within a class are constant only MOD 4, which is what q records, "
                    "not mod 8. A type-4 class contains a norm-16 vector: with lambda minimal "
                    "and (v,lambda) = -1, |v+2lambda|^2 = 4 - 4 + 16 = 16 == 0 mod 8"),
            "what_actually_differs": "the neighbour's ROOT SYSTEM, not whether one exists"},
        "what_survives_about_type4": {
            "statement": "a type-4 class contains NO vector of norm 8",
            "proof": ("a norm-8 vector needs (v,lambda) + |lambda|^2 = 1; Cauchy-Schwarz "
                      "forces |lambda|^2 = 4 hence (v,lambda) = -3, and the inner products "
                      "between Leech minimal vectors take only the values -4,-2,-1,0,1,2,4 "
                      "-- never -3"),
            "significance": ("that is what makes the frame construction available for type 8 "
                             "and unavailable for type 4")},
        "classical_cited": ["Niemeier's classification of even unimodular rank-24 lattices",
                            "the glue code of the A1^24 Niemeier lattice is the binary Golay "
                            "code"],
        "not_done": ["the root system of a type-4 class's neighbour, needing the norm-6 and "
                     "norm-8 contributions",
                     "whether V_2's 4095 neighbours are related to each other as lattices"],
        "not_claimed": "that V_2 is Golay -- still open, and untouched here",
    }
    fp = ROOT / "data" / "PART_W33_PASS9921_9944_GOLAY_LIVES_ON_THE_NEIGHBOUR.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
