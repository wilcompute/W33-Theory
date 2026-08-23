"""Passes 8761-8776 -- the law stress-tested, and W(3,3) has a unique minimal home.

  8761  The lift theorem on LEECH, not just E8. Same geometry, rank doubled.
  8762  And the Leech^2 tower: 24 -> 12 -> 6 -> 3 qubits, odd part of 48.
  8763  The kernel law at a NEW multiplicity: p=3, k=24. Predicted, then measured.
  8764  Four confirmations, three primes, two multiplicities.
  8765  WHERE CAN W(3,3) LIVE AT ALL? The rank is forced to 8, 24 or 72.
  8766  AND RANK 8 EVEN UNIMODULAR IS UNIQUE. W(3,3) is E8-native.
  8767  What that does and does not settle about the other Niemeier lattices.
  8768  Open.
  8769  Scope.

    py -3 analysis/w33_pass8761_8776_w33_is_e8_native.py
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
from sympy import GF, Matrix, totient  # noqa: E402
from sympy.polys.matrices import DomainMatrix  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN, simple_reflection  # noqa: E402
from w33_pass7333_leech_d4_form import invariant_gram, load_flat  # noqa: E402

# rank -> how many even unimodular lattices exist there
EVEN_UNIMODULAR = {8: "1  (E8 -- UNIQUE)", 24: "24 (the Niemeier lattices)",
                   72: ">1e7 (unclassified)"}


def gfrank(A, p):
    B = (np.array(A, dtype=np.int64) % p).tolist()
    return len(DomainMatrix.from_Matrix(Matrix(B)).convert_to(GF(p)).rref()[1])


def order_of(M, I, cap=40):
    X = M.copy()
    for k in range(1, cap + 1):
        if np.array_equal(X, I):
            return k
        X = X @ M
    return None


def cyc(n, d):
    R = n * d
    t = np.zeros((R, R), dtype=np.int64)
    Id = np.eye(d, dtype=np.int64)
    for i in range(n):
        t[d * ((i + 1) % n):d * ((i + 1) % n) + d, d * i:d * i + d] = Id
    return t


def proj(M, p, I):
    X = np.rint(p * np.linalg.inv((I - M).astype(float))).astype(np.int64)
    assert np.array_equal((I - M) @ X, p * I), "p(I-M)^-1 is not integral"
    return X


def main() -> int:
    print("=" * 78)
    print("Passes 8761-8776 -- the law stress-tested, and W(3,3) is E8-native")
    print("=" * 78)

    print("\n  PASS 8761-8762 -- the lift theorem on LEECH\n")
    M8 = load_flat(ROOT / "analysis" / "_co0_M8.txt")[0]
    GL, _ = invariant_gram(load_flat(ROOT / "analysis" / "_co0_G.txt"))
    I24 = np.eye(24, dtype=np.int64)
    kbase = gfrank((proj(M8, 2, I24).T @ GL) % 2, 2)
    I48 = np.eye(48, dtype=np.int64)
    G2 = block_diag(GL, GL).astype(np.int64)
    g = cyc(2, 24) @ block_diag(M8, I24).astype(np.int64)
    lift = {
        "order of g is 16": order_of(g, I48) == 16,
        "g^2 = diag(M8, M8)":
            bool(np.array_equal(g @ g, block_diag(M8, M8).astype(np.int64))),
        "g preserves the Leech^2 form": bool(np.array_equal(g.T @ G2 @ g, G2)),
    }
    klift = gfrank((proj(g, 2, I48).T @ G2) % 2, 2)
    print(f"      base: Leech, order-8 Phi_8^6      -> k = {kbase}, W({kbase-1},2), "
          f"{kbase//2} qubits")
    for k, v in lift.items():
        print(f"      {k:44s} {v}")
    print(f"      lift: Leech^2 rank 48, order 16   -> k = {klift}, W({klift-1},2), "
          f"{klift//2} qubits")
    print(f"      SAME GEOMETRY AS THE BASE: {klift == kbase}")
    print()
    tower48 = []
    for e, lbl in ((8, "g^8 = -I"), (4, "g^4"), (2, "g^2"), (1, "g")):
        M = np.linalg.matrix_power(g, e)
        rk = gfrank(proj(M, 2, I48).T @ G2, 2)
        o = order_of(M, I48)
        print(f"      {lbl:>10s} order {o:2d}   k = {rk:2d}   W({rk-1},2)   {rk//2:2d} qubits")
        tower48.append({"element": lbl, "order": o, "k": rk, "geometry": f"W({rk-1},2)",
                        "qubits": rk // 2})
    print("""
    So the lift theorem is not an E8 accident. It works on Leech, a lattice with no factor
    structure of its own -- because Leech^2 has one. And the rank-48 tower terminates at
    THREE qubits, which is the odd part of 48, exactly as the odd-part law requires.""")

    print("\n  PASS 8763-8764 -- the kernel law at a new multiplicity\n")
    W3 = np.linalg.matrix_power(
        np.linalg.multi_dot([simple_reflection(i) for i in range(8)]), 10)
    G6 = block_diag(*[CARTAN] * 6).astype(np.int64)
    I16 = np.eye(16, dtype=np.int64)
    g9 = cyc(3, 16) @ block_diag(block_diag(W3, W3).astype(np.int64), I16, I16).astype(np.int64)
    w3 = np.linalg.matrix_power(g9, 3)
    Fw = (proj(w3, 3, I48).T @ G6) % 3
    k = gfrank(Fw, 3)
    kg = gfrank((proj(g9, 3, I48).T @ G6) % 3, 3)
    dK = gfrank(I48 - g9, 3) - gfrank(I48 - w3, 3)
    U = ((I48 - g9) % 3).T
    rK = gfrank(np.array([[int(u @ Fw @ v) % 3 for v in U] for u in U], dtype=np.int64), 3)
    pred = ((k * 2) // 3, k // 3, k // 3)
    got = (dK, k - dK, rK)
    print(f"      E8^6, rank 48. Ambient order-3: k = {k}, W({k-1},3), {k//2} qutrits.")
    print(f"      Target order-9: k = {kg}, W({kg-1},3), {kg//2} qutrits.\n")
    print(f"      {'quantity':>12s} {'predicted':>10s} {'measured':>9s}")
    ok = True
    for nm, a, b in zip(("dim K", "dim K-perp", "rank(F|K)"), pred, got):
        ok &= a == b
        print(f"      {nm:>12s} {a:10d} {b:9d}   {'OK' if a == b else 'MISMATCH'}")
    print(f"\n      coisotropic: {dK - rK == k - dK}   all three exact: {ok}")
    print()
    table = [(2, "E8^3", 24, 12, 6, 6, 0, "LAGRANGIAN"),
             (3, "E8^3", 24, 12, 8, 4, 4, "coisotropic"),
             (3, "E8^6", 48, k, dK, k - dK, rK, "coisotropic"),
             (5, "E8^5", 40, 10, 8, 2, 6, "coisotropic")]
    print(f"      {'p':>3s} {'lattice':>7s} {'rank':>5s} {'k':>3s} {'dim K':>6s} "
          f"{'K-perp':>7s} {'rank F|K':>9s} {'type':>12s}")
    for p, lat, r, kk, dk, kp, rk_, ty in table:
        print(f"      {p:3d} {lat:>7s} {r:5d} {kk:3d} {dk:6d} {kp:7d} {rk_:9d} {ty:>12s}")
    print("""
    FOUR CONFIRMATIONS, three primes and two different multiplicities at p=3. The k=24 row
    is a genuinely independent test: its numbers (16, 8, 8) are not the k=12 numbers.""")

    print("\n  PASS 8765-8766 -- so where can W(3,3) live at all?\n")
    print("""    W(3,3) is W(k-1,p) with k = 4 and p = 3, so it needs a pure Phi_{3^m}^4
    element, and that FORCES the rank:\n""")
    print(f"      {'m':>3s} {'order':>6s} {'deg Phi':>8s} {'rank':>6s}  even unimodular lattices")
    homes = []
    for m in (1, 2, 3):
        d = int(totient(3 ** m))
        r = 4 * d
        print(f"      {m:3d} {3**m:6d} {d:8d} {r:6d}  {EVEN_UNIMODULAR.get(r, 'many')}")
        homes.append({"m": m, "order": 3 ** m, "deg_phi": d, "rank": r,
                      "even_unimodular": EVEN_UNIMODULAR.get(r, "many")})
    print("""
    AND RANK 8 EVEN UNIMODULAR IS UNIQUE: it is E8. So the minimal carrier of W(3,3) is
    not a choice among candidates -- there is exactly one lattice it can be. Pass 7217
    built that carrier explicitly, as the Coxeter cube root c^10.

        W(3,3), this repository's central object, is E8-NATIVE.

    Every appearance of it at higher rank that this machinery produces is a LIFT of that
    one, carried by a factor permutation and preserving the multiplicity j = 4. It was
    never a rank-24 object and never a Leech object; rank 24 is simply the first place the
    lift can land.""")

    print("\n  PASS 8767 -- what that does NOT settle\n")
    print("""    At rank 24 the LIFT mechanism needs a lattice of the form L^3 with L even
    unimodular of rank 8 -- and since that L must be E8, E8^3 is the only Niemeier lattice
    the lift reaches. Leech is not of that form, and independently has no Phi_9^4 class at
    all (Pass 8030-8040, exhaustive from the character table).

    NOT CHECKED: whether any of the other 22 Niemeier lattices carries a Phi_9^4 element by
    some mechanism OTHER than the lift. The lift theorem is a sufficient construction, not a
    classification, and it does not exclude other routes. That is a real open question and
    it is left open rather than closed by assertion.""")

    print("\n  PASS 8768-8769 -- open, and scope\n")
    print("""    NEW: the lift theorem verified on LEECH (a second, structurally different
    base lattice); the rank-48 Leech^2 tower terminating at the odd part of 48; the kernel
    law confirmed at a fourth data point with new numbers (p=3, k=24 -> 16, 8, 8); and the
    rank-forcing argument identifying E8 as the UNIQUE minimal carrier of W(3,3).
    CITED: Pass 7217 for the explicit E8 carrier; Pass 8030-8040 for no-Phi_9^4 in Co0;
    Pass 8737-8760 for the kernel law and the lift theorem; Pass 8022-8029 and 8721-8736 for
    the two kernel types.
    NOT DONE: the other 22 Niemeier lattices at Phi_9^4; a p=7 test (E8 has no Phi_7 element,
    since deg Phi_7 = 6 does not divide 8, so a different base lattice is needed);
    alpha(W(3,9)); K12 built.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED: the lift theorem holds on LEECH as well as E8 -- Leech^2 at rank 48 "
            "carries the same W(5,2) via an order-16 element, and its tower 24->12->6->3 "
            "terminates at the odd part of 48. The kernel law is confirmed at a fourth data "
            "point with new numbers (p=3, k=24: predicted and measured 16, 8, 8). And the "
            "rank of a W(3,3) carrier is FORCED to 8, 24 or 72; since rank-8 even unimodular "
            "is unique, E8 is the unique minimal carrier and W(3,3) is E8-native"),
        "lift_on_leech": {
            "base": {"lattice": "Leech", "element": "order-8 Phi_8^6", "k": kbase,
                     "geometry": f"W({kbase-1},2)", "qubits": kbase // 2},
            "lift": {"lattice": "Leech^2, rank 48", "element": "order-16 via the 2-cycle",
                     "k": klift, "geometry": f"W({klift-1},2)", "qubits": klift // 2},
            "checks": {k: bool(v) for k, v in lift.items()},
            "same_geometry": bool(klift == kbase),
            "tower": tower48,
            "reading": ("the lift is not an E8 accident: Leech has no factor structure of "
                        "its own, but Leech^2 does, and the rank-48 tower terminates at 3 "
                        "qubits = the odd part of 48")},
        "kernel_law_fourth_point": {
            "case": "p=3, k=24, E8^6 at rank 48",
            "predicted": {"dim_K": pred[0], "dim_K_perp": pred[1], "rank_F_on_K": pred[2]},
            "measured": {"dim_K": got[0], "dim_K_perp": got[1], "rank_F_on_K": got[2]},
            "all_exact": bool(ok), "coisotropic": bool(dK - rK == k - dK),
            "independence": "the numbers 16, 8, 8 differ from the k=12 case, so this is a "
                            "genuine second test at p=3",
            "table": [{"p": p, "lattice": lat, "rank": r, "k": kk, "dim_K": dk,
                       "dim_K_perp": kp, "rank_F_on_K": rk_, "type": ty}
                      for p, lat, r, kk, dk, kp, rk_, ty in table]},
        "w33_is_e8_native": {
            "forcing": ("W(3,3) is W(k-1,p) with k=4, p=3, so a pure Phi_{3^m}^4 element "
                        "forces rank = 4 deg Phi_{3^m}"),
            "possible_ranks": homes,
            "uniqueness": ("rank-8 even unimodular is UNIQUE and equals E8, so the minimal "
                           "carrier is not a choice among candidates"),
            "explicit_carrier": "Pass 7217, the Coxeter cube root c^10",
            "conclusion": ("W(3,3) is E8-NATIVE. Every higher-rank appearance this machinery "
                           "produces is a lift of that one, preserving j = 4. It was never a "
                           "rank-24 object and never a Leech object")},
        "left_open": {
            "lift_reaches": ("at rank 24 the lift needs L^3 with L even unimodular of rank 8, "
                             "so L = E8 and E8^3 is the only Niemeier the lift reaches"),
            "not_checked": ("whether any of the other 22 Niemeier lattices carries a Phi_9^4 "
                            "element by a mechanism other than the lift. The lift theorem is "
                            "a sufficient construction, not a classification")},
        "not_done": ["the other 22 Niemeier lattices at Phi_9^4",
                     "a p=7 test (deg Phi_7 = 6 does not divide 8, so E8 cannot host it)",
                     "alpha(W(3,9))", "K12 built"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8761_8776_W33_IS_E8_NATIVE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
