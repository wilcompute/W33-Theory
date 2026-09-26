#!/usr/bin/env python3
"""Pass 10968: geometric R-symmetries open matter parity in exactly one model -- and the same
R-symmetry keeps the exotics massless.  Plus the Z12-I census, where the pattern repeats.

Builds on Pass 10967 (most general torus x space-group matter parity: 0/215).  That scope left out
the geometric R-symmetries of the Z6-II lattice (Z6^R x Z3^R x Z2^R from the G2, SU(3), SU(2)^2
plane rotations), whose W-invariant combinations act on superfields as non-R symmetries.

A. Adding them (charges q_sh + oscillator per plane, frozen from the orbifolder; W-invariance
   imposed exactly) matter parity exists in 3 of the 128 Z6-II models instead of 1; two close by
   one Farkas vector, and Z6II_23 acquires 38 FI-cancelling D-flat directions that preserve a
   matter parity, each with 3 odd lepton doublets, an even H_d and an even H_u.
B. The element is a genuine symmetry: an explicit witness is invariant on all 1524 couplings the
   orbifolder allows (frozen dump), and the selection rules implemented here reproduce the
   orbifolder's 144 order-5 u^c d^c d^c couplings exactly (672 pass without the R rules).
C. Those vacua are supersymmetric: W|_S vanishes to all orders in all 38 (lattice criterion), and 26
   have no coupling phi * S^a with one field outside S through order K (selection rules).
D. But in every one of the 38, the mass terms u.u^c, d.d^c, e.e^c of the vector-like exotics are
   forbidden to ALL orders: v_Xbar + v_X - w is not in the lattice spanned by the vacuum fields and
   the discrete integrality vectors.  Without the R rules 13 d.d^c pairs would be allowed.  The
   unbroken R-symmetry that makes the vacuum F-flat is the one that keeps 3 + 5 + 3 exotic states
   massless (cf. Kappl et al., arXiv:0812.2120, where the same mechanism sets mu = 0).
E. Z12-I census (289 inequivalent SMs from 1167 A8 shift classes, frozen ledger): a general torus
   element gives an MSSM-viable parity (3 odd families, even H_u, H_d, every exotic pair
   parity-allowed) in 32 models; 14 have an FI-cancelling D-flat direction compatible with it.
   Every one fails the mass test: 5 already with gauge + point-group rules (a vector-like mass
   forbidden at all orders), the other 9 with the per-plane R rules sum R^i = -1 mod (12,12,3)
   (labelled tentative: the Z12-I geometry file defines no R-symmetries).
"""
from __future__ import annotations

import gzip
import importlib.util
import itertools
import json
import re
import sys
from collections import Counter
from fractions import Fraction
from math import lcm
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10967", ROOT / "analysis" / "w33_pass10967_fi_vacuum_regenerates_rpv.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
P = M.P
Z12 = ROOT / "data" / "w33_pass10968_z12_left_chiral_ledger.json.gz"
OUT = ROOT / "data" / "w33_pass10968_r_symmetry_parity_and_massless_exotics.json"
Z6II23 = "Z6-II|Z6II_23__SM_20260917_2913"
K_F = int(__import__("os").environ.get("W33_P10968_KF", "10"))
ab = lambda s: abs(int(re.match(r"(-?\d+)", s).group(1)))


# ----------------------------------------------------------------------------- generic helpers
def compositions(n, k):
    for tot in range(1, k + 1):
        for c in itertools.combinations(range(tot + n - 1), n - 1):
            prev, out = -1, []
            for x in c:
                out.append(x - prev - 1)
                prev = x
            out.append(tot + n - 2 - prev)
            yield out


def lattice_member(gens):
    den = lcm(*[v.denominator for g in gens for v in g])
    G = sp.Matrix([[int(v * den) for v in g] for g in gens]).T
    H = hermite_normal_form(G)
    B = sp.Matrix.hstack(*[H[:, j] for j in range(H.cols) if any(H[:, j])])

    def inl(u):
        if any((v * den).denominator != 1 for v in u):
            return False
        try:
            c, prm = B.gauss_jordan_solve(sp.Matrix([int(v * den) for v in u]))
        except ValueError:
            return False
        c = c.subs({p: 0 for p in prm})
        return all(sp.fraction(x)[1] == 1 for x in c)
    return inl


def real2(even, odd):
    return M.realizable([list(v) for v in odd] + [list(v) for v in even], list(range(len(odd))))


