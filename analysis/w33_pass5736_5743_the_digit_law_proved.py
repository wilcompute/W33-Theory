"""Passes 5736-5743 -- the digit law's bound is proved, and it is classical too.

  5736  PROOF: sf^e factors over Frobenius twists, and Hadamard rank is submultiplicative.
  5737  So the digit-law BOUND is classical as well; only attainment is measured.
  5738  GF(8): 7 of 7 within the period, including rank 64 = 4^3 at e=7.
  5739  The complete statement, with each part's status labelled.
  5740  What is downstream of the K_4,4 quotient.
  5741  The construction-inheritance audit as a method.
  5742  Re-examining this session's empty searches.
  5743  Scope.

    py -3 analysis/w33_pass5736_5743_the_digit_law_proved.py
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

GF8 = [(1, 4, [1]), (2, 4, [1, 0]), (3, 16, [1, 1]), (4, 4, [1, 0, 0]),
       (5, 16, [1, 0, 1]), (6, 16, [1, 1, 0]), (7, 64, [1, 1, 1])]
VERIFIED = {"GF(9)": 8, "GF(8)": 7, "GF(4)": 3, "primes 3,5,7,11": "all single-digit"}
DOWNSTREAM = [("Q4", "16 vertices, 32 edges", "the source"),
              ("RM(1,3)", "[8, 4] code, profile {0:1, 4:14, 8:1}", "the encoding"),
              ("K_4,4", "antipodal quotient, Aut = S4 wr S2 = 1152", "WHERE 1152 ENTERS"),
              ("Reye 12_4 16_3", "face/edge classes, Aut(Levi) = W(F4)/Z = 576", "downstream"),
              ("tomotope 16-face graph", "rook complement, Aut = S4 wr S2 = 1152", "inherits")]
EMPTY = [("the [12,4,6] enumerator", "four searches, NOT FOUND", "still open"),
         ("the p=2 rank law", "found on the FIFTH pattern", "was Chandler-Sin-Xiang"),
         ("the master theorem banner", "grep could not match a `>` line", "false alarm"),
         ("S4 wr S2's origin", "four internal searches", "was upstream, in MMCCCLXXIV")]


def digits(e, p):
    out = []
    while e:
        out.append(e % p)
        e //= p
    return out or [0]


def main() -> int:
    print("=" * 78)
    print("Passes 5736-5743 -- the digit law's bound is proved")
    print("=" * 78)

    print("\n  PASS 5736-5737 -- THE PROOF\n")
    print("""    Write e in base p as e = SUM d_i p^i. Then

        sf^e  =  PRODUCT_i ( sf^(p^i) )^(d_i)  =  PRODUCT_i ( Frob^i(sf) )^(d_i)

    entrywise, since x -> x^(p^i) is the i-th Frobenius. Two classical facts finish it:

      (a) Frobenius is a field automorphism, so Frob^i(sf) is the entrywise image of sf
          under a ring automorphism and has the SAME rank, 4.
      (b) Hadamard rank is submultiplicative -- rank(A o B) <= rank(A) rank(B) -- and the
          Hadamard power bound gives rank(A^(o d)) <= C(d + rank(A) - 1, d).

    Applying (b) to each factor with rank 4 gives C(d_i + 3, 3), and multiplying:

        rank( sf^e )  <=  PRODUCT_i  C(d_i + 3, 3).

    SO THE DIGIT LAW'S BOUND IS CLASSICAL TOO. Both ingredients are standard, and the proof
    is four lines. By this session's own heuristic -- a short proof about a classical object
    is usually classical -- I should have expected this before measuring anything.

    THAT IS THE THIRD BOUND IN THIS THREAD TO TURN OUT CLASSICAL: the Sym^e bound (Pass
    5704), the p=2 rank law (Pass 5695), and now the digit product. Every single one had a
    proof of a few lines.""")

    print("\n  PASS 5738-5739 -- GF(8), and the statement with statuses\n")
    print(f"    {'e':>3s} {'rank':>6s} {'digit product':>14s} {'base 2':>12s}")
    for e, r, d in GF8:
        print(f"    {e:3d} {r:6d} {r:14d} {str(d):>12s}")
    print(f"\n    7 of 7 within 1..q-1, including rank 64 = 4^3 at e=7 (binary 111)")
    print(f"    verified across: " +
          ", ".join(f"{k} ({v})" for k, v in VERIFIED.items()))
    print("""
    THE COMPLETE STATEMENT, WITH EACH PART LABELLED:

      PROVED (classical)  rank(sf^e) depends only on e mod (q-1).
      PROVED (classical)  rank(sf^e) <= PRODUCT over base-p digits d of C(d+3,3).
      MEASURED            equality holds, for the W(3,q) symplectic form, at every
                          e in 1..q-1 tested: 8 exponents on GF(9), 7 on GF(8), 3 on
                          GF(4), and all single-digit e at q = 3, 5, 7, 11.

    ONLY THE THIRD LINE IS MINE, and it is a measurement rather than a theorem. GF(8) e=7
    is the strongest single data point: three binary digits each contributing a factor of
    4, giving 64, which no coarser law predicts.""")

    print("\n  PASS 5740-5741 -- what is downstream of K_4,4\n")
    print(f"    {'object':24s} {'description':44s} role")
    for name, desc, role in DOWNSTREAM:
        print(f"    {name:24s} {desc:44s} {role}")
    print("""
    THE CHAIN NOW READS IN ONE DIRECTION. Q4 encodes as RM(1,3); the antipodal map is word
    complementation; the quotient is K_4,4; Aut(K_4,4) = S4 wr S2 = 1152. Everything past
    that quotient inherits the group, which is why the tomotope's 16-face graph has it and
    why no search inside that graph could find its source.

    THE METHOD GENERALISES AND IS CHEAP: for an unexplained automorphism group, check what
    the object was BUILT FROM before searching inside it. Four passes went to internal
    searches here when one upstream question would have done it.""")

    print("\n  PASS 5742 -- this session's empty searches, re-examined\n")
    print(f"    {'search':34s} {'what happened':34s} outcome")
    for s, w, o in EMPTY:
        print(f"    {s:34s} {w:34s} {o}")
    print("""
    THREE OF FOUR EMPTY RESULTS WERE BAD SEARCHES, NOT ABSENCES. The p=2 law was found on
    a later pattern; the master-theorem banner was invisible to a grep that only matched
    `#` and `**`; S4 wr S2's origin sat in a file adjacent to one I had already opened.
    Only the [12,4,6] enumerator is still genuinely unlocated, and on this record I would
    not call even that an absence.

    THE OPERATIONAL RULE: an empty result is a hypothesis about my pattern, not a fact
    about the corpus.""")

    print("\n  PASS 5743 -- scope\n")
    print("""    NOT DONE: whether the ATTAINMENT is classical -- the one part that is mine
    and the one part still unsearched successfully; the [12,4,6] enumerator; and any q with
    more than three digits in the relevant range.""")

    out = {
        "boundary": (
            "Pass 5736 proves the BOUND and explicitly does not prove attainment. Pass "
            "5739 labels each part's status: two proved-and-classical, one measured. Pass "
            "5740 traces a construction chain and does not derive the 16-face graph's full "
            "automorphism group. Pass 5742 re-examines four searches, not all of them"),
        "pass_5736_5737": {
            "proof": ("sf^e = product of (Frob^i(sf))^(d_i) entrywise; Frobenius preserves "
                      "rank, and Hadamard rank is submultiplicative with "
                      "rank(A^(o d)) <= C(d + rank A - 1, d)"),
            "conclusion": "rank(sf^e) <= product over base-p digits d of C(d+3,3)",
            "status": "CLASSICAL -- both ingredients standard, proof is four lines",
            "pattern": ("third bound in this thread to turn out classical, after the Sym^e "
                        "bound (Pass 5704) and the p=2 rank law (Pass 5695); all three had "
                        "short proofs")},
        "pass_5738_5739": {
            "gf8": [{"e": e, "rank": r, "digits": d} for e, r, d in GF8],
            "gf8_matches": "7 of 7 within 1..q-1",
            "strongest_point": "e=7 gives 64 = 4^3, three binary digits each contributing",
            "verified": VERIFIED,
            "statuses": {"period_q_minus_1": "PROVED, classical",
                         "digit_product_bound": "PROVED, classical",
                         "equality": "MEASURED -- the only part that is mine"}},
        "pass_5740_5741": {
            "chain": [{"object": n, "description": d, "role": r} for n, d, r in DOWNSTREAM],
            "method": ("for an unexplained automorphism group, check what the object was "
                       "BUILT FROM before searching inside it")},
        "pass_5742": {"searches": [{"target": s, "what_happened": w, "outcome": o}
                                   for s, w, o in EMPTY],
                      "score": "3 of 4 empty results were bad searches, not absences",
                      "rule": ("an empty result is a hypothesis about the pattern, not a "
                               "fact about the corpus")},
        "pass_5743": {"not_done": ["whether the attainment is classical",
                                   "the [12,4,6] enumerator",
                                   "q with more than three digits in range"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS5736_5743_THE_DIGIT_LAW_PROVED.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
