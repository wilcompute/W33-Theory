"""Pass 7341 -- Leech at d = 8, 9 and 13: three more rungs from the same machinery.

WHAT THE CENSUS PREDICTS. Co0's fixed-point-free elements at these orders are

    d=8   Phi_8^6          det(I-M) = 2^6  = 64    F_2^6    63 points of PG(5,2)
    d=9   Phi_9^3 Phi_3^3  det(I-M) = 3^6  = 729   F_3^6   364 points of PG(5,3)
    d=13  Phi_13^2         det(I-M) = 13^2 = 169   F_13^2   14 points of PG(1,13)

and all three fibrations are uniform: 196560 divided by 63, 728 and 168 gives 3120, 270 and
1170 exactly. So every point is hit in each case and only the FORM is open, exactly as at
d=4 where the answer was W(11,2).

WHAT IS AT STAKE. A nondegenerate alternating form on F_2^6 is W(5,2), the THREE-QUBIT Pauli
commutation geometry; on F_3^6 it is W(5,3), the three-qutrit one. PG(1,13) is a line and
carries nothing. So d=8 and d=9 would extend the tower to three-qudit systems, while d=13
is expected to be empty of content.

THE FORM, generalised from the two solved cases. At d=3 the working form was (I - J^2)^T G
and at d=4 it was (I + M)^T G. Both are p * (I-M)^{-1} transposed, times G, with p the
residue prime: 3(I-J)^{-1} = I - J^2 and 2(I-M)^{-1} = I + M. That candidate is tested here
first, alongside others, and whichever DESCENDS with the right rank is the one used. Nothing
is named unless the rank matches the quotient dimension.

    py -3 analysis/w33_pass7341_leech_d8_d9_d13.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
from w33_pass7333_leech_d4_form import load_flat, invariant_gram  # noqa: E402

CASES = [(8, 2, 6, 64, "PG(5,2)", 63, "W(5,2) = three qubits"),
         (9, 3, 6, 729, "PG(5,3)", 364, "W(5,3) = three qutrits"),
         (13, 13, 2, 169, "PG(1,13)", 14, "a line, no content expected")]


def rank_modp(A, p):
    B = (np.array(A, dtype=np.int64) % p).astype(np.int64)
    n, m = B.shape
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if B[i, c] % p), None)
        if piv is None:
            continue
        B[[r, piv]] = B[[piv, r]]
        inv = pow(int(B[r, c]), -1, p)
        B[r] = (B[r] * inv) % p
        for i in range(n):
            if i != r and B[i, c] % p:
                B[i] = (B[i] - B[i, c] * B[r]) % p
        r += 1
    return r


def main() -> int:
    print("=" * 78)
    print("Pass 7341 -- Leech at d = 8, 9, 13")
    print("=" * 78)

    gens = load_flat(ROOT / "analysis" / "_co0_G.txt")
    G, dim = invariant_gram(gens)
    if G is None:
        print("\n  invariant Gram not recovered -- aborting")
        return 1
    print(f"\n  invariant Gram recovered (solution space dim {dim}), "
          f"preserved by both generators: "
          f"{all(np.array_equal(g.T @ G @ g, G) for g in gens)}")

    I24 = np.eye(24, dtype=np.int64)
    results = {}
    for d, p, k, det, space, pts, target in CASES:
        fp = ROOT / "analysis" / f"_co0_M{d}.txt"
        if not fp.is_file():
            print(f"\n  d={d}: element file missing")
            continue
        M = load_flat(fp)[0]
        dd = int(round(np.linalg.det((I24 - M).astype(float))))
        print(f"\n  d={d}: det(I-M) = {dd} (need {det}), "
              f"M preserves the form: {np.array_equal(M.T @ G @ M, G)}")
        if dd != det:
            print("    element does not match the census -- skipping")
            continue
        N = I24 - M
        # p * (I-M)^{-1}, integral in the solved cases
        Pinv = p * np.linalg.inv(N.astype(float))
        integral = np.allclose(Pinv, np.rint(Pinv), atol=1e-6)
        cands = []
        if integral:
            cands.append((f"({p}(I-M)^-1)^T G", np.rint(Pinv).astype(np.int64).T @ G))
        cands += [("(Mx,y)", M.T @ G), ("(x,y)", G),
                  ("(I+M)^T G", (I24 + M).T @ G)]
        print(f"    p*(I-M)^-1 integral: {integral}")
        print(f"      {'form':22s} {'rank mod p':>11s} {'alternating':>12s} {'descends':>9s}")
        best = None
        for name, F in cands:
            rk = rank_modp(F, p)
            alt = all(int(F[i, i]) % p == 0 for i in range(24))
            rs = np.random.RandomState(1)
            ok = True
            for _ in range(200):
                x = rs.randint(-4, 5, 24)
                y = rs.randint(-4, 5, 24)
                z = rs.randint(-4, 5, 24)
                if int((x + N @ z) @ F @ y) % p != int(x @ F @ y) % p:
                    ok = False
                    break
            print(f"      {name:22s} {rk:11d} {str(alt):>12s} {str(ok):>9s}")
            if ok and rk == k:
                best = (name, alt, rk)
        if best:
            name, alt, rk = best
            verdict = (f"{target}" if alt else
                       f"descends with rank {rk} but NOT alternating -- orthogonal, not W")
            print(f"    -> {verdict}   (via {name})")
            results[d] = {"form": name, "rank": rk, "alternating": bool(alt),
                          "space": space, "points": pts, "verdict": verdict}
        else:
            print(f"    -> no candidate descends with rank {k}; nothing claimed")
            results[d] = {"verdict": "no descending form of the right rank found"}

    out = {"boundary": ("extends the Leech quotient analysis to d = 8, 9 and 13. A geometry "
                        "is named only when a form both DESCENDS and has rank equal to the "
                        "quotient dimension; otherwise nothing is claimed"),
           "cases": {str(d): results.get(d, {"verdict": "not run"})
                     for d, *_ in CASES}}
    op = ROOT / "data" / "PART_W33_PASS7341_LEECH_D8_D9_D13.json"
    op.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {op.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