# ----------------------------------------------------------------------------- MSSM matcher
def match_search(realz, base_even, species, leptons, max_tests=30000):
    """exact DFS: pair every Xbar with a distinct X of opposite phase, 3 leftover X odd; leptons:
    one bl = H_u even, the other bl paired with l, of the 4 leftover l one H_d even, 3 odd."""
    slots = lambda es: [tuple(v) for _, v, m in es for _ in range(m)]
    tasks = [("pair", slots(X), slots(Xb)) for X, Xb in species] + [("lep", slots(leptons[0]), slots(leptons[1]))]
    stats = Counter()
    found = []

    def ok(e, o):
        stats["tests"] += 1
        if stats["tests"] > max_tests:
            raise TimeoutError
        return realz(e, o)

    add = lambda u, v: tuple(a + b for a, b in zip(u, v))

    def match(ti, X, Xb, used, j, even, odd):
        if found:
            return
        if j == len(Xb):
            rest = [X[i] for i in range(len(X)) if i not in used]
            if tasks[ti][0] == "pair":
                if len(rest) == 3 and ok(even, odd + rest):
                    nxt(ti + 1, even, odd + rest)
            elif len(rest) == 4:
                for h in dict.fromkeys(rest):
                    o2 = list(rest)
                    o2.remove(h)
                    if ok(even + [h], odd + o2):
                        found.append(True)
                        return
            return
        tried = set()
        for i in range(len(X)):
            if i in used or X[i] in tried:
                continue
            tried.add(X[i])
            e2 = even + [add(X[i], Xb[j])]
            if ok(e2, odd):
                match(ti, X, Xb, used | {i}, j + 1, e2, odd)

    def nxt(ti, even, odd):
        if found:
            return
        kind, X, Xb = tasks[ti]
        if kind == "pair":
            if len(X) - len(Xb) != 3:
                return
            match(ti, X, Xb, frozenset(), 0, even, odd)
        else:
            if len(X) - len(Xb) != 3:
                return
            for h in dict.fromkeys(Xb):
                rest = list(Xb)
                rest.remove(h)
                if ok(even + [h], odd):
                    match(ti, X, rest, frozenset(), 0, even + [h], odd)
                    if found:
                        return

    try:
        nxt(0, [tuple(v) for v in base_even], [])
        verdict = "viable" if found else "none"
    except TimeoutError:
        verdict = "timeout"
    return verdict, dict(stats)


# ----------------------------------------------------------------------------- Z6-II with R
class Z6IIR:
    def __init__(self, name, ledger, disc, dump):
        self.name, self.b = name, name.split("|")[1]
        d = disc[self.b]
        self.RN = [(int(x.split(":")[0]), Fraction(x.split(":")[1])) for x in d["R"]]
        d2 = json.loads(json.dumps(d))
        d2["nonR_orders"] = d["nonR_orders"] + [n for n, _ in self.RN]
        for v in d2["fields"].values():
            v["nonR"] = v["nonR"] + v["R"]
        self.d2 = d2
        self.orders, self.left = M.fields(ledger[name], d2)
        self.nq = len(self.left[0]["q"])
        nd = len(self.orders)
        self.vec = {f["name"]: f["q"] + f["ext"] for f in self.left}
        self.virtual = [[Fraction(0)] * self.nq + [Fraction(int(i == j)) for j in range(nd)] for i in range(nd)]
        self.wvec = [Fraction(0)] * (self.nq + len(d["nonR_orders"])) + [w / n for n, w in self.RN]
        self.raw = {f["name"]: f for f in ledger[name]["left"]}
        self.dump = dump.get(self.b, {})
        self.tr0 = sum((f["dimprod"] * f["q"][0] for f in self.left), Fraction(0))
        lab = [f for f in self.left if f["base"] in P.SMY]
        y = P.solve_affine([f["q"] for f in lab], [P.SMY[f["base"]] for f in lab])[0]
        self.sing = [f for f in self.left if f["trivial"] and P.dot(y, f["q"]) == 0]
        self.matter = [list(k) for k in dict.fromkeys(tuple(self.vec[f["name"]]) for f in self.left if f["base"] in P.MATTER)]

    def R(self, even, odd=()):
        vecs = self.matter + [list(v) for v in odd] + [list(v) for v in even] + self.virtual + [self.wvec]
        return M.realizable(vecs, list(range(len(self.matter) + len(odd))))

    def lab(self, p):
        return sorted((f["name"] for f in self.left if f["base"] == p), key=lambda x: int(x.split("_")[1]))

    def mult(self, n):
        qd = self.raw[self.lab("q")[0]]["dim"].split(",")
        ld = self.raw[self.lab("l")[0]]["dim"].split(",")
        c3 = [i for i, x in enumerate(qd) if ab(x) == 3][0]
        w2 = [i for i, x in enumerate(ld) if ab(x) == 2 and ab(qd[i]) == 2][0]
        m = 1
        for i, x in enumerate(self.raw[n]["dim"].split(",")):
            if i not in (c3, w2):
                m *= ab(x)
        return m


