"""Pass 7309 -- E8^3 at d=9: the tower's rank-24 rung, without needing Co0.

WHY THIS AND NOT LEECH. The Niemeier census (Pass 7304) says exactly seven of the 24
Niemeier lattices admit a uniform nontrivial quotient, and E8^3 is one of them, usable at
d=9. Leech is richer but its automorphism group Co0 is not available here. E8^3 is built
from three copies of a lattice already in hand, so the rank-24 rung is testable TODAY.

THE ELEMENT, and it is forced rather than searched. On E8^3 put

    M(x, y, z) = (Jz, x, y)

with J the order-3 fixed-point-free element of W(E8). Then M^3 = J (+) J (+) J, so M has
order 9; and M(x,y,z) = (x,y,z) forces x = y = z with Jz = z, hence z = 0, so M is
fixed-point-free. No search is needed at all.

WHAT THE ARITHMETIC PREDICTS. deg(Phi_9) = 6 and rank 24, so k = 4 and
det(I - M) = Phi_9(1)^4 = 3^4 = 81: the quotient is F_3^4 with 80 nonzero classes. E8^3 has
3 x 240 = 720 minimal vectors and 720/80 = 9 exactly, so the fibration is uniform, with 40
projective points -- the SAME target as E8 at d=3.

The question is whether those 40 points carry W(3,3). Verified against SRG(40,12,2,4) or
nothing is claimed.

    py -3 analysis/w33_pass7309_e8cubed_d9.py
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import (  # noqa: E402
    CARTAN, roots_in_root_basis, simple_reflection, order_of,
)


def main() -> int:
    print("=" * 78)
    print("Pass 7309 -- E8^3 at d=9, the rank-24 rung")
    print("=" * 78)

    R8 = roots_in_root_basis()
    R8a = np.array(R8, dtype=np.int64)
    I8 = np.eye(8, dtype=np.int64)
    gens = [simple_reflection(i) for i in range(8)]
    cox = I8.copy()
    for g in gens:
        cox = cox @ g
    J = np.linalg.matrix_power(cox, 10)
    assert order_of(J, 8) == 3

    # E8^3: block-diagonal Gram, 720 roots embedded one block at a time
    G = np.zeros((24, 24), dtype=np.int64)
    for b in range(3):
        G[8 * b:8 * b + 8, 8 * b:8 * b + 8] = CARTAN
    roots = []
    for b in range(3):
        for v in R8a:
            w = np.zeros(24, dtype=np.int64)
            w[8 * b:8 * b + 8] = v
            roots.append(w)
    Rr = np.array(roots, dtype=np.int64)
    print(f"\n  E8^3: {len(Rr)} minimal vectors (expect 3 x 240 = 720)")
    print(f"  norms: {sorted({int(v @ G @ v) for v in Rr})}   (expect {{2}})")

    # M(x,y,z) = (Jz, x, y)
    M = np.zeros((24, 24), dtype=np.int64)
    M[0:8, 16:24] = J        # x' = J z
    M[8:16, 0:8] = I8        # y' = x
    M[16:24, 8:16] = I8      # z' = y
    o = order_of(M, 20)
    d = int(round(np.linalg.det(np.eye(24) - M)))
    print(f"\n  M(x,y,z) = (Jz, x, y): order {o}, det(I-M) = {d}   (need 9 and 81)")
    M3 = np.linalg.matrix_power(M, 3)
    blockJ = np.zeros((24, 24), dtype=np.int64)
    for b in range(3):
        blockJ[8 * b:8 * b + 8, 8 * b:8 * b + 8] = J
    print(f"    M^3 = J(+)J(+)J ? {np.array_equal(M3, blockJ)}")
    rootset = set(map(tuple, Rr.tolist()))
    print(f"    preserves the 720 minimal vectors? "
          f"{set(map(tuple, (Rr @ M.T).tolist())) == rootset}")
    if o != 9 or d != 81:
        print("  not the element the arithmetic predicts -- aborting")
        return 1

    # class map: exact via the adjugate (det = 81)
    N = np.eye(24, dtype=np.int64) - M
    adj = np.rint(81 * np.linalg.inv(N.astype(float))).astype(np.int64)
    assert np.allclose(adj @ N, 81 * np.eye(24), atol=1e-5), "adjugate not integral"
    classes: dict[tuple, list[int]] = {}
    for i, v in enumerate(Rr):
        classes.setdefault(tuple(int(x) % 81 for x in (adj @ v)), []).append(i)
    sizes = sorted({len(v) for v in classes.values()})
    print(f"\n  classes mod (I-M): {len(classes)}   fibre sizes {sizes}")
    if len(classes) != 80 or sizes != [9]:
        print("  NOT 80 classes of 9 -- nothing claimed")
        return 1
    print("    80 classes of exactly 9  (F_3^4 has 80 nonzero vectors)")

    # projective: identify c with 2c mod 3 in the F_3^4 sense -- work via +-
    proj: dict[tuple, list[int]] = {}
    for c, mem in classes.items():
        neg = tuple((-x) % 81 for x in c)
        proj.setdefault(min(c, neg), []).extend(mem)
    psz = sorted({len(v) for v in proj.values()})
    print(f"    projective classes: {len(proj)}   fibre sizes {psz}")
    if len(proj) != 40:
        print("  NOT 40 projective points -- nothing claimed")
        return 1

    keys = sorted(proj)
    reps = [Rr[proj[k][0]] for k in keys]
    best = None
    for name, F in (("(Mx,y)-(x,My)", M.T @ G - G @ M),
                    ("(Mx,y)", M.T @ G),
                    ("(M^3x,y)-(x,M^3y)", M3.T @ G - G @ M3),
                    ("(x,y)+(Mx,y)", G + M.T @ G)):
        A = np.zeros((40, 40), dtype=np.int64)
        for i in range(40):
            for j in range(i + 1, 40):
                if int(reps[i] @ F @ reps[j]) % 3 == 0:
                    A[i, j] = A[j, i] = 1
        deg = sorted({int(A[i].sum()) for i in range(40)})
        ev = Counter(np.linalg.eigvalsh(A.astype(float)).round(5))
        spec = sorted(round(float(k)) for k, n in ev.items() for _ in range(n))
        isw = deg == [12] and spec == sorted([12] + [2] * 24 + [-4] * 15)
        print(f"    form {name:22s} degrees {str(deg):26s} SRG(40,12,2,4)={isw}")
        if isw:
            best = (name, dict(sorted((float(a), b) for a, b in ev.items())))
    print()
    if best:
        print(f"  *** E8^3 AT d=9 GIVES W(3,3) ***  via {best[0]}, spectrum {best[1]}")
    else:
        print("  none of the candidate forms gives SRG(40,12,2,4) -- reporting that, not a claim")

    out = {"boundary": ("tests the rank-24 rung on E8^3, which the Niemeier census says is "
                        "usable at d=9. Claims nothing unless SRG(40,12,2,4) is verified"),
           "minimal_vectors": len(Rr), "order": o, "det_I_minus_M": d,
           "classes": len(classes), "fibre_size": sizes,
           "projective": len(proj), "gives_W33": best is not None,
           "form": best[0] if best else None}
    fp = ROOT / "data" / "PART_W33_PASS7309_E8CUBED_D9.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
