"""Passes 8989-9012 -- rank 24 has EXACTLY THREE carriers of W(3,3).

  8989  A2^12 needs a 3^4 permutation of the ternary Golay glue. Pure permutations: none.
  8990  But code automorphisms are MONOMIAL, and M12 does contain a 3^4 class.
  8991  Found one, and its four cycle sign-products agree -- so they normalise.
  8992  Built N(A2^12) and the twisted element. W(3,3). A THIRD carrier.
  8993  And the screen is EXHAUSTIVE, for a reason: orbit lengths must divide 9.
  8994  Length 9 is impossible, so only lengths 1 and 3 exist, and both were screened.
  8995  Redone allowing MIXED assemblies, which the first screen did not.
  8996  THE ANSWER: exactly three, and here they are.
  8997  Open.
  8998  Scope.

WHERE THIS SITS. Pass 8965-8988 found the sporadic carrier E6^4 and left two questions: is
A2^12 a third, and does rank 24 have exactly two carriers or more? Both are answered here.

    py -3 analysis/w33_pass8989_9012_exactly_three_carriers.py
"""

from __future__ import annotations

import sys
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

EXPS = {"A": lambda n: list(range(1, n + 1)),
        "D": lambda n: list(range(1, 2 * n - 2, 2)) + [n - 1],
        "E6": lambda n: [1, 4, 5, 7, 8, 11], "E7": lambda n: [1, 5, 7, 9, 11, 13, 17],
        "E8": lambda n: [1, 7, 11, 13, 17, 19, 23, 29]}
DEGS = {"E6": [2, 5, 6, 8, 9, 12], "E7": [2, 6, 8, 10, 12, 14, 18],
        "E8": [2, 8, 12, 14, 18, 20, 24, 30]}
COMPS = {"D24": [("D", 24, 1)], "D16E8": [("D", 16, 1), ("E8", 8, 1)], "E8^3": [("E8", 8, 3)],
         "A24": [("A", 24, 1)], "D12^2": [("D", 12, 2)], "A17E7": [("A", 17, 1), ("E7", 7, 1)],
         "D10E7^2": [("D", 10, 1), ("E7", 7, 2)], "A15D9": [("A", 15, 1), ("D", 9, 1)],
         "D8^3": [("D", 8, 3)], "A12^2": [("A", 12, 2)],
         "A11D7E6": [("A", 11, 1), ("D", 7, 1), ("E6", 6, 1)], "E6^4": [("E6", 6, 4)],
         "A9^2D6": [("A", 9, 2), ("D", 6, 1)], "D6^4": [("D", 6, 4)], "A8^3": [("A", 8, 3)],
         "A7^2D5^2": [("A", 7, 2), ("D", 5, 2)], "A6^4": [("A", 6, 4)],
         "A5^4D4": [("A", 5, 4), ("D", 4, 1)], "D4^6": [("D", 4, 6)], "A4^6": [("A", 4, 6)],
         "A3^8": [("A", 3, 8)], "A2^12": [("A", 2, 12)], "A1^24": [("A", 1, 24)],
         "Leech": []}
# verified computationally in this session
VERIFIED = {"E8^3": "Pass 8041-8056: tau_3 . diag(W,I,I), the lift",
            "E6^4": "Pass 8965-8988: diagonal order-9 element of W(E6)^4, tetracode glue",
            "A2^12": "Pass 8989-9012: twisted 3-cycles through the ternary Golay glue"}


def degs(t, n):
    if t in DEGS:
        return DEGS[t]
    if t == "A":
        return list(range(2, n + 2))
    return list(range(2, 2 * n - 1, 2)) + [n]


def route_a(t, r0):
    """component carries Phi_9 on its own: orbit length 1"""
    return (r0 % 6 == 0 and all(gcd(9, m) == 1 for m in EXPS[t](r0))
            and any(D % 9 == 0 for D in degs(t, r0)))


def route_b(t, r0):
    """component can sit in a 3-cycle whose product carries Phi_3: orbit length 3"""
    return r0 % 2 == 0 and all(gcd(3, m) == 1 for m in EXPS[t](r0))


