"""Driver for Passes 9961-9984 -- computes every number the write-up reports.

Recomputes, from the E8 Cartan matrix and the stored order-4 isometry:
  * Phi_d(1) over a range of d                        (the limitation theorem)
  * the d=8, l=3 hyperbolic split of E8^2 mod 3       (the third branch)
  * E8/3E8 as H(3,9), with all four GQ parameters
  * E8/2E8 as H(3,4), with all four GQ parameters
  * the exact refinement of Q+(7,2) by the F_4 Hermitian structure

    py -3 analysis/w33_pass9961_9984_unitary_driver.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import block_diag
from sympy import Matrix, Poly, cyclotomic_poly, factor_list, symbols
from sympy.polys.domains import GF
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

X = symbols("x")
G8 = np.array(CARTAN, dtype=np.int64)
I8 = np.eye(8, dtype=np.int64)


def gf_rank(A, p):
    M = Matrix((np.array(A) % p).astype(int).tolist())
    return len(DomainMatrix.from_Matrix(M).convert_to(GF(p)).rref()[1])


def gf_nullspace(A, p):
    M = Matrix((np.array(A) % p).astype(int).tolist())
    ns = DomainMatrix.from_Matrix(M).convert_to(GF(p)).nullspace().to_Matrix()
    return np.array(ns.tolist(), dtype=object).astype(np.int64) % p


def coxeter_power_10():
    """The fixed-point-free order-3 isometry of E8, as Cox^10."""
    cox = I8.copy()
    for i in range(8):
        s = I8.copy().astype(np.int64)
        s[i, :] = s[i, :] - G8[i, :]
        cox = cox @ s
    return np.linalg.matrix_power(cox, 10)


def polar_census(M, G, p, deg, field_mul, field_conj, form):
    """Census a polar space on L/pL viewed over F_(p^deg) with M as the field generator."""
    n = G.shape[0]
    basis, span = [], []
    for k in range(n):
        e = np.zeros(n, dtype=np.int64)
        e[k] = 1
        cand = span + [e % p, (M @ e) % p]
        if gf_rank(np.array(cand), p) == len(span) + deg:
            basis.append(e)
            span = cand
        if len(basis) * deg == n:
            break
    scal = [tuple(c) for c in itertools.product(range(p), repeat=deg)]

    def vec(cs):
        out = np.zeros(n, dtype=np.int64)
        for (a, b), e in zip(cs, basis):
            out = out + a * e + b * (M @ e)
        return out % p

    zero = tuple([0] * deg)
    one = tuple([1] + [0] * (deg - 1))
    pts = []
    for cs in itertools.product(scal, repeat=len(basis)):
        if all(c == zero for c in cs):
            continue
        j = next(i for i, c in enumerate(cs) if c != zero)
        if cs[j] != one:
            continue
        v = vec(cs)
        if form(v, v) == zero:
            pts.append(v)
    key = lambda v: tuple(int(t) % p for t in v)  # noqa: E731
    idx = {key(v): i for i, v in enumerate(pts)}
    npl = p ** deg + 1
    lines = set()
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            if form(pts[a], pts[b]) != zero:
                continue
            L = set()
            for s in scal:
                for u in scal:
                    if s == zero and u == zero:
                        continue
                    z = (s[0] * pts[a] + s[1] * (M @ pts[a])
                         + u[0] * pts[b] + u[1] * (M @ pts[b])) % p
                    if key(z) in idx:
                        L.add(idx[key(z)])
            if len(L) == npl:
                lines.add(frozenset(L))
    per_pt = {}
    for L in lines:
        for q in L:
            per_pt[q] = per_pt.get(q, 0) + 1
    return {"points": len(pts), "lines": len(lines),
            "points_per_line": sorted({len(L) for L in lines}),
            "lines_per_point": sorted(set(per_pt.values())), "pts": pts, "basis": basis}


def main() -> int:
    print("=" * 78)
    print("Passes 9961-9984 driver")
    print("=" * 78)

    print("\n[1] the limitation theorem: Phi_d(1) is 1 or a prime\n")
    vals = {}
    for d in range(2, 40):
        vals[d] = int(Poly(cyclotomic_poly(d, X), X).eval(1))
    taken = sorted(set(vals.values()))
    print(f"    values of Phi_d(1) for d < 40 : {taken}")
    print(f"    proper prime powers among them: "
          f"{[q for q in (4, 8, 9, 16, 25, 27) if q in taken]}  (empty = theorem holds)")

    print("\n[2] third branch: d=8, l=3 on E8^2 (rank 16)\n")
    M8 = np.loadtxt(ROOT / "analysis" / "_e8_ord8.txt", dtype=np.int64)
    G16 = block_diag(G8, G8).astype(np.int64)
    M16 = block_diag(M8, M8).astype(np.int64)
    h, hb = [Poly(f, X, modulus=3) for f, _ in factor_list(cyclotomic_poly(8, X), modulus=3)[1]]

    def ev(poly, M, n):
        c = poly.all_coeffs()[::-1]
        out = np.zeros((n, n), dtype=np.int64)
        for i, co in enumerate(c):
            out = out + int(co) * np.linalg.matrix_power(M, i)
        return out % 3

    V, Vp = gf_nullspace(ev(h, M16, 16), 3), gf_nullspace(ev(hb, M16, 16), 3)
    print(f"    dim ker h(M) = {V.shape[0]},  dim ker hbar(M) = {Vp.shape[0]}")
    print(f"    G(V,V) zero      : {not ((V @ G16 @ V.T) % 3).any()}")
    print(f"    G(V',V') zero    : {not ((Vp @ G16 @ Vp.T) % 3).any()}")
    print(f"    G(V,V') rank     : {gf_rank(V @ G16 @ Vp.T, 3)}  (nondegenerate pairing)")

    print("\n[3] E8/3E8 = H(3,9)\n")
    M4 = np.loadtxt(ROOT / "analysis" / "_e8_ord4.txt", dtype=np.int64)
    assert np.array_equal(M4 @ M4, -I8) and np.array_equal(M4.T @ G8 @ M4, G8)

    def mul9(u, v):
        a, b = u
        c, d = v
        return ((a * c - b * d) % 3, (a * d + b * c) % 3)

    def h9(x, y):
        return (int(x @ G8 @ y) % 3, (-int((M4 @ x) @ G8 @ y)) % 3)

    r9 = polar_census(M4, G8, 3, 2, mul9, None, h9)
    print(f"    points {r9['points']}   lines {r9['lines']}   "
          f"points/line {r9['points_per_line']}   lines/point {r9['lines_per_point']}")
    print(f"    incidence closes : "
          f"{r9['points'] * r9['lines_per_point'][0] == r9['lines'] * r9['points_per_line'][0]}")

    print("\n[4] E8/2E8 = H(3,4), and the refinement of Q+(7,2)\n")
    W = coxeter_power_10()
    assert not (I8 + W + W @ W).any() and np.array_equal(W.T @ G8 @ W, G8)

    def cj4(u):
        a, b = u
        return ((a + b) % 2, b % 2)

    def mul4(u, v):
        a, b = u
        c, d = v
        return ((a * c + b * d) % 2, (a * d + b * c + b * d) % 2)

    w2 = cj4((0, 1))

    def h4(x, y):
        return mul4(w2, (int(x @ G8 @ y) % 2, int((W @ x) @ G8 @ y) % 2))

    r4 = polar_census(W, G8, 2, 2, mul4, cj4, h4)
    print(f"    points {r4['points']}   lines {r4['lines']}   "
          f"points/line {r4['points_per_line']}   lines/point {r4['lines_per_point']}")
    sing = {tuple(map(int, v)) for v in itertools.product(range(2), repeat=8)
            if any(v) and (int(np.array(v) @ G8 @ np.array(v)) // 2) % 2 == 0}
    expanded = set()
    for x in r4["pts"]:
        for a, b in ((1, 0), (0, 1), (1, 1)):
            expanded.add(tuple(map(int, (a * x + b * (W @ x)) % 2)))
    print(f"    q-singular points of Q+(7,2) : {len(sing)}")
    print(f"    isotropic F_4-points expanded: {len(expanded)}")
    print(f"    sets EQUAL                   : {expanded == sing}"
          f"   (symmetric difference {len(expanded ^ sing)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