def z6ii_general_parity_with_R(ledger, disc):
    out, summ = {}, Counter()
    for name in sorted(ledger):
        if not name.startswith("Z6-II|"):
            continue
        b = name.split("|")[1]
        d = disc[b]
        RN = [(int(x.split(":")[0]), Fraction(x.split(":")[1])) for x in d["R"]]
        d2 = json.loads(json.dumps(d))
        d2["nonR_orders"] = d["nonR_orders"] + [n for n, _ in RN]
        for v in d2["fields"].values():
            v["nonR"] = v["nonR"] + v["R"]
        nq = len(ledger[name]["left"][0]["q"])
        wvec = [Fraction(0)] * (nq + len(d["nonR_orders"])) + [w / n for n, w in RN]
        orig = M.realizable
        M.general_parity.__globals__["realizable"] = lambda vecs, odd, _o=orig: _o(vecs + [wvec], odd)
        try:
            rec = M.general_parity(name, ledger[name], d2)
        finally:
            M.general_parity.__globals__["realizable"] = orig
        rec.pop("farkas", None)
        out[name] = rec
        summ["models"] += 1
        summ["parity_exists"] += rec["parity_exists"]
        v = rec.get("verdict", "")
        summ["closed_farkas"] += v.startswith("closed: Farkas")
        summ["closed_rays"] += v.startswith("closed: every")
        summ["with_realizable_fi_rays"] += v == "COUNTEREXAMPLE"
    return out, dict(summ)


def z6ii23_vacua(Z):
    ever = [k for k in dict.fromkeys(tuple(Z.vec[f["name"]]) for f in Z.sing) if Z.R([k])]
    names = {}
    for f in Z.sing:
        names.setdefault(tuple(Z.vec[f["name"]]), f["name"])
    ut = sorted({k[:Z.nq] for k in ever})
    s = 1 if Z.tr0 > 0 else -1
    rays = P.cone_rays([list(t[1:]) for t in ut])
    neg = [r for r in rays if sum((s * ut[i][0] * r[i] for i in range(len(ut))), Fraction(0)) < 0]
    supports = []
    for r in neg:
        sup = [ut[i] for i in range(len(ut)) if r[i] != 0]
        choices = [[k for k in ever if k[:Z.nq] == u] for u in sup]
        for ch in itertools.product(*choices):
            if Z.R(list(ch)):
                supports.append([names[k] for k in ch])
                break
    return dict(ever_even=len(ever), rays=len(rays), fi_rays=len(neg)), supports


def witness(rows, target):
    Lc = lcm(*[v.denominator for r in rows for v in r] + [t.denominator for t in target])
    A = sp.Matrix([[int(v * Lc) for v in r] for r in rows])
    S_, U, _ = sp.matrices.normalforms.smith_normal_decomp(A, domain=sp.ZZ)
    r = sum(1 for i in range(min(S_.shape)) if S_[i, i] != 0)
    t = sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in target])
    Ut = U * t
    c = [-Ut[i] for i in range(r, A.rows)]
    assert all(sp.fraction(v)[1] == 1 for v in c)
    n = U.inv() * sp.Matrix([0] * r + c)
    sol, prm = A.gauss_jordan_solve((t + n) * Lc)
    sol = sol.subs({p: 0 for p in prm})
    return [Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1])) for v in sol]


