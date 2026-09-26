#!/usr/bin/env python3
"""Pass 10960: exhaustive matter-even D-flat closure of the W(3,3) heterotic Standard Models.

The question (open problem 1 of the Forty Points paper; the Holotrade gate
``analysis/w33_matter_even_dflat_exhaustive_gate.py`` of 2026-09-21):

    In the 215 three-family Standard Models found in the Z6-I and Z6-II orbifolds of
    the W(3,3) twist, is there a vacuum that cancels the anomalous Fayet-Iliopoulos
    term with D-flat singlet VEVs while condensing ONLY singlets that are even under
    a matter parity?  If yes, the class survives with proton stability; if no, the
    class is excluded as a realistic MSSM in singlet vacua.

Prior art (cited, not reclaimed):
  * Holotrade 0fee779 / TOE ledger 78ec0a0fc: a Z2 subgroup of U(1)_{B-L} exists in
    all 87 Z6-I models; bare udd, qLd^c, LLe^c are matter-odd; Yukawas and mu even.
  * Holotrade 28620b4 / TOE ledger a3dbdf2d7: D-flat in 23/87 Z6-I and 105/128 Z6-II;
    every D-flat support found contains a matter-odd singlet -- but the B-L freedom
    was SAMPLED (60 choices per model), so this was explicitly not a proof.
  * Holotrade gate 2ebfb50/6fbd638: the raw spectra sp1/sp2 were not in any repo, so
    the proof could not be completed; the gate specifies the exact closure contract
    (solve x = x0 + N t over Q, enumerate every realizable parity class, Farkas
    witness for every infeasible class, any feasible primal ray is a counterexample).

What this pass adds:
  1. The raw orbifolder spectra were recovered from the WSL scan tree
     (~/orb/scan/cp/spec1: 87 Z6-I, ~/orb/scan/cp2/sp: 128 Z6-II) and frozen here as a
     normalized left-chiral ledger with exact rational charges (sha256 recorded).
  2. The gate contract is executed WITHOUT sampling, with exact certificates:
       - no D-flat direction at all: exact Farkas vector lambda with
         s*c_s + lambda.m_s >= 0 on every singlet type (so s*c.a >= 0 for every
         D-flat a, and the FI term cannot be cancelled);
       - D-flat, but the singlets that can be even for SOME B-L choice are not:
         one exact Farkas vector on that union;
       - otherwise: every anomaly-cancelling extreme ray (cdd, exact) is shown
         non-realizable as all-even by an exact Smith-normal-form obstruction.
  3. A strictly different, more general parity family is scanned exhaustively:
     every Z2 character of the full U(1) charge lattice that is odd on all
     q, u^c, d^c, e^c fields (not only exp(i pi 3(B-L))), each with an exact
     Farkas certificate.
  4. Positive controls: the D-flat machinery reproduces 23 + 105 = 128 D-flat models
     with exact witness rays; B-L exists in exactly 88 models; realizable parity
     classes are found (with explicit rational t) whenever they exist.

Scope: singlet directions (fields trivial under every nonabelian factor, Y = 0),
exactly the space of the gate contract.  Nonabelian (composite) flat directions are
NOT covered and are recorded as the remaining loophole.
"""
from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import os
import re
import sys
from fractions import Fraction
from math import lcm
from pathlib import Path

import cdd
import cdd.gmp as cg
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_decomp

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "w33_pass10960_heterotic_left_chiral_ledger.json.gz"
OUT = ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json"
Z2OUT = ROOT / "data" / "w33_pass10960_z2_character_certificates.json.gz"

SMY = {"q": Fraction(1, 6), "bq": Fraction(-1, 6), "u": Fraction(2, 3), "bu": Fraction(-2, 3),
       "d": Fraction(-1, 3), "bd": Fraction(1, 3), "e": Fraction(-1), "be": Fraction(1),
       "l": Fraction(-1, 2), "bl": Fraction(1, 2)}
BL = {"q": Fraction(1, 3), "bu": Fraction(-1, 3), "bd": Fraction(-1, 3), "be": Fraction(1)}
MATTER = ("q", "bu", "bd", "be")
LINE = re.compile(r"^S (\S+) k=(\d+) susy=(\d+) dim=(\S+) q=(\S+)")


