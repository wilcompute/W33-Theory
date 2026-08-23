"""Passes 9301-9324 -- why W(3,3) is rare at rank 24 and the qubit geometries are not.

  9301  The p=2 analogue of the three-carrier theorem, screened.
  9302  Orbit lengths for order 4: 1, 2 or 4, and 4 is impossible.
  9303  LENGTH 2 IS THE DIFFERENCE. It works for every component type, always.
  9304  18 of 23 root systems admit Phi_4^12 arithmetically, against 3 of 24 for Phi_9^4.
  9305  And the d=2 rung is UNIVERSAL: every Niemeier lattice has it, no glue check needed.
  9306  THE REASON: orbit lengths divide the element order, and 2 | 4 while 2 does not | 9.
  9307  So the rarity of W(3,3) traces to a parity fact about 9, not to anything about E8.
  9308  What is verified here, and what is only arithmetic.
  9309  Open.
  9310  Scope.

WHERE THIS SITS. Pass 8989-9012 settled the qutrit question at rank 24: exactly three
Niemeier carriers of W(3,3), all built. The obvious companion question -- how many carry the
QUBIT geometries -- had not been asked, and the answer turns out to explain the qutrit one.

CROSS-LANE NOTE. The other lane has since built on the three-carrier classification
(analysis/w33_rank24_root_shadow_core.py cites "the three exact rank-24 carriers classified
in Pass 8989-9012") and taken it toward root shadows and the E6 line stabiliser. This pass
goes the other way, to p=2, and does not overlap that work.

    py -3 analysis/w33_pass9301_9324_why_qutrits_are_rare.py
"""

from __future__ import annotations

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
from scipy.linalg import block_diag  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN  # noqa: E402

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
         "A3^8": [("A", 3, 8)], "A2^12": [("A", 2, 12)], "A1^24": [("A", 1, 24)]}
QUTRIT_CARRIERS = ["E8^3", "E6^4", "A2^12"]


def degs(t, n):
    if t in DEGS:
        return DEGS[t]
    if t == "A":
        return list(range(2, n + 2))
    return list(range(2, 2 * n - 1, 2)) + [n]


def len1_phi4(t, n):
    """component alone carries Phi_4: needs even rank, all exponents odd, 4 | a degree"""
    return n % 2 == 0 and all(m % 2 == 1 for m in EXPS[t](n)) and any(D % 4 == 0
                                                                     for D in degs(t, n))


def rank_mod2(A):
    B = (np.array(A, dtype=np.int64) % 2).astype(np.int64)
    n, m = B.shape
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if B[i, c]), None)
        if piv is None:
            continue
        B[[r, piv]] = B[[piv, r]]
        for i in range(n):
            if i != r and B[i, c]:
                B[i] = (B[i] + B[r]) % 2
        r += 1
    return r


