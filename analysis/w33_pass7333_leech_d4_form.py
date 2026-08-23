"""Pass 7333 -- the Leech lattice at d=4: which form does the quotient carry?

WHERE THIS COMES FROM. Censusing Co0 = Aut(Leech) in the ATLAS 24-dimensional INTEGRAL
representation showed its order-4 elements have six (trace, det(I-M)) signatures, exactly one
of which is the pure power Phi_4^12: trace 0, det 4096 = 2^12, with M^2 = -I. So Leech is a
rank-12 Z[i]-module, and

    Leech / (I-M)Leech = F_2^12,  4095 nonzero classes,  196560 / 4095 = 48 vectors each.

The fibration is uniform and covers ALL 4095 points of PG(11,2), so the minimal vectors are
not needed to say which points are hit -- every one is. The only question left is the FORM.

WHAT IS AT STAKE. Alternating and nondegenerate means W(11,2), the symplectic polar space of
PG(11,2) -- which is the Pauli commutation geometry of SIX QUBITS. Quadratic instead means an
orthogonal polar space. Neither is assumed.

TWO EXPORT LESSONS, both paid for. GAP's String() wraps long lines with a trailing backslash
that can split a token: a minus sign left at a line end parses away and silently drops the sign, which made
the first export fail every check while looking plausible. And QUIT cannot appear inside an
if-block. The element is now written flat, one row per line, and re-verified on the Python
side (M^2 = -I, trace 0, det 4096) before anything is computed from it.

    py -3 analysis/w33_pass7333_leech_d4_form.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402


def load_flat(path: Path, n: int = 24):
    rows = [[int(x) for x in ln.split()] for ln in
            path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    mats = [np.array(rows[i:i + n], dtype=np.int64) for i in range(0, len(rows), n)]
    return mats


def invariant_gram(gens, n=24):
    """g^T G g = G vectorises as (g^T (x) g^T) vec(G) = vec(G)."""
    blocks = []
    for g in gens:
        K = np.kron(g.T.astype(np.float64), g.T.astype(np.float64))
        blocks.append(K - np.eye(n * n))
    A = np.vstack(blocks)
    _, s, Vt = np.linalg.svd(A)
    ns = Vt[np.sum(s > 1e-6):]
    if ns.shape[0] == 0:
        return None, 0
    v = ns[0].reshape(n, n)
    # dim is 1, so the form is unique up to scale. Normalise by the smallest
    # nonzero magnitude rather than the largest -- that is what makes the entries
    # land on integers.
    nz = np.abs(v[np.abs(v) > 1e-9])
    if nz.size == 0:
        return None, ns.shape[0]
    v = v / nz.min()
    Gi = np.rint(v).astype(np.int64)
    if not np.allclose(v, Gi, atol=1e-4):
        return None, ns.shape[0]
    from math import gcd
    g0 = 0
    for x in Gi.flatten():
        g0 = gcd(g0, abs(int(x)))
    if g0:
        Gi = Gi // g0
    return Gi, ns.shape[0]


def rank_mod2(A):
    B = (A % 2).astype(np.int64) % 2
    B = B.copy()
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
    print("Pass 7333 -- Leech at d=4: the induced form")
    print("=" * 78)

    mp = ROOT / "analysis" / "_co0_M.txt"
    gp = ROOT / "analysis" / "_co0_G.txt"
    if not (mp.is_file() and gp.is_file()):
        print("\n  exported files missing -- run the GAP export first")
        return 1
    M = load_flat(mp)[0]
    gens = load_flat(gp)
    I24 = np.eye(24, dtype=np.int64)
    print(f"\n  element re-verified in Python: M^2 = -I {np.array_equal(M @ M, -I24)}, "
          f"trace {int(np.trace(M))}, "
          f"det(I-M) {int(round(np.linalg.det((I24 - M).astype(float))))}")
    print(f"  generators loaded: {len(gens)}")

    G, dim = invariant_gram(gens)
    print(f"\n  invariant-form space dimension: {dim}")
    if G is None:
        print("  no integral invariant form recovered -- aborting")
        return 1
    sym = np.array_equal(G, G.T)
    ev = np.linalg.eigvalsh(G.astype(float))
    print(f"    symmetric {sym}, positive definite {bool(ev.min() > 1e-9)}, "
          f"diagonal {sorted(set(int(x) for x in np.diag(G)))}")
    for i, g in enumerate(gens):
        print(f"    generator {i} preserves it: {np.array_equal(g.T @ G @ g, G)}")
    print(f"    M preserves it: {np.array_equal(M.T @ G @ M, G)}")

    N = I24 - M
    print(f"\n  (I-M)^2 = -2M ? {np.array_equal(N @ N, -2 * M)}   "
          f"-> the quotient is an F_2 space")

    print(f"\n      {'form':16s} {'alternating':>12s} {'symmetric':>10s} {'rank mod 2':>11s}")
    results = {}
    for name, F in (("((I+M)x, y)", G + M.T @ G),
                    ("(Mx, y)", M.T @ G),
                    ("(x, y)", G)):
        alt = all(int(F[i, i]) % 2 == 0 for i in range(24))
        symm = np.array_equal((F - F.T) % 2, np.zeros((24, 24), dtype=np.int64))
        rk = rank_mod2(F)
        results[name] = {"alternating": bool(alt), "symmetric_mod2": bool(symm), "rank": rk}
        print(f"      {name:16s} {str(alt):>12s} {str(symm):>10s} {rk:11d}")

    print("""
  READ THE RANK COLUMN. The quotient is 12-dimensional over F_2, so a form that
  descends to a NONDEGENERATE form there has rank 12 mod 2. Rank 24 means the form
  does not descend at all; rank 0 means it vanishes mod 2.""")

    out = {"boundary": ("determines the form induced on Leech/(I-M)Leech = F_2^12 by the "
                        "Phi_4^12 element. The point set is all 4095 of PG(11,2); this pass "
                        "reports the form's rank and symmetry, and does NOT name a polar "
                        "space unless the rank is 12"),
           "element": {"order": 4, "trace": 0, "det_I_minus_M": 4096, "M2": "-I"},
           "invariant_form_space_dim": int(dim),
           "gram_symmetric": bool(sym),
           "forms": results,
           "export_lessons": [
               "GAP String() line-wraps with a backslash that can split a token, silently "
               "dropping a minus sign",
               "GAP QUIT cannot appear inside an if-block"]}
    op = ROOT / "data" / "PART_W33_PASS7333_LEECH_D4_FORM.json"
    op.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {op.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