# ------------------------------------------------------------------ ledger
def _frac(s: str) -> Fraction:
    f = Fraction(s).limit_denominator(10**6)
    assert abs(float(f) - float(s)) < 1e-9, s
    assert 18 % f.denominator == 0, ("unexpected denominator", s, f)
    return f


def parse_raw(fn: Path) -> dict:
    nu1, fi, fields = None, None, []
    for line in open(fn):
        if line.startswith("NU1"):
            nu1 = int(line.split()[1])
        elif line.startswith("ANOM"):
            fi = line.split()[3]
        elif line.startswith("S "):
            m = LINE.match(line)
            assert m, line
            name, k, susy, dim, q = m.groups()
            if int(susy) != 2:  # left-chiral only
                continue
            fields.append(dict(name=name, k=int(k), dim=dim, q=[str(_frac(x)) for x in q.split(",")]))
    assert nu1 is not None and all(len(f["q"]) == nu1 for f in fields)
    return dict(nu1=nu1, fi_header=fi, left=fields)


def build_ledger(raw_root: Path) -> None:
    models = {}
    for tag, sub in (("Z6-I", "z6i"), ("Z6-II", "z6ii")):
        for fn in sorted((raw_root / sub).glob("*.sp")):
            models[f"{tag}|{fn.stem}"] = parse_raw(fn)
    assert len(models) == 215, len(models)
    blob = json.dumps(models, sort_keys=True).encode()
    with gzip.GzipFile(LEDGER, "wb", mtime=0) as fh:
        fh.write(blob)


def load_ledger() -> tuple[dict, str]:
    raw = LEDGER.read_bytes()
    return json.loads(gzip.decompress(raw)), hashlib.sha256(raw).hexdigest()


