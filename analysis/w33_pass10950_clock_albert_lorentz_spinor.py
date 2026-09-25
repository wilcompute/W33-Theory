#!/usr/bin/env python3
"""Pass 10950 -- Lorentz so(1,9), the Weyl spinor 16 and matter parity in the clock Albert algebra.

Pass 10949 built, from the committed executable E8 bracket, a 27-dimensional
Euclidean Jordan algebra A inside p+ = {a8 = 0, a7 = +1} using the Hermitian
Jordan triple of the clock real form E7(-25).  This pass derives its symmetry
algebras objectwise and exactly:

  * Der(A) = [L_A, L_A] has dimension 52 and negative-definite trace form (compact F4);
  * str0(A) = Der(A) + L(A_0) has dimension 78 and trace-form inertia (26,52): E6(-26);
  * the stabiliser Der_c of a primitive idempotent c has dimension 36 (spin(9));
  * Der_c + L(spatial Peirce-0) is 45-dimensional and acts faithfully on the Peirce 10
    as the full Lie algebra of its Lorentzian (1,9) determinant: so(1,9);
  * the Peirce 16 is an absolutely irreducible real so(1,9) module: the Majorana-Weyl spinor;
  * a 3+1 split (time u = e - c, a frame direction, a Hermitian complex line) leaves
    so(1,3)+so(6) (dimension 21) whose commutant on the 16 is a complex structure:
    16 = (2,4) + conjugate;
  * the repository's Q_psi charge 27 = 16_1 + 10_-2 + 1_4 with triad pattern
    40 x (-2,1,1) + 5 x (-2,-2,4) is 6 L_c - 2 for every coordinate idempotent, and
    matter parity (-1)^Q_psi is the Peirce symmetry U_{2c-e} = the 2 pi rotation of Spin(9).

Finite exact algebra; the so(1,9) is an idempotent stabiliser in E6(-26), not a derived
physical spacetime.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from math import lcm
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import expm
from sympy import QQ
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10950_clock_albert_lorentz_spinor.json"
QPSI = ROOT / "data/w33_qpsi_matter_parity_e8_d8_bridge.json"

_spec = importlib.util.spec_from_file_location(
    "p10949", ROOT / "analysis/w33_pass10949_freudenthal_quasiconformal_clock_cone.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)


# ----------------------------------------------------------------- exact helpers
def dm(rows):
    return DomainMatrix([[QQ(int(Fr(x).numerator), int(Fr(x).denominator)) for x in r] for r in rows],
                        (len(rows), len(rows[0])), QQ)


def rank(rows):
    return dm(rows).rank()


def nullspace(rows):
    """Basis (list of Fraction lists) of {x : rows @ x = 0}."""
    ns = dm(rows).nullspace().to_Matrix()
    return [[Fr(int(sp.Rational(v).p), int(sp.Rational(v).q)) for v in ns.row(i)] for i in range(ns.rows)]


def ints(M):
    return np.array([[int(x) for x in r] for r in M], dtype=np.int64)


def inertia_int(G):
    return P.exact_inertia([[int(x) for x in r] for r in np.asarray(G)])


# ----------------------------------------------------------------- the clock Albert algebra
def build_clock_albert():
    E = P.E8()
    meta = json.loads(P.META.read_text())
    byroot = {tuple(r["root_orbit"]): r for r in meta["rows"]}
    canon = json.loads(P.CANON.read_text())
    dsign = {tuple(sorted(map(int, x["triple"]))): int(x["sign"]) for x in canon["solution"]["d_triples"]}
    comp = {a: (-1) ** (sum(E.root_of[a]) % 2) for a in E.root_of}
    Pp = sorted(i for i, r in E.root_of.items() if r[7] == 0 and r[6] == 1)

    def tb(i, j, k):
        res = defaultdict(int)
        for m, c1 in E.br(i, E.neg[j]).items():
            for t, c2 in E.br(m, k).items():
                res[t] += -comp[j] * c1 * c2
        return {t: c for t, c in res.items() if c}

    def triple(x, y, z):
        res = defaultdict(P.CQ)
        for i, a in x.items():
            for j, b in y.items():
                bc = b.conj()
                for k, c in z.items():
                    coef = a * bc * c
                    for t, v in tb(i, j, k).items():
                        res[t] = res[t] + coef * v
        return {t: v for t, v in res.items() if v.nz()}

    lab = {i: byroot[E.root_of[i]]["i27"] for i in Pp}
    ofl = {v: k for k, v in lab.items()}
    frame = sorted(dsign)[0]
    G = [ofl[t] for t in frame]
    one = P.CQ(1)
    Evec = {g: one for g in G}
    star = {}
    for a in Pp:
        (b, v), = triple(Evec, {a: one}, Evec).items()
        star[a] = (b, v.a / 2)
    basis, seen, labels = [], set(), []
    for a in Pp:
        if a in seen:
            continue
        b, s = star[a]
        if b == a:
            seen.add(a)
            basis.append({a: one} if s == 1 else {a: P.CQ(0, 1)})
            labels.append(("fixed", lab[a], lab[a]))
        else:
            seen |= {a, b}
            basis.append({a: one, b: P.CQ(s)})
            basis.append({a: P.CQ(0, 1), b: P.CQ(0, -s)})
            labels.append(("pair_re", lab[a], lab[b]))
            labels.append(("pair_im", lab[a], lab[b]))
    rows = []
    for x in basis:
        col = []
        for a in Pp:
            c = x.get(a, P.CQ())
            col += [c.a, c.b]
        rows.append(col)
    Mb = sp.Matrix(rows).T
    Mp = (Mb.T * Mb).inv() * Mb.T

    def coords(x):
        v = []
        for a in Pp:
            c = x.get(a, P.CQ())
            v += [c.a, c.b]
        sol = Mp * sp.Matrix(v)
        assert Mb * sol == sp.Matrix(v)
        return [Fr(int(t.p), int(t.q)) for t in sol]

    n = len(basis)
    prod = np.empty((n, n, n), dtype=object)
    for i in range(n):
        for j in range(i, n):
            t = triple(basis[i], Evec, basis[j])
            c = coords({k: v * Fr(1, 2) for k, v in t.items()})
            prod[i, j, :] = c
            prod[j, i, :] = c
    idx_of = {next(iter(x)): k for k, x in enumerate(basis) if len(x) == 1 and next(iter(x.values())) == one}
    return {"n": n, "prod": prod, "frame": frame, "G": G, "idx": idx_of, "labels": labels,
            "dsign": dsign}


def main(write=True):
    J = build_clock_albert()
    n, prodF, dsign = J["n"], J["prod"], J["dsign"]
    den = lcm(*[x.denominator for x in prodF.flat])
    Pi = np.array([[[int(x * den) for x in prodF[i, j]] for j in range(n)] for i in range(n)], dtype=np.int64)
    # scaled multiplication operators: Ls[i][k, j] = den * (b_i o b_j)_k
    Ls = np.stack([Pi[i].T for i in range(n)])  # Ls[i] @ x  = den * (b_i o x)

    def Lv(x):  # den * L_x for an integer vector x
        return np.tensordot(np.asarray(x, dtype=np.int64), Ls, axes=1)

    def mulv(x, y):  # den * (x o y)
        return np.asarray(x, dtype=np.int64) @ np.tensordot(Pi, np.asarray(y, dtype=np.int64), axes=([1], [0]))

    I = np.eye(n, dtype=np.int64)
    idx, G = J["idx"], J["G"]
    evec = sum(I[idx[g]] for g in G)
    cvec = I[idx[G[0]]]
    e2, e3 = I[idx[G[1]]], I[idx[G[2]]]
    assert all((mulv(evec, I[k]) == den * I[k]).all() for k in range(n))
    trL = np.array([np.trace(Ls[i]) for i in range(n)])  # den * Tr L_{b_i}

    def T(x):
        return Fr(int(np.dot(trL, x)), 9 * den)

    out = {"schema": "w33.pass10950.clock_albert_lorentz_spinor.v1",
           "parents": ["data/w33_pass10949_freudenthal_quasiconformal_clock_cone.json",
                       "analysis/w33_pass10949_freudenthal_quasiconformal_clock_cone.py",
                       "data/w33_qpsi_matter_parity_e8_d8_bridge.json"],
           "scaling": f"multiplication operators stored as {den} * L_x (integer)"}

    # ---- Der = span [L_i, L_j] ---------------------------------------------------------
    comms = [Ls[i] @ Ls[j] - Ls[j] @ Ls[i] for i, j in itertools.combinations(range(n), 2)]
    flatc = [c.flatten().tolist() for c in comms]
    r_der = rank(flatc)
    # pick an explicit independent subset
    basisD, chosen = [], []
    for k, v in enumerate(flatc):
        if rank(chosen + [v]) > len(chosen):
            chosen.append(v)
            basisD.append(comms[k])
        if len(chosen) == r_der:
            break
    assert r_der == 52 == len(basisD)
    # derivation property for the basis: D(b_i o b_j) = D b_i o b_j + b_i o D b_j (all scaled)
    der_fail = 0
    for D in basisD:
        for i in range(n):
            lhs = D @ Pi[i].T  # columns j: D (den b_i o b_j)
            rhs = Ls[i] @ D + np.stack([mulv(D[:, i], I[j]) for j in range(n)]).T
            der_fail += not (lhs == rhs).all()
    gD = np.array([[np.trace(A @ B) for B in basisD] for A in basisD])
    inD = inertia_int(gD)
    assert der_fail == 0 and inD == (0, 52, 0)

    # ---- str0 = Der + L(traceless) ------------------------------------------------------
    # traceless elements x - T(x) e/3, scaled to integers
    tl = []
    for k in range(n):
        tk = T(I[k])
        tl.append([Fr(int(I[k][t])) - tk * int(evec[t]) / 3 for t in range(n)])
    tl_den = lcm(*[x.denominator for v in tl for x in v])
    tl_int = [np.array([int(x * tl_den) for x in v], dtype=np.int64) for v in tl]
    Ltl = [Lv(v) for v in tl_int]
    r_tl = rank([m.flatten().tolist() for m in Ltl])
    assert r_tl == 26
    # generating identities: [D, L_x] = L_{Dx}
    gen_fail = 0
    for D in basisD:
        for k in range(n):
            lhs = D @ Ls[k] - Ls[k] @ D
            rhs = Lv(D[:, k])  # both sides equal den^3 * L_{D b_k}
            gen_fail += not (lhs == rhs).all()
    assert gen_fail == 0
    str_basis = basisD + [m for m in Ltl]
    r_str = rank([m.flatten().tolist() for m in str_basis])
    assert r_str == 78
    tl_ind = []
    for m in Ltl:
        if rank([x.flatten().tolist() for x in basisD + tl_ind + [m]]) > 52 + len(tl_ind):
            tl_ind.append(m)
    sb = basisD + tl_ind
    gS = np.array([[np.trace(A @ B) for B in sb] for A in sb], dtype=object)
    inS = inertia_int(gS)
    assert inS == (26, 52, 0)
    out["structure"] = {
        "Der_dimension": r_der, "Der_is_derivation_failures": der_fail,
        "Der_trace_form_inertia": list(inD), "Der_real_form": "compact F4",
        "traceless_multiplications": r_tl,
        "generating_identity_[D,L_x]=L_(Dx)_failures": gen_fail,
        "str0_dimension": r_str, "str0_trace_form_inertia": list(inS),
        "str0_real_form": "E6(-26) (signature 26-52 = -26)",
    }

    # ---- Peirce data of c ----------------------------------------------------------------
    Lc = Lv(cvec)
    A0 = nullspace(Lc.tolist())
    Ahalf = nullspace((2 * Lc - den * I).tolist())
    assert len(A0) == 10 and len(Ahalf) == 16
    A0i = [np.array([int(x * lcm(*[y.denominator for y in v])) for x in v], dtype=np.int64) for v in A0]
    Hi = [np.array([int(x * lcm(*[y.denominator for y in v])) for x in v], dtype=np.int64) for v in Ahalf]
    uvec = evec - cvec

    # ---- Der_c = spin(9) -----------------------------------------------------------------
    Dc_rows = np.stack([D @ cvec for D in basisD]).T.tolist()  # 27 x 52
    co = nullspace(Dc_rows)
    Dc = []
    for cvec_ in co:
        l = lcm(*[x.denominator for x in cvec_])
        M = sum(int(x * l) * D for x, D in zip(cvec_, basisD))
        Dc.append(M)
    assert len(Dc) == 36
    inDc = inertia_int(np.array([[np.trace(A @ B) for B in Dc] for A in Dc], dtype=object))
    assert inDc == (0, 36, 0)

    # ---- Lorentz algebra ------------------------------------------------------------------
    trform = lambda x, y: Fr(int(np.dot(trL, mulv(x, y))), 9 * den * den)
    spatial = []
    uu = trform(uvec, uvec)
    for v in A0i:
        coef = trform(v, uvec) / uu
        w = [Fr(int(a)) - coef * int(b) for a, b in zip(v, uvec)]
        l = lcm(*[x.denominator for x in w])
        spatial.append(np.array([int(x * l) for x in w], dtype=np.int64))
    assert rank([s.tolist() for s in spatial]) == 9
    sp9 = []
    for s in spatial:
        if rank([x.tolist() for x in sp9 + [s]]) > len(sp9):
            sp9.append(s)
    assert len(sp9) == 9
    kills_c = all((mulv(s, cvec) == 0).all() for s in sp9)
    boosts = [Lv(s) for s in sp9]
    lor = Dc + boosts
    r_lor = rank([m.flatten().tolist() for m in lor])
    assert kills_c and r_lor == 45
    # Der_c preserves the spatial Peirce-0 space (so closure follows from the str identities)
    Sp_rows = [s.tolist() for s in sp9]
    pres = all(rank(Sp_rows + [(D @ s).tolist()]) == 9 for D in Dc for s in sp9)
    assert pres
    # determinant form on A0 in the basis A0i: rank-2 spin factor with unit u
    A0mat = np.stack(A0i).T  # 27 x 10

    def coords_A0(v):
        sol = sp.Matrix(A0mat.tolist()).solve_least_squares(sp.Matrix(list(map(int, v))))
        assert sp.Matrix(A0mat.tolist()) * sol == sp.Matrix(list(map(int, v)))
        return [sp.Rational(x) for x in sol]

    # t0(y) = 2 Tr(L_y|A0)/Tr(L_u|A0) ; det0 = (t0^2 - t0(y^2))/2
    A0M = sp.Matrix(A0mat.tolist())
    A0pinv = (A0M.T * A0M).inv() * A0M.T

    def trA0(y):
        img = sp.Matrix((Lv(y) @ A0mat).tolist())
        return (A0pinv * img).trace()

    tu = trA0(uvec)

    def t0(y):
        return 2 * trA0(y) / tu

    def det0(y, dy=1):
        y2 = mulv(y, y)  # den * y o y
        return (t0(y) ** 2 - t0(y2) / den) / 2

    Gd = sp.zeros(10, 10)
    for i in range(10):
        for j in range(10):
            s = A0i[i] + A0i[j]
            Gd[i, j] = (det0(s) - det0(A0i[i]) - det0(A0i[j])) / 2
    lor_inertia = P.exact_inertia([[Fr(int(sp.Rational(x).p), int(sp.Rational(x).q)) for x in Gd.row(i)] for i in range(10)])
    assert lor_inertia == (1, 9, 0)
    inv_fail, images = 0, []
    for M in lor:
        R = A0pinv * sp.Matrix((M @ A0mat).tolist())  # 10 x 10 action in A0 basis
        assert A0M * R == sp.Matrix((M @ A0mat).tolist())
        images.append([x for x in R])
        inv_fail += (R.T * Gd + Gd * R) != sp.zeros(10, 10)
    img_rank = rank([[Fr(int(sp.Rational(x).p), int(sp.Rational(x).q)) for x in im] for im in images])
    assert inv_fail == 0 and img_rank == 45

    # ---- spinor module ---------------------------------------------------------------------
    Hmat = sp.Matrix(np.stack(Hi).T.tolist())
    Hpinv = (Hmat.T * Hmat).inv() * Hmat.T

    def rep16(M):
        img = sp.Matrix((M @ np.stack(Hi).T).tolist())
        R = Hpinv * img
        assert Hmat * R == img
        return R

    spin = [rep16(M) for M in lor]

    def commutant(mats, d):
        eqs = []
        for R in mats:
            for r in range(d):
                for c in range(d):
                    row = [0] * (d * d)
                    for k in range(d):
                        if R[k, c] != 0:
                            row[r * d + k] += R[k, c]
                        if R[r, k] != 0:
                            row[k * d + c] -= R[r, k]
                    eqs.append([Fr(int(sp.Rational(x).p), int(sp.Rational(x).q)) for x in row])
        return nullspace(eqs)

    com16 = commutant(spin, 16)
    assert len(com16) == 1

    # ---- 3+1 split ---------------------------------------------------------------------------
    s0 = e2 - e3
    labels = J["labels"]
    Lsp = [s.tolist() for s in sp9]
    line = None
    for k, (kind, la, lb) in enumerate(labels):
        if kind == "pair_re":
            zr, zi = I[k], I[k + 1]
            if all(rank(Lsp + [z.tolist()]) == 9 for z in (zr, zi)) and trform(zr, s0) == 0 and trform(zi, s0) == 0:
                line = (la, lb, zr, zi)
                break
    assert line is not None
    la, lb, zr, zi = line
    V4 = [uvec, s0, zr, zi]
    V4c = [coords_A0(v) for v in V4]
    comp_eqs = [[sum(V4c[a][i] * Gd[i, j] for i in range(10)) for j in range(10)] for a in range(4)]
    V6c = nullspace([[Fr(int(sp.Rational(x).p), int(sp.Rational(x).q)) for x in r] for r in comp_eqs])
    assert len(V6c) == 6
    V4m = sp.Matrix([[sp.Rational(x) for x in v] for v in V4c]).T
    V6m = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in v] for v in V6c]).T
    # conditions: sum_k a_k R_k maps V4 into V4 and V6 into V6
    proj4 = sp.eye(10) - V4m * (V4m.T * V4m).inv() * V4m.T
    proj6 = sp.eye(10) - V6m * (V6m.T * V6m).inv() * V6m.T
    conds = []
    Rm = [sp.Matrix(10, 10, im) for im in images]
    blocks = [proj4 * R * V4m for R in Rm], [proj6 * R * V6m for R in Rm]
    for group in blocks:
        rows, cols = group[0].shape
        for r in range(rows):
            for c in range(cols):
                conds.append([Fr(int(sp.Rational(Bk[r, c]).p), int(sp.Rational(Bk[r, c]).q)) for Bk in group])
    sub_co = nullspace(conds)
    assert len(sub_co) == 21
    sub16 = []
    for cv in sub_co:
        R = sp.zeros(16, 16)
        for x, Sk in zip(cv, spin):
            if x:
                R += sp.Rational(x.numerator, x.denominator) * Sk
        sub16.append(R)
    com21 = commutant(sub16, 16)
    assert len(com21) == 2
    C1, C2 = [sp.Matrix(16, 16, [sp.Rational(x.numerator, x.denominator) for x in v]) for v in com21]
    Id = sp.eye(16)
    # the commutant contains the identity; find the traceless generator and its square
    Y = C1 if (C1 - C1[0, 0] * Id) != sp.zeros(16, 16) else C2
    Y0 = Y - (Y.trace() / 16) * Id
    Y2 = Y0 * Y0
    lam = Y2[0, 0]
    complex_structure = (Y2 == lam * Id) and lam < 0
    assert complex_structure
    out["lorentz"] = {
        "peirce_dims": {"A1": 1, "A1/2": 16, "A0": 10},
        "Der_c_dimension": 36, "Der_c_trace_inertia": list(inDc), "Der_c": "spin(9), compact",
        "boosts": "L_y, y in the Peirce-0 space trace-orthogonal to u = e - c (9); L_y c = 0",
        "lorentz_algebra_dimension": r_lor,
        "A0_determinant_inertia": list(lor_inertia),
        "determinant_invariance_failures": inv_fail,
        "faithful_image_dimension_in_gl(A0)": img_rank,
        "reading": "the full Lie algebra of the (1,9) determinant on the Peirce 10: so(1,9)",
        "spinor_module_dimension": 16, "spinor_commutant_dimension": len(com16),
        "spinor_reading": "absolutely irreducible real 16: the Majorana-Weyl spinor of so(1,9)",
    }
    out["three_plus_one"] = {
        "time": "u = e - c", "frame_direction": "s0 = e_g2 - e_g3",
        "hermitian_complex_line_i27_labels": [la, lb],
        "subalgebra_dimension": len(sub_co), "reading": "so(1,3) + so(6) = 6 + 15",
        "commutant_on_16_dimension": len(com21),
        "commutant_contains_complex_structure": bool(complex_structure),
        "spinor_branching": "16 = (2,4) + conjugate under sl(2,C) + su(4)",
    }

    # ---- Q_psi = 6 L_c - 2 and matter parity ----------------------------------------------------
    qpsi_cert = json.loads(QPSI.read_text())
    target = {tuple(p["Qpsi"]): p["count"] for p in qpsi_cert["E6_cubic"]["patterns"]}
    assert target == {(-2, 1, 1): 40, (-2, -2, 4): 5}
    assert qpsi_cert["E6_27"]["branching"] == "27 = 16_1 + 10_-2 + 1_4"
    ok = 0
    for i in range(27):
        q = {j: (4 if j == i else (-2 if any(i in t and j in t for t in dsign) else 1)) for j in range(27)}
        ok += (Counter(q.values()) == Counter({1: 16, -2: 10, 4: 1})
               and all(sum(q[x] for x in t) == 0 for t in dsign)
               and Counter(tuple(sorted(q[x] for x in t)) for t in dsign) == Counter(target))
    assert ok == 27
    # Peirce symmetry U_s = 2 L_s^2 - L_{s^2}, s = 2c - e   (scaled: den^2 U_s)
    s = 2 * cvec - evec
    Lsv = Lv(s)
    ss = mulv(s, s)  # den * s o s = den * e
    Us_scaled = 2 * (Lsv @ Lsv) - den * Lv(ss // den)  # den^2 * (2 L_s^2 - L_{s o s})
    assert (Us_scaled % (den * den) == 0).all()
    Us = Us_scaled // (den * den)
    on1 = (Us @ cvec == cvec).all()
    on0 = all((Us @ v == v).all() for v in A0i)
    onh = all((Us @ v == -v).all() for v in Hi)
    auto = all((Us @ (Pi[i] @ np.eye(n, dtype=np.int64)).T[:, j] == mulv(Us[:, i], Us[:, j])).all()
               for i in range(n) for j in range(n))
    assert on1 and on0 and onh and auto
    # 2 pi rotation (floating): D_rot = [L_s0, L_z] kills c and rotates exactly the (s0, z) plane of A0
    Drot = Lv(s0) @ Lv(zr) - Lv(zr) @ Lv(s0)
    assert (Drot @ cvec == 0).all() and rank([m.flatten().tolist() for m in Dc] + [Drot.flatten().tolist()]) == 36
    A0f = A0mat.astype(float)
    Df = Drot.astype(float)
    R = np.linalg.lstsq(A0f, Df @ A0f, rcond=None)[0]
    ev = np.linalg.eigvals(R)
    nz = sorted(abs(ev.imag[abs(ev.imag) > 1e-9]))
    assert len(nz) == 2 and abs(nz[0] - nz[1]) < 1e-9 and np.max(np.abs(ev.real)) < 1e-9
    w = nz[0]
    err = float(np.max(np.abs(expm(2 * np.pi / w * Df) - Us.astype(float))))
    assert err < 1e-8
    out["matter_parity"] = {
        "Qpsi_as_peirce_operator": "Q_psi = 6 L_c - 2 (Peirce 1 -> 4, 1/2 -> 1, 0 -> -2)",
        "coordinate_idempotents_reproducing_Qpsi_spectrum_and_triad_patterns": ok,
        "repository_Qpsi_patterns": {str(k): v for k, v in target.items()},
        "peirce_symmetry_U_(2c-e)": {"A1": bool(on1), "A0": bool(on0), "A1/2": bool(onh), "automorphism": bool(auto)},
        "two_pi_rotation_equals_U_s_max_error": err,
        "reading": ("Matter parity (-1)^Q_psi on the 27 is the Peirce symmetry of a primitive idempotent; "
                    "in the clock real form it is the 2 pi rotation of Spin(9) < Spin(1,9): +1 on the "
                    "Lorentz vector 10 and scalar 1, -1 on the Weyl spinor 16.  The repository's Q_psi "
                    "is matched to 6 L_c - 2 up to the W(E6)-transitive choice of coordinate idempotent."),
    }
    out["status"] = "PASS_CLOCK_ALBERT_F4_E6M26_SO19_WEYL_SPINOR_AND_MATTER_PARITY_AS_PEIRCE_SYMMETRY"
    out["theorem"] = (
        "The Euclidean Albert algebra of the clock real form has Der of dimension 52 with negative-"
        "definite trace form (compact F4) and str0 of dimension 78 with inertia (26,52) (E6(-26)). "
        "A primitive idempotent's stabiliser in Der is 36-dimensional; with the nine Peirce-0 "
        "multiplications it forms a 45-dimensional algebra acting faithfully on the Peirce 10 as the "
        "Lie algebra of its (1,9) determinant (so(1,9)) and absolutely irreducibly on the Peirce 16 "
        "(Majorana-Weyl spinor). A 3+1 split leaves so(1,3)+so(6) with a complex commutant on the 16. "
        "The repository's Q_psi on the 27 is 6L_c-2 and matter parity is the Peirce symmetry, equal to "
        "the 2 pi rotation of Spin(9)."
    )
    out["prior_art_and_boundary"] = {
        "repo_prior_art": [
            "data/w33_qpsi_matter_parity_e8_d8_bridge.json (Q_psi 16_1+10_-2+1_4, triad patterns)",
            "commit 5419c27 (27 lines, W(D5) stabiliser, 27 = 1+10+16)",
            "BREAKTHROUGH_DCCLXXXVII.md, scripts/w33_exact_sector_physics.py (count-level Pati-Salam SU(4))",
            "analysis/w33_pass10949_freudenthal_quasiconformal_clock_cone.py (the clock Albert algebra)",
        ],
        "external": [
            "Faraut-Koranyi, Analysis on Symmetric Cones",
            "Baez, The Octonions, Bull. AMS 39 (2002): f4, e6(-26), sl(2,O) = so(9,1)",
            "Manogue-Dray-Wilson, Octions: an E8 description of the Standard Model, JMP 63 (2022)",
            "Baez-Huerta, Division algebras and supersymmetry I (2010)",
        ],
        "boundary": ("Exact finite algebra. so(1,9) is an idempotent stabiliser inside E6(-26); it is not "
                     "claimed to be the Lorentz group of physical spacetime, and the Pati-Salam statement is "
                     "a branching fact, not gauge dynamics, chirality selection or masses."),
    }
    out["sha256_of_payload"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    if write:
        OUT.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    r = main(True)
    print(r["status"])
    print(json.dumps({k: r[k] for k in ("structure", "lorentz", "three_plus_one", "matter_parity")}, indent=1, default=str))
