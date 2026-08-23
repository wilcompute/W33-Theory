"""Passes 8030-8040 -- the qutrit branch of the Leech tower, and the doily it just misses.

  8030  Random search cannot reach the fixed-point-free order-3 class. Measured, not guessed.
  8031  The trace census: only -3 and 0 occur. The class is at density ~1e-13.
  8032  The maximal-subgroup route, and why its candidate was REJECTED.
  8033  The ATLAS has no 24-dimensional integral representation of 6.Suz.
  8034  So stop hunting for the matrix: the result does not need one.
  8035  THE THEOREM: a fixed-point-free order-3 isometry of an even unimodular rank-2k
        lattice gives W(k-1,3), with no computation.
  8036  Control: the argument reproduces E8 -> W(3,3), which Pass 7217 found independently.
  8037  LEECH -> W(11,3). Six qutrits.
  8038  The branch stops ONE RUNG SHORT OF THE DOILY -- and now that is a theorem.
  8039  The two branches, and their two different reasons for stopping.
  8040  Scope.

    py -3 analysis/w33_pass8030_8040_the_qutrit_branch.py
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
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN, simple_reflection  # noqa: E402

# from the exhaustive character-table check, Pass 8035 (analysis/_co0_order9_classes.txt):
# every order-9 class of 2.Co1 in the 24-dimensional representation, written as
# a copies of 1, b blocks of Phi_3, c blocks of Phi_9.
ORDER9_CLASSES = [(55, -3, -3, 0, 3, 3), (57, 0, -3, 2, 2, 3), (59, 3, -3, 4, 1, 3)]


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


def main() -> int:
    print("=" * 78)
    print("Passes 8030-8040 -- the qutrit branch, and the doily it just misses")
    print("=" * 78)

    print("\n  PASS 8030-8034 -- four ways not to get the matrix, and why that is fine\n")
    print("""    Pass 8022-8029 retracted a filter of mine that had deleted rungs of the Leech
    quotient tower for a reason that was never about the form. The same filter deleted d=3,
    and the d=3 element is not exotic: it is exactly what makes the COMPLEX Leech lattice a
    rank-12 Z[omega] module with Aut = 6.Suz, already recorded in this repo at
    analysis/w33_complex_leech_suzuki_chain.py. So the rung should be real. Getting the
    matrix, however, failed four times, and each failure is worth recording.

    RANDOM SEARCH CANNOT REACH IT, and this was measured rather than assumed. Over 4000
    random words, 1679 elements of order 3 appeared. Their traces were only -3 and 0 --
    fixed spaces of dimension 6 and 8. The fixed-point-free class has trace -12 and never
    appeared. It cannot: its centraliser is 6.Suz, so its density in Co0 is about 1/2.7e12.
    Reporting that as "no such element" would have been the timed-out-search-as-negative
    mistake this repo has paid for before, so it is reported as what it is.

    THE MAXIMAL-SUBGROUP ROUTE PRODUCED A CANDIDATE, AND IT WAS REJECTED. Taking maxes-2 of
    2.Co1 and computing the commutant of its derived subgroup gave a 2-dimensional algebra
    containing an integral matrix W with W^3 = I, W^2 + W + I = 0, trace -12 and
    det(I-W) = 3^12 -- every arithmetic property wanted. But W does NOT preserve the
    invariant Gram, and multiplication by omega on a Z[omega]-lattice always preserves the
    trace form. So W is not omega. It was discarded, not published. A sweep of maxes 1-8
    produced no fixed-point-free order-3 ISOMETRY at all, and long words made the commutant
    numerics ill-conditioned besides.

    AND THE ATLAS HAS NO INTEGRAL 24-DIMENSIONAL 6.Suz: only a permutation representation on
    196560 points and 12-dimensional ones over F7, F13 and F25.

    At which point the right move is to stop hunting. The result does not need the matrix.""")

    print("\n  PASS 8035 -- THE THEOREM\n")
    print("""    Let L be an even unimodular lattice of rank 2k with Gram G, and let w be an
    isometry of order 3 with characteristic polynomial Phi_3^k -- fixed-point-free. Then:

      (a) w^2 + w + I = 0, so (I-w)(w+2I) = 2I - w - w^2 = 2I + I = 3I.
          Hence P := w + 2I is exactly 3(I-w)^{-1}, and it is an INTEGER matrix.

      (b) By the purity theorem (other lane, Pass7973-7980), pure Phi_{p^r} support forces
          an elementary quotient, so L/(I-w)L = F_3^k.

      (c) F := P^T G satisfies F + F^T = G(w + w^2) + 4G = -G + 4G = 3G, which vanishes
          mod 3. So F is ANTISYMMETRIC mod 3; and 2 F_ii = 0 with 2 a unit forces every
          diagonal entry to vanish. F is ALTERNATING.

      (d) Mod 3, F = G(w^2 + 2I) = G(w^2 - I), and w^2 - I = (w - I)(w + I) with
          w + I = -w^2 invertible. So rank F = rank(w - I) mod 3 = k exactly.
          F is NONDEGENERATE.

    A nondegenerate alternating form on F_3^k is the symplectic polar space W(k-1,3).
    No matrix is required anywhere in that argument.""")

    print("\n  PASS 8036 -- control: does it reproduce a case already known?\n")
    cox = np.eye(8, dtype=np.int64)
    for i in range(8):
        cox = cox @ simple_reflection(i)
    W = np.linalg.matrix_power(cox, 10)
    I8 = np.eye(8, dtype=np.int64)
    G8 = CARTAN.copy()
    P = W + 2 * I8
    F = P.T @ G8
    ctrl = {
        "W^3 = I": bool(np.array_equal(np.linalg.matrix_power(W, 3), I8)),
        "W^2 + W + I = 0": bool(not (W @ W + W + I8).any()),
        "det(I-W) = 3^4": int(round(np.linalg.det((I8 - W).astype(float)))) == 81,
        "preserves the Cartan form": bool(np.array_equal(W.T @ G8 @ W, G8)),
        "P = 3(I-W)^-1": bool(np.array_equal((I8 - W) @ P, 3 * I8)),
        "F antisymmetric mod 3": bool(not ((F + F.T) % 3).any()),
        "F diagonal zero mod 3": bool(all(int(F[i, i]) % 3 == 0 for i in range(8))),
    }
    for k, v in ctrl.items():
        print(f"      {k:32s} {v}")
    rk = rank_modp(F, 3)
    print(f"      {'rank mod 3':32s} {rk} of 8  ->  W({rk - 1},3)")
    print("""
    E8 with its Coxeter cube root gives W(3,3) -- which is exactly what Pass 7217 found by
    an entirely different route, building the 6:1 Eisenstein fibration explicitly. The
    general argument reproduces a known answer on the one case where a matrix is in hand.""")

    print("\n  PASS 8037 -- and applied to Leech\n")
    print("""    Rank 24, so k = 12, and the fixed-point-free order-3 isometry is classical --
    it IS the complex Leech structure, Aut = 6.Suz. No new existence claim is needed and none
    is made. The theorem then gives

        Leech / (I - omega) Leech  =  F_3^12,  carrying W(11,3):  SIX QUTRITS.

    This is the rung my Pass 7351 uniformity filter deleted, alongside W(23,2). Same error,
    same correction: 196560 is not divisible by 3^12 - 1, but that measures whether the
    MINIMAL VECTORS cover the quotient evenly, not whether the geometry exists.""")

    print("\n  PASS 8038 -- and it stops one rung short of the doily\n")
    print("""    The next rung down needs a cube root of omega: order 9, pure support Phi_9^k
    with k deg(Phi_9) = 24. Since deg(Phi_9) = 6 that forces k = 4, quotient F_3^4 -- which
    is W(3,3). THE DOILY. This repository's central object would be the next rung of the
    Leech qutrit branch.

    It is not there. Pass 7343 said so from a census; a census is only as exhaustive as its
    enumeration, so here it is settled from the character table of 2.Co1 instead. Writing an
    order-9 element's eigenvalues as a copies of 1, b blocks of Phi_3 and c blocks of Phi_9,
    the character determines (a,b,c) via chi(1) = a + 2b + 6c = 24, chi(g) = a - b, and
    chi(g^3) = a + 2b - 3c. There is exactly ONE degree-24 character and exactly THREE
    order-9 classes:\n""")
    print(f"      {'class':>6s} {'chi(g)':>7s} {'chi(g^3)':>9s} {'a':>3s} {'b':>3s} {'c':>3s}"
          f"   {'char poly':>20s}")
    for cl, cg, cg3, a, b, c in ORDER9_CLASSES:
        cp = (f"{'(x-1)^' + str(a) + ' ' if a else ''}"
              f"{'Phi_3^' + str(b) + ' ' if b else ''}Phi_9^{c}")
        print(f"      {cl:6d} {cg:7d} {cg3:9d} {a:3d} {b:3d} {c:3d}   {cp:>20s}")
    print("""
    Every one of them has c = 3. Phi_9^4 would be (a,b,c) = (0,0,4) and it does not occur.
    Co0 has no such element, so the qutrit branch STOPS at six qutrits, one rung above the
    doily. Note class 55 is fixed-point-free (a = 0) and still fails -- being
    fixed-point-free is not enough, the support must be PURE.""")

    print("\n  PASS 8039 -- the two branches stop for two different reasons\n")
    print("""      2-branch   W(23,2) -> W(11,2) -> W(5,2)      12 -> 6 -> 3 qubits
      3-branch   W(11,3)                                6 qutrits

    The qubit branch stops ARITHMETICALLY: a fourth rung needs Phi_16^3, giving the
    odd-dimensional F_2^3, where every alternating form is degenerate. 24 = 8 * 3 with 3 odd,
    and no property of Co0 enters.

    The qutrit branch stops GROUP-THEORETICALLY: the arithmetic is perfectly happy with
    Phi_9^4 -- 24 = 6 * 4, quotient F_3^4, an even dimension, W(3,3) -- and it is Co0 that
    declines to supply the element. Two branches, two genuinely different obstructions.

    And E8 supplies exactly the rung Leech cannot: E8 -> W(3,3) is the doily, verified at
    Pass 7217 and reproduced above. The doily is reachable from E8 and NOT from Leech.""")

    print("\n  PASS 8040 -- scope\n")
    print("""    NEW: the general theorem (fixed-point-free order-3 isometry of an even
    unimodular rank-2k lattice gives W(k-1,3)); its E8 control; W(11,3) for Leech; and the
    exhaustive character-table proof that Co0 has no Phi_9^4, which upgrades the Pass 7343
    census to a theorem and locates the doily one rung below the branch.
    REJECTED, NOT PUBLISHED: the maxes-2 candidate W, which had every arithmetic property but
    was not an isometry.
    CITED, NOT CLAIMED: the complex Leech / 6.Suz structure (classical, and already in this
    repo); the purity theorem (other lane, Pass7973-7980).
    NOT DONE: an explicit omega matrix in the Co0 basis; K12 built; alpha(W(3,9)); q=11 at
    68; Coolsaet unread.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "THEOREM: a fixed-point-free order-3 isometry with char poly Phi_3^k on an even "
            "unimodular lattice of rank 2k yields a nondegenerate ALTERNATING form on "
            "F_3^k, i.e. W(k-1,3) -- proved algebraically, controlled against E8 where it "
            "reproduces the independently-found W(3,3). For Leech this gives W(11,3), six "
            "qutrits. EXHAUSTIVE from the 2.Co1 character table: no Phi_9^4 class exists, so "
            "the qutrit branch stops one rung above W(3,3), the doily"),
        "why_no_matrix": {
            "random_search": ("4000 words gave 1679 order-3 elements with traces only -3 and "
                              "0; the fixed-point-free class has trace -12 and centraliser "
                              "6.Suz, so density ~1/2.7e12 -- unreachable, and reported as "
                              "unreachable rather than absent"),
            "maxes_route": ("maxes-2 derived subgroup gave an integral W with W^3=I, "
                            "W^2+W+I=0, trace -12, det(I-W)=3^12 -- but NOT an isometry of "
                            "the Gram, so it is not omega and was rejected"),
            "maxes_sweep": "maxes 1-8 yielded no fixed-point-free order-3 isometry",
            "atlas": ("no 24-dimensional integral representation of 6.Suz exists; only "
                      "p196560 and 12-dimensional reps over F7, F13, F25"),
            "resolution": "the theorem needs no matrix"},
        "theorem": {
            "hypothesis": ("L even unimodular of rank 2k with Gram G; w an isometry of order "
                           "3 with char poly Phi_3^k"),
            "step_a": "w^2+w+I=0 gives (I-w)(w+2I)=3I, so P:=w+2I is exactly 3(I-w)^-1",
            "step_b": "purity (Pass7973-7980) gives L/(I-w)L = F_3^k",
            "step_c": ("F:=P^T G has F+F^T = G(w+w^2)+4G = 3G = 0 mod 3, so F is "
                       "antisymmetric; 2F_ii=0 with 2 a unit forces zero diagonal"),
            "step_d": ("mod 3, F = G(w^2-I) with w^2-I=(w-I)(w+I) and w+I=-w^2 invertible, "
                       "so rank F = rank(w-I) = k exactly"),
            "conclusion": "nondegenerate alternating on F_3^k, i.e. W(k-1,3)"},
        "e8_control": {**{k: bool(v) for k, v in ctrl.items()},
                       "rank_mod3": int(rk), "geometry": f"W({rk-1},3)",
                       "agrees_with": "Pass 7217, which built the E8 fibration explicitly"},
        "leech": {"rank": 24, "k": 12, "geometry": "W(11,3)", "reads_as": "six qutrits",
                  "element": ("classical: the complex Leech structure, Aut = 6.Suz, already "
                              "recorded at analysis/w33_complex_leech_suzuki_chain.py"),
                  "note": "this is a rung the Pass 7351 uniformity filter wrongly deleted"},
        "no_phi9_fourth": {
            "method": ("exhaustive over classes from the 2.Co1 character table, decoding "
                       "(a,b,c) from chi(1)=a+2b+6c=24, chi(g)=a-b, chi(g^3)=a+2b-3c"),
            "degree_24_characters": 1,
            "order9_classes": [{"class": cl, "chi_g": cg, "chi_g3": cg3,
                                "ones": a, "phi3_blocks": b, "phi9_blocks": c}
                               for cl, cg, cg3, a, b, c in ORDER9_CLASSES],
            "phi9_fourth_present": False,
            "consequence": ("the qutrit branch stops at six qutrits; W(3,3), the doily, is "
                            "the rung below and Co0 does not supply the element"),
            "upgrades": "the Pass 7343 census, from an enumeration to a theorem"},
        "two_branches": {
            "qubit": {"chain": "W(23,2) -> W(11,2) -> W(5,2)", "counts": [12, 6, 3],
                      "stops_because": ("ARITHMETIC: a fourth rung needs Phi_16^3, giving "
                                        "odd-dimensional F_2^3 where every alternating form "
                                        "is degenerate; 24 = 8*3 with 3 odd")},
            "qutrit": {"chain": "W(11,3)", "counts": [6],
                       "stops_because": ("GROUP-THEORETIC: the arithmetic admits Phi_9^4 "
                                         "(24 = 6*4, quotient F_3^4 = W(3,3)) and Co0 has no "
                                         "such class")},
            "the_doily": ("W(3,3) is reachable from E8 (Pass 7217, reproduced here as the "
                          "control) and NOT from Leech")},
        "rejected": {"object": "the maxes-2 commutant element W",
                     "had": "order 3, minimal polynomial Phi_3, trace -12, det(I-W) = 3^12",
                     "failed": "does not preserve the invariant Gram, so it is not an isometry",
                     "action": "discarded"},
        "not_done": ["an explicit omega in the Co0 basis", "K12 built", "alpha(W(3,9))",
                     "q=11 at 68", "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8030_8040_QUTRIT_BRANCH.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
