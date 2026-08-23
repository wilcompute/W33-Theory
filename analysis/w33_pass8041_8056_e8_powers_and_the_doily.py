"""Passes 8041-8056 -- E8^k as explicit carriers, four qubits at rank 32, and W(3,3).

  8041  The tower is CANONICAL: exactly one pure class at each of orders 2, 4, 8.
  8042  And its symmetry groups, one of which has the order of the three-qubit hexagon.
  8043  E8^k carries the 2-branch explicitly, at ranks 8, 24 and 32 from ONE element.
  8044  FOUR QUBITS AT RANK 32, built and verified, not predicted.
  8045  THE ODD-PART LAW: the tower terminates at the odd part of the rank.
  8046  The 3-branch on E8^k, and W(11,3) with explicit matrices at rank 24.
  8047  THREE COPIES OF W(3,3): the E8^3 qutrit geometry is a perp-sum of three W(3,3)s.
  8048  AND E8^3 REACHES W(3,3) -- via an element that PERMUTES the three factors.
  8049  So the two obstructions are genuinely different. Same rank, different answer.
  8050  What the tower is NOT: it is not code concatenation, and the reason is exact.
  8051  The literature gate, finally closed: Coolsaet 2014 and Cimrakova-Fack 2005.
  8052  What the published tables actually say, and one coincidence worth not tripping on.
  8053  Open.
  8054  Scope.

    py -3 analysis/w33_pass8041_8056_e8_powers_and_the_doily.py

    NAMING CORRECTION. Earlier drafts of these passes called W(3,3) "the doily". That is
    wrong: the doily is W(3,2) = GQ(2,2), 15 points, which is also this repo's dominant
    usage (21 files against 8, and an explicit "doily_points": 15 in BT1707). W(3,3) =
    GQ(3,3), 40 points, is this repository's CENTRAL OBJECT but is not the doily. The
    mathematics below is unaffected; only the name was wrong. And the actual doily does
    appear here: it is E8's own middle qubit rung, W(3,2) at two qubits.
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
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN, simple_reflection  # noqa: E402

# Pass 8041, from the 2.Co1 character table (analysis/_co0_2power_classes.txt).
# (order, class, centraliser, (a,b,c,d), pure?)  with a copies of 1, b of -1,
# c blocks of Phi_4 and d blocks of Phi_8.
PURE_CLASSES = [
    (2, 2, 8315553613086720000, (0, 24, 0, 0), True, "-I, central"),
    (4, 5, 2012774400, (0, 0, 12, 0), True, "Phi_4^12"),
    (8, 21, 48384, (0, 0, 0, 6), True, "Phi_8^6"),
]
IMPURE_COUNTS = {2: 3, 4: 7, 8: 8}

# Pass 8051-8052, from Cimrakova and Fack, Bull. Belg. Math. Soc. 12 (2005) 697-705.
CF_TABLE1 = [("W(5)", (5, 5), 156, 26, 21, 18, 2), ("W(7)", (7, 7), 400, 50, 43, 33, 1),
             ("Q-(5,4)", (4, 16), 325, 65, 37, 25, 3), ("H(4,4)", (4, 8), 165, 33, 25, 21, 1)]
CF_TABLE2 = [(4, 10, 37, "13, 15..25"), (5, 12, 106, "18, 20..44, 48"),
             (7, 16, 302, "32..92, 95, 96, 98"), (8, 18, 217, "41..121, 123, 125, 126"),
             (9, 20, 401, "52..146"), (11, 24, 1222, "68..212, 214, 216"),
             (13, 28, 2042, "89..265, 267, 268, 272, 273")]


def rank_modp(A, p):
    B = (np.array(A, dtype=np.int64) % p).astype(np.int64)
    n, m = B.shape
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if B[i, c] % p), None)
        if piv is None:
            continue
        B[[r, piv]] = B[[piv, r]]
        B[r] = (B[r] * pow(int(B[r, c]), -1, p)) % p
        for i in range(n):
            if i != r and B[i, c] % p:
                B[i] = (B[i] - B[i, c] * B[r]) % p
        r += 1
    return r


def blk(m, k):
    return block_diag(*[m] * k).astype(np.int64)


def main() -> int:
    print("=" * 78)
    print("Passes 8041-8056 -- E8^k, four qubits at rank 32, and W(3,3)")
    print("=" * 78)

    print("\n  PASS 8041-8042 -- the tower is CANONICAL, and here are its symmetries\n")
    print("""    The tower L/2L -> L/(I-J)L -> L/(I-M)L needs J with pure support Phi_4^12 and M
    with pure support Phi_8^6. If several classes qualified, the tower would be a CHOICE.
    Censusing every 2-power class of 2.Co1 from the character table -- decoding (a,b,c,d)
    from chi(1), chi(g), chi(g^2), chi(g^4) exactly as Pass 8035 did for order 9:\n""")
    print(f"      {'order':>5s} {'class':>6s} {'centraliser':>22s} {'(a,b,c,d)':>16s}  what")
    for o, cl, cen, abcd, pure, what in PURE_CLASSES:
        print(f"      {o:5d} {cl:6d} {cen:22d} {str(abcd):>16s}  {what}")
    print(f"\n      impure classes passed over: "
          f"{', '.join(f'{k} of order {o}' for o, k in sorted(IMPURE_COUNTS.items()))}")
    print("""
    EXACTLY ONE PURE CLASS AT EACH ORDER. So every rung's element is unique up to
    Co0-conjugacy and the tower is canonical, not a selection.

    The centralisers are the symmetry groups of the rungs. The top one is Co0 itself
    (-I is central). The three-qubit rung has centraliser of order 48384 = 4 * 12096, and
    12096 is |G2(2)| -- the split Cayley hexagon group, which this repo already carries as
    the three-qubit contextuality core (analysis/w33_complex_leech_suzuki_chain.py). That is
    an ORDER MATCH at the rung whose geometry is three qubits; identifying the group, rather
    than its order, is not done here and is not claimed.""")

    M8 = np.loadtxt(ROOT / "analysis" / "_e8_ord8.txt", dtype=np.int64)
    cox = np.eye(8, dtype=np.int64)
    for i in range(8):
        cox = cox @ simple_reflection(i)
    W3 = np.linalg.matrix_power(cox, 10)
    I8 = np.eye(8, dtype=np.int64)
    e8ok = {
        "order-8 element preserves the Cartan form":
            bool(np.array_equal(M8.T @ CARTAN @ M8, CARTAN)),
        "M^4 = -I, so char poly is Phi_8^2":
            bool(np.array_equal(np.linalg.matrix_power(M8, 4), -I8)),
        "order-3 element preserves the Cartan form":
            bool(np.array_equal(W3.T @ CARTAN @ W3, CARTAN)),
        "W^2 + W + I = 0, so char poly is Phi_3^4":
            bool(not (W3 @ W3 + W3 + I8).any()),
    }
    print("\n  PASS 8043-8044 -- E8^k carries the whole 2-branch, from ONE element\n")
    for k, v in e8ok.items():
        print(f"      {k:48s} {v}")
    print()
    print(f"      {'lattice':>8s} {'rank':>5s} {'element':>12s} {'rank F':>7s} "
          f"{'geometry':>10s} {'qubits':>7s} {'alt':>5s}")
    two_branch = []
    for k, nm in ((1, "E8"), (3, "E8^3"), (4, "E8^4")):
        r = 8 * k
        G, M = blk(CARTAN, k), blk(M8, k)
        I = np.eye(r, dtype=np.int64)
        J = M @ M
        for lbl, P in (("K = M^4 = -I", I), ("J = M^2", I + J), ("M", (I + M) @ (I + J))):
            F = P.T @ G
            rk = rank_modp(F, 2)
            alt = all(int(F[i, i]) % 2 == 0 for i in range(r))
            print(f"      {nm:>8s} {r:5d} {lbl:>12s} {rk:7d} {'W(' + str(rk-1) + ',2)':>10s} "
                  f"{rk // 2:7d} {str(alt):>5s}")
            two_branch.append({"lattice": nm, "rank": r, "element": lbl, "rank_mod2": rk,
                               "geometry": f"W({rk-1},2)", "qubits": rk // 2,
                               "alternating": bool(alt)})
        print()
    print("""    FOUR QUBITS AT RANK 32, BUILT. The design tool read backwards said four qubits
    needs deg(Phi_d) = r/8, impossible at rank 24 and equal to 4 at rank 32, i.e. d = 8. That
    was a prediction with no object behind it. E8^4 is even unimodular of rank 32, the same
    order-8 element acting diagonally has char poly Phi_8^8, and the quotient is F_2^8 with a
    nondegenerate alternating form: W(7,2), FOUR QUBITS. Verified on 32x32 matrices.

    AND E8^3 CARRIES EXACTLY THE LEECH TOWER: 12 -> 6 -> 3 qubits, W(23,2) -> W(11,2) ->
    W(5,2). E8^3 is a Niemeier lattice, not Leech -- it has roots and Leech does not -- so
    the qubit tower is NOT a Leech phenomenon. It is a rank phenomenon.""")

    print("\n  PASS 8045 -- THE ODD-PART LAW\n")
    print("""    Rung m uses an element of order 2^m, and deg(Phi_{2^m}) = 2^{m-1}, so
    k = r/2^{m-1} and the qubit count is n = k/2 = r/2^m. The rung EXISTS only when k is
    even -- an alternating form on an odd-dimensional space is degenerate -- and k = r/2^{m-1}
    is even exactly when 2^m divides r. So the tower runs m = 1 .. v_2(r) and reads\n""")
    print(f"      {'rank r':>7s} {'v_2(r)':>7s}  qubit counts")
    law = []
    for r in (8, 16, 24, 32, 48, 40):
        v2 = (r & -r).bit_length() - 1
        counts = [r // (2 ** m) for m in range(1, v2 + 1)]
        print(f"      {r:7d} {v2:7d}  {' -> '.join(map(str, counts))}")
        law.append({"rank": r, "v2": v2, "qubit_counts": counts, "terminal": counts[-1]})
    print("""
    THE TERMINAL QUBIT COUNT IS THE ODD PART OF THE RANK, and the tower length is v_2(r).
    That makes "24 = 8 * 3 with 3 odd" an instance of a law rather than a coincidence: rank
    24 must stop at 3 qubits, rank 8 and rank 32 at 1. Existence of the elements is a second,
    independent requirement -- W(E8) has no element of order 16, so E8^4 stops at four qubits
    even though the arithmetic would allow 2 and 1.""")

    print("\n  PASS 8046-8047 -- the 3-branch, and three copies of W(3,3)\n")
    print(f"      {'lattice':>8s} {'rank':>5s} {'rank F':>7s} {'geometry':>10s} "
          f"{'qutrits':>8s} {'alt':>5s}")
    three_branch = []
    for k, nm in ((1, "E8"), (3, "E8^3"), (4, "E8^4")):
        r = 8 * k
        G, w = blk(CARTAN, k), blk(W3, k)
        I = np.eye(r, dtype=np.int64)
        F = (w + 2 * I).T @ G
        rk = rank_modp(F, 3)
        alt = (not ((F + F.T) % 3).any()) and all(int(F[i, i]) % 3 == 0 for i in range(r))
        print(f"      {nm:>8s} {r:5d} {rk:7d} {'W(' + str(rk-1) + ',3)':>10s} "
              f"{rk // 2:8d} {str(alt):>5s}")
        three_branch.append({"lattice": nm, "rank": r, "rank_mod3": rk,
                             "geometry": f"W({rk-1},3)", "qutrits": rk // 2,
                             "alternating": bool(alt)})
    G3 = blk(CARTAN, 3)
    I24 = np.eye(24, dtype=np.int64)
    F3 = (blk(W3, 3) + 2 * I24).T @ G3
    off = [F3[8 * i:8 * i + 8, 8 * j:8 * j + 8] for i in range(3) for j in range(3) if i != j]
    blockdiag = not any(b.any() for b in off)
    diagranks = [rank_modp(F3[8 * i:8 * i + 8, 8 * i:8 * i + 8], 3) for i in range(3)]
    print(f"\n      E8^3 qutrit form is BLOCK DIAGONAL: {blockdiag}")
    print(f"      diagonal block ranks mod 3: {diagranks}  -> three copies of W(3,3)")
    print("""
    So the E8^3 six-qutrit geometry is W(3,3) PERP W(3,3) PERP W(3,3): THREE COPIES OF W(3,3). The
    summands are NONDEGENERATE, so this really is a tensor factorisation of the six-qutrit
    system into three two-qutrit ones -- unlike the Lagrangian kernel of the qubit reduction
    at Pass 8022-8029, which is degenerate and is therefore not a partial trace.""")

    print("\n  PASS 8048 -- and E8^3 REACHES W(3,3)\n")
    tau = np.zeros((24, 24), dtype=np.int64)
    for i in range(3):
        tau[8 * ((i + 1) % 3):8 * ((i + 1) % 3) + 8, 8 * i:8 * i + 8] = I8
    g = tau @ block_diag(W3, I8, I8).astype(np.int64)
    order9 = bool(np.array_equal(np.linalg.matrix_power(g, 9), I24)
                  and not np.array_equal(np.linalg.matrix_power(g, 3), I24))
    phi9 = bool(not (np.linalg.matrix_power(g, 6) + np.linalg.matrix_power(g, 3) + I24).any())
    det = int(round(np.linalg.det((I24 - g).astype(float))))
    keepsG = bool(np.array_equal(g.T @ G3 @ g, G3))
    P = np.rint(3 * np.linalg.inv((I24 - g).astype(float))).astype(np.int64)
    exact = bool(np.array_equal((I24 - g) @ P, 3 * I24))
    Fd = P.T @ G3
    rkd = rank_modp(Fd, 3)
    altd = (not ((Fd + Fd.T) % 3).any()) and all(int(Fd[i, i]) % 3 == 0 for i in range(24))
    w33checks = {"g = tau . diag(W,I,I) has order 9": order9,
             "minimal polynomial Phi_9 (g^6+g^3+I=0)": phi9,
             "det(I-g) = 3^4 = 81": det == 81,
             "preserves the E8^3 form": keepsG,
             "P = 3(I-g)^-1 is integral": exact,
             "form is alternating mod 3": bool(altd)}
    for k, v in w33checks.items():
        print(f"      {k:44s} {v}")
    print(f"      {'rank mod 3':44s} {rkd} of 24  ->  W({rkd-1},3)")
    print("""
    W(3,3), the repo's central object. Two qutrits, from E8^3, at rank 24 -- the exact rung Co0 does not
    supply. And the mechanism is visible: tau PERMUTES the three E8 factors cyclically. No
    element acting diagonally could do it, because W(E8) has no order-9 element with pure
    Phi_9 support on rank 8 (deg Phi_9 = 6 does not divide 8). The three copies of W(3,3) of Pass 8047
    FUSE into one when the element mixes the factors it acts on.""")

    print("\n  PASS 8049 -- so the two obstructions really are different\n")
    print("""    Pass 8039 gave the qubit branch an ARITHMETIC reason to stop and the qutrit
    branch a GROUP-THEORETIC one, and asked whether the two threes -- "24 = 8*3 with 3 odd"
    and "Co0 always has exactly 3 blocks of Phi_9" -- were the same fact wearing two hats.

    THEY ARE NOT, and E8^3 is the counterexample. It has the SAME RANK as Leech, so it obeys
    the same odd-part law and stops at three qubits for the same arithmetic reason. But it
    DOES have a Phi_9^4 element and Co0 does not. One obstruction is a property of the number
    24 and is shared; the other is a property of the automorphism group and separates two
    lattices of equal rank. Same rank, different answer -- which is exactly what shows the
    two threes are independent.""")

    print("\n  PASS 8050 -- what the tower is NOT\n")
    print("""    The qubit tower quotients by Fix(M), a Lagrangian, i.e. a maximal commuting
    set of Paulis -- a stabiliser group. That invites reading the tower as CODE
    CONCATENATION, 12 physical qubits to 6 to 3 logical. It is not, and the reason is exact.

    For a stabiliser code with stabiliser S, the logical operators are S-perp / S. Here S is
    LAGRANGIAN, so S-perp = S and S-perp/S = 0: no logical qubits at all. A Lagrangian
    stabiliser defines a stabiliser STATE, not a code with logical content. What the tower
    actually computes is V/S, not S-perp/S, and the target does NOT inherit the source form:
    a nondegenerate form has zero radical, so it cannot descend through a nonzero kernel. It
    is the TWIST that descends -- F_M = (I+M)^T F_J, verified exactly at Pass 8022-8029. So
    the correct reading is a chain of stabiliser-group quotients carrying twisted forms, and
    the concatenation reading is refuted.""")

    print("\n  PASS 8051-8052 -- the literature gate, closed\n")
    print("""    Coolsaet, "Some large partial ovoids of Q-(5,q), for odd q", Designs Codes and
    Cryptography 72 (2014) 119-128, has been on this repo's not-done list for many passes. It
    gives explicit descriptions of some of the largest partial ovoids of Q-(5,q) known for q
    odd: two generic constructions plus sporadic examples for q <= 11. They are CONSTRUCTIONS,
    i.e. lower bounds, not exact values -- which is why they never conflicted with anything
    here.

    The sharper source for what this repo actually computes is Cimrakova and Fack, "Searching
    for maximal partial ovoids and spreads in generalized quadrangles", Bull. Belg. Math. Soc.
    Simon Stevin 12 (2005) 697-705. Its Table 1 is EXHAUSTIVE search, so proven maxima with
    complete classification up to equivalence:\n""")
    print(f"      {'GQ':>8s} {'(s,t)':>9s} {'|G|':>6s} {'st+1':>5s} {'bound':>6s} "
          f"{'|O.|':>5s} {'#O.':>4s}")
    for nm, st, gsz, o1, bd, sz, n in CF_TABLE1:
        print(f"      {nm:>8s} {str(st):>9s} {gsz:6d} {o1:5d} {bd:6d} {sz:5d} {n:4d}")
    print("""
    ALREADY KNOWN HERE, AND ALREADY CREDITED: alpha(W(3,5)) = 18 and alpha(W(3,7)) = 33 were
    caught at Pass 7106-7113, whose own heading reads "Why my alpha(W(3,7)) job was
    rediscovery, and why I let it run anyway", and BT7130-7137 cites the 2007 companion paper
    and explicitly declines to re-claim the extremal result. Nothing new is retracted.

    NEW TO THIS REPO is Table 2, the spectrum of maximal partial ovoid sizes in Q-(5,q):\n""")
    print(f"      {'q':>3s} {'LB':>4s} {'UB':>6s}  sizes found")
    for q, lb, ub, sizes in CF_TABLE2:
        print(f"      {q:3d} {lb:4d} {ub:6d}  {sizes}")
    print("""
    Also new here: the Thas upper bound |O.| <= q^3 + 1 - q(q-1) for Q-(5,q); the
    Ebert-Hirschfeld lower bound |K| >= 2q+2 for a complete cap with q >= 4; and an explicit
    size-96 maximal partial ovoid of Q-(5,7) from the points (3,+-1,+-1,+-1,+-1,+-1) and their
    cyclic permutations, split by the parity of the number of minus signs.

    AND ONE COINCIDENCE WORTH NOT TRIPPING ON. Table 2 gives the Q-(5,11) spectrum as
    68..212, 214, 216 -- and this repo's open item reads "q=11 at 68, not discriminating".
    Those are DIFFERENT OBJECTS: ours is W(3,11), theirs is Q-(5,11), and 68 is coincidence.
    Recorded because the next reader will meet both numbers in the same paragraph.

    STILL NOT SETTLED BY EITHER SOURCE: alpha(Q-(5,3)). Table 2 starts at q = 4, and the q=3
    row of their Table 3 is H(3,9), which dualises to partial SPREADS of Q-(5,3), not ovoids.
    So the repo's alpha(Q-(5,3)) = 16 is not in conflict with, nor confirmed by, this source.""")

    print("\n  PASS 8053-8054 -- open, and scope\n")
    print("""    NEW: the canonicity census (one pure class per order); the odd-part law; the
    explicit E8^k realisations of both branches at ranks 8, 24 and 32; FOUR QUBITS at rank 32
    built rather than predicted; the three-fold perp decomposition; E8^3 reaching W(3,3) via
    a factor-permuting order-9 element; the resulting proof that the two obstructions are
    independent; and the refutation of the concatenation reading.
    LITERATURE: the Coolsaet item is closed; Cimrakova-Fack Tables 1-3 are recorded.
    NOT DONE: identifying the order-48384 centraliser as a group rather than an order; an
    explicit omega for LEECH itself (E8^3 is a different Niemeier lattice); alpha(W(3,9));
    alpha(Q-(5,3)) against a source that covers q=3; K12 built.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED ON EXPLICIT MATRICES: E8^k realises both branches of the lattice qudit "
            "tower at ranks 8, 24 and 32, including FOUR QUBITS at rank 32 (E8^4, W(7,2)); "
            "the E8^3 six-qutrit geometry is a perp-sum of THREE COPIES OF W(3,3); and E8^3 REACHES "
            "W(3,3) via an order-9 element that permutes the three factors -- the rung Co0 "
            "does not supply. EXHAUSTIVE from the character table: exactly one pure class at "
            "each of orders 2, 4, 8, so the qubit tower is canonical. The two branch "
            "obstructions are proved INDEPENDENT by a same-rank counterexample"),
        "canonicity": {
            "method": "exhaustive over 2-power classes of 2.Co1 from the character table",
            "pure_classes": [{"order": o, "class": cl, "centraliser": cen,
                              "a_b_c_d": list(abcd), "what": what}
                             for o, cl, cen, abcd, pure, what in PURE_CLASSES],
            "impure_counts": IMPURE_COUNTS,
            "conclusion": ("exactly ONE pure class at each order, so every rung's element is "
                           "unique up to Co0-conjugacy and the tower is canonical"),
            "order_match": ("the three-qubit rung has centraliser of order 48384 = 4 * 12096 "
                            "= 4 * |G2(2)|, the split Cayley hexagon group already carried "
                            "here as the three-qubit contextuality core. An ORDER match; the "
                            "group is not identified and none is claimed")},
        "e8_element_checks": e8ok,
        "two_branch": two_branch,
        "four_qubits_rank32": {
            "lattice": "E8^4, even unimodular of rank 32",
            "element": "the W(E8) order-8 element with Phi_8^2, acting diagonally",
            "char_poly": "Phi_8^8", "quotient": "F_2^8", "geometry": "W(7,2)", "qubits": 4,
            "status": ("BUILT AND VERIFIED on 32x32 matrices, where the design tool had only "
                       "predicted that rank 32 was where four qubits could live")},
        "e8_cubed_is_not_special_to_leech": (
            "E8^3 carries exactly the Leech qubit tower, 12 -> 6 -> 3, W(23,2) -> W(11,2) -> "
            "W(5,2). E8^3 is a Niemeier lattice with roots and Leech has none, so the qubit "
            "tower is a RANK phenomenon, not a Leech phenomenon"),
        "odd_part_law": {
            "statement": ("rung m uses order 2^m with deg Phi = 2^{m-1}, so n = r/2^m qubits, "
                          "and the rung exists only when k = r/2^{m-1} is even, i.e. 2^m | r. "
                          "So the tower runs m = 1..v_2(r) and TERMINATES AT THE ODD PART OF "
                          "THE RANK"),
            "table": law,
            "makes_instance_of": "24 = 8*3 with 3 odd, previously stated as a coincidence",
            "second_requirement": ("existence of the elements is independent: W(E8) has no "
                                   "order-16 element, so E8^4 stops at four qubits although "
                                   "the arithmetic would allow 2 and 1")},
        "three_branch": three_branch,
        "three_doilies": {
            "form_block_diagonal": bool(blockdiag),
            "diagonal_block_ranks_mod3": diagranks,
            "reading": ("the E8^3 six-qutrit geometry is W(3,3) PERP W(3,3) PERP W(3,3); the "
                        "summands are NONDEGENERATE so this is a genuine tensor factorisation "
                        "into three two-qutrit systems, unlike the degenerate Lagrangian "
                        "kernel of the qubit reduction")},
        "e8_cubed_reaches_W33": {
            "element": "tau . diag(W,I,I), with tau the cyclic permutation of the E8 factors",
            "checks": w33checks, "rank_mod3": int(rkd), "geometry": f"W({rkd-1},3)",
            "reading": ("W(3,3), two qutrits, at rank 24 -- the rung Co0 does not supply. "
                        "The element PERMUTES the three factors; no diagonal element could, "
                        "since deg Phi_9 = 6 does not divide 8. The three copies of W(3,3) FUSE")},
        "obstructions_are_independent": {
            "question": ("are '24 = 8*3 with 3 odd' and 'Co0 always has exactly 3 blocks of "
                         "Phi_9' the same fact?"),
            "answer": "NO",
            "witness": ("E8^3 has the same rank as Leech, obeys the same odd-part law and "
                        "stops at three qubits for the same arithmetic reason -- but it HAS a "
                        "Phi_9^4 element and Co0 does not. Same rank, different answer"),
            "consequence": ("one obstruction is a property of the number 24 and is shared; "
                            "the other is a property of the automorphism group and separates "
                            "lattices of equal rank")},
        "not_code_concatenation": {
            "tempting_reading": "12 -> 6 -> 3 as concatenated stabiliser codes",
            "refutation": ("the kernel is LAGRANGIAN, so S-perp = S and S-perp/S = 0 -- no "
                           "logical qubits. A Lagrangian stabiliser is a stabiliser STATE, "
                           "not a code. The tower computes V/S, not S-perp/S"),
            "what_it_is": ("a chain of stabiliser-group quotients in which the target carries "
                           "the TWISTED form F_M = (I+M)^T F_J, since a nondegenerate form "
                           "cannot descend through a nonzero kernel")},
        "literature": {
            "coolsaet_2014": {
                "cite": ("K. Coolsaet, Some large partial ovoids of Q-(5,q), for odd q, "
                         "Designs Codes and Cryptography 72 (2014) 119-128"),
                "content": ("explicit descriptions of some of the largest known partial ovoids "
                            "of Q-(5,q) for odd q: two generic constructions plus sporadic "
                            "examples for q <= 11, using non-standard elliptic quadratic forms"),
                "status": ("CONSTRUCTIONS, i.e. lower bounds, not exact values -- which is why "
                           "they never conflicted with anything here. Item closed")},
            "cimrakova_fack_2005": {
                "cite": ("M. Cimrakova and V. Fack, Searching for maximal partial ovoids and "
                         "spreads in generalized quadrangles, Bull. Belg. Math. Soc. Simon "
                         "Stevin 12 (2005) 697-705"),
                "table1_exhaustive_proven_maxima": [
                    {"GQ": nm, "s_t": list(st), "points": gsz, "st_plus_1": o1,
                     "best_bound": bd, "largest": sz, "inequivalent": n}
                    for nm, st, gsz, o1, bd, sz, n in CF_TABLE1],
                "table2_Qminus5q_spectrum": [
                    {"q": q, "lower_bound": lb, "upper_bound": ub, "sizes_found": s}
                    for q, lb, ub, s in CF_TABLE2],
                "thas_bound": "|O'| <= q^3 + 1 - q(q-1) for partial ovoids of Q-(5,q)",
                "ebert_hirschfeld": "a complete cap of Q-(5,q) has |K| >= 2q+2 for q >= 4",
                "explicit_construction": ("a size-96 maximal partial ovoid of Q-(5,7) from "
                                          "(3,+-1,+-1,+-1,+-1,+-1) and cyclic permutations, "
                                          "split by parity of the number of minus signs")},
            "already_credited_here": ("alpha(W(3,5)) = 18 and alpha(W(3,7)) = 33 were caught "
                                      "at Pass 7106-7113 and BT7130-7137, which cite the 2007 "
                                      "companion and decline to re-claim. Nothing is retracted"),
            "coincidence_flag": ("Table 2 gives the Q-(5,11) spectrum as 68..212,214,216 and "
                                 "this repo's open item reads 'q=11 at 68'. DIFFERENT OBJECTS "
                                 "-- ours is W(3,11), theirs Q-(5,11). Recorded so the next "
                                 "reader does not conflate them"),
            "still_open": ("alpha(Q-(5,3)) is settled by neither source: Table 2 starts at "
                           "q=4, and their q=3 row is H(3,9), which dualises to partial "
                           "SPREADS of Q-(5,3), not ovoids")},
        "not_done": ["identify the order-48384 centraliser as a group, not an order",
                     "an explicit omega for LEECH itself (E8^3 is a different Niemeier lattice)",
                     "alpha(W(3,9))", "alpha(Q-(5,3)) against a source covering q=3",
                     "K12 built"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8041_8056_E8_POWERS_AND_THE_DOILY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