def main() -> int:
    print("=" * 78)
    print("Passes 9301-9324 -- why qutrits are rare at rank 24")
    print("=" * 78)

    print("\n  PASS 9301-9303 -- the orbit argument at p = 2\n")
    print("""    An element with char poly Phi_4^12 has minimal polynomial Phi_4, hence order
    exactly 4, so its component permutation has orbits of length 1, 2 or 4.

      LENGTH 4 IS IMPOSSIBLE, for the same reason length 9 was at p=3: the eigenvalues on
      such an orbit are the four 4th roots of the cycle product's eigenvalues, and those
      always include a non-primitive one.

      LENGTH 1 needs the component to carry Phi_4 alone: even rank, all exponents odd, and
      4 dividing a degree. That holds for D_n with n even, and for E8.

      LENGTH 2 IS THE DIFFERENCE. The 2-cycle product must be -I on the component, and -1
      is an automorphism of EVERY lattice. So length 2 is arithmetically available for ANY
      component type, with no condition at all -- only an even multiplicity.

    At p=3 there was no such route. Orbit lengths divide the order 9, which is ODD, so
    length 2 never arises and every component had to satisfy the 9-coprimality condition
    individually or sit in a 3-cycle.""")

    print("\n  PASS 9304 -- the screen, and the contrast\n")
    print(f"      {'root system':>10s} {'assignment':>38s} {'Phi_4^12':>9s} {'Phi_9^4':>8s}")
    ok_list = []
    rows = []
    for nm, cs in COMPS.items():
        bits, ok = [], True
        for t, n, mult in cs:
            a, b = len1_phi4(t, n), mult % 2 == 0
            bits.append(f"{t}{n}x{mult}:" + ("len1" if a else ("pair" if b else "NONE")))
            ok &= (a or b)
        if ok:
            ok_list.append(nm)
        q = nm in QUTRIT_CARRIERS
        rows.append({"root_system": nm, "phi4_admissible": bool(ok), "phi9_carrier": bool(q)})
        print(f"      {nm:>10s} {' '.join(bits):>38s} {str(ok):>9s} {str(q):>8s}")
    print(f"""
      Phi_4^12 (six qubits): {len(ok_list)} of 23 root systems admissible
      Phi_9^4  (two qutrits): {len(QUTRIT_CARRIERS)} of 24, and those are PROVEN, all built

      failures at p=2: {[n for n in COMPS if n not in ok_list]}
      -- exactly the systems with an odd-multiplicity component that cannot stand alone.""")

    print("\n  PASS 9305 -- and the d=2 rung is universal\n")
    print("""    The order-2 element is -I, which is an automorphism of EVERY lattice. So
    L/2L = F_2^24 exists for all 24 Niemeier lattices with no glue check whatsoever. (Per
    Pass 8925-8940 that rung is really ORTHOGONAL rather than symplectic, since an even
    lattice gives L/2L a quadratic form; the point here is only that it always exists.)

    So the three p=2 rungs at rank 24 go: universal at order 2, common at order 4, and the
    order-8 rung sits between. The p=3 rung is the rare one.""")

    print("\n  PASS 9306-9307 -- the reason, stated plainly\n")
    print("""        Orbit lengths divide the element order.
        For Phi_4 the order is 4, which is EVEN, so length 2 is available -- and length 2
        needs nothing but -1, which every lattice has.
        For Phi_9 the order is 9, which is ODD, so length 2 is unavailable, and the only
        routes are "component carries Phi_9 alone" or "three components in a cycle".

    THE RARITY OF W(3,3) AT RANK 24 IS A PARITY FACT ABOUT 9, not a fact about E8. Nothing
    in the argument mentions E8 at all; E8^3 is simply one of the three systems that happens
    to satisfy the 3-cycle condition. That also sharpens what E8-nativity does and does not
    say: E8 is forced at the MINIMAL rank 8, where the even unimodular lattice is unique.
    At rank 24 it has no privilege -- it is one of three, and two of the three have nothing
    to do with it.""")

    print("\n  PASS 9308 -- what is verified and what is only arithmetic\n")
    M4 = np.loadtxt(ROOT / "analysis" / "_e8_ord4.txt", dtype=np.int64)
    G3 = block_diag(CARTAN, CARTAN, CARTAN).astype(np.int64)
    J = block_diag(M4, M4, M4).astype(np.int64)
    I24 = np.eye(24, dtype=np.int64)
    F = (I24 + J).T @ G3
    rk = rank_mod2(F)
    check = {"J^2 = -I": bool(np.array_equal(J @ J, -I24)),
             "preserves the E8^3 form": bool(np.array_equal(J.T @ G3 @ J, G3)),
             "det(I-J) = 2^12": int(round(np.linalg.det((I24 - J).astype(float)))) == 4096,
             "rank(F) mod 2 = 12": rk == 12,
             "alternating": bool(all(int(F[i, i]) % 2 == 0 for i in range(24)))}
    for k, v in check.items():
        print(f"      E8^3 at order 4 -- {k:32s} {v}")
    print(f"      -> W({rk-1},2), {rk // 2} qubits, on E8^3\n")
    print("""    VERIFIED six-qubit carriers: Leech (Pass 7333-7340) and E8^3 (above, and Pass
    8041-8056). The other sixteen admissible systems are ARITHMETIC ONLY -- the screen shows
    no obstruction, but the glue constraint is not checked for them. A pairing element must
    also preserve the glue code, and that is a real condition: it is exactly what nearly
    killed A2^12 at p=3, where the pure-permutation search failed and only the MONOMIAL
    lift worked. So "18 admissible" is an upper bound on the count, not the count.""")

    print("\n  PASS 9309-9310 -- open, and scope\n")
    print("""    NEW: the p=2 orbit argument (lengths 1, 2, 4 with 4 impossible); the
    observation that length 2 is universally available because every lattice has -1; the
    screen giving 18 of 23 admissible against 3 of 24 proven at p=3; and the identification
    of the CAUSE as the parity of the element order rather than anything about E8.
    VERIFIED: Leech and E8^3 as six-qubit carriers. The other sixteen are arithmetic only.
    NOT DONE: the glue check for the sixteen, which would turn the upper bound into a count;
    the order-8 (three-qubit) screen; alpha(W(3,9)); K12 built.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "The p=2 analogue of the rank-24 qutrit classification. Orbit lengths for a "
            "Phi_4^12 element are 1, 2 or 4 with 4 impossible, and LENGTH 2 is available for "
            "any component type because -1 is an automorphism of every lattice. That gives "
            "18 of 23 root systems arithmetically admissible for six qubits, against exactly "
            "3 of 24 PROVEN for two qutrits. The cause is parity: orbit lengths divide the "
            "element order, and 2 divides 4 but not 9. The rarity of W(3,3) at rank 24 is "
            "therefore a fact about 9 being odd, not a fact about E8"),
        "orbit_argument_p2": {
            "order": 4, "orbit_lengths": [1, 2, 4],
            "length_4_impossible": ("the eigenvalues are the four 4th roots of the cycle "
                                    "product's eigenvalues and always include a non-primitive "
                                    "one"),
            "length_1_condition": "even rank, all exponents odd, 4 | a degree (D_even and E8)",
            "length_2_condition": ("the 2-cycle product must be -I, which every lattice "
                                   "admits; so the only condition is even multiplicity")},
        "screen": rows,
        "counts": {"phi4_admissible_of_23": len(ok_list),
                   "phi9_carriers_of_24": len(QUTRIT_CARRIERS),
                   "phi4_failures": [n for n in COMPS if n not in ok_list]},
        "d2_rung_universal": ("the order-2 element is -I, an automorphism of every lattice, "
                              "so L/2L exists for all 24 Niemeier lattices with no glue "
                              "check. Per Pass 8925-8940 that rung is orthogonal rather than "
                              "symplectic"),
        "the_reason": {
            "statement": ("orbit lengths divide the element order. Phi_4 has order 4, which "
                          "is EVEN, so length 2 is available and needs nothing but -1. Phi_9 "
                          "has order 9, which is ODD, so length 2 is unavailable"),
            "consequence": ("the rarity of W(3,3) at rank 24 is a parity fact about 9, and "
                            "nothing in the argument mentions E8"),
            "sharpens": ("E8-nativity is forced at the MINIMAL rank 8, where the even "
                         "unimodular lattice is unique. At rank 24 E8 has no privilege -- it "
                         "is one of three carriers and two have nothing to do with it")},
        "verified_qubit_carriers": {
            "Leech": "Pass 7333-7340",
            "E8^3": {**{k: bool(v) for k, v in check.items()},
                     "geometry": f"W({rk-1},2)", "qubits": rk // 2}},
        "honest_limit": ("the other sixteen admissible systems are ARITHMETIC ONLY. A pairing "
                         "element must also preserve the glue code, which is a real condition "
                         "-- it is what nearly killed A2^12 at p=3, where the pure-permutation "
                         "search failed and only the monomial lift worked. So 18 is an UPPER "
                         "BOUND on the count, not the count"),
        "not_done": ["the glue check for the sixteen, turning the bound into a count",
                     "the order-8 (three-qubit) screen", "alpha(W(3,9))", "K12 built"],
    }
    fp = ROOT / "data" / "PART_W33_PASS9301_9324_WHY_QUTRITS_ARE_RARE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
