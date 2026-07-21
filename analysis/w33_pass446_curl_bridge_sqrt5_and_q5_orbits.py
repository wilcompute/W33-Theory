#!/usr/bin/env python3
"""Pass 446: the exp-9 PDS is section-shaped in its own group, a numerical
Weil-spectrum match accompanies the exact curved graph factor, and Aut(H_5)
has 20,592 section orbits at q=5.

Three computations bridging the newest results of both streams (their 443
curl classification, my 445 companion PDS), plus the Lean and survey artifacts
shipped alongside.

=== 1. THE CURL<->EXP-9 BRIDGE: THE COMPANION PDS IS SECTION-SHAPED ===

Pass 445 built the PDS D9 in R = 3^{1+2}_- (exponent 9). Question: does 443's
flat/curved dichotomy see it? First, is D9 even section-shaped in R? Computed:

  * the 8 noncentral elements of D9 hit the 8 nonzero cosets of Z(R) EXACTLY
    ONCE: D9 = (a section of R/Z) u (Z \\ {1}), the same shape as the
    Heisenberg PDS;
  * choosing the transversal x^a y^b of R (x of order 9, y of order 3), the
    section's central offsets and the decomposition are computed.

The earlier draft called this section flat, but it never implemented the
required offset-linearity/curl equations.  This pass therefore certifies the
section shape and decomposition only; flatness in the Pass-443 sense remains
an explicit follow-up calculation.

=== 2. AN EXACT GRAPH FACTOR AND A NUMERICAL WEIL-SPECTRUM MATCH ===

Their 443 curved class has characteristic factor (x^2 - x - 11)^6, splitting
field Q(sqrt45) = Q(sqrt5) -- a real quadratic field inside a q=3 object.
Computed here:

  * the curved-graph nonrational eigenvalues are exactly the roots of
    x^2 - x - 11 (verified from the built graph);
  * one $3\times3$ complex matrix model passes all 729 multiplication tests
    numerically, and its sum has real eigenvalues matching the same quadratic
    roots to the recorded tolerance.

The arithmetic statement disc(x^2-x-11) = 45 = 9*5 is exact.  The matrix
comparison is numerical evidence, not an exact Gauss-sum identity or proof of
origin; the former exact-origin wording is withdrawn.

=== 3. q=5 SECTION ORBITS: EXACTLY 20,592 ===

Their v1.4 gate 4 asks for the q=5 section classification without raw
5^12-enumeration. Executed here by Burnside on the quotient:

  * inverse-closed sections of (H_5/Z) \\ {0} = central-offset functions on
    the 12 coset PAIRS: a 12-dimensional F_5 space;
  * inner automorphisms shift offsets by linear functionals (the 2-dim
    subspace L = {c_w}); the full action is the affine
    GL(2,5)-by-linear-offset action of order 480*25 = 12,000, including the
    determinant twist on the centre;
  * exact affine Burnside averaging gives

        ** number of Aut(H_5)-orbits = 20,592. **

The integer counting floor is ceil(5^12/12,000) = 20,346, so this action is
nearly free.  This corrects
the abandoned three-class draft: q=5 does not collapse to flat plus two
curved classes.  Later passes study the much larger fixed-sheet SL(2,5)
action separately; the two orbit counts must not be conflated.

=== SHIPPED ALONGSIDE ===

formal/W33/Pass446CoverArray.lean -- the cover-law and nesting arithmetic
identities (shell sums, b1, trace-pinned multiplicities, SRG parameter
algebra) in the Pass-441 Lean idiom, imported by formal/W33.lean. NOT built
locally (no Lake in this container, per formal/README); the pinned CI Lean
job is the checker, and this is stated rather than hidden.

papers/register_cell_filtration_survey.tex -- the cross-stream survey: one
object, one filtration (cover -> sections -> curl -> conductor -> Hjelmslev),
the no-go boundary, and the attribution table.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass446_curl_bridge_sqrt5_and_q5_orbits.json"


def perm_tools(n):
    ident = tuple(range(n))

    def comp(a, b):
        return tuple(a[i] for i in b)

    def inv(p):
        r = [0] * n
        for i, j in enumerate(p):
            r[j] = i
        return tuple(r)

    def order(p):
        o, c = 1, p
        while c != ident:
            c = comp(p, c)
            o += 1
        return o

    def closure(gs, cap):
        s = {ident}
        fr = [ident]
        while fr:
            nf = []
            for x in fr:
                for g in gs:
                    y = comp(g, x)
                    if y not in s:
                        s.add(y)
                        nf.append(y)
                        if len(s) > cap:
                            return s
            fr = nf
        return s

    return ident, comp, inv, order, closure


def main():
    checks = {}

    # ================= 1. the curl<->exp-9 bridge =================
    def hmul(g, h, q=3):
        return (
            (g[0] + h[0]) % q,
            (g[1] + h[1]) % q,
            (g[2] + h[2] - g[0] * h[1] + h[0] * g[1]) % q,
        )

    elems = [(a, b, c) for a in range(3) for b in range(3) for c in range(3)]
    eidx = {e: i for i, e in enumerate(elems)}
    D = [(v0, v1, 0) for v0 in range(3) for v1 in range(3) if (v0, v1) != (0, 0)] + [
        (0, 0, c) for c in range(1, 3)
    ]
    A = np.zeros((27, 27), np.int8)
    for i, g in enumerate(elems):
        for d in D:
            A[i, eidx[hmul(g, d)]] = 1
    transL = [tuple(eidx[hmul(h, x)] for x in elems) for h in elems]
    up = tuple(eidx[((g[0]) % 3, (g[0] + g[1]) % 3, g[2])] for g in elems)
    I27, comp, inv, order, closure = perm_tools(27)
    Syl = closure(transL + [up], 90)
    Sl = list(Syl)
    fg = [comp(comp(a, b), comp(inv(a), inv(b))) for a in Sl[:30] for b in Sl[:30]] + [
        comp(a, comp(a, a)) for a in Sl
    ]
    Phi = closure([g for g in fg if g != I27] or [I27], 100)
    reps, seen = [], set()
    for a in Sl:
        key = frozenset(comp(a, f) for f in Phi)
        if key not in seen:
            seen.add(key)
            reps.append(a)
    exp9 = []
    for c2 in combinations(range(1, len(reps)), 2):
        Hs = closure(list(Phi) + [reps[c2[0]], reps[c2[1]]], 27)
        if len(Hs) == 27:
            Hl = list(Hs)
            reg = all(h == I27 or all(h[i] != i for i in range(27)) for h in Hl)
            ords = sorted({order(h) for h in Hl if h != I27})
            if reg and ords == [3, 9]:
                exp9.append(Hl)
    checks["exp9_subgroups_found"] = len(exp9) >= 1
    R = exp9[0]
    D9 = [r for r in R if r != I27 and A[0, r[0]]]
    Z_R = [r for r in R if all(comp(r, s) == comp(s, r) for s in R)]
    Zset = {tuple(z) for z in Z_R}
    # (a) section-shaped: 8 noncentral D9 elements hit 8 distinct Z-cosets
    noncen = [r for r in D9 if tuple(r) not in Zset]
    cosets = set()
    for r in noncen:
        key = frozenset(tuple(comp(r, z)) for z in Z_R)
        cosets.add(key)
    checks["D9_noncentral_8"] = len(noncen) == 8
    checks["D9_hits_8_distinct_cosets"] = len(cosets) == 8
    checks["D9_is_section_plus_centre"] = (
        len(noncen) == 8 and len(cosets) == 8 and len(D9) == 10
    )
    # (b) flatness in R: pick generators x (order 9), y in R, transversal x^a y^b
    xg = next(r for r in R if order(r) == 9)
    yg = next(
        r
        for r in R
        if order(r) == 3 and tuple(r) not in Zset and comp(r, xg) != comp(xg, r)
    )
    z_c = comp(comp(xg, yg), comp(inv(xg), inv(yg)))  # commutator, central
    checks["commutator_central"] = tuple(z_c) in Zset and z_c != I27
    # transversal: t(a,b) = x^a y^b, a,b in 0..2; central offsets of D9:
    # for each noncentral d in D9, find (a,b,k): d = x^a y^b z^k
    zpow = {tuple(I27): 0}
    zz = z_c
    for k in (1, 2):
        zpow[tuple(zz)] = k
        zz = comp(z_c, zz)
    offs = {}
    ok_decomp = True
    for d in noncen:
        found = False
        for a in range(9):
            for b in range(3):
                t = I27
                for _ in range(a):
                    t = comp(xg, t)
                for _ in range(b):
                    t = comp(yg, t)
                w = comp(inv(t), d)
                if tuple(w) in zpow:
                    # coset label = (a mod 3, b) on R/Z (x^3 is central!)
                    lab = (a % 3, b)
                    offs.setdefault(lab, []).append((a, b, zpow[tuple(w)]))
                    found = True
                    break
            if found:
                break
        if not found:
            ok_decomp = False
    checks["decomposition_ok"] = ok_decomp
    # This verifies section shape and transversal decomposition.  It does not
    # implement the Pass-443 offset-linearity/curl equations, so no flatness
    # check is claimed here.
    checks["D9_section_shape_and_decomposition_verified"] = (
        checks["D9_is_section_plus_centre"] and ok_decomp
    )

    # ================= 2. the sqrt5 origin =================
    # THEIR conventions (Pass 443): PAIRS ordering + curved rep (0,0,0,1);
    # sections are section-ONLY Cayley sets (8-regular) -- the first draft
    # wrongly added the centre and got a 10-regular graph; caught by the
    # charpoly check.
    PAIRS = [((0, 1), (0, 2)), ((1, 0), (2, 0)), ((1, 1), (2, 2)), ((1, 2), (2, 1))]
    coffs = (0, 0, 0, 1)
    Dc = []
    for (v, nv), c0 in zip(PAIRS, coffs):
        Dc.append((v[0], v[1], c0))
        Dc.append((nv[0], nv[1], (-c0) % 3))
    Ac = np.zeros((27, 27), np.int8)
    for i, g in enumerate(elems):
        for d in Dc:
            Ac[i, eidx[hmul(g, d)]] = 1
    x = sp.Symbol("x")
    cp = sp.factor(sp.Matrix(Ac.tolist()).charpoly(x).as_expr())
    target = (x - 8) * (x + 1) ** 14 * (x**2 - x - 11) ** 6
    checks["curved_charpoly_matches_443"] = sp.expand(cp - target) == 0
    w3 = np.exp(2j * np.pi / 3)
    X = np.roll(np.eye(3), 1, axis=0)
    Z = np.diag([1, w3, w3**2])

    def rho(g, eps=1, gamma=1, kappa=0):
        a, b, c = g
        return (w3 ** (eps * (c + kappa * a * b))) * (
            np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, (b * gamma) % 3)
        )

    model = None
    for eps in (1, 2):
        for gamma in (1, 2):
            for kappa in (0, 1, 2):
                ok = all(
                    np.allclose(
                        rho(hmul(g, h), eps, gamma, kappa),
                        rho(g, eps, gamma, kappa) @ rho(h, eps, gamma, kappa),
                        atol=1e-9,
                    )
                    for g in elems
                    for h in elems
                )  # ALL 729 pairs
                if ok:
                    model = (eps, gamma, kappa)
                    break
            if model:
                break
        if model:
            break
    checks["weil_model_numerically_verified_all_729"] = model is not None
    M = sum(rho(d, *model) for d in Dc)
    evM = np.linalg.eigvals(M)
    r1, r2 = sp.solve(x**2 - x - 11, x)
    vals = {round(float(r1), 5), round(float(r2), 5)}
    got = {round(float(v), 5) for v in evM.real}
    checks["weil_sum_eigs_real"] = bool(np.allclose(evM.imag, 0, atol=1e-6))
    checks["sqrt5_numerically_matches_weil_sum"] = len(vals & got) == 2
    checks["third_eigenvalue_minus1"] = any(abs(v + 1) < 1e-6 for v in evM.real)
    checks["disc_45_is_9_times_5"] = 45 == 9 * 5
    weil_eigs = [float(v) for v in np.round(sorted(evM.real), 6)]

    # ================= 3. q=5 Burnside: orbits on sections =================
    # CORRECTED from the first draft, which forgot the determinant twist on the
    # centre and used the wrong quotient derivation.  Aut(H_5)-orbits on
    # inverse-closed sections
    # = orbits of the AFFINE group GL(2,5) x L (L = linear offsets, from inner
    # automorphisms) on the 12-dim offset space, where g in GL(2,5) acts on
    # offsets with the DET twist (the centre transforms by det g):
    #     (g.c)(g*pair) = det(g) * sgn * c(pair).
    # Affine Burnside: #orbits = (1/(480*25)) * sum_g |im(1-g) cap L| * 5^{dim ker(1-g)}.
    q5 = 5
    vecs5 = [(a, b) for a in range(5) for b in range(5) if (a, b) != (0, 0)]
    pairs5 = []
    used = set()
    for v in vecs5:
        nv = ((-v[0]) % 5, (-v[1]) % 5)
        key = tuple(sorted([v, nv]))
        if key not in used:
            used.add(key)
            pairs5.append(key)
    pidx = {p: i for i, p in enumerate(pairs5)}
    checks["twelve_pairs"] = len(pairs5) == 12
    gl25 = []
    for m in product(range(5), repeat=4):
        if (m[0] * m[3] - m[1] * m[2]) % 5 != 0:
            gl25.append(((m[0], m[1]), (m[2], m[3])))
    checks["gl25_order_480"] = len(gl25) == 480

    def f5_rank(Mat):
        Mw = Mat.copy() % 5
        rows, cols = Mw.shape
        pr = 0
        for c_ in range(cols):
            piv = None
            for r_ in range(pr, rows):
                if Mw[r_, c_] % 5:
                    piv = r_
                    break
            if piv is None:
                continue
            Mw[[pr, piv]] = Mw[[piv, pr]]
            invp = pow(int(Mw[pr, c_]), 3, 5)
            Mw[pr] = (Mw[pr] * invp) % 5
            for r_ in range(rows):
                if r_ != pr and Mw[r_, c_] % 5:
                    Mw[r_] = (Mw[r_] - Mw[r_, c_] * Mw[pr]) % 5
            pr += 1
        return pr

    def cw_offsets(wv):
        return np.array(
            [(wv[0] * p[0][1] - wv[1] * p[0][0]) % 5 for p in pairs5], np.int64
        )

    Lb = [cw_offsets((1, 0)), cw_offsets((0, 1))]
    total = 0
    for m in gl25:
        det = (m[0][0] * m[1][1] - m[0][1] * m[1][0]) % 5
        Mg = np.zeros((12, 12), np.int64)
        for p in pairs5:
            v = p[0]
            w = (
                (m[0][0] * v[0] + m[0][1] * v[1]) % 5,
                (m[1][0] * v[0] + m[1][1] * v[1]) % 5,
            )
            tgt = tuple(sorted([w, ((-w[0]) % 5, (-w[1]) % 5)]))
            sgn = 1 if w == tgt[0] else -1
            Mg[pidx[tgt], pidx[p]] = (det * sgn) % 5
        Delta = (Mg - np.eye(12, dtype=np.int64)) % 5
        rk = f5_rank(Delta)
        dim_ker = 12 - rk
        # |im(1-g) cap L|: dim = rk + 2 - dim(im + L)
        stacked = np.concatenate(
            [Delta.T % 5, np.stack(Lb) % 5], axis=0
        )  # rows span im+L
        dim_sum = f5_rank(stacked.T)
        dim_cap = rk + 2 - dim_sum
        total += (5**dim_cap) * (5**dim_ker)
    denom = 480 * 25
    checks["burnside_integral"] = total % denom == 0
    n_orbits = total // denom
    q5_orbits = n_orbits
    checks["q5_orbit_count_20592"] = n_orbits == 20592
    checks["integer_counting_floor_20346"] = (5**12 + 12000 - 1) // 12000 == 20346
    checks["action_nearly_free"] = n_orbits - 20346 < 300
    # validate the formula on the known q=3 case: 2 orbits
    # (compact inline re-run at q=3)
    q3v = 3
    vecs3 = [(a, b) for a in range(3) for b in range(3) if (a, b) != (0, 0)]
    pr3 = []
    us3 = set()
    for v in vecs3:
        nv = ((-v[0]) % 3, (-v[1]) % 3)
        key = tuple(sorted([v, nv]))
        if key not in us3:
            us3.add(key)
            pr3.append(key)
    pi3 = {p: i for i, p in enumerate(pr3)}
    gl3 = [
        ((m[0], m[1]), (m[2], m[3]))
        for m in product(range(3), repeat=4)
        if (m[0] * m[3] - m[1] * m[2]) % 3
    ]

    def rank_q(Mat, qq):
        Mw = Mat.copy() % qq
        rows, cols = Mw.shape
        pr_ = 0
        for c_ in range(cols):
            piv = None
            for r_ in range(pr_, rows):
                if Mw[r_, c_] % qq:
                    piv = r_
                    break
            if piv is None:
                continue
            Mw[[pr_, piv]] = Mw[[piv, pr_]]
            invp = pow(int(Mw[pr_, c_]), qq - 2, qq)
            Mw[pr_] = (Mw[pr_] * invp) % qq
            for r_ in range(rows):
                if r_ != pr_ and Mw[r_, c_] % qq:
                    Mw[r_] = (Mw[r_] - Mw[r_, c_] * Mw[pr_]) % qq
            pr_ += 1
        return pr_

    Lb3 = [
        np.array([(1 * p[0][1] - 0 * p[0][0]) % 3 for p in pr3], np.int64),
        np.array([(0 * p[0][1] - 1 * p[0][0]) % 3 for p in pr3], np.int64),
    ]
    tot3 = 0
    for m in gl3:
        det = (m[0][0] * m[1][1] - m[0][1] * m[1][0]) % 3
        Mg = np.zeros((4, 4), np.int64)
        for p in pr3:
            v = p[0]
            w = (
                (m[0][0] * v[0] + m[0][1] * v[1]) % 3,
                (m[1][0] * v[0] + m[1][1] * v[1]) % 3,
            )
            tgt = tuple(sorted([w, ((-w[0]) % 3, (-w[1]) % 3)]))
            sgn = 1 if w == tgt[0] else -1
            Mg[pi3[tgt], pi3[p]] = (det * sgn) % 3
        Delta = (Mg - np.eye(4, dtype=np.int64)) % 3
        rk = rank_q(Delta, 3)
        stacked = np.concatenate([Delta.T % 3, np.stack(Lb3) % 3], axis=0)
        dsum = rank_q(stacked.T, 3)
        dcap = rk + 2 - dsum
        tot3 += (3**dcap) * (3 ** (4 - rk))
    checks["formula_validates_q3_two_orbits"] = tot3 == 2 * 48 * 9

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass446.curl_bridge_sqrt5_q5_orbits.v1",
        "status": "PASS" if all_pass else "FAIL",
        "HEADLINE": (
            "THREE results. (1) The exp-9 companion PDS is SECTION-SHAPED: "
            "D9's eight noncentral elements hit the eight Z(R)-cosets exactly "
            "once.  The earlier flatness claim is withdrawn because the curl "
            "equations were not implemented. (2) The curved graph factor "
            "(x^2-x-11)^6 (disc 45 = 9*5) is exact; a 3x3 complex matrix model "
            "numerically matches the same quadratic after all 729 multiplication "
            "tests.  This is evidence, not an exact Weil/Gauss-sum origin. "
            "(3) BURNSIDE AT "
            f"q=5: Aut(H_5)-orbits on inverse-closed sections = {q5_orbits} "
            "under the complete determinant-twisted affine action of order "
            "12,000.  This is close to the integer counting floor 20,346 and is not a "
            "three-class stratification.  Their v1.4 gate 4 is answered by "
            "Burnside instead of 5^12 enumeration."
        ),
        "weil_sum_eigenvalues": weil_eigs,
        "q5_section_orbits": q5_orbits,
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "passed": sum(payload["checks"].values()),
                "total": len(payload["checks"]),
                "q5_orbits": q5_orbits,
                "weil_eigs": weil_eigs,
            }
        )
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
