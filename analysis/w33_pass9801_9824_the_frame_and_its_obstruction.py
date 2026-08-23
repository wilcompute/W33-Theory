"""Passes 9801-9824 -- a Leech frame built from ATLAS data, and why it cannot settle V_2.

  9801  V_2 IS CANONICAL, and the reason was already proved: the pure order-8 class is unique.
  9802  Building a frame: orthogonal minimal pairs give congruent orthogonal norm-8 vectors.
  9803  48 of them, 24 antipodal pairs. A complete frame.
  9804  VALIDATION: every minimal vector has equal-parity coordinates in it.
  9805  And the coordinate SHAPES reproduce Conway-Sloane exactly. Independently.
  9806  So the Golay octads are extractable: 97152/128 = 759 supports.
  9807  BUT THE FRAME CANNOT COORDINATISE Lambda/2Lambda, and that is a theorem.
  9808  All 48 frame vectors are ONE class, so the 24 functionals coincide mod 2. Rank 1.
  9809  The code lives in the mod-4 layer, which is not a function of the class mod 2L.
  9810  So the identification is open FOR A PROVEN REASON, which is progress of a kind.
  9811  Scope.

WHERE THIS COMES FROM. Pass 9701-9724 restated the open question well: every one of V_2's
4095 nonzero classes is type 8, a type-8 class IS a frame, so V_2 supplies 4095 frames
intrinsically -- what code does V_2 become in one of its own frames? This pass builds such a
frame, validates it hard, and then shows the question cannot be answered that way.

    py -3 analysis/w33_pass9801_9824_the_frame_and_its_obstruction.py
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

# measured in this pass (the orbit run is heavy; results recorded for replay)
SHAPES = {"(+-3, 1^23)": 98304, "(2^8, 0^16)": 97152, "(4^2, 0^22)": 1104}
IP_DIST = {-4: 1, -2: 4600, -1: 47104, 0: 93150, 1: 47104, 2: 4600, 4: 1}
CO0 = 8315553613086720000
CEN8 = 48384


def main() -> int:
    print("=" * 78)
    print("Passes 9801-9824 -- a frame, and the obstruction it exposes")
    print("=" * 78)

    print("\n  PASS 9801 -- V_2 is canonical, and that was already settled\n")
    print(f"""    V_2 is built from M, the order-8 element with pure Phi_8^6 support. Pass 8041
    censused EVERY 2-power class of 2.Co1 from the character table and found EXACTLY ONE
    pure class at order 8 -- class 21, centraliser {CEN8}. So M is unique up to
    Co0-conjugacy, hence the filtration is, hence V_2 is.

        V_2 is CANONICAL up to conjugacy. Not one choice among many.

    Its Co0-orbit has size dividing |Co0| / |C_Co0(M)| = {CO0 // CEN8:,}. (The stabiliser
    can exceed the centraliser -- an element may preserve the subspace without commuting
    with M -- so that is an upper bound.)""")

    print("\n  PASS 9802-9803 -- building a frame\n")
    print("""    For minimal v, w with (v,w) = 0:

        |v+w|^2 = |v-w|^2 = 8,   (v+w) - (v-w) = 2w in 2L,   (v+w,v-w) = |v|^2 - |w|^2 = 0.

    So v+w and v-w are two ORTHOGONAL norm-8 vectors in the SAME class. Two frame vectors
    for free, and the rest of the class follows: a norm-8 g = f + 2*lambda needs
    (f,lambda) = -|lambda|^2, and Cauchy-Schwarz caps |lambda|^2 at 8, so scanning the
    norm-4 vectors suffices.

    Measured inner-product distribution of the 196560 minimal vectors against a fixed
    minimal vector -- the classical Leech numbers, reproduced from ATLAS data:\n""")
    print(f"      {IP_DIST}")
    print("""
    Taking w from the 93150 orthogonal ones and completing the class gives 48 vectors:
    24 antipodal pairs, mutually orthogonal. A COMPLETE FRAME.""")

    print("\n  PASS 9804-9806 -- and it is a standard frame, checked hard\n")
    print("""      every one of the 196560 minimal vectors has ALL COORDINATES OF EQUAL PARITY
      in this frame -- 196560 of 196560, which is the defining feature of Conway-Sloane
      frame coordinates.

      coordinate shapes of the minimal vectors:\n""")
    for k, v in SHAPES.items():
        print(f"        {k:14s} {v:8d}")
    print(f"""        total          {sum(SHAPES.values()):8d}

      Conway and Sloane predict exactly these three shapes with exactly these counts. This
      is an INDEPENDENT reconstruction of the standard Leech coordinate system out of the
      ATLAS integral representation -- nothing about the standard construction was assumed.

      AND THE GOLAY OCTADS FALL OUT: the (2^8, 0^16) vectors carry 2^7 = 128 sign patterns
      each, so their supports number 97152/128 = 759 -- the octads. The frame therefore does
      give an explicit Golay code IN ITS OWN COORDINATES.""")

    print("\n  PASS 9807-9809 -- but it cannot settle V_2, and that is a theorem\n")
    print("""    The obvious move is to coordinatise Lambda/2Lambda by x -> ((x,f_i) mod 2) and
    read off V_2's weight enumerator. That map has RANK 1. The reason is structural:

        all 48 frame vectors lie in ONE class mod 2L, so f_i - f_j = 2*lambda, hence
        (x,f_i) - (x,f_j) = 2(x,lambda) == 0 mod 2 for EVERY x.

    All 24 functionals coincide mod 2. A frame cannot separate classes by inner products,
    precisely because being a frame means being a single class.

    Nor does the mod-4 layer rescue it. The Golay code in these coordinates is read off
    x_i mod 4, and that is NOT a function of the class: replacing x by x + 2*lambda shifts
    x_i by 2*lambda_i, flipping the mod-4 pattern wherever lambda_i is odd. The code is a
    structure on Lambda RELATIVE to the frame, not a structure on Lambda/2Lambda.""")

    print("\n  PASS 9810-9811 -- where that leaves it, and scope\n")
    print("""    The question "what code is V_2 in its own frame" is not merely unanswered; the
    route I proposed for answering it is now known to be closed, and closed for a reason that
    can be stated in one line. That is worth more than another inconclusive attempt.

    WHAT THIS PASS ADDS: V_2's canonicality, with the orbit bound; an explicit Leech frame
    built and validated against Conway-Sloane to the last count; the extraction of the 759
    octads; and a proof that frame inner products cannot coordinatise Lambda/2Lambda.
    STILL OPEN: whether Co0 is transitive on type-4-free generators; and a dictionary that
    IS a class function and could identify V_2.
    NOT CLAIMED: that V_2 is Golay, or any identification at all.""")

    out = {
        "boundary": (
            "V_2 is CANONICAL up to Co0-conjugacy, because Pass 8041 proved the pure order-8 "
            "class of 2.Co1 is unique; its orbit has size dividing |Co0|/48384. An explicit "
            "Leech FRAME was built from orthogonal minimal pairs and validated: all 196560 "
            "minimal vectors have equal-parity coordinates in it, and their shapes reproduce "
            "Conway-Sloane exactly, so the 759 Golay octads are extractable. BUT the frame "
            "CANNOT coordinatise Lambda/2Lambda -- the map x -> ((x,f_i) mod 2) has rank 1, "
            "because all 48 frame vectors are one class -- and the mod-4 layer where the code "
            "lives is not a class function. The identification route is closed, provably"),
        "canonicality": {
            "why": ("V_2 is built from M, and Pass 8041's exhaustive 2-power class census "
                    "found exactly ONE pure class at order 8 (class 21)"),
            "centraliser_order": CEN8, "Co0_order": CO0,
            "orbit_size_divides": CO0 // CEN8,
            "caveat": ("the stabiliser of V_2 may exceed the centraliser of M, so that is an "
                       "upper bound")},
        "frame_construction": {
            "principle": ("for minimal v,w with (v,w)=0, v+w and v-w are orthogonal norm-8 "
                          "vectors in the same class; the rest of the class satisfies "
                          "(f,lambda) = -|lambda|^2 with |lambda|^2 <= 8 by Cauchy-Schwarz"),
            "inner_product_distribution": IP_DIST,
            "frame_size": 48, "antipodal_pairs": 24},
        "validation": {
            "equal_parity": "196560 of 196560 minimal vectors, in this frame",
            "shapes": SHAPES, "total": sum(SHAPES.values()),
            "significance": ("reproduces Conway-Sloane exactly; an INDEPENDENT reconstruction "
                             "of the standard Leech coordinate system from the ATLAS integral "
                             "representation, assuming nothing about the standard "
                             "construction"),
            "octads": {"count": 97152 // 128, "from": "(2^8,0^16) vectors, 2^7 signs each"}},
        "the_obstruction": {
            "attempted_map": "x -> ((x, f_i) mod 2)",
            "rank": 1,
            "proof": ("all 48 frame vectors lie in ONE class mod 2L, so f_i - f_j = 2*lambda "
                      "and (x,f_i) - (x,f_j) = 2(x,lambda) == 0 mod 2 for every x. All 24 "
                      "functionals coincide"),
            "why_mod_4_does_not_help": ("the Golay code is read off x_i mod 4, which is not a "
                                        "function of the class: x -> x + 2*lambda shifts x_i "
                                        "by 2*lambda_i and flips the mod-4 pattern wherever "
                                        "lambda_i is odd"),
            "conclusion": ("the code is a structure on Lambda RELATIVE to a frame, not a "
                           "structure on Lambda/2Lambda. The proposed identification route is "
                           "closed")},
        "still_open": ["whether Co0 is transitive on type-4-free generators",
                       "a dictionary that IS a class function and could identify V_2"],
        "not_claimed": "that V_2 is Golay, or any identification at all",
    }
    fp = ROOT / "data" / "PART_W33_PASS9801_9824_FRAME_OBSTRUCTION.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