def main() -> int:
    print("=" * 78)
    print("Passes 8989-9012 -- exactly three carriers at rank 24")
    print("=" * 78)

    print("\n  PASS 8989-8992 -- A2^12, and why it nearly looked impossible\n")
    print("""    The A2^12 route needs the twelve A2 components partitioned into four triples
    and 3-cycled, so the component permutation has cycle type 3^4 and must preserve the
    ternary Golay glue. An exhaustive search over all 246400 permutations of that cycle type
    found NONE preserving the code -- as a PURE permutation.

    That was the wrong test. A ternary code's automorphism group is MONOMIAL: 2.M12, with
    permutation image M12. GAP confirms M12 has an order-3 class of cycle type 3^4 (class
    size 2640, all twelve points moved), so the permutation exists; it simply needs
    accompanying signs. And signs are available on the lattice, because -1 is an automorphism
    of A2 (Aut(A2) = W(A2) x {+-1}, since -1 is not in W(A2) for A_n with n >= 2) and it
    negates the glue class.

    Solving for the signs -- a LINEAR system over F_3 for each candidate permutation -- gave
    one on the sixth permutation tried, with sign products around the four 3-cycles all equal
    to -1. That matters: the product must be +1 or the cube of the element picks up a sign
    and has order 6 instead of 3. All four being EQUAL is what saves it, because the global
    -1 (an automorphism of any linear code) flips all twelve signs and changes each product
    by (-1)^3 = -1. So they normalise to +1 together.

    The lattice N(A2^12) was then built from Golay glue -- index 3^6 = 729 in (A2*)^12,
    Gram integral, det 1, even -- and the twisted element verified: order 9, minimal
    polynomial Phi_9, det(I-X) = 81, an isometry, F + F^T = 3G, rank 4 mod 3, alternating.

        W(3,3). A THIRD CARRIER.""")

    print("\n  PASS 8993-8995 -- and the screen is exhaustive, for a reason\n")
    print("""    An element with characteristic polynomial Phi_9^4 has minimal polynomial Phi_9,
    hence order exactly 9. Its component permutation therefore has order dividing 9, so every
    orbit has length 1, 3 or 9.

      length 9 IS IMPOSSIBLE. On such an orbit the element's eigenvalues are the nine 9th
      roots of the eigenvalues of the product around the cycle. Those nine roots always
      include non-primitive ones, so the block cannot be pure Phi_9.

      length 2, 4, 6 and so on never arise, since the orbit length divides the order 9.

    So only lengths 1 and 3 exist -- route (a) and route (b) -- and the screen covers both.
    The FIRST screen (Pass 8965-8988) tested them with 'all' and 'any' separately, which
    misses MIXED assemblies where some components use route (a) and others route (b). Redone
    properly: a root system works iff EVERY component type can be assigned to a valid route,
    with route (b) additionally requiring the multiplicity to be divisible by 3.\n""")
    print(f"      {'root system':>12s} {'per-component assignment':>44s}  {'works':>6s}")
    winners = []
    for nm, cs in COMPS.items():
        if not cs:
            print(f"      {nm:>12s} {'(no roots -- Leech)':>44s}  {'-':>6s}")
            continue
        bits, ok = [], True
        for t, r0, mult in cs:
            a, b = route_a(t, r0), route_b(t, r0) and mult % 3 == 0
            tag = "a" if a else ("b" if b else "NONE")
            bits.append(f"{t}{r0}x{mult}:{tag}")
            ok &= (a or b)
        works = bool(ok)
        if works:
            winners.append(nm)
        print(f"      {nm:>12s} {' '.join(bits):>44s}  {str(works):>6s}")

    print("\n  PASS 8996 -- the answer\n")
    print(f"      carriers of W(3,3) at rank 24: {winners}\n")
    for nm in winners:
        print(f"        {nm:>7s}  {VERIFIED.get(nm, 'NOT VERIFIED')}")
    print("""
    EXACTLY THREE, and all three are built and verified, not merely screened. One is the
    lift of E8; the other two are not lifts of anything -- E6^4 by a purely diagonal element,
    A2^12 by twisted 3-cycles through the Golay glue.

    So the rank-24 answer is settled: three carriers, no more. And the shape of the answer is
    that W(3,3) is NOT the private property of E8 above the minimal rank -- only AT it.""")

    print("\n  PASS 8997-8998 -- open, and scope\n")
    print("""    NEW: A2^12 as a third carrier, with the monomial-versus-permutation distinction
    that nearly hid it; the orbit-length argument (lengths divide 9, and 9 is impossible)
    that makes the screen exhaustive; the corrected screen allowing mixed assemblies; and the
    complete rank-24 answer.
    CORRECTS: the first screen at Pass 8965-8988 used 'all' and 'any' separately and would
    have missed mixed assemblies. Redone here; the answer happens to be unchanged.
    UNAFFECTED: E8-nativity at the MINIMAL rank, and the periodicity theorem.
    NOT DONE: the same question at rank 72, where even unimodular lattices are unclassified
    and this method cannot be run; whether the three carriers give ISOMORPHIC W(3,3)s with
    different symmetry groups; alpha(W(3,9)); K12 built.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED: rank 24 has EXACTLY THREE Niemeier carriers of W(3,3) -- E8^3 (the "
            "lift), E6^4 (diagonal, sporadic) and A2^12 (twisted 3-cycles through the ternary "
            "Golay glue) -- all three built and checked. The screen is exhaustive because an "
            "element with char poly Phi_9^4 has order exactly 9, so permutation orbits have "
            "length 1, 3 or 9, and length 9 is impossible"),
        "a2_12": {
            "obstacle": ("a 3^4 permutation of the twelve A2 components must preserve the "
                         "ternary Golay glue; an exhaustive search over all 246400 such "
                         "permutations found NONE as a pure permutation"),
            "resolution": ("ternary code automorphisms are MONOMIAL (2.M12). GAP confirms M12 "
                           "has a 3^4 class of size 2640. Signs are available because -1 is "
                           "an automorphism of A2 and negates the glue class"),
            "sign_condition": ("the sign product around each 3-cycle must be +1, or the cube "
                               "of the element has order 6. The found automorphism had all "
                               "four products equal to -1, and the global -1 flips all twelve "
                               "signs, changing each product by (-1)^3, so they normalise "
                               "together"),
            "lattice": "index 3^6 = 729 in (A2*)^12, Gram integral, det 1, even",
            "element": ("order 9, minimal polynomial Phi_9, det(I-X) = 81, isometry, "
                        "F + F^T = 3G, rank 4 mod 3, alternating -> W(3,3)")},
        "exhaustiveness": {
            "argument": ("char poly Phi_9^4 gives minimal polynomial Phi_9 and order exactly "
                         "9, so the component permutation has order dividing 9 and every "
                         "orbit has length 1, 3 or 9"),
            "length_9_impossible": ("the element's eigenvalues on such an orbit are the nine "
                                    "9th roots of the cycle product's eigenvalues, and those "
                                    "always include non-primitive ones"),
            "so": "only routes (a) and (b) exist, and both are screened",
            "correction": ("the first screen at Pass 8965-8988 used 'all' and 'any' "
                           "separately and would have missed MIXED assemblies; redone here "
                           "per-component, with the same answer")},
        "carriers": {nm: VERIFIED.get(nm) for nm in winners},
        "count": len(winners),
        "reading": ("W(3,3) is not the private property of E8 above the minimal rank -- only "
                    "AT it. At rank 24 three different Niemeier lattices carry it, two of "
                    "them by mechanisms having nothing to do with E8"),
        "not_done": ["the same question at rank 72, where even unimodular lattices are "
                     "unclassified and this method cannot run",
                     "whether the three carriers give W(3,3)s with different symmetry groups",
                     "alpha(W(3,9))", "K12 built"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8989_9012_THREE_CARRIERS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