def z6ii23_checks(Z, supports):
    # doublets: 3 odd l + even H_d + even H_u for every support
    L_, BL_ = Z.lab("l"), Z.lab("bl")
    dbl_ok = 0
    for S in supports:
        Sv = [Z.vec[n] for n in S]
        lodd = [x for x in L_ if Z.R(Sv, [Z.vec[x]])]
        leven = [x for x in L_ if Z.R(Sv + [Z.vec[x]])]
        beven = [x for x in BL_ if Z.R(Sv + [Z.vec[x]])]
        hit = False
        for trio in itertools.combinations(lodd, 3):
            for hd in leven:
                if hd in trio:
                    continue
                for hu in beven:
                    if Z.R(Sv + [Z.vec[hd], Z.vec[hu]], [Z.vec[x] for x in trio]):
                        hit = True
                        break
                if hit:
                    break
            if hit:
                break
        dbl_ok += hit
    # witness on the first support, invariance on every dumped coupling
    S0 = supports[0]
    odd_names = sorted({f["name"] for f in Z.left if f["base"] in P.MATTER})
    rows = [Z.vec[n] for n in odd_names] + [Z.vec[n] for n in S0] + Z.virtual + [Z.wvec]
    x = witness(rows, [Fraction(1, 2)] * len(odd_names) + [Fraction(0)] * (len(rows) - len(odd_names)))
    phase = {n: sum(a * b for a, b in zip(v, x)) % 1 for n, v in Z.vec.items()}
    tot = bad = 0
    for lines in Z.dump.values():
        for cpl in lines:
            tot += 1
            bad += sum(phase[f] for f in cpl) % 1 != 0
    # selection rules reproduce the orbifolder's order-5 udd list exactly
    ORD = Z.d2["nonR_orders"][: len(Z.d2["nonR_orders"]) - len(Z.RN)]
    nnr = len(ORD)

    def allowed(fields, use_r=True):
        t = [sum(Z.vec[f][k] for f in fields) for k in range(len(Z.wvec))]
        if any(v != 0 for v in t[:Z.nq]) or any(v.denominator != 1 for v in t[Z.nq:Z.nq + nnr]):
            return False
        return (not use_r) or all((a - w).denominator == 1 for a, w in zip(t[Z.nq + nnr:], Z.wvec[Z.nq + nnr:]))
    dumped = {tuple(sorted(c)) for c in Z.dump["udd_to_order6"] if len(c) == 5}
    mine, noR = set(), set()
    npairs = {}
    for n1, n2 in itertools.combinations_with_replacement(Z.lab("n"), 2):
        npairs.setdefault(tuple(Z.vec[n1][k] + Z.vec[n2][k] for k in range(Z.nq)), []).append((n1, n2))
    for u in Z.lab("bu"):
        for d1, d2 in itertools.combinations_with_replacement(Z.lab("bd"), 2):
            key = tuple(-(Z.vec[u][k] + Z.vec[d1][k] + Z.vec[d2][k]) for k in range(Z.nq))
            for n1, n2 in npairs.get(key, ()):
                c = (u, d1, d2, n1, n2)
                if allowed(c):
                    mine.add(tuple(sorted(c)))
                if allowed(c, use_r=False):
                    noR.add(tuple(sorted(c)))
    # per support: all-orders lattice tests and F-flatness to K_F
    nd = len(Z.orders)
    sing_triv = [f["name"] for f in Z.sing]
    per = []
    for S in supports:
        gens = [Z.vec[n] for n in S] + [[Fraction(0)] * Z.nq + [Fraction(int(i == j)) for j in range(nd)] for i in range(nd)]
        inl = lattice_member(gens + [Z.wvec])
        inl_s = lattice_member(gens)
        rec = {"support": S, "W|_S_possible": inl_s([-w for w in Z.wvec])}
        for Xb, X in (("bq", "q"), ("u", "bu"), ("d", "bd"), ("e", "be"), ("bl", "l")):
            rec[f"{Xb}.{X}"] = sum(inl_s([p + q - w for p, q, w in zip(Z.vec[a], Z.vec[b], Z.wvec)]) for a in Z.lab(Xb) for b in Z.lab(X))
        pure = lin = 0
        outside = {}
        for o in sing_triv:
            if o not in S:
                outside.setdefault(tuple(-v for v in Z.vec[o][:Z.nq]), []).append(o)
        for a in compositions(len(S), K_F):
            flds = [n for n, e in zip(S, a) for _ in range(e)]
            u1 = tuple(sum(e * Z.vec[n][k] for n, e in zip(S, a)) for k in range(Z.nq))
            if all(v == 0 for v in u1):
                pure += allowed(flds)
            if sum(a) < K_F:
                lin += sum(allowed(flds + [o]) for o in outside.get(u1, ()))
        rec.update(F_pure=pure, F_linear=lin)
        per.append(rec)
    # control: drop R coordinates -> vector-like masses become allowed
    keep = Z.nq + nnr
    S0v = [Z.vec[n][:keep] for n in S0] + [[Fraction(0)] * Z.nq + [Fraction(int(i == j)) for j in range(nnr)] for i in range(nnr)]
    inl0 = lattice_member(S0v)
    ctrl = {f"{Xb}.{X}": sum(inl0([p + q for p, q in zip(Z.vec[a][:keep], Z.vec[b][:keep])]) for a in Z.lab(Xb) for b in Z.lab(X))
            for Xb, X in (("d", "bd"), ("bl", "l"))}
    return dict(doublet_structure_ok=dbl_ok, witness_couplings_checked=tot, witness_noninvariant=bad,
                udd5_dumped=len(dumped), udd5_mine=len(mine), udd5_exact=mine == dumped, udd5_without_R=len(noR),
                control_without_R=ctrl), per