# ------------------------------------------------------------------ exact helpers
def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def Fr(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(str(x))


def solve_affine(A, b):
    """x0, N with {x : A x = b} = x0 + span(N) over Q, or None."""
    M = sp.Matrix([[sp.Rational(v.numerator, v.denominator) for v in row] for row in A])
    r = sp.Matrix([sp.Rational(v.numerator, v.denominator) for v in b])
    if M.rank() != M.row_join(r).rank():
        return None
    sol, params = M.gauss_jordan_solve(r)
    x0 = sol.subs({p: 0 for p in params})
    return [Fr(v) for v in x0], [[Fr(v) for v in n] for n in M.nullspace()]


def farkas(C, M):
    """exact lambda with C_s + lambda.M_s >= 0 for all s, or None (cdd gmp LP)."""
    k = len(M[0]) if M else 0
    if not C:
        return []
    rows = [[Fr(c)] + [Fr(v) for v in m] for c, m in zip(C, M)]
    mat = cg.matrix_from_array(rows, rep_type=cdd.RepType.INEQUALITY)
    mat.obj_type = cdd.LPObjType.MAX
    mat.obj_func = tuple([Fraction(0)] * (k + 1))
    lp = cg.linprog_from_matrix(mat)
    cg.linprog_solve(lp)
    if lp.status == cdd.LPStatusType.OPTIMAL:
        lam = [Fr(v) for v in lp.primal_solution]
        assert all(c + dot(lam, m) >= 0 for c, m in zip(C, M))
        return lam
    assert lp.status == cdd.LPStatusType.INCONSISTENT, lp.status
    return None


def dflat_witness(C, M):
    """exact a >= 0 with M a = 0 and C.a = -1 (a D-flat, FI-cancelling direction), or None."""
    n = len(C)
    k = len(M[0])
    rows, lin = [], []
    for j in range(k):
        rows.append([Fraction(0)] + [Fr(M[i][j]) for i in range(n)])
        lin.append(len(rows) - 1)
    rows.append([Fraction(1)] + [Fr(c) for c in C])  # 1 + C.a = 0
    lin.append(len(rows) - 1)
    for i in range(n):
        e = [Fraction(0)] * (n + 1)
        e[i + 1] = Fraction(1)
        rows.append(e)
    mat = cg.matrix_from_array(rows, lin_set=set(lin), rep_type=cdd.RepType.INEQUALITY)
    mat.obj_type = cdd.LPObjType.MAX
    mat.obj_func = tuple([Fraction(0)] * (n + 1))
    lp = cg.linprog_from_matrix(mat)
    cg.linprog_solve(lp)
    if lp.status != cdd.LPStatusType.OPTIMAL:
        return None
    a = [Fr(v) for v in lp.primal_solution]
    assert all(v >= 0 for v in a)
    assert all(sum((M[i][j] * a[i] for i in range(n)), Fraction(0)) == 0 for j in range(k))
    assert dot(C, a) == -1
    return a


def cone_rays(M):
    """exact extreme rays of {a >= 0 : sum_i a_i M_i = 0} (M: list of type vectors)."""
    n, k = len(M), len(M[0])
    rows, lin = [], []
    for j in range(k):
        rows.append([Fraction(0)] + [Fr(M[i][j]) for i in range(n)])
        lin.append(j)
    for i in range(n):
        e = [Fraction(0)] * (n + 1)
        e[i + 1] = Fraction(1)
        rows.append(e)
    mat = cg.matrix_from_array(rows, lin_set=set(lin), rep_type=cdd.RepType.INEQUALITY)
    gen = cg.copy_generators(cg.polyhedron_from_matrix(mat))
    assert not gen.lin_set, "cone is pointed"
    return [[Fr(v) for v in r[1:]] for r in gen.array if r[0] == 0]


def realizable(alpha, beta):
    """exists t in Q^k, m in Z^R with alpha + beta t = 2m?  Exact, with witness or obstruction."""
    R = len(alpha)
    k = len(beta[0])
    B = sp.Matrix([[sp.Rational(b.numerator, b.denominator) for b in row] for row in beta])
    a = sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in alpha])
    Y = B.T.nullspace()
    if Y:
        Ym = sp.Matrix.hstack(*Y).T
        Yi = sp.Matrix([[int(v * lcm(*[int(sp.fraction(w)[1]) for w in Ym.row(i)])) for v in Ym.row(i)]
                        for i in range(Ym.rows)])
        rhs = Yi * a
        if any(sp.fraction(v)[1] != 1 for v in rhs):
            return False, {"kind": "nonintegral", "Y": [[int(v) for v in Yi.row(i)] for i in range(Yi.rows)]}
        A = 2 * Yi
        S, U, V = smith_normal_decomp(A, domain=sp.ZZ)
        c = U * rhs
        z = []
        for i in range(S.rows):
            d = S[i, i] if i < S.cols else 0
            if d == 0:
                if c[i] != 0:
                    return False, {"kind": "smith_zero_row", "row": i}
                z.append(0)
            else:
                if c[i] % d != 0:
                    return False, {"kind": "smith_divisibility", "row": i, "d": int(d), "c": int(c[i])}
                z.append(c[i] // d)
        z += [0] * (S.cols - len(z))
        m = V * sp.Matrix(z[: S.cols])
    else:
        m = sp.zeros(R, 1)
    rhs2 = 2 * m - a
    t, params = B.gauss_jordan_solve(rhs2)
    t = t.subs({p: 0 for p in params})
    tq = [Fr(v) for v in t]
    vals = [alpha[i] + dot(beta[i], tq) for i in range(R)]
    assert all(v.denominator == 1 and v.numerator % 2 == 0 for v in vals)
    return True, {"t": [str(v) for v in tq]}


def lattice_coords(vectors):
    den = lcm(*[v.denominator for vec in vectors for v in vec])
    Mi = sp.Matrix([[int(v * den) for v in vec] for vec in vectors])
    H = hermite_normal_form(Mi.T)
    Bm = sp.Matrix.hstack(*[H[:, j] for j in range(H.cols) if any(H[:, j])])
    coords = []
    for i in range(Mi.rows):
        c, params = Bm.gauss_jordan_solve(Mi.row(i).T)
        c = c.subs({p: 0 for p in params})
        assert all(sp.fraction(x)[1] == 1 for x in c)
        coords.append([int(x) for x in c])
    return Bm.cols, coords


# ------------------------------------------------------------------ one model
def base_of(name):
    return re.sub(r"_\d+$", "", name)


def analyse(name, model, z2store):
    nu1 = model["nu1"]
    left = []
    for f in model["left"]:
        dims = f["dim"].split(",")
        left.append(dict(name=f["name"], base=base_of(f["name"]),
                         trivial=all(abs(int(re.match(r"(-?\d+)", d).group(1))) == 1 and "adj" not in d for d in dims),
                         dimprod=abs(eval("*".join(re.match(r"(-?\d+)", d).group(1) for d in dims))),
                         q=[Fraction(x) for x in f["q"]]))
    rec = dict(nu1=nu1, fi_header=model["fi_header"], left=len(left))
    tr = [sum((f["dimprod"] * f["q"][i] for f in left), Fraction(0)) for i in range(nu1)]
    assert all(v == 0 for v in tr[1:]), (name, tr)
    rec["trace_anomalous"] = str(tr[0])
    lab = [f for f in left if f["base"] in SMY]
    ysol = solve_affine([f["q"] for f in lab], [SMY[f["base"]] for f in lab])
    assert ysol is not None
    y = ysol[0]
    sing = [f for f in left if f["trivial"] and dot(y, f["q"]) == 0]
    types = {}
    for f in sing:
        types.setdefault(tuple(f["q"]), []).append(f["name"])
    T = list(types)
    rec.update(singlets=len(sing), singlet_types=len(T))
    if tr[0] == 0:
        rec["anomaly_free"] = True
        return rec
    s = 1 if tr[0] > 0 else -1
    C = [s * t[0] for t in T]
    M = [list(t[1:]) for t in T]
    lam_all = farkas(C, M)
    rec["dflat_any"] = lam_all is None
    if lam_all is not None:
        rec["farkas_all"] = [str(v) for v in lam_all]
    else:
        a = dflat_witness(C, M)
        rec["dflat_witness"] = {types[T[i]][0]: str(a[i]) for i in range(len(T)) if a[i] != 0}
    # ---------------- B-L family (gate contract)
    A = [f["q"] for f in left if f["base"] in BL]
    b = [BL[f["base"]] for f in left if f["base"] in BL]
    sol = solve_affine(A, b)
    rec["bl_direction"] = sol is not None
    if sol is not None:
        x0, N = sol
        rec["bl_nullspace_dim"] = len(N)
        alpha = [3 * dot(x0, t) for t in T]
        beta = [[3 * dot(n, t) for n in N] for t in T]
        never_even = [i for i in range(len(T)) if not any(beta[i]) and
                      not (alpha[i].denominator == 1 and alpha[i].numerator % 2 == 0)]
        U = [i for i in range(len(T)) if i not in never_even]
        rec["never_even_types"] = [{"fields": types[T[i]], "three_BminusL": str(alpha[i])} for i in never_even]
        rec["ever_even_types"] = len(U)
        # parity content of the doublets over the whole freedom
        for lb in ("l", "bl"):
            rec[f"doublet_3BL_{lb}"] = sorted({(str(3 * dot(x0, f["q"])), tuple(str(3 * dot(n, f["q"])) for n in N))
                                               for f in left if f["base"] == lb})
        if lam_all is not None:
            rec["bl_verdict"] = "closed: no D-flat direction at all"
        else:
            lamU = farkas([C[i] for i in U], [M[i] for i in U])
            if lamU is not None:
                rec["bl_verdict"] = "closed: ever-even singlets are never D-flat (one Farkas vector)"
                rec["farkas_ever_even"] = [str(v) for v in lamU]
            else:
                rays = cone_rays([M[i] for i in U])
                neg = [r for r in rays if sum((C[U[i]] * r[i] for i in range(len(U))), Fraction(0)) < 0]
                certs, hits = [], []
                for r in neg:
                    S_ = [U[i] for i in range(len(U)) if r[i] != 0]
                    ok, why = realizable([alpha[i] for i in S_], [beta[i] for i in S_])
                    (hits if ok else certs).append({"support": [types[T[i]][0] for i in S_], "why": why})
                rec["extreme_rays"] = len(rays)
                rec["anomaly_cancelling_rays"] = len(neg)
                rec["realizable_even_rays"] = len(hits)
                rec["ray_obstruction_kinds"] = sorted({c["why"]["kind"] for c in certs})
                rec["bl_verdict"] = ("COUNTEREXAMPLE: matter-even D-flat direction exists" if hits else
                                     "closed: every anomaly-cancelling extreme ray is parity-obstructed")
                if hits:
                    rec["counterexamples"] = hits[:5]
        # positive realizability controls
        ctrl = []
        for i in U[:6]:
            ok, why = realizable([alpha[i]], [beta[i]])
            ctrl.append(ok)
        rec["control_single_type_realizable"] = all(ctrl)
    # ---------------- general Z2 characters
    r, coords = lattice_coords([f["q"] for f in left])
    idx = {f["name"]: i for i, f in enumerate(left)}
    is_m = [f["base"] in MATTER for f in left]
    nchar, nflat, certs = 0, 0, []
    for eps in itertools.product((0, 1), repeat=r):
        par = [sum(e * c for e, c in zip(eps, co)) % 2 for co in coords]
        if not all(p == 1 for p, m in zip(par, is_m) if m):
            continue
        nchar += 1
        ev = [i for i, t in enumerate(T) if par[idx[types[t][0]]] == 0]
        lam = farkas([C[i] for i in ev], [M[i] for i in ev])
        if lam is None:
            nflat += 1
        else:
            certs.append({"eps": list(eps), "lambda": [str(v) for v in lam], "even_types": len(ev)})
    rec.update(lattice_rank=r, z2_matter_parities=nchar, z2_even_dflat=nflat)
    z2store[name] = certs
    return rec


def main():
    raw = os.environ.get("W33_ORB_RAW")
    if raw:
        build_ledger(Path(raw))
    ledger, sha = load_ledger()
    z2store = {}
    results = {}
    for name in sorted(ledger):
        results[name] = analyse(name, ledger[name], z2store)
        r = results[name]
        print(f"{name:40s} dflat={r.get('dflat_any')} BL={r.get('bl_direction')} "
              f"verdict={r.get('bl_verdict', '-')} z2={r.get('z2_matter_parities')}/{r.get('z2_even_dflat')}", flush=True)
    anom = [k for k, v in results.items() if not v.get("anomaly_free")]
    summary = dict(
        models=len(results),
        anomaly_free=len(results) - len(anom),
        dflat_any_Z6I=sum(1 for k in anom if k.startswith("Z6-I|") and results[k]["dflat_any"]),
        dflat_any_Z6II=sum(1 for k in anom if k.startswith("Z6-II|") and results[k]["dflat_any"]),
        bl_direction=sum(1 for v in results.values() if v.get("bl_direction")),
        bl_counterexamples=sum(1 for v in results.values() if str(v.get("bl_verdict", "")).startswith("COUNTER")),
        bl_closed_no_dflat=sum(1 for v in results.values() if v.get("bl_verdict") == "closed: no D-flat direction at all"),
        bl_closed_farkas_union=sum(1 for v in results.values() if str(v.get("bl_verdict", "")).startswith("closed: ever-even")),
        bl_closed_by_rays=sum(1 for v in results.values() if str(v.get("bl_verdict", "")).startswith("closed: every")),
        z2_models_with_parity=sum(1 for v in results.values() if v.get("z2_matter_parities")),
        z2_characters=sum(v.get("z2_matter_parities", 0) for v in results.values()),
        z2_even_dflat=sum(v.get("z2_even_dflat", 0) for v in results.values()),
    )
    cert = dict(pass_id=10960, ledger=str(LEDGER.relative_to(ROOT)).replace(os.sep, "/"), ledger_sha256=sha,
                summary=summary, models=results)
    OUT.write_text(json.dumps(cert, indent=1, sort_keys=True), encoding="utf-8")
    with gzip.GzipFile(Z2OUT, "wb", mtime=0) as fh:
        fh.write(json.dumps(z2store, sort_keys=True).encode())
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
