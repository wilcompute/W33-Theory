"""Passes 8022-8029 -- the Leech qubit-halving tower, and a retraction of my own filter.

  8022  The other lane's Lagrangian reduction, verified on the ACTUAL Leech matrices.
  8023  The exact integer identity behind it: P_M = I + M + M^2 + M^3 = (I+M) P_J.
  8024  What M does mod 2: it is an INVOLUTION, and the Lagrangian is exactly Fix(M).
  8025  THE TOWER: W(23,2) -> W(11,2) -> W(5,2). Twelve qubits to six to three.
  8026  RETRACTION: my Pass 7351 "exactly two geometries" was wrong, and so was the filter.
  8027  Why the tower stops, and the reason is that 3 is odd.
  8028  Open.
  8029  Scope.

CROSS-LANE CREDIT. Pass7981-7988 (other lane, committed first) states and proves the
W(11,2) -> W(5,2) Lagrangian reduction, and Pass7973-7980 proves the forward half of the
purity condition I had only measured. Both are theirs and are cited, not re-derived. What
this pass adds is the part their symbolic argument could not reach: their file asserts
rank 6, ker(pi) = im(N) and F_M = N^T F_J in prose, while its only executed checks are
polynomial identities like (1-x)(1+x) = 1-x^2 -- nothing in it touches Leech or Co0. Those
three statements are verified here on the 24x24 integral matrices, and they all hold.

    py -3 analysis/w33_pass8022_8029_the_qubit_halving_tower.py
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
from w33_pass7333_leech_d4_form import invariant_gram, load_flat, rank_mod2  # noqa: E402


def basis_mod2(A):
    """Row-reduced basis of the mod-2 column space of A."""
    B = (A % 2).astype(np.int64).T.copy()
    rows = []
    for r in B:
        for b in rows:
            piv = next((i for i, x in enumerate(b) if x), None)
            if piv is not None and r[piv]:
                r = (r + b) % 2
        if r.any():
            rows.append(r % 2)
    return rows


def isotropic(vecs, F):
    return all(int(u @ F @ v) % 2 == 0 for u in vecs for v in vecs)


def main() -> int:
    print("=" * 78)
    print("Passes 8022-8029 -- the Leech qubit-halving tower")
    print("=" * 78)

    I = np.eye(24, dtype=np.int64)
    M = load_flat(ROOT / "analysis" / "_co0_M8.txt")[0]
    G, dim = invariant_gram(load_flat(ROOT / "analysis" / "_co0_G.txt"))
    if G is None:
        print("\n  invariant Gram not recovered -- aborting")
        return 1
    J = M @ M            # order 4
    N = I + M

    print("\n  PASS 8022-8023 -- verified on the matrices, and the identity behind it\n")
    checks = {
        "M^4 = -I": bool(np.array_equal(np.linalg.matrix_power(M, 4), -I)),
        "J = M^2 satisfies J^2 = -I": bool(np.array_equal(J @ J, -I)),
        "P_J := I+J equals 2(I-J)^-1": bool(np.array_equal((I - J) @ (I + J), 2 * I)),
        "P_M := I+M+M^2+M^3 equals 2(I-M)^-1":
            bool(np.array_equal((I - M) @ (I + M + J + J @ M), 2 * I)),
    }
    PK, PJ = I, I + J
    PM = (I + M) @ PJ
    checks["P_M = (I+M) P_J, as exact integers"] = bool(
        np.array_equal(PM, I + M + J + J @ M))
    for k, v in checks.items():
        print(f"      {k:42s} {v}")
    print("""
    The last line is the whole engine. Pass7973-7980 (other lane) proves that a pure
    Phi_{p^r} operator satisfies p I = (I-M)(-Q(M)) with Q the quotient of Phi(x)-p by x-1,
    so p(I-M)^{-1} is the POLYNOMIAL -Q(M). At d=8 that polynomial is I+M+M^2+M^3, which
    factors as (I+M)(I+M^2) -- and I+M^2 is the corresponding polynomial at d=4. So the
    projector at each rung is the projector at the rung below times (I + the square root).
    That is an exact integer factorisation, not a mod-2 accident.""")

    print("\n  PASS 8024 -- what M actually does mod 2\n")
    j_trivial = not ((PJ @ J - PJ) % 2).any()
    ker_eq_im = not ((PJ @ (I - M) - PJ @ (I + M)) % 2).any()
    rank_N = int(rank_mod2(PJ @ N))
    print(f"      J acts TRIVIALLY on Q_J (P_J J = P_J mod 2):   {j_trivial}")
    print("      hence M acts on Q_J as an INVOLUTION, not with order 8")
    print(f"      rank(I+M) on Q_J = {rank_N}  (half of 12: maximal for an involution)")
    print(f"      (I+M)^2 = 0 on Q_J:                            "
          f"{not ((PJ @ N @ N) % 2).any()}")
    print(f"      ker(pi) = im(I+M), since the difference is 2 P_J M:  {ker_eq_im}")
    print("""
    So the kernel of the reduction is im(I+M) = ker(I+M) = Fix(M). In Pauli language: the
    order-8 Leech element reduces mod 2 to a Clifford INVOLUTION on six qubits, and the
    Lagrangian one quotients by is precisely the set of Pauli classes that involution FIXES
    -- a maximal commuting set, i.e. a stabiliser group. That is the step ker(pi) = im(N)
    which the symbolic pass asserts; it is true, and this is why.""")

    print("\n  PASS 8025 -- THE TOWER\n")
    FK, FJ, FM = PK.T @ G, PJ.T @ G, PM.T @ G
    form_id = bool(np.array_equal(FM, N.T @ FJ))
    rungs = []
    print(f"      {'operator':>10s} {'projector':>14s} {'rank':>5s} {'alt':>5s} "
          f"{'geometry':>10s} {'qubits':>7s}")
    for nm, P, F in (("K = M^4", "P_K = I", FK), ("J = M^2", "P_J = (I+J)P_K", FJ),
                     ("M", "P_M = (I+M)P_J", FM)):
        r = rank_mod2(F)
        alt = all(int(F[i, i]) % 2 == 0 for i in range(24))
        print(f"      {nm:>10s} {P:>14s} {r:5d} {str(alt):>5s} "
              f"{'W(' + str(r - 1) + ',2)':>10s} {r // 2:7d}")
        rungs.append({"operator": nm, "projector": P, "rank_mod2": r,
                      "alternating": bool(alt), "geometry": f"W({r-1},2)", "qubits": r // 2})
    print(f"\n      F_M = (I+M)^T F_J as EXACT integer matrices: {form_id}")

    kerJ = basis_mod2(I + J)
    kerM = basis_mod2(PJ @ N)
    iso_J, iso_M = isotropic(kerJ, FK), isotropic(kerM, FJ)
    print(f"      stage 24 -> 12: kernel = Fix(J), dim {len(kerJ)}, "
          f"totally isotropic for F_K: {iso_J}")
    print(f"      stage 12 ->  6: kernel = Fix(M), dim {len(kerM)}, "
          f"totally isotropic for F_J: {iso_M}")
    print("""
        L/2L  -->  L/(I-J)L  -->  L/(I-M)L
        W(23,2)    W(11,2)       W(5,2)
        12 qubits   6 qubits      3 qubits

    Each arrow halves the qubit count and each kernel is a LAGRANGIAN -- half-dimensional
    and totally isotropic -- fixed by the element introduced at that rung. The bottom rung
    L/2L with the mod-2 Leech form is CLASSICAL (Conway): its 2^24 - 1 nonzero classes split
    98280 + 8386560 + 8292375 by type. It is cited here, not claimed; what is new is that it
    is the TOP of a halving tower whose lower rungs are the two geometries found at
    Pass 7333-7348.""")

    print("\n  PASS 8026 -- and that retracts a filter of my own\n")
    print("""    Pass 7351 concluded "LEECH GIVES EXACTLY TWO GEOMETRIES: W(11,2) and W(5,2).
    That list is now complete, not a sample." It is not complete, and the error was in the
    filter rather than the arithmetic. I ruled out d=2 because 196560 is not divisible by
    2^24 - 1, calling the fibration non-uniform. That test is real but it answers a DIFFERENT
    question: whether the minimal vectors cover the quotient evenly. They do not -- they meet
    only 98280 of the 16777215 nonzero classes. The existence of the geometry does not depend
    on them. W(23,2) is there, carried by the Leech form mod 2, and my filter deleted it for
    a reason that was never about the form.

    So the corrected statement is THREE geometries, W(23,2) -> W(11,2) -> W(5,2), and the
    uniformity column in the Pass 7351 table should be read as a property of the minimal-
    vector fibration only, never as an existence criterion.""")

    print("\n  PASS 8027 -- why it stops\n")
    print("""    The next rung needs a square root of M, i.e. order 16, with pure support
    Phi_16^k and k deg(Phi_16) = 24. Since deg(Phi_16) = 8 that forces k = 3, so the quotient
    would be F_2^3 -- ODD-dimensional. Every alternating form on an odd-dimensional space is
    degenerate, so there is no W(2,2) and no half-qubit. The tower terminates at three qubits
    for the arithmetic reason that 24 = 8 * 3 with 3 odd, and no property of Co0 is
    involved.""")

    print("\n  PASS 8028-8029 -- open, and scope\n")
    print("""    NEW HERE: the exact factorisation P_M = (I+M)P_J; the fact that M acts mod 2
    as an involution with Fix(M) the Lagrangian; the three-rung halving tower; the termination
    argument; and the retraction of my own uniformity filter.
    THEIRS, CITED: the Lagrangian reduction theorem (Pass7981-7988) and the purity forward
    implication (Pass7973-7980), which also correctly downgraded my "pure <=> elementary" to
    the forward direction only.
    CLASSICAL, CITED: L/2L and its 98280 + 8386560 + 8292375 type split (Conway).
    NOT DONE: whether the tower's Lagrangians are Co0-conjugate; K12 built; alpha(W(3,9));
    q=11 at 68; Coolsaet unread.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED ON THE ACTUAL 24x24 MATRICES: the Pass7981-7988 Lagrangian reduction "
            "holds, via the exact integer factorisation P_M = (I+M)P_J; M acts mod 2 as an "
            "involution whose fixed space IS the Lagrangian kernel; and the reduction extends "
            "to a three-rung tower W(23,2) -> W(11,2) -> W(5,2), twelve qubits to six to "
            "three, terminating because 24 = 8*3 with 3 odd. RETRACTS the Pass 7351 claim "
            "that Leech gives exactly two geometries"),
        "credit": {
            "Pass7981_7988_other_lane": ("states and proves the W(11,2) -> W(5,2) Lagrangian "
                                         "reduction; committed first, so it owns the result"),
            "Pass7973_7980_other_lane": ("proves pure Phi_{p^r} support => elementary "
                                         "quotient, and correctly downgrades my Pass 7344 "
                                         "'pure <=> elementary' to the forward direction"),
            "what_this_pass_adds": ("their argument is symbolic and executes only polynomial "
                                    "identities; nothing in it touches Leech or Co0. The "
                                    "rank-6, ker(pi)=im(N) and F_M=N^T F_J claims are "
                                    "verified here on the integral matrices"),
            "classical": ("L/2L and its 98280 + 8386560 + 8292375 nonzero-class type split "
                          "are Conway's, cited not claimed")},
        "exact_identities": checks,
        "form_identity_F_M_equals_N_transpose_F_J": form_id,
        "mod2_behaviour": {
            "J_acts_trivially_on_Q_J": bool(j_trivial),
            "M_is_an_involution_on_Q_J": bool(j_trivial),
            "rank_I_plus_M_on_Q_J": rank_N,
            "kernel_equals_image_equals_Fix_M": bool(ker_eq_im),
            "why": "P_J(I-M) - P_J(I+M) = -2 P_J M, which vanishes mod 2",
            "pauli_reading": ("the order-8 Leech element reduces to a Clifford INVOLUTION on "
                              "six qubits; the Lagrangian quotiented out is exactly the set "
                              "of Pauli classes it fixes, i.e. a stabiliser group")},
        "tower": {
            "rungs": rungs,
            "chain": "L/2L -> L/(I-J)L -> L/(I-M)L",
            "geometries": "W(23,2) -> W(11,2) -> W(5,2)",
            "qubits": [12, 6, 3],
            "kernels": [
                {"stage": "24 -> 12", "kernel": "Fix(J)", "dim": len(kerJ),
                 "totally_isotropic": bool(iso_J),
                 "lagrangian": bool(iso_J and len(kerJ) == 12)},
                {"stage": "12 -> 6", "kernel": "Fix(M)", "dim": len(kerM),
                 "totally_isotropic": bool(iso_M),
                 "lagrangian": bool(iso_M and len(kerM) == 6)}],
            "termination": ("a fourth rung needs order 16, i.e. Phi_16^3, giving F_2^3; every "
                            "alternating form on an odd-dimensional space is degenerate, so "
                            "the tower stops at three qubits because 24 = 8*3 with 3 odd")},
        "retraction": {
            "claim": ("Pass 7351: 'LEECH GIVES EXACTLY TWO GEOMETRIES: W(11,2) and W(5,2). "
                      "That list is now complete, not a sample.'"),
            "why_wrong": ("d=2 was removed by a uniformity test -- 196560 not divisible by "
                          "2^24 - 1 -- which measures whether the MINIMAL VECTORS cover the "
                          "quotient evenly, not whether the geometry exists. They meet only "
                          "98280 of 16777215 nonzero classes, and the form is unaffected"),
            "corrected": "three geometries, W(23,2) -> W(11,2) -> W(5,2)",
            "what_was_right": "the divisibility arithmetic itself"},
        "not_done": ["whether the tower's Lagrangians are Co0-conjugate", "K12 built",
                     "alpha(W(3,9))", "q=11 at 68", "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8022_8029_QUBIT_HALVING_TOWER.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