# ----------------------------------------------------------------------------- Z12-I
def z12_models():
    with gzip.open(Z12, "rt") as fh:
        return json.load(fh)


def z12_analyse(name, m):
    fl = m["left"]
    order = m["pg_order"]
    vec = {f["name"]: [Fraction(x) for x in f["q"]] + [Fraction(f["pg"]) / order] for f in fl}
    qd = next(f for f in fl if P.base_of(f["name"]) == "q")["dim"].split(",")
    ld = next(f for f in fl if P.base_of(f["name"]) == "l")["dim"].split(",")
    c3 = [i for i, x in enumerate(qd) if ab(x) == 3][0]
    w2 = [i for i, x in enumerate(ld) if ab(x) == 2 and ab(qd[i]) == 2][0]

    def mult(f):
        mm = 1
        for i, x in enumerate(f["dim"].split(",")):
            if i not in (c3, w2):
                mm *= ab(x)
        return mm
    ent = lambda b: [(f["name"], [Fraction(x) for x in f["q"]], mult(f)) for f in fl if P.base_of(f["name"]) == b]
    species = [(ent("q"), ent("bq")), (ent("bu"), ent("u")), (ent("bd"), ent("d")), (ent("be"), ent("e"))]
    leptons = (ent("l"), ent("bl"))
    counts = [sum(e[2] for e in X) - sum(e[2] for e in Xb) for X, Xb in species + [leptons]]
    rec = {}
    if counts != [3, 3, 3, 3, 3]:
        return dict(verdict="nonstandard species counts", counts=counts)
    v, st = match_search(real2, [], species, leptons)
    rec["parity"] = v
    if v != "viable":
        rec["verdict"] = "no MSSM-viable parity" if v == "none" else "matcher timeout"
        return rec
    q = {f["name"]: [Fraction(x) for x in f["q"]] for f in fl}
    dims = {f["name"]: f["dim"] for f in fl}
    tr0 = sum(q[n][0] * eval("*".join(str(ab(x)) for x in dims[n].split(","))) for n in q)
    lab = [n for n in q if P.base_of(n) in P.SMY]
    y = P.solve_affine([q[n] for n in lab], [P.SMY[P.base_of(n)] for n in lab])[0]
    sing = [n for n in q if P.base_of(n) == "n" and all(ab(x) == 1 and "adj" not in x for x in dims[n].split(",")) and P.dot(y, q[n]) == 0]
    if tr0 == 0:
        rec["verdict"] = "anomaly free"
        return rec
    s = 1 if tr0 > 0 else -1
    types = list(dict.fromkeys(tuple(q[n]) for n in sing))
    lam = P.farkas([s * t[0] for t in types], [list(t[1:]) for t in types]) if types else []
    if lam is not None:
        rec["verdict"] = "closed: no FI-cancelling D-flat direction"
        return rec
    rays = P.cone_rays([list(t[1:]) for t in types])
    neg = [r for r in rays if sum((s * types[i][0] * r[i] for i in range(len(types))), Fraction(0)) < 0]
    S = None
    for r in neg:
        Sv = [list(types[i]) for i in range(len(types)) if r[i] != 0]
        if match_search(real2, Sv, species, leptons)[0] == "viable":
            S = [next(n for n in sing if tuple(q[n]) == tuple(x)) for x in Sv]
            break
    if S is None:
        rec["verdict"] = f"closed: {len(neg)} FI rays, none parity-viable"
        return rec
    rec["support"] = S
    # all-orders lattice test with gauge + point group (robust: extra rules only forbid more)
    nq = len(fl[0]["q"])
    inl = lattice_member([vec[n] for n in S] + [[Fraction(0)] * nq + [Fraction(1)]])
    labn = lambda p: [f["name"] for f in fl if P.base_of(f["name"]) == p]
    need = {}
    robust_dead = []
    for Xb, X in (("bq", "q"), ("u", "bu"), ("d", "bd"), ("e", "be"), ("bl", "l")):
        if not labn(Xb):
            continue
        n_ok = sum(inl([a + b for a, b in zip(vec[x], vec[z])]) for x in labn(Xb) for z in labn(X))
        need[f"{Xb}.{X}"] = n_ok
        if n_ok == 0:
            robust_dead.append(f"{Xb}.{X}")
    rec["pairs_allowed_gauge_pg"] = need
    if robust_dead:
        rec["verdict"] = "dead (robust): no " + ", ".join(robust_dead) + " mass term at any order"
        return rec
    # tentative per-plane R rules sum R^i = -1 mod (12,12,3): numerical ranks to order 9
    Nn = (12, 12, 3)
    for f in fl:
        vec[f["name"]] = vec[f["name"]] + [Fraction(r) / Ni for r, Ni in zip(f["rq"].split(","), Nn)]
    W = [Fraction(-1, Ni) for Ni in Nn]

    def allowed(fields):
        t = [sum(vec[f][k] for f in fields) for k in range(len(vec[fields[0]]))]
        return all(v == 0 for v in t[:nq]) and t[nq].denominator == 1 and all((a - w).denominator == 1 for a, w in zip(t[nq + 1:], W))
    rng = np.random.default_rng(7)
    vev = {x: 0.3 * np.exp(2j * np.pi * rng.random()) * (0.5 + rng.random()) for x in S}
    monos = [[0] * len(S)] + list(compositions(len(S), 7))
    ranks = {}
    for Xb, X in (("d", "bd"), ("bl", "l")):
        R_, C_ = labn(Xb), labn(X)
        Mx = np.zeros((len(R_), len(C_)), complex)
        for i, a in enumerate(R_):
            for j, b in enumerate(C_):
                for mo in monos:
                    flds = [a, b] + [x for x, e in zip(S, mo) for _ in range(e)]
                    if allowed(flds):
                        Mx[i, j] += (rng.normal() + 1j * rng.normal()) * np.prod([vev[x] ** e for x, e in zip(S, mo)])
        sv = np.linalg.svd(Mx, compute_uv=False)
        rank = int((sv > 1e-12 * max(1e-300, sv.max())).sum())
        ranks[f"{Xb}.{X}"] = [rank, len(R_) - (Xb == "bl")]
    rec["ranks_with_tentative_R"] = ranks
    short = [k for k, (r_, n_) in ranks.items() if r_ < n_]
    rec["verdict"] = ("dead (tentative R rules): rank-deficient " + ", ".join(short)) if short else "SURVIVES mass test"
    return rec


