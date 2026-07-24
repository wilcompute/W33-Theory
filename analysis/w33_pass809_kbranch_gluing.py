#!/usr/bin/env python3
"""Pass 809: the k-branch gluing generalization.

Proposition prop:two-branch (Pass 806) glues the two saturated eigenlattices of
an operator with S(S-cI)=0.  Many substrate operators have more than two integer
eigenvalues -- the corrected flat block has two, but the K-track's signed-turn
operator K has the four eigenvalues -6, 2, 4, 10 -- so the gluing of ALL the
saturated eigenlattices is the natural object.  This pass states and validates
the k-branch version.

SET-UP.  Let S be an integral operator on Z^n, diagonalisable over Q with
distinct integer eigenvalues c_1 < ... < c_k and saturated eigenlattices
L_i = ker(S - c_i I).  The spectral projector onto L_i is
P_i = N_i / D_i with N_i = prod_{j != i}(S - c_j I) (an integer operator) and
D_i = prod_{j != i}(c_i - c_j) (a nonzero integer).  A vector v lies in the
direct sum of the saturated eigenlattices iff every P_i v is integral, i.e.

    v in (+)_i L_i   <=>   N_i v = 0  (mod D_i)  for all i,

so the gluing is

    Z^n / (+)_i L_i   =   Z^n / ( intersection_i ker(N_i mod D_i) ).

This reduces to Proposition prop:two-branch when k = 2 (there N_1 = S - c_2 and
D_1 = c_1 - c_2 = the eigenvalue gap, the single conductor).  For k >= 3 the
gluing is supported on the several products D_i, not a single conductor.

VALIDATION.  On constructed integer operators with prescribed integer spectrum the
projector-congruence gluing is checked against (i) the direct quotient by the
saturated eigenlattices and (ii) brute enumeration of the image of
Z^n -> (+)_i (Z/D_i)^n (finite because lcm(D_i) . Z^n lies in the kernel).  The
corrected flat block is recovered as the k = 2 case: gluing (Z/2)^{(q-1)^2/2}.
A worked k = 3 spectrum {2,4,10} gives gluing [2, 48], genuinely multi-conductor.

BOUNDARY.  The theorem needs the eigenvalues to be rational integers with S
diagonalisable; the modulus-q^n flat block (Pass 807) has an irrational spectrum
and is out of scope.  The K-operator computation (four eigenvalues) is the
intended application and is set up but not carried out here; this pass certifies
the general method and its k = 2 specialisation.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from math import gcd
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass809_kbranch_gluing.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def _lcm(a, b):
    return a * b // gcd(a, b)


def _torsion(Mcols):
    if not Mcols or Mcols.cols == 0:
        return []
    D = smith_normal_form(Mcols, domain=sp.ZZ)
    r = min(D.shape)
    return sorted(abs(int(D[i, i])) for i in range(r) if abs(int(D[i, i])) > 1)


def _primitive(v):
    dens = [sp.Rational(x).q for x in v]
    L = 1
    for d in dens:
        L = sp.ilcm(L, d)
    vi = [int(sp.Rational(x) * L) for x in v]
    g = 0
    for x in vi:
        g = gcd(g, x)
    if g > 1:
        vi = [x // g for x in vi]
    return vi


def gluing_projector_congruence(S, cs):
    """gluing = Z^n / intersection_i ker(N_i mod D_i), by projecting ker of [N_i | -D_i I]."""
    n = S.shape[0]
    total = 0
    data = []
    for c in cs:
        N = sp.eye(n)
        D = 1
        for d in cs:
            if d != c:
                N = N * (S - d * sp.eye(n))
                D *= (c - d)
        data.append((N, abs(D)))
        total += n
    ncols = n + n * len(cs)
    A = sp.zeros(total, ncols)
    r, col = 0, n
    for (N, D) in data:
        A[r:r + n, 0:n] = N
        A[r:r + n, col:col + n] = -D * sp.eye(n)
        r += n
        col += n
    proj = [_primitive(list(v[:n])) for v in A.nullspace()]
    Lb = sp.Matrix(proj).T if proj else sp.zeros(n, 0)
    return _torsion(Lb)


def gluing_direct_saturated(S, cs):
    """gluing = Z^n / (+)_i L_i via primitive eigenvectors (saturated for simple spectra)."""
    n = S.shape[0]
    cols = []
    for c in cs:
        for v in (S - c * sp.eye(n)).nullspace():
            cols.append(_primitive(list(v)))
    return _torsion(sp.Matrix(cols).T)


def gluing_brute_order(S, cs):
    """|gluing| by enumerating image of Z^n -> (+)_i (Z/D_i)^n (mod m = lcm D_i)."""
    n = S.shape[0]
    Ds, Ns = [], []
    for c in cs:
        N = sp.eye(n)
        D = 1
        for d in cs:
            if d != c:
                N = N * (S - d * sp.eye(n))
                D *= (c - d)
        Ns.append([[int(N[i, j]) for j in range(n)] for i in range(n)])
        Ds.append(abs(int(D)))
    m = 1
    for D in Ds:
        m = _lcm(m, D)
    seen = set()
    for v in itertools.product(range(m), repeat=n):
        key = []
        for N, D in zip(Ns, Ds):
            for i in range(n):
                key.append(sum(N[i][j] * v[j] for j in range(n)) % D)
        seen.add(tuple(key))
    return len(seen)


def part_A_validation(checks):
    rows = {}
    ok = True
    examples = [
        ("eig_2_4_10", sp.Matrix([[2, 1, 1], [0, 4, 1], [0, 0, 10]]), [2, 4, 10]),
        ("eig_0_3_6", sp.Matrix([[0, 2, 1], [0, 3, 1], [0, 0, 6]]), [0, 3, 6]),
        ("eig_m6_2_4", sp.Matrix([[-6, 1, 2], [0, 2, 3], [0, 0, 4]]), [-6, 2, 4]),
    ]
    for name, S, cs in examples:
        g1 = gluing_projector_congruence(S, cs)
        g2 = gluing_direct_saturated(S, cs)
        order = 1
        for x in g1:
            order *= x
        ob = gluing_brute_order(S, cs)
        agree = (g1 == g2 and order == ob)
        if not agree:
            ok = False
        rows[name] = {"eigenvalues": cs, "gluing": g1,
                      "direct_matches": g1 == g2,
                      "order": order, "brute_order": ob,
                      "all_agree": agree}
    checks["three_methods_agree_on_k_branch"] = ok
    return {"rows": rows,
            "theorem": "gluing = Z^n / intersection_i ker(N_i mod D_i)",
            "reading": (
                "For k>=3 integer eigenvalues the saturated-eigenlattice gluing "
                "is Z^n modulo the intersection of the congruence kernels "
                "N_i v = 0 mod D_i; three independent methods "
                "(projector-congruence, direct saturated quotient, brute image "
                "enumeration) agree, e.g. spectrum {2,4,10} gives [2,48].")}


def part_B_flatblock_k2(checks):
    """The k=2 case recovers the corrected flat-block gluing (Z/2)^{(q-1)^2/2}."""
    rows = {}
    ok = True
    for p in (3, 5):
        R, C = LF(p, 1), Cyc(p, 1)
        H = Heis(R, C)
        q = H.q
        deg = len(C.zero())
        n = q * deg
        F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
        # integer representation of F
        M = sp.zeros(n, n)
        for jc in range(q):
            for ds in range(deg):
                u = [0] * deg
                u[ds] = 1
                col = jc * deg + ds
                for ir in range(q):
                    pr = C.mul(tuple(u), F[ir][jc])
                    for e in range(deg):
                        M[ir * deg + e, col] = pr[e]
        g = gluing_projector_congruence(M, [q - 1, -(q + 1)])
        exp = (q - 1) ** 2 // 2
        from collections import Counter
        struct = dict(Counter(g))
        good = (struct == {2: exp})
        if not good:
            ok = False
        rows[f"q{q}"] = {"gluing": struct, "expected": {"2": exp},
                         "matches_pass808": good}
    checks["k2_recovers_corrected_flatblock"] = ok
    return {"rows": rows,
            "reading": (
                "Setting k=2 with the flat block's eigenvalues q-1 and -(q+1), "
                "the k-branch method returns the corrected pure 2-torsion gluing "
                "(Z/2)^{(q-1)^2/2} of Pass 808, confirming the generalization is "
                "consistent with the corrected two-branch result.")}


def part_C_scope(checks):
    checks["boundary_stated"] = True
    return {"target": (
        "The K-track signed-turn operator K has four integer eigenvalues "
        "-6, 2, 4, 10; its full four-branch gluing is the intended application "
        "of this method and the next computation."),
        "out_of_scope": (
            "The modulus-q^n flat block has an irrational spectrum (Pass 807) "
            "and no integer eigenlattices, so the k-branch method does not "
            "apply to it."),
        "multi_conductor": (
            "For k>=3 the gluing is supported on the products "
            "D_i = prod_{j!=i}(c_i-c_j), not a single conductor; a closed "
            "structural form in terms of the D_i is open.")}


def main_payload():
    checks = {}
    A = part_A_validation(checks)
    B = part_B_flatblock_k2(checks)
    C = part_C_scope(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass809.kbranch_gluing.v1",
        "status": status,
        "headline": (
            "THE k-BRANCH GLUING GENERALIZATION.  For an integral operator S "
            "diagonalisable over Q with distinct integer eigenvalues c_1..c_k "
            "and saturated eigenlattices L_i=ker(S-c_iI), the spectral projector "
            "P_i=N_i/D_i (N_i=prod_{j!=i}(S-c_j), D_i=prod_{j!=i}(c_i-c_j)) gives "
            "the gluing Z^n/(+)_i L_i = Z^n/intersection_i ker(N_i mod D_i), "
            "reducing to Proposition prop:two-branch at k=2 (single conductor = "
            "eigenvalue gap).  Validated three independent ways on constructed "
            "spectra ({2,4,10} -> [2,48]) and shown to recover the corrected "
            "flat-block (Z/2)^{(q-1)^2/2} at k=2.  For k>=3 the gluing is "
            "multi-conductor, supported on the D_i.  The K-track's four-eigenvalue "
            "signed-turn operator is the intended next application."),
        "part_A_validation": A,
        "part_B_flatblock_k2": B,
        "part_C_scope": C,
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 809 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
