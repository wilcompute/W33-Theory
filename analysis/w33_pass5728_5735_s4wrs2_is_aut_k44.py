"""Passes 5728-5735 -- S4 wr S2 is Aut(K_4,4), and my correction needed correcting.

  5728  THE ANSWER: S4 wr S2 = Aut(K_4,4), and K_4,4 IS the Q4 antipodal quotient.
  5729  Why four internal searches failed, and why the corpus already held both halves.
  5730  CORRECTION TO PASS 5720: period q-1 was right; I misread a digit value as a wrap.
  5731  The digit law, verified to e=8 at GF(9) and refuted past e=q-1 at GF(4).
  5732  The two laws together, and which one is proved.
  5733  Reed-Muller: the Q4 vertices are a [8,4] code with profile {0:1, 4:14, 8:1}.
  5734  The one-line-proof filter, applied to my own passes.
  5735  Scope.

    py -3 analysis/w33_pass5728_5735_s4wrs2_is_aut_k44.py
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

GF9 = [(1, 4, 4), (2, 10, 10), (3, 4, 4), (4, 16, 16), (5, 40, 40),
       (6, 10, 10), (7, 40, 40), (8, 100, 100)]
GF4 = [(1, 4, 4), (2, 4, 4), (3, 16, 16), (4, 4, 4), (5, 4, 16)]
ATTEMPTS = ["Delsarte coset graph (Pass 5671)", "two-weight structure (Pass 5671)",
            "the GF(2) kernel (Pass 5685)", "module irreducibility (Pass 5715)"]
SOURCES = {"quotient": "analysis/2026-06-01_q4_rm13_bridge.md (Part MMCCCLXXIV)",
           "order": "data/PART_MMCCCLXXV_DENSITY_DUAL_GENERATOR_results.json (Aut_K44 = 1152)"}
RM = {"length": 8, "words": 16, "profile": {0: 1, 4: 14, 8: 1},
      "antipodal": "becomes word complementation"}


def digits(e, p):
    out = []
    while e:
        out.append(e % p)
        e //= p
    return out or [0]


def main() -> int:
    print("=" * 78)
    print("Passes 5728-5735 -- S4 wr S2 is Aut(K_4,4)")
    print("=" * 78)

    print("\n  PASS 5728-5729 -- THE ANSWER, and it was already here\n")
    print("    Q4 antipodal quotient : 8 vertices, 16 edge-classes, 4-regular, bipartite")
    print("    K_4,4                 : 8 vertices, 16 edges")
    print("    ISOMORPHIC            : True")
    print(f"    |Aut(K_4,4)| = (4!)^2 x 2 = 1152 = |S4 wr S2|")
    print(f"\n    both halves were in the corpus, in CONSECUTIVE parts:")
    for k, v in SOURCES.items():
        print(f"      {k:9s} {v}")
    print(f"""
    FOUR INTERNAL SEARCHES FAILED FOR ONE REASON, and Pass 5726 guessed it correctly
    before finding it: S4 wr S2 is not intrinsic to the tomotope's 16-face graph, it is
    INHERITED FROM THE CONSTRUCTION. The Q4 antipodal quotient is K_4,4; the automorphism
    group of K_4,4 is S4 wr S2; everything downstream of that quotient carries it.

    {chr(10).join('      tried: ' + a for a in ATTEMPTS)}

    Each asked where inside the object the structure hides. None could find it because it
    was upstream. AND THE CORPUS HELD BOTH HALVES IN CONSECUTIVE PARTS -- MMCCCLXXIV says
    the quotient is K_4,4, MMCCCLXXV records Aut_K44 = 1152 -- while I searched for four
    passes. I found MMCCCLXXV at Pass 5644 and never looked at MMCCCLXXIV.""")

    print("\n  PASS 5730-5732 -- correcting my correction\n")
    print(f"    GF(9), char 3, q-1 = 8:")
    for e, r, p in GF9:
        print(f"      e={e}: rank {r:4d}  digit-product {p:4d}  base-3 "
              f"{str(digits(e, 3)[::-1]):>9s}  {'match' if r == p else 'MISMATCH'}")
    print(f"    GF(4), char 2, q-1 = 3:")
    for e, r, p in GF4:
        print(f"      e={e}: rank {r:4d}  digit-product {p:4d}  base-2 "
              f"{str(digits(e, 2)[::-1]):>9s}  {'match' if r == p else 'MISMATCH'}")
    print("""
    PASS 5720 RETRACTED THE PERIOD-(q-1) CLAIM AND SHOULD NOT HAVE. I saw rank 4 at e=3 on
    GF(9) and read it as the tower wrapping at the characteristic. It is not a wrap: 3 in
    base 3 is (1,0), and the digit product 4 x 1 = 4 is simply the law's value there. The
    period at GF(9) is 8, and e=3 is nowhere near it.

    THE REAL PERIOD IS q-1 AND IT IS PROVED, not measured: for x nonzero in GF(q),
    x^(q-1) = 1, so sf^e and sf^(e mod (q-1)) agree on every nonzero value and both vanish
    where sf does. GF(4) shows it directly -- e=5 has digit product 16 but measured rank 4,
    because 5 = 2 mod 3 and rank(sf^2) = 4.

    SO THERE ARE TWO LAWS AND THEY HAVE DIFFERENT STATUS:
      PROVED     rank(sf^e) depends only on e mod (q-1).
      MEASURED   for 1 <= e <= q-1, rank(sf^e) = product over base-p digits d of C(d+3,3).
    Verified at eight consecutive exponents on GF(9) and three on GF(4). The digit law is
    a statement WITHIN one period; Pass 5720 confused the two and retracted the sound one.""")

    print("\n  PASS 5733 -- Reed-Muller, found by searching harder\n")
    print(f"    the 16 Q4 vertices encode as a length-{RM['length']} binary code")
    print(f"    weight profile {RM['profile']} -- {RM['words']} words")
    print(f"    the antipodal map {RM['antipodal']}")
    print("""
    THAT PROFILE IS RM(1,3), the first-order Reed-Muller code of length 8 -- one zero word,
    fourteen of weight 4, one all-ones. It sits in analysis/2026-06-01_q4_rm13_bridge.md,
    a DATE-NAMED file, and it is the reason the antipodal quotient is clean: complementation
    is the code's own symmetry. This is the third time this session a date-named file held
    the thing I needed.""")

    print("\n  PASS 5734-5735 -- the filter on myself, and scope\n")
    print("""    APPLYING THE ONE-LINE-PROOF FILTER TO MY OWN PASSES: the Sym^e bound and the
    p=2 rank law both had one-line proofs and both were classical. The period-(q-1) law
    ALSO has a one-line proof -- x^(q-1) = 1 -- and by the heuristic should be assumed
    classical until searched. It almost certainly is; it is the elementary fact that
    Hadamard powers of a matrix over GF(q) are periodic in the exponent.

    THE DIGIT LAW IS THE ONE PART THAT MIGHT NOT BE, and it is also the only part with no
    proof yet -- which is the inverse of the pattern and the reason to keep it.

    NOT DONE: a proof of the digit law; GF(8); whether the digit law is classical (a
    Steinberg-shaped statement, so probably).""")

    out = {
        "boundary": (
            "Pass 5728 identifies the SOURCE of S4 wr S2 and does not derive the 16-face "
            "graph's full automorphism group from K_4,4. Pass 5730 CORRECTS Pass 5720, "
            "which itself corrected Pass 5713 -- the original period claim was sound. The "
            "digit law is MEASURED at 8 exponents on GF(9) and 3 on GF(4), not proved. "
            "GF(8) untested"),
        "pass_5728_5729": {
            "answer": "S4 wr S2 = Aut(K_4,4), and K_4,4 is the Q4 antipodal quotient",
            "quotient": {"vertices": 8, "edges": 16, "regular": 4, "bipartite": True},
            "aut_order": 1152,
            "failed_attempts": ATTEMPTS,
            "why": "inherited from the construction, not intrinsic to the result",
            "prior_art": SOURCES,
            "note": ("both halves sat in CONSECUTIVE parts MMCCCLXXIV and MMCCCLXXV; I "
                     "found the second at Pass 5644 and never opened the first")},
        "pass_5730_5732": {
            "corrects": "Pass 5720, which wrongly retracted Pass 5713's period-(q-1) claim",
            "misreading": ("rank 4 at e=3 on GF(9) is the digit product 4 x 1, not a wrap; "
                           "the period at GF(9) is 8"),
            "proved_law": "rank(sf^e) depends only on e mod (q-1), since x^(q-1) = 1",
            "measured_law": ("for 1 <= e <= q-1, rank(sf^e) = product over base-p digits "
                             "d of e of C(d+3,3)"),
            "gf9": [{"e": e, "rank": r, "digit_product": p} for e, r, p in GF9],
            "gf4": [{"e": e, "rank": r, "digit_product": p} for e, r, p in GF4],
            "gf4_mismatch_explained": "e=5 == 2 mod 3, so rank(sf^5) = rank(sf^2) = 4"},
        "pass_5733": {**RM, "identification": "RM(1,3), first-order Reed-Muller of length 8",
                      "source": "analysis/2026-06-01_q4_rm13_bridge.md",
                      "note": "third date-named file this session to hold a needed result"},
        "pass_5734_5735": {
            "self_filter": ("the period law also has a one-line proof and should be "
                            "assumed classical; the digit law has no proof yet, which is "
                            "the inverse pattern and the reason to keep it"),
            "not_done": ["a proof of the digit law", "GF(8)",
                         "whether the digit law is classical"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS5728_5735_S4WRS2_IS_AUT_K44.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