# ----------------------------------------------------------------------------- main
def main():
    ledger, sha = P.load_ledger()
    disc, dump = M.load(M.DISC), M.load(M.RPV)
    A_models, A = z6ii_general_parity_with_R(ledger, disc)
    print("A", A, flush=True)
    Z = Z6IIR(Z6II23, ledger, disc, dump)
    vac, supports = z6ii23_vacua(Z)
    print("vacua", vac, len(supports), flush=True)
    B, per = z6ii23_checks(Z, supports)
    print("B", B, flush=True)
    C = dict(supports=len(supports),
             W_S_forbidden_all_orders=sum(not r["W|_S_possible"] for r in per),
             F_flat_to_K=sum(r["F_pure"] == 0 and r["F_linear"] == 0 for r in per), K=K_F,
             u_bu_forbidden_all=sum(r["u.bu"] == 0 for r in per),
             d_bd_forbidden_all=sum(r["d.bd"] == 0 for r in per),
             e_be_forbidden_all=sum(r["e.be"] == 0 for r in per),
             max_bq_q=max(r["bq.q"] for r in per), max_bl_l=max(r["bl.l"] for r in per))
    print("C/D", C, flush=True)
    z12 = z12_models()
    E_models, E = {}, Counter()
    for name in sorted(z12):
        r = z12_analyse(name, z12[name])
        E_models[name] = r
        E[r["verdict"].split(":")[0].split(" (")[0] if "closed" not in r["verdict"] else "closed"] += 1
        if "support" in r:
            print(name, r["verdict"], flush=True)
    print("E", dict(E), flush=True)
    OUT.write_text(json.dumps(dict(pass_id=10968, ledger_sha256=sha, summary=dict(A=A, vacua=vac, B=B, CD=C, E=dict(E)),
                                   z6ii_models=A_models, z6ii23_supports=per, z12_models=E_models),
                              indent=1, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
